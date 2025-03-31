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
        self.workbench_dir = f"{ROOT}/workbench/{self.book_name}" # working directory
        self.images: list[str] = None # stores image filenames
        self.progress: dict[str, str] = None # stores image processing progress, key is image filename, value is status ("waiting", "processing", "done")

    def CleanupWorkbench(self):
        """
        Clean up the workbench
        """
        # Delete the working directory
        if DirExist(self.workbench_dir): DeleteDir(self.workbench_dir)

    def InitWorkbench(self):
        # Create working directory
        if not DirExist(self.workbench_dir):
            MakeDir(self.workbench_dir)
        else: # Workbench already contains a book with the same name
            pass # TODO Ask user or raise exception?

        # Copy source file to working directory
        CopyFile(self.options["input_path"], f"{self.workbench_dir}/origin.epub")
        # Unpack source file
        UnpackZip(f"{self.workbench_dir}/origin.epub", f"{self.workbench_dir}/unpack")
        # Check if the `image` directory exists in the unpacked directory
        if not DirExist(f"{self.workbench_dir}/unpack/image"): # If it doesn't exist, the epub source file is corrupted or has no images
            raise FileCorruptedError(f"Input file '{self.options["input_path"]}' is corrupted or it has no images.")
        # Get image list
        self.images = GetDirList(f"{self.workbench_dir}/unpack/image", "file")
        self.progress = {image_name: "waiting" for image_name in self.images}
        # Create directory for processed images
        MakeDir(f"{self.workbench_dir}/processed")

        # Save options and progress
        self.WriteOptions()
        self.WriteProgress()

    def GenerateTarget(self):
        """
        Generate target file
        """
        # Copy processed images to unpacked directory (overwrite)
        CopyDir(f"{self.workbench_dir}/processed", f"{self.workbench_dir}/unpack/image")
        # Compress files to output directory
        output_path = self.options["output_path"]
        tmp_output_path = f"{GetFileDir(output_path)}/${GetFileNameWithoutExt(output_path)}.tmp"
        MakeDir(GetFileDir(output_path))
        PackZip(f"{self.workbench_dir}/unpack", tmp_output_path)
        MoveFile(tmp_output_path, output_path, exist_ok=True)
        # Delete working directory
        # self.CleanupWorkbench()

    def ProcessAllImage(self, family: Family):
        """Returns a generator that yields the number of completed images and total image count each time"""
        # Read options and progress
        self.ReadOptions()
        self.ReadProgress()
        # Change all images with "processing" status to "waiting" status (previous processing incomplete), keep images with "done" status unchanged
        for image_name, status in self.progress.items():
            if status == "processing": self.progress[image_name] = "waiting"

        # Get the number of completed images and total image count
        done_count = self.GetStatusCount("done")
        total_count = len(self.progress)
        yield (done_count, total_count)
        
        # Process images
        while self.ProcessOneImage(family):
            done_count += 1
            yield (done_count, total_count)

    def ProcessOneImage(self, family: Family) -> bool:
        """
        Process one image, returns whether there is another image to process
        """
        image_name = self.GetOneWaitingImage()
        if image_name is None: return False
        self.progress[image_name] = "processing"
        self.WriteProgress()
        # Process image
        input_file  = f"{self.workbench_dir}/unpack/image/{image_name}"
        output_file = f"{self.workbench_dir}/processed/{image_name}"
        family.ProcessImage(input_file, output_file)
        self.ScaleAndCompress(output_file, output_file, self.options["scale"] / family.model_scale, self.options["quality"])

        self.progress[image_name] = "done"
        self.WriteProgress()
        return True
    
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
        for image_name, status in self.progress.items():
            if status == "waiting": return image_name
        return None
    
    def GetStatusCount(self, count_status: str) -> int:
        """
        Count the number of images with the specified status in the current progress
        count_status: Status to count, "waiting", "processing", "done"
        """
        return len([image_name for image_name, status in self.progress.items() if status == count_status])


