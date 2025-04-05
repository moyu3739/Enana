import subprocess
from utility import *
from Error import *
from Family import Family


class RealEsrganNcnnVulkan(Family):
    """Real-ESRGAN-ncnn-vulkan super-resolution model family"""
    family_name = "realesrgan-ncnn-vulkan"
    description = "Real-ESRGAN-ncnn-vulkan is a Real-time Image Super-Resolution Model based on Efficient Residual Block." # family description information
    supported_image_exts = [".jpg", ".png", ".webp"]

    def __init__(self, options: dict):
        super().__init__(options)
        self.CheckIOOptions()
        self.CheckModelOptions()

    def ProcessImage(self, input_file: str, output_file: str):
        """
        Process image
        Args:
            input_file: Input image file path
            output_file: Output image file path
        """
        cmd = [
            f"{ROOT}/family/{self.family_name}/{self.family_name}",
            "-i", input_file,
            "-o", output_file,
            "-s", str(self.model_scale),
            "-n", self.options["model"],
        ]
        try:
            subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            info = f"Model '{self.options["model"]}' of family '{self.options["family"]}' FAILED:\n" \
                   f"stdout: {e.stdout}\n" \
                   f"stderr: {e.stderr}"
            raise ModelRuntimeError(info) from e

    @classmethod
    def GetAllModels(cls) -> list[str]:
        """
        Get all model names of Real-ESRGAN-ncnn-vulkan family
        """
        # Get all files under the model path
        files = GetDirList(f"{ROOT}/family/{cls.family_name}/models", "file")
        # Must have both .bin and .param files with the same name
        models = ["realesr-animevideov3"] # Default model
        for file in files:
            if file.endswith(".bin"):
                model_name = file[:-4]
                if f"{model_name}.param" in files:
                    models.append(model_name)
        return models

    @classmethod
    def GetDescription(cls) -> str:
        """
        Get the description information of the Real-ESRGAN family
        """
        return cls.description



if __name__ == "__main__":
    real_esrgan = RealEsrganNcnnVulkan(None)
    print(real_esrgan.GetAllLocalFamilies())
    print(real_esrgan.GetAllModels())
    print(real_esrgan.GetDescription())

