import os
import zipfile
import sys


APP_NAME = "enana" # E NAtive Neural Amplifier

# Set ROOT path according to the running mode of the program
if getattr(sys, "frozen", False):
    # Run as a frozen executable, ROOT is the directory of the executable
    ROOT = os.path.dirname(sys.executable)
    USAGE_PROG = APP_NAME
else:
    # Run as a Python script, ROOT is the parent directory of the script
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    USAGE_PROG = "python main.py"


##################################################################
##          Functions for File and Directory Operations         ##
##################################################################

def UnpackZip(zip_path: str, extract_folder: str):
    """
    Extract ZIP file to specified directory
    Args:
        zip_path: Path of the ZIP file
        extract_folder: Target directory for extraction
    """
    # Open ZIP file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract files to specified directory
        zip_ref.extractall(extract_folder)

def PackZip(src_folder: str, zip_path: str):
    """
    Package specified directory into a ZIP file
    Args:
        src_folder: Path of the source directory
        zip_path: Path of the ZIP file
    """
    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        # Traverse all files in the directory
        for foldername, subfolders, filenames in os.walk(src_folder):
            for filename in filenames:
                # Concatenate full path
                file_path = os.path.join(foldername, filename)
                # Add to ZIP file
                zip_ref.write(file_path, os.path.relpath(file_path, src_folder))

def GetDirList(dir_path: str, type = "both") -> list[str]:
    """
    List all files and subdirectories in a directory
    Args:
        dir_path: Directory path
        type: What to list, "file" for files, "dir" for subdirectories, "both" for both
        return: List of all files and subdirectories in the directory
    """
    # Check if directory exists
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory {dir_path} does not exist or is not a directory.")
    # Get all files and subdirectories in the directory
    items = os.listdir(dir_path)
    # Filter by type
    if type == "file":
        return [item for item in items if os.path.isfile(os.path.join(dir_path, item))]
    elif type == "dir":
        return [item for item in items if os.path.isdir(os.path.join(dir_path, item))]
    else:
        return items
    
def FileExist(file_path: str) -> bool:
    """
    Check if a file exists
    Args:
        file_path: File path
        return: Returns True if the file exists, otherwise returns False
    """
    return os.path.isfile(file_path)

def DirExist(dir_path: str) -> bool:
    """
    Check if a directory exists
    Args:
        dir_path: Directory path
        return: Returns True if the directory exists, otherwise returns False
    """
    return os.path.isdir(dir_path)

def MakeDir(dir_name: str):
    """
    Create a directory
    Args:
        dir_name: Directory name
    """
    # Create directory
    os.makedirs(dir_name, exist_ok=True)

def GetFileName(file_path: str) -> str:
    """
    Get file name (with extension)
    Args:
        file_path: File path
        return: File name (with extension)
    """
    return os.path.basename(file_path)

def GetFileNameWithoutExt(file_path: str) -> str:
    """
    Get file name (without extension)
    Args:
        file_path: File path
        return: File name (without extension)
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def GetFileExt(file_path: str) -> str:
    """
    Get file extension
    Args:
        file_path: File path
        return: File extension
    """
    return os.path.splitext(file_path)[1]

def GetFileDir(file_path: str) -> str:
    """
    Get directory containing the file
    Args:
        file_path: File path
        return: Directory containing the file
    """
    dir = os.path.dirname(file_path)
    return dir if dir else "."

def CopyFile(src_path: str, dst_path: str):
    """
    Copy a file
    Args:
        src_path: Source file path
        dst_path: Destination file path
    """
    # Copy file
    with open(src_path, 'rb') as src_file:
        with open(dst_path, 'wb') as dest_file:
            dest_file.write(src_file.read())

def CopyDir(src_path: str, dst_path: str):
    """
    Copy a directory
    Args:
        src_path: Source directory path
        dst_path: Destination directory path
    """
    MakeDir(dst_path)
    # Traverse all files and subdirectories in the source directory
    for item in os.listdir(src_path):
        # Concatenate full path
        src_item = os.path.join(src_path, item)
        dst_item = os.path.join(dst_path, item)
        # If it is a directory, recursively copy
        if os.path.isdir(src_item):
            MakeDir(dst_item)
            CopyDir(src_item, dst_item)
        else:
            CopyFile(src_item, dst_item)

def DeleteFile(file_path: str):
    """
    Delete a file
    Args:
        file_path: File path
    """
    # Delete file
    os.remove(file_path)

def DeleteDir(dir_path: str):
    """
    Delete a directory
    Args:
        dir_path: Directory path
    """
    # Delete directory and its contents
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            DeleteDir(item_path)
        else:
            DeleteFile(item_path)
    os.rmdir(dir_path)

def MoveFile(src_path: str, dst_path: str, exist_ok: bool = False):
    """
    Move a file
    Args:
        src_path: Source file path
        dst_path: Destination file path
        exist_ok: Whether to overwrite if the destination file already exists
    """
    if exist_ok:
        if FileExist(dst_path): DeleteFile(dst_path)
        elif DirExist(dst_path): raise IsADirectoryError(f"Destination path '{dst_path}' is a directory, but not a file.")
        os.rename(src_path, dst_path)
    else:
        if os.path.exists(dst_path):
            raise FileExistsError(f"Destination file or directory '{dst_path}' already exists.")
        os.rename(src_path, dst_path)

def SearchFiles(dir_path: str, exts: list[str]) -> list[str]:
    """
    Search for files with specified extensions in a directory
    Args:
        dir_path: Directory path
        exts: List of file extensions to search for (e.g. ['.jpg', '.png'])
        return: List of file paths that match the specified extensions
    """
    # Check if directory exists
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory {dir_path} does not exist or is not a directory.")
    # Search for files with specified extensions
    files = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in exts):
                files.append(os.path.join(root, filename))
    return files


##############################################################
##                      Other Functions                     ##
##############################################################

def Ceil(x: float) -> int:
    """
    Ceiling function (round up)
    Args:
        x: Float number
        return: Integer
    """
    return int(x) + (x % 1 > 0) if x > 0 else int(x)



if __name__ == "__main__":
    # Test the functions
    exts = [".jpg", ".png"]
    dir_path = "."
    files = SearchFiles(dir_path, exts)
    for file in files:
        print(file)
