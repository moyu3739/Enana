import os
import sys


APP_NAME = "enana" # E NAtive Neural Amplifier
VERSION = "0.3.2" # Version number

# if running with python
if sys.argv[0].lower().endswith(".py"):
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    USAGE_PROG = f"python {sys.argv[0]}"
else:
    ROOT = os.path.dirname(os.path.abspath(__file__))
    USAGE_PROG = APP_NAME



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
    import zipfile
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
    import zipfile
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
        raise FileNotFoundError(f"Directory '{dir_path}' does not exist or is not a directory.")
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
    Copy a file, if the source file and destination file are the same, do nothing
    Args:
        src_path: Source file path
        dst_path: Destination file path
    """
    # normalize paths
    src_path = os.path.abspath(src_path)
    dst_path = os.path.abspath(dst_path)
    # check if source path is same as destination path
    if src_path == dst_path: return    

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
    # normalize paths
    src_path = os.path.abspath(src_path)
    dst_path = os.path.abspath(dst_path)
    # check if source path is same as destination path
    if src_path == dst_path: return    
    # check if destination path is a subdirectory of source path
    if dst_path.startswith(src_path + os.sep):
        raise ValueError(f"Destination path '{dst_path}' is a subdirectory of source path '{src_path}'")
    
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

def ClearDir(dir_path: str):
    """
    Clear a directory (delete all files and subdirectories)
    Args:
        dir_path: Directory path
    """
    # Delete all files and subdirectories in the directory
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            DeleteDir(item_path)
        else:
            DeleteFile(item_path)

def DeleteDir(dir_path: str):
    """
    Delete a directory
    Args:
        dir_path: Directory path
    """
    ClearDir(dir_path)
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

def SearchFiles(dir_path: str, exts: list[str], relative: bool = False) -> list[str]:
    """
    Search for files with specified extensions in a directory
    Args:
        dir_path: Directory path
        exts: List of file extensions to search for (e.g. ['.jpg', '.png'])
        relative: Whether to return relative paths (True) or absolute paths (False)
        return: List of file paths that match the specified extensions
    """
    # Check if directory exists
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory '{dir_path}' does not exist or is not a directory.")
    # Search for files with specified extensions
    files = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in exts):
                file_path = os.path.join(root, filename)
                if relative:
                    file_path = os.path.relpath(file_path, dir_path)
                files.append(file_path)
    return files

def SearchFilesRegex(dir_path: str, regex: str, relative: bool = False) -> list[str]:
    """
    Search for files matching the specified regex in a directory
    Args:
        dir_path: Directory path
        regex: Regular expression to match relative path to `dir_path`
        relative: Whether to return relative paths (True) or absolute paths (False)
        return: List of file paths that fully match the specified regex
    """
    import re
    # Check if directory exists
    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory '{dir_path}' does not exist or is not a directory.")
    # Search for files matching the specified regex
    files = []
    for root, _, filenames in os.walk(dir_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if re.fullmatch(regex, file_path):
                if relative:
                    file_path = os.path.relpath(file_path, dir_path)
                files.append(file_path)
    return files


##################################################################
##                 Functions for PDF Operations                 ##
##################################################################

def PdfExtractImages(pdf_path: str, output_dir: str, jpg_quality: int = 95):
    """
    Extract images from PDF file and save them to specified directory
    
    Args:
        pdf_path: PDF file path
        output_dir: Output directory path
    """
    from pymupdf import Document as PdfDoc
    from pymupdf import Page as PdfPage
    from pymupdf import Pixmap as PdfPixmap

    # make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # open the PDF file
    doc = PdfDoc(pdf_path)
    
    # traverse each page
    for page in doc:
        # get image list
        image_list = page.get_images(full=True)
        
        # traverse each image in the page
        for img_info in image_list:
            # get image xref
            xref = img_info[0]
            
            # extract image bytes and smask
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_smask = base_image["smask"]
            image_ext = base_image["ext"]
            # print(f"xref={xref}, ext={image_ext}, smask={image_smask}")

            # without mask, save directly
            if image_smask == 0:
                image_path = f"{output_dir}/{xref}.{image_ext}"
                pix = PdfPixmap(image_bytes)
                pix.save(image_path, jpg_quality=jpg_quality)
            # with mask, save with alpha channel
            else:
                image_path = f"{output_dir}/{xref}.png"
                pix = PdfPixmap(image_bytes)
                mask = PdfPixmap(doc.extract_image(image_smask)["image"])
                pix_a = PdfPixmap(pix, mask)
                pix_a.save(image_path)
    
    doc.close()

def PdfReplaceOneImage(page, xref: int, filename=None, pixmap=None, stream=None):
    """
    Replace the image referred to by xref.

    Args:
        xref: the xref of the image to replace.
        filename, pixmap, stream: exactly one of these must be provided. The
            meaning being the same as in Page.insert_image.
    """
    from pymupdf import Document as PdfDoc
    from pymupdf import Page as PdfPage
    from pymupdf import Pixmap as PdfPixmap

    doc = page.parent  # the owning document
    if not doc.xref_is_image(xref):
        raise ValueError("xref not an image")  # insert new image anywhere in page
    if bool(filename) + bool(stream) + bool(pixmap) != 1:
        raise ValueError("Exactly one of filename/stream/pixmap must be given")
    new_xref = page.insert_image(
        page.rect, filename=filename, stream=stream, pixmap=pixmap
    )
    doc.xref_copy(new_xref, xref)  # copy over new to old
    page.delete_image(new_xref) # delete the new image reference
    last_contents_xref = page.get_contents()[-1]

    # new image insertion has created a new /Contents source,
    # which we will set to spaces now
    doc.update_stream(last_contents_xref, b" ")
    page._image_info = None  # clear cache of extracted image information

    

def PdfReplaceImages(pdf_path: str, images: dict[int, str], output_pdf_path: str):
    """
    Replace images in PDF file with specified images
    
    Args:
        pdf_path: original PDF path
        images: dict{xref: image path}
        output_pdf_path: output PDF path
    """
    from pymupdf import Document as PdfDoc
    from pymupdf import Page as PdfPage
    from pymupdf import Pixmap as PdfPixmap

    # open the PDF file
    doc = PdfDoc(pdf_path)

    # traverse each page, collect all images in the PDF
    all_images: list[tuple[PdfPage, int]] = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_info in image_list:
            xref = img_info[0]
            all_images.append((page, xref))
        
    # traverse each image in the PDF, replace it with the corresponding image
    for page, xref in all_images:
        image_path = images.get(xref)
        if image_path is None: continue
        PdfReplaceOneImage(page, xref, filename=image_path)
    
    # save the modified PDF
    doc.ez_save(output_pdf_path, deflate_images=False, garbage=4)
    doc.close()

def PdfGetFirstImage(pdf_path: str) -> tuple[int, dict] | tuple[None, None]:
    """
    Get the xref and information of the first image in the PDF file.
    """
    from pymupdf import Document as PdfDoc
    from pymupdf import Page as PdfPage
    from pymupdf import Pixmap as PdfPixmap

    # open the PDF file
    doc = PdfDoc(pdf_path)
    # traverse each page
    for page in doc:
        image_list = page.get_images(full=True) # get image list
        if len(image_list) > 0:
            xref = image_list[0][0]
            return xref, doc.extract_image(xref)
    return None, None


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
    # # Test the functions
    # exts = [".jpg", ".png"]
    # dir_path = "D:/PythonProject/Enana"
    # files = SearchFiles(dir_path, exts, relative=True)
    # for file in files:
    #     print(file)

    # DeleteDir("test")

    dir_path = "."
    regex = r".*\.epub"
    files = SearchFilesRegex(dir_path, regex, True)
    for file in files:
        print(file)
    print(len(files))
