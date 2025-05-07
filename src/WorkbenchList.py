from utility import *
from Error import *
from Workbench import Workbench

from EpubWorkbench import EpubWorkbench
from PDFWorkbench import PDFWorkbench
# TODO: add more workbench


ADAPTED_WORKBENCH_LIST = {
    EpubWorkbench.source_type: EpubWorkbench,
    PDFWorkbench.source_type: PDFWorkbench,
    # TODO: add more family
}

def GetWorkbenchClass(file_name: str) -> type[Workbench]:
    """
    Get the workbench class according to the input file name
    """
    source_type = GetFileExt(file_name)
    if source_type.lower() not in ADAPTED_WORKBENCH_LIST:
        raise UnsupportedSourceTypeError(f"Source type '{source_type}' is not supported. "\
                                         f"Supported types: {[k for k in ADAPTED_WORKBENCH_LIST.keys()]}")
    return ADAPTED_WORKBENCH_LIST[source_type.lower()]

