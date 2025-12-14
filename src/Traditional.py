import subprocess
from utility import *
from Error import *
from Family import Family
from PIL import Image


class Traditional(Family):
    """traditonal image scaling algorithm family"""
    family_name = "traditional"
    description = "Traditional image scaling algorithms including nearest, bilinear, bicubic, lanczos and hqnx." # family description information
    supported_image_exts = [".jpg", ".jpeg", ".png", ".webp"]
    resample_map = {
        "nearest": Image.Resampling.NEAREST,
        "bilinear": Image.Resampling.BILINEAR,
        "bicubic": Image.Resampling.BICUBIC,
        "lanczos": Image.Resampling.LANCZOS,
    }

    def __init__(self, options: dict):
        super().__init__(options)
        self.CheckOptions()
        self.model_scale = self.options["scale"]

    def ProcessImage(self, input_file: str, output_file: str):
        """
        Process image with Pillow-based interpolation
        """
        model = self.options["model"].lower()
        if model not in self.resample_map:
            raise ModelRuntimeError(f"Model '{model}' of family '{self.family_name}' is not supported.")
        try:
            with Image.open(input_file) as img:
                new_size = (
                    int(round(img.width * self.options["scale"])),
                    int(round(img.height * self.options["scale"]))
                )
                if new_size[0] <= 0 or new_size[1] <= 0:
                    raise ScaleValueInvalidError(f"Invalid target size {new_size} for scale {self.options['scale']}.")
                out = img.resize(new_size, resample=self.resample_map[model])
                out.save(output_file)
        except Exception as e:
            info = f"Model '{model}' of family '{self.family_name}' FAILED:\n{e}"
            raise ModelRuntimeError(info) from e

    @classmethod
    def GetAllModels(cls) -> list[str]:
        """
        Get all supported interpolation algorithm names
        """
        return list(cls.resample_map.keys())

    @classmethod
    def GetDescription(cls) -> str:
        """
        Get the description of this family
        """
        return cls.description
    
    @classmethod
    def GetDefaultModel(cls) -> list[str]:
        """
        Get the default model name of this family
        """
        return "bicubic"

