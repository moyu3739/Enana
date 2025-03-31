import subprocess
from utility import *
from Error import *
from Family import Family


class RealEsrganNcnnVulkan(Family):
    """Real-ESRGAN-ncnn-vulkan 超分辨率模型系列"""
    family_name = "realesrgan-ncnn-vulkan" # 系列名称，用于在本地文件系统中查找模型
    description = "Real-ESRGAN-ncnn-vulkan is a Real-time Image Super-Resolution Model based on Efficient Residual Block." # 系列描述信息

    def __init__(self, options: dict):
        super().__init__(options)
        self.CheckIOOptions()
        self.CheckModelOptions()

    def ProcessImage(self, input_file: str, output_file: str):
        """
        处理图片
        Args:
            input_file: 输入图片文件路径
            output_file: 输出图片文件路径
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
            raise ModelRuntimeError(f"Model '{self.options["model"]}' of family '{self.family_name}' FAILED.") from e

    @classmethod
    def GetAllModels(cls) -> list[str]:
        """
        获取 Real-ESRGAN 系列的所有模型名称
        """
        # 获取模型路径下的所有文件
        files = GetDirList(f"{ROOT}/family/{cls.family_name}/models", "file")
        # 必须同时有同名的 .bin 和 .param 文件
        models = ["realesr-animevideov3"] # 默认模型
        for file in files:
            if file.endswith(".bin"):
                model_name = file[:-4]
                if f"{model_name}.param" in files:
                    models.append(model_name)
        return models

    @classmethod
    def GetDescription(cls) -> str:
        """
        获取 Real-ESRGAN 系列的描述信息
        """
        return cls.description



if __name__ == "__main__":
    real_esrgan = RealEsrganNcnnVulkan(None)
    print(real_esrgan.GetAllLocalFamilies())
    print(real_esrgan.GetAllModels())
    print(real_esrgan.GetDescription())

