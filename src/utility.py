import os
import zipfile

APP_NAME = "HimageEpub"
ROOT = "D:/PythonProject/HimageEpub"


##############################################################
##                  文件和目录操作相关的函数                  ##
##############################################################

def UnpackZip(zip_path: str, extract_folder: str):
    """
    解压缩ZIP文件到指定目录
    Args:
        zip_path: ZIP文件路径
        extract_folder: 解压缩目标目录
    """
    # 打开ZIP文件
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 解压文件到指定目录
        zip_ref.extractall(extract_folder)

def PackZip(src_folder: str, zip_path: str):
    """
    将指定目录打包成ZIP文件
    Args:
        src_folder: 源目录路径
        zip_path: ZIP文件路径
    """
    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        # 遍历目录中的所有文件
        for foldername, subfolders, filenames in os.walk(src_folder):
            for filename in filenames:
                # 拼接完整路径
                file_path = os.path.join(foldername, filename)
                # 添加到ZIP文件中
                zip_ref.write(file_path, os.path.relpath(file_path, src_folder))

def GetDirList(dir_path: str, type = "both") -> list[str]:
    """
    列出目录中的所有文件和子目录
    Args:
        dir_path: 目录路径
        type: 列出文件还是子目录，"file"表示文件，"dir"表示子目录，"both"表示两者都列出
        return: 目录中的所有文件和子目录列表
    """
    # 检查目录是否存在
    if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory {dir_path} does not exist or is not a directory.")
    # 获取目录中的所有文件和子目录
    items = os.listdir(dir_path)
    # 根据类型过滤
    if type == "file":
        return [item for item in items if os.path.isfile(os.path.join(dir_path, item))]
    elif type == "dir":
        return [item for item in items if os.path.isdir(os.path.join(dir_path, item))]
    else:
        return items
    
def FileExist(file_path: str) -> bool:
    """
    检查文件是否存在
    Args:
        file_path: 文件路径
        return: 如果文件存在返回True，否则返回False
    """
    return os.path.isfile(file_path)

def DirExist(dir_path: str) -> bool:
    """
    检查目录是否存在
    Args:
        dir_path: 目录路径
        return: 如果目录存在返回True，否则返回False
    """
    return os.path.isdir(dir_path)

def MakeDir(dir_name: str):
    """
    创建目录
    Args:
        dir_name: 目录名称
    """
    # 创建目录
    os.makedirs(dir_name, exist_ok=True)

def GetFileName(file_path: str) -> str:
    """
    获取文件名（带扩展名）
    Args:
        file_path: 文件路径
        return: 文件名（带扩展名）
    """
    return os.path.basename(file_path)

def GetFileNameWithoutExt(file_path: str) -> str:
    """
    获取文件名（不带扩展名）
    Args:
        file_path: 文件路径
        return: 文件名（不带扩展名）
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def GetFileExt(file_path: str) -> str:
    """
    获取文件扩展名
    Args:
        file_path: 文件路径
        return: 文件扩展名
    """
    return os.path.splitext(file_path)[1]

def GetFileDir(file_path: str) -> str:
    """
    获取文件所在目录
    Args:
        file_path: 文件路径
        return: 文件所在目录
    """
    dir = os.path.dirname(file_path)
    return dir if dir else "."

def CopyFile(src_path: str, dst_path: str):
    """
    复制文件
    Args:
        src_path: 源文件路径
        dst_path: 目标文件路径
    """
    # 复制文件
    with open(src_path, 'rb') as src_file:
        with open(dst_path, 'wb') as dest_file:
            dest_file.write(src_file.read())

def CopyDir(src_path: str, dst_path: str):
    """
    复制目录
    Args:
        src_path: 源目录路径
        dst_path: 目标目录路径
    """
    MakeDir(dst_path)
    # 遍历源目录中的所有文件和子目录
    for item in os.listdir(src_path):
        # 拼接完整路径
        src_item = os.path.join(src_path, item)
        dst_item = os.path.join(dst_path, item)
        # 如果是目录，则递归复制
        if os.path.isdir(src_item):
            MakeDir(dst_item)
            CopyDir(src_item, dst_item)
        else:
            CopyFile(src_item, dst_item)

def DeleteFile(file_path: str):
    """
    删除文件
    Args:
        file_path: 文件路径
    """
    # 删除文件
    os.remove(file_path)

def DeleteDir(dir_path: str):
    """
    删除目录
    Args:
        dir_path: 目录路径
    """
    # 删除目录及其内容
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            DeleteDir(item_path)
        else:
            DeleteFile(item_path)
    os.rmdir(dir_path)

def MoveFile(src_path: str, dst_path: str, exist_ok: bool = False):
    """
    移动文件
    Args:
        src_path: 源文件路径
        dst_path: 目标文件路径
        exist_ok: 如果目标文件已存在，是否覆盖
    """
    if exist_ok:
        if FileExist(dst_path): DeleteFile(dst_path)
        elif DirExist(dst_path): raise IsADirectoryError(f"Destination path '{dst_path}' is a directory, but not a file.")
        os.rename(src_path, dst_path)
    else:
        if os.path.exists(dst_path):
            raise FileExistsError(f"Destination file or directory '{dst_path}' already exists.")
        os.rename(src_path, dst_path)


##############################################################
##                         其他函数                          ##
##############################################################

def Ceil(x: float) -> int:
    """
    向上取整
    Args:
        x: 浮点数
        return: 整数
    """
    return int(x) + (x % 1 > 0) if x > 0 else int(x)