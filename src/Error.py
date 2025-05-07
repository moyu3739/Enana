# Command line option errors
class OptionsError(Exception):
    """Raised when the command line options are invalid."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class InputFileNotFoundError(OptionsError, FileNotFoundError):
    """Raised when the input file is not found."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class UnsupportedSourceTypeError(OptionsError):
    """Raised when the source type is not supported."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class OutputPathIsDirError(OptionsError, IsADirectoryError):
    """Raised when the output path is a directory."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class FamilyNotFoundError(OptionsError):
    """Raised when the family is not found."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class ModelNotFoundError(OptionsError):
    """Raised when the model is not found."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class ScaleValueInvalidError(OptionsError, ValueError):
    """Raised when the scale value is invalid."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class PreScaleValueInvalidError(OptionsError, ValueError):
    """Raised when the pre-scale value is invalid."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class JobsValueInvalidError(OptionsError, ValueError):
    """Raised when the jobs value is invalid."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class ImageQualityValueInvalidError(OptionsError, ValueError):
    """Raised when the image quality level value is invalid."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class NoAvailableModelError(OptionsError):
    """Raised when there is no available model."""
    def __init__(self, *args) -> None:
        super().__init__(*args)


# Errors during processing (after workbench initialization)
class FileCorruptedError(RuntimeError):
    """Raised when the EPUB file is corrupted."""
    def __init__(self, *args) -> None:
        super().__init__(*args)

class ModelRuntimeError(RuntimeError):
    """Raised when the model runtime error."""
    def __init__(self, *args) -> None:
        super().__init__(*args)
