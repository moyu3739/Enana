import json
from PIL import Image
from utility import *
from Error import *
from Family import Family


class Workbench:
    """Workbench class"""

    def __init__(self, options):
        self.options = options
        self.book_name = GetFileNameWithoutExt(self.options["input_path"])
        if options["preview"]:
            self.workbench_dir = f"{ROOT}/workbench/.preview/{self.book_name}" # working directory
        else:
            self.workbench_dir = f"{ROOT}/workbench/{self.book_name}" # working directory
        self.progress: dict[str, str] = None # stores image processing progress, key is image filename, value is status ("waiting", "processing", "done")

    def CleanupWorkbench(self):
        """
        Clean up the workbench
        """
        # Delete the working directory
        if DirExist(self.workbench_dir): DeleteDir(self.workbench_dir)

    def WorkbenchExist(self) -> bool:
        """
        Check if the workbench exists
        """
        return DirExist(self.workbench_dir)

    def InitWorkbench(self, image_exts: list[str]):
        """
        Args:
            image_exts: List of image file extensions to be processed, e.g. ['.jpg', '.png']
        """
        # Create working directory
        if not DirExist(self.workbench_dir):
            MakeDir(self.workbench_dir)
        else: # Workbench already contains a book with the same name
            pass # TODO Ask user or raise exception?

        # Copy source file to working directory
        CopyFile(self.options["input_path"], f"{self.workbench_dir}/original.epub")
        # Unpack source file
        UnpackZip(f"{self.workbench_dir}/original.epub", f"{self.workbench_dir}/unpack")
        # Get image list
        images = SearchFiles(f"{self.workbench_dir}/unpack", image_exts)
        self.progress = {image_path: "waiting" for image_path in images}
        if len(images) == 0:
            raise FileCorruptedError(f"Input file '{self.options["input_path"]}' is corrupted or it has no images.")

        # Save options and progress
        self.WriteOptions()
        self.WriteProgress()

    def ProcessAllImage(self, family: Family):
        """Returns a generator that yields the number of completed images and total image count each time"""
        # Read options and progress
        self.ReadOptions()
        self.ReadProgress()
        # Change all images with non-"done" status to "waiting" status (previous processing incomplete), keep images with "done" status unchanged
        for image_path, status in self.progress.items():
            if status != "done": self.progress[image_path] = "waiting"

        # Get the number of completed images and total image count
        done_count = self.GetStatusCount("done")
        total_count = len(self.progress)
        yield (done_count, total_count)
        
        # Process images
        while self.ProcessOneImage(family):
            done_count += 1
            yield (done_count, total_count)

    def GenerateEpubTarget(self):
        """
        Generate EPUB target file
        """
        # Compress files to output directory
        target_path = self.options["output_path"]
        tmp_target_path = f"{GetFileDir(target_path)}/${GetFileNameWithoutExt(target_path)}.tmp"
        MakeDir(GetFileDir(target_path))
        PackZip(f"{self.workbench_dir}/unpack", tmp_target_path)
        MoveFile(tmp_target_path, target_path, exist_ok=True)
        # Delete working directory
        self.CleanupWorkbench()

    def GeneratePreviewImage(self, family: Family):
        """
        Generate preview image
        """
        # Get the preview image name
        preview_image_path = self.GetPreviewImage()
        preview_image_name = GetFileNameWithoutExt(preview_image_path)
        preview_image_ext = GetFileExt(preview_image_path)
        # Process image
        original_path  = preview_image_path
        processed_path = f"{self.workbench_dir}/preview{preview_image_ext}"
        family.ProcessImage(original_path, processed_path)
        self.ScaleAndCompress(processed_path, processed_path, self.options["scale"] / family.model_scale, self.options["quality"])        
        # Copy original and processed preview image to output directory
        target_dir = f"{GetFileDir(self.options["output_path"])}"
        MakeDir(target_dir)
        CopyFile(
            original_path,
            f"{target_dir}/[{APP_NAME}-preview original] {preview_image_name}{preview_image_ext}",
        )
        CopyFile(
            processed_path,
            f"{target_dir}/[{APP_NAME}-preview processed] {preview_image_name}{preview_image_ext}",
        )
        # Delete working directory
        self.CleanupWorkbench()

    def ProcessOneImage(self, family: Family) -> bool:
        """
        Process one image, returns whether there is another image to process
        """
        image_path = self.GetOneWaitingImage()
        if image_path is None: return False
        self.progress[image_path] = "processing"
        self.WriteProgress()
        # Process image
        family.ProcessImage(image_path, image_path)
        self.ScaleAndCompress(image_path, image_path, self.options["scale"] / family.model_scale, self.options["quality"])

        self.progress[image_path] = "done"
        self.WriteProgress()
        return True
    
    def GetPreviewImage(self) -> str:
        """
        Get the preview image path.
        If there is a cover image, return it. Otherwise, return the first image.
        """
        for image_path in self.progress.keys():
            if GetFileNameWithoutExt(image_path).lower() == "cover": return image_path
        return list(self.progress.keys())[0] # Return the first image name if no cover image is found
    
    @classmethod
    def ScaleAndCompress(cls, input_file: str, output_file: str, scale_ratio: float, quality_level: int):
        """
        Scale and compress image
        Args:
            input_file: Input image file path
            output_file: Output image file path
            scale_ratio: Scale ratio
            quality_level: Quality level (0-100), higher value means less compression
        """
        # Open image
        img = Image.open(input_file)
        
        if scale_ratio != 1.0:
            # Calculate new dimensions
            new_width = int(img.width * scale_ratio)
            new_height = int(img.height * scale_ratio)
            # Scale image (using high-quality LANCZOS resampling)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if quality_level < 100:
            match img.format:
                case "JPEG": img.save(output_file, quality=quality_level, optimize=True)
                case "PNG": img.save(output_file, compress_level=7, optimize=True)
                case _: img.save(output_file, quality=quality_level, optimize=True)

    def ReadOptions(self) -> dict:
        with open(f"{self.workbench_dir}/options.json", "r") as f:
            self.options = json.load(f)

    def WriteOptions(self):
        with open(f"{self.workbench_dir}/options.json", "w") as f:
            json.dump(self.options, f, indent=4)

    def ReadProgress(self) -> dict[str, str]:
        with open(f"{self.workbench_dir}/progress.json", "r") as f:
            self.progress = json.load(f)

    def WriteProgress(self):
        with open(f"{self.workbench_dir}/progress.json", "w") as f:
            json.dump(self.progress, f, indent=4)

    def GetOneWaitingImage(self) -> str | None:
        """
        Get one image name that is waiting to be processed
        """
        for image_path, status in self.progress.items():
            if status == "waiting": return image_path
        return None
    
    def GetStatusCount(self, count_status: str) -> int:
        """
        Count the number of images with the specified status in the current progress
        count_status: Status to count, "waiting", "processing", "done"
        """
        return len([image_path for image_path, status in self.progress.items() if status == count_status])


