import abc
import subprocess
from utility import *
from Error import *


class Family(abc.ABC):
    """This is an abstract class representing a family of super-resolution models"""
    family_name = None # Family name
    description = None # Family description

    def __init__(self, options: dict):
        self.options = options
        self.model_scale: int = None # Model scaling factor

    def CheckIOOptions(self):
        """
        Check if the IO options meet the requirements, throw an exception if not
        """
        # Check if the input file exists
        if not FileExist(self.options["input_path"]):
            raise InputFileNotFoundError(f"Input file '{self.options["input_path"]}' does not exist or is not a file.")
        # Check if the input file is an EPUB file
        if GetFileExt(self.options["input_path"]).lower() != ".epub":
            raise NotEpubFileError(f"Input file '{self.options["input_path"]}' is not an EPUB file.")
        # Check if the output file path already exists as a directory
        if DirExist(self.options["output_path"]):
            raise OutputPathIsDirError(f"Output path '{self.options["output_path"]}' already exists as a directory.")
    
    def CheckModelOptions(self):
        """
        Check if the model options meet the requirements,
        meanwhile fill in default options if necessary
        """
        # If no model name is given, use the first model by default,
        # if no available model, throw an exception
        if self.options["model"] is None:
            model_list = self.GetAllModels()
            if len(model_list) == 0:
                raise NoAvailableModelError(f"No available model for family '{self.family_name}'.")
            self.options["model"] = model_list[0]

        # The model name must be in the list of available models
        if self.options["model"] not in self.GetAllModels():
            raise ModelNotFoundError(f"Model '{self.options["model"]}' is not an available models for family '{self.family_name}'.")
        
        # Confirm the actual scaling factor (float) and the model scaling factor (integer)
        self.model_scale = self.ParseScaleFromModelName(self.options["model"])
        if self.model_scale is not None: # Can parse the model scaling factor from the model name
            # If no actual scaling factor is given, use the model scaling factor
            if self.options["scale"] is None: self.options["scale"] = self.model_scale
            # The actual scaling factor must be between 1 and model_scale
            if not 1.0 < self.options["scale"] <= self.model_scale:
                raise ScaleValueInvalidError(f"Scale factor must in range (1, {self.model_scale}] "\
                                            f"for model '{self.options["model"]}' of family '{self.family_name}', "\
                                            f"but got {self.options["scale"]}.")
        else: # Cannot parse the model scaling factor from the model name
            # If no actual scaling factor is given, use the default actual scaling factor 2
            if self.options["scale"] is None: self.options["scale"] = 2
            # Use the given actual scaling factor rounded up as the model scaling factor
            self.model_scale = Ceil(self.options["scale"])

    @abc.abstractmethod
    def ProcessImage(self, input_file: str, output_file: str):
        """
        Process image
        """
        pass

    @classmethod
    def ParseScaleFromModelName(cls, model_name: str) -> int | None:
        """
        Parse the model scaling factor from the model name
        """
        model_name = model_name.lower()
        if "x2" in model_name or "2x" in model_name: return 2
        if "x3" in model_name or "3x" in model_name: return 3
        if "x4" in model_name or "4x" in model_name: return 4
        return None

    @classmethod
    def GetAllLocalFamilies(cls) -> list[str]:
        """
        Get the names of all super-resolution model families
        """
        return GetDirList(f"{ROOT}/family", "dir")

    @classmethod
    @abc.abstractmethod
    def GetDescription(self) -> str:
        """
        Get the description of this family
        """
        pass

    @classmethod
    @abc.abstractmethod
    def GetAllModels(cls) -> list[str]:
        """
        Get all model names of this family
        """
        pass


class CommonFamilyBase(Family):
    """
    The base class of the family that does general processing
    adds pass-through functionality on top of the parent class Family,
    but not all features are guaranteed to work properly
    """
    def __init__(self, options):
        super().__init__(options)
    

def MakeCommonFamilyClass(family_name_: str, description_: str = None):
    """
    Create a common family class with the given family name and description.
    This class inherits from CommonFamilyBase and implements the ProcessImage method.
    However, it does not guarantee that all features will work properly.
    """
    class CommonFamily(CommonFamilyBase):
        """
        A model family that does general processing, adds pass-through functionality
        on top of the parent class Family, but not all features are guaranteed to work properly
        """
        family_name = family_name_
        description = f"Family '{family_name_}' is a local but not specifically implemented family. So you should use it with caution."\
                      if description_ is None else description_
        
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
            # Two possible command line parameter formats, use -m or -n to specify the model name
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
            Get the description of this family
            """
            return cls.description

        @classmethod
        def GetAllModels(cls) -> list[str]:
            """
            Get all model names of this family
            """
            # List all file names (without extension, remove duplicates) in the `models` directory (if exists)
            if DirExist(f"{ROOT}/family/{cls.family_name}/models"):
                files = GetDirList(f"{ROOT}/family/{cls.family_name}/models", "file")
                models = {GetFileNameWithoutExt(file) for file in files}
                return list(models)
            # If there is no `models` directory, list all directory names in family directory
            else:
                return GetDirList(f"{ROOT}/family/{cls.family_name}", "dir")
            
    return CommonFamily

