import abc
import subprocess
from PIL import Image
from utility import *
from Error import *


class Family(abc.ABC):
    """这是一个抽象类，表示超分辨率模型的一个系列"""
    family_name = None # 系列名称
    description = None # 系列描述信息

    def __init__(self, options: dict):
        self.options = options
        self.model_scale: int = None # 模型放大倍数

    def CheckIOOptions(self):
        """
        检查选项是否符合要求，如果不符合则抛出异常
        """
        # 检查输入文件是否存在
        if not FileExist(self.options["input_path"]):
            raise InputFileNotFoundError(f"Input file '{self.options["input_path"]}' does not exist or is not a file.")
        # 检查输入文件是否是 EPUB 文件
        if GetFileExt(self.options["input_path"]).lower() != ".epub":
            raise NotEpubFileError(f"Input file '{self.options["input_path"]}' is not an EPUB file.")
        # 检查输出文件路径是否已经存在一个目录
        if DirExist(self.options["output_path"]):
            raise OutputPathIsDirError(f"Output path '{self.options["output_path"]}' already exists as a directory.")
    
    def CheckModelOptions(self):
        """
        填充默认选项，如果没有给定选项，则使用默认值
        """
        # 如果没有给定模型名，默认使用第一个模型，如果没有可用模型，则抛出异常
        if self.options["model"] is None:
            model_list = self.GetAllModels()
            if len(model_list) == 0:
                raise NoAvailableModelError(f"No available model for family '{self.family_name}'.")
            self.options["model"] = model_list[0]

        # 模型名称必须在可用模型列表中
        if self.options["model"] not in self.GetAllModels():
            raise ModelNotFoundError(f"Model '{self.options["model"]}' is not an available models for family '{self.family_name}'.")
        
        # 确认实际放大倍数（浮点数）和模型放大倍数（整数）
        self.model_scale = self.ParseScaleFromModelName(self.options["model"])
        if self.model_scale is not None: # 可以从模型名称中解析出模型放大倍数
            # 如果没有给实际放大倍数，使用模型放大倍数
            if self.options["scale"] is None: self.options["scale"] = self.model_scale
            # 实际放大倍数必须在 1 到 model_scale 之间
            if not 1.0 < self.options["scale"] <= self.model_scale:
                raise ScaleValueInvalidError(f"Scale factor must in range (1, {self.model_scale}] "\
                                            f"for model '{self.options["model"]}' of family '{self.family_name}', "\
                                            f"but got {self.options["scale"]}.")
        else: # 不能从模型名称中解析出模型放大倍数
            # 如果没有给定实际放大倍数，使用默认实际放大倍数 2
            if self.options["scale"] is None: self.options["scale"] = 2
            # 使用给定的实际放大倍数向上取整，作为模型放大倍数
            self.model_scale = Ceil(self.options["scale"])

    @abc.abstractmethod
    def ProcessImage(self, input_file: str, output_file: str):
        """
        处理图片
        """
        pass

    @classmethod
    def ParseScaleFromModelName(cls, model_name: str) -> int | None:
        """
        从模型名称中解析出模型放大倍数
        """
        model_name = model_name.lower()
        if "x2" in model_name or "2x" in model_name: return 2
        if "x3" in model_name or "3x" in model_name: return 3
        if "x4" in model_name or "4x" in model_name: return 4
        return None

    @classmethod
    def GetAllLocalFamilies(cls) -> list[str]:
        """
        获取所有超分辨率模型系列的名称
        """
        return GetDirList(f"{ROOT}/family", "dir")

    @classmethod
    @abc.abstractmethod
    def GetDescription(self) -> str:
        """
        获取该系列的描述信息
        """
        pass

    @classmethod
    @abc.abstractmethod
    def GetAllModels(cls) -> list[str]:
        """
        获取该系列的所有模型名称
        """
        pass


class CommonFamilyBase(Family):
    """做通用处理的模型系列的基类，在父类 Family 基础上添加通过功能，但不保证所有功能都能正常工作"""
    def __init__(self, options):
        super().__init__(options)
    

def MakeCommonFamilyClass(family_name_: str, description_: str = None):
    class CommonFamily(CommonFamilyBase):
        """做通用处理的模型系列，在父类 Family 基础上添加通过功能，但不保证所有功能都能正常工作"""
        family_name = family_name_
        description = f"Family '{family_name_}' is a local but not specifically implemented family. So you should use it with caution."\
                      if description_ is None else description_
        
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
            # 两种可能的命令行参数格式，用 -m 或 -n 指定模型名称
            cmd1 = [
                f"{ROOT}/family/{self.family_name}/{self.family_name}",
                "-i", input_file,
                "-o", output_file,
                "-s", str(self.model_scale),
                "-n", self.options["model"],
            ]
            cmd2 = [
                f"{ROOT}/family/{self.family_name}/{self.family_name}",
                "-i", input_file,
                "-o", output_file,
                "-s", str(self.model_scale),
                "-m", self.options["model"],
            ]

            try:
                subprocess.run(cmd1, check=True, shell=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                try:
                    subprocess.run(cmd2, check=True, shell=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    raise ModelRuntimeError(f"Model '{self.options["model"]}' of family '{self.options["family"]}' FAILED.") from e

        @classmethod
        def GetDescription(cls) -> str:
            """
            获取该系列的描述信息
            """
            return cls.description

        @classmethod
        def GetAllModels(cls) -> list[str]:
            """
            获取该系列的所有模型名称
            """
            # 列出自身 family 目录中 models 目录（如果存在）中的所有文件名（不带扩展名，去除重复）
            if DirExist(f"{ROOT}/family/{cls.family_name}/models"):
                files = GetDirList(f"{ROOT}/family/{cls.family_name}/models", "file")
                models = {GetFileNameWithoutExt(file) for file in files}
                return list(models)
            # 如果没有 models 目录，则列出自身 family 目录中的所有目录名
            else:
                return GetDirList(f"{ROOT}/family/{cls.family_name}", "dir")
            
    return CommonFamily

