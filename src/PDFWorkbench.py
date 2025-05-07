from utility import *
from Error import *
from Workbench import Workbench


class PDFWorkbench(Workbench):
    """PDF Workbench class"""
    source_type = ".pdf" # Source type, file type to be processed

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
        CopyFile(self.options["input_path"], f"{self.workbench_dir}/o.pdf")
        MakeDir(self.original_dir)
        MakeDir(self.processed_dir)
        # Extract images from PDF
        PdfExtractImages(f"{self.workbench_dir}/o.pdf", self.original_dir)

        # Get image list
        images = SearchFiles(self.original_dir, image_exts, relative=True)
        self.progress.LoadTasks(images)
        if len(images) == 0:
            raise FileCorruptedError(f"Input file '{self.options["input_path"]}' is corrupted or it has no images.")

        # Save progress
        self.WriteProgress()

    def GenerateTarget(self):
        """
        Generate PDF target file
        """
        # Compress files to output directory
        target_path = self.options["output_path"]
        MakeDir(GetFileDir(target_path))

        images = {
            int(GetFileNameWithoutExt(image_relpath)): f"{self.processed_dir}/{image_relpath}"
            for image_relpath in self.progress.tasks.keys()
        }
        PdfReplaceImages(f"{self.workbench_dir}/o.pdf", images, target_path)

        # Delete working directory
        self.CleanupWorkbench()
    
    def GetPreviewImageXrefAndExt(self) -> str:
        """
        Get xref and extension name of the preview image
        """
        xref, info = PdfGetFirstImage(f"{self.workbench_dir}/o.pdf")
        ext = info["ext"]
        return xref, ext

    def GetPreviewImageIOPath(self) -> tuple[str, str]:
        """
        Get the preview image input and output path.
        """
        # Get the preview image name
        preview_image_xref, preview_image_ext = self.GetPreviewImageXrefAndExt()
        # Process image
        original_path  = f"{self.original_dir}/{preview_image_xref}.{preview_image_ext}"
        processed_path = f"{self.workbench_dir}/preview.{preview_image_ext}"
        return original_path, processed_path

    def GetImageIOPath(self, task: str) -> tuple[str, str]:
        """
        Get the image input and output path.
        """
        original_path = f"{self.original_dir}/{task}"
        processed_path = f"{self.processed_dir}/{task}"
        return original_path, processed_path




if __name__ == "__main__":
    pdf_path = "a_enana.pdf"
    output_directory = "test"
    PdfExtractImages(pdf_path, output_directory)

    # pdf_path = "test/a.pdf"
    # image_paths = {
    #     9: "test/image/1.png",
    #     10: "test/image/2.png",
    #     11: "test/image/3.png",
    # }
    # output_pdf_path = "test/aa.pdf"
    # PdfReplaceImages(pdf_path, image_paths, output_pdf_path)

    # pdf_path = "test/aa.pdf"
    # output_directory = "test"
    # PdfExtractImages(pdf_path, output_directory)

    # options = {
    #     "preview": False,
    #     "input_path": "test/a.pdf",
    #     "output_path": "test/aa.pdf",
    # }
    # w = PDFWorkbench(options)
    # w.InitWorkbench([".png"])

