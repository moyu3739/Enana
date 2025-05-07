from utility import *
from Error import *
from Workbench import Workbench


class EpubWorkbench(Workbench):
    """EPUB Workbench class"""
    source_type = ".epub" # Source type, file type to be processed

    def __init__(self, options):
        super().__init__(options)
        self.original_dir = f"{self.workbench_dir}/original"
        self.processed_dir = f"{self.workbench_dir}/processed"
        self.CheckOptions()

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
        UnpackZip(f"{self.workbench_dir}/o.epub", self.original_dir)
        if not self.options["preview"]:
            CopyDir(self.original_dir, self.processed_dir)
        # Get image list
        images = SearchFiles(self.original_dir, image_exts, relative=True)
        self.progress.LoadTasks(images)
        if len(images) == 0:
            raise FileCorruptedError(f"Input file '{self.options["input_path"]}' is corrupted or it has no images.")

        # Save progress
        self.WriteProgress()

    def GenerateTarget(self):
        """
        Generate EPUB target file
        """
        # Compress files to output directory
        target_path = self.options["output_path"]
        tmp_target_path = f"{GetFileDir(target_path)}/${GetFileNameWithoutExt(target_path)}.tmp"
        MakeDir(GetFileDir(target_path))
        PackZip(self.processed_dir, tmp_target_path)
        MoveFile(tmp_target_path, target_path, exist_ok=True)
        # Delete working directory
        self.CleanupWorkbench()
    
    def GetPreviewImage(self) -> str:
        """
        Get the preview image path.
        If there is a cover image, return it. Otherwise, return the first image.
        """
        for image_relpath in self.progress.tasks.keys():
            if GetFileNameWithoutExt(image_relpath).lower() == "cover": return image_relpath
        return list(self.progress.tasks.keys())[0] # Return the first image name if no cover image is found

    def GetPreviewImageIOPath(self) -> tuple[str, str]:
        """
        Get the preview image input and output path.
        """
        # Get the preview image name
        preview_image_relpath = self.GetPreviewImage()
        preview_image_ext = GetFileExt(preview_image_relpath)
        # Process image
        original_path  = f"{self.original_dir}/{preview_image_relpath}"
        processed_path = f"{self.workbench_dir}/preview{preview_image_ext}"
        return original_path, processed_path

    def GetImageIOPath(self, task: str) -> tuple[str, str]:
        """
        Get the image input and output path.
        """
        original_path = f"{self.original_dir}/{task}"
        processed_path = f"{self.processed_dir}/{task}"
        return original_path, processed_path

