import threading
import concurrent.futures
from PIL import Image
from utility import *
from Error import *
from Family import Family
from Progress import Progress


class Workbench:
    """Workbench class"""

    def __init__(self, options):
        self.options = options
        self.book_name = GetFileNameWithoutExt(self.options["input_path"])
        if options["preview"]:
            self.workbench_dir = f"{ROOT}/workbench/.preview/{self.book_name}" # working directory
        else:
            self.workbench_dir = f"{ROOT}/workbench/{self.book_name}" # working directory
        self.progress = Progress()

    def CleanupWorkbench(self):
        """
        Clean up the workbench
        """
        # Delete the working directory
        if DirExist(self.workbench_dir): DeleteDir(self.workbench_dir)

    def WorkbenchInitialized(self) -> bool:
        """
        Check if the workbench exists
        """
        # progress.json existing is a sign that the workbench has been initialized
        return FileExist(f"{self.workbench_dir}/progress.json")

    def InitWorkbench(self, image_exts: list[str]):
        """
        Args:
            image_exts: List of image file extensions to be processed, e.g. ['.jpg', '.png']
        """
        if DirExist(self.workbench_dir): DeleteDir(self.workbench_dir) # Delete the working directory if it exists
        MakeDir(self.workbench_dir) # Create the working directory

        # Copy source file to working directory
        CopyFile(self.options["input_path"], f"{self.workbench_dir}/o.epub")
        # Unpack source file
        UnpackZip(f"{self.workbench_dir}/o.epub", f"{self.workbench_dir}/original")
        if not self.options["preview"]:
            CopyDir(f"{self.workbench_dir}/original", f"{self.workbench_dir}/processed")
        # Get image list
        images = SearchFiles(f"{self.workbench_dir}/original", image_exts, relative=True)
        self.progress.LoadTasks(images)
        if len(images) == 0:
            raise FileCorruptedError(f"Input file '{self.options["input_path"]}' is corrupted or it has no images.")

        # Save progress
        self.WriteProgress()

    def ProcessAllImage(self, family: Family):
        """Returns a generator that yields the number of completed images and total image count each time"""
        # Read progress
        self.ReadProgress()
        self.progress.RefreshUndoneTask()

        # Process images
        def Process(t_id):
            while self.ProcessOneImage(family): pass

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.options["jobs"]) as executor:
            # use list() to force the generator to run to get exceptions,
            # if a sub-thread raises an exception, it will be re-raised here
            list(executor.map(Process, range(self.options["jobs"])))

    def GenerateEpubTarget(self):
        """
        Generate EPUB target file
        """
        # Compress files to output directory
        target_path = self.options["output_path"]
        tmp_target_path = f"{GetFileDir(target_path)}/${GetFileNameWithoutExt(target_path)}.tmp"
        MakeDir(GetFileDir(target_path))
        PackZip(f"{self.workbench_dir}/processed", tmp_target_path)
        MoveFile(tmp_target_path, target_path, exist_ok=True)
        # Delete working directory
        self.CleanupWorkbench()

    def GeneratePreviewImage(self, family: Family):
        """
        Generate preview image
        """
        # Get the preview image name
        preview_image_relpath = self.GetPreviewImage()
        preview_image_ext = GetFileExt(preview_image_relpath)
        # Process image
        original_path  = f"{self.workbench_dir}/original/{preview_image_relpath}"
        processed_path = f"{self.workbench_dir}/preview{preview_image_ext}"
        self.ScaleAndCompress(original_path, processed_path, self.options["pre_scale"], 100)
        family.ProcessImage(processed_path, processed_path)
        self.ScaleAndCompress(processed_path, processed_path, self.options["scale"] / family.model_scale, self.options["quality"])        
        # Copy original and processed preview image to output directory
        target_dir = f"{GetFileDir(self.options["output_path"])}"
        MakeDir(target_dir)
        CopyFile(
            original_path,
            f"{target_dir}/[{APP_NAME}-preview] original{preview_image_ext}",
        )
        CopyFile(
            processed_path,
            f"{target_dir}/[{APP_NAME}-preview] processed{preview_image_ext}",
        )
        # Delete working directory
        self.CleanupWorkbench()

    def ProcessOneImage(self, family: Family) -> bool:
        """
        Process one image, returns whether there is another image to process
        """
        image_relpath = self.progress.GetOneTaskOfStatusAndUpdate("waiting", "processing")
        if image_relpath is None: return False # No more images to process
        original_path = f"{self.workbench_dir}/original/{image_relpath}"
        processed_path = f"{self.workbench_dir}/processed/{image_relpath}"
        
        self.WriteProgress()
        # Pre-scale image
        self.ScaleAndCompress(original_path, processed_path, self.options["pre_scale"], 100)
        # Process image with super-resolution model
        family.ProcessImage(processed_path, processed_path)
        # Scale and compress image
        self.ScaleAndCompress(processed_path, processed_path, self.options["scale"] / family.model_scale, self.options["quality"])

        self.progress.Update(image_relpath, "done")
        self.WriteProgress()
        return True
    
    def GetPreviewImage(self) -> str:
        """
        Get the preview image path.
        If there is a cover image, return it. Otherwise, return the first image.
        """
        for image_relpath in self.progress.tasks.keys():
            if GetFileNameWithoutExt(image_relpath).lower() == "cover": return image_relpath
        return list(self.progress.tasks.keys())[0] # Return the first image name if no cover image is found

    def ReadProgress(self):
        self.progress.Load(f"{self.workbench_dir}/progress.json")

    def WriteProgress(self):
        self.progress.Dump(f"{self.workbench_dir}/progress.json")

    def GetProgressStatistics(self):
        """
        Get the number of completed images and total image count
        """
        done_count = self.progress.GetTaskNumOfStatus("done")
        total_count = self.progress.GetTaskNum()
        return (done_count, total_count)

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
        if scale_ratio == 1.0 and quality_level == 100:
            CopyFile(input_file, output_file)
            return

        # Open image
        img = Image.open(input_file)
        
        if scale_ratio != 1.0:
            # Calculate new dimensions
            new_width = int(img.width * scale_ratio)
            new_height = int(img.height * scale_ratio)
            # Scale image (using high-quality LANCZOS resampling)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        match img.format:
            case "JPEG": img.save(output_file, quality=quality_level, optimize=True)
            case "PNG": img.save(output_file, compress_level=7, optimize=True)
            case _: img.save(output_file, quality=quality_level, optimize=True)


