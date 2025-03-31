import json
from PIL import Image
from utility import *
from Error import *
from Family import Family


class Workbench:
    """工作区类"""

    def __init__(self, options):
        self.options = options
        self.book_name = GetFileNameWithoutExt(self.options["input_path"])
        self.workbench_dir = f"{ROOT}/workbench/{self.book_name}" # 工作目录
        self.images: list[str] = None # 存放图片文件名
        self.progress: dict[str, str] = None # 存放图片处理进度，key为图片文件名，value为状态 ("waiting", "processing", "done")

    def CleanupWorkbench(self):
        """
        清理工作区
        """
        # 删除工作目录
        if DirExist(self.workbench_dir): DeleteDir(self.workbench_dir)

    def InitWorkbench(self):
        # 创建工作目录
        if not DirExist(self.workbench_dir):
            MakeDir(self.workbench_dir)
        else: # 工作区已经存在同名书
            pass # TODO 询问用户 or 抛出异常？

        # 将源文件复制到工作目录
        CopyFile(self.options["input_path"], f"{self.workbench_dir}/origin.epub")
        # 将源文件解包
        UnpackZip(f"{self.workbench_dir}/origin.epub", f"{self.workbench_dir}/unpack")
        # 检查解包目录中 image 目录是否存在
        if not DirExist(f"{self.workbench_dir}/unpack/image"): # 如果不存在，说明 epub 源文件损坏或没有图片
            raise FileCorruptedError(f"Input file '{self.options["input_path"]}' is corrupted or it has no images.")
        # 获取图片列表
        self.images = GetDirList(f"{self.workbench_dir}/unpack/image", "file")
        self.progress = {image_name: "waiting" for image_name in self.images}
        # 创建存放处理后图片的目录
        MakeDir(f"{self.workbench_dir}/himage")

        # 保存选项和进度
        self.WriteOptions()
        self.WriteProgress()

    def GenerateTarget(self):
        """
        生成目标文件
        """
        # 将处理后的图片复制到解包目录中（覆盖）
        CopyDir(f"{self.workbench_dir}/himage", f"{self.workbench_dir}/unpack/image")
        # 压缩文件到输出目录
        output_path = self.options["output_path"]
        tmp_output_path = f"{GetFileDir(output_path)}/${GetFileNameWithoutExt(output_path)}.tmp"
        MakeDir(GetFileDir(output_path))
        PackZip(f"{self.workbench_dir}/unpack", tmp_output_path)
        MoveFile(tmp_output_path, output_path, exist_ok=True)
        # 删除工作目录
        # self.CleanupWorkbench()

    def ProcessAllImage(self, family: Family):
        """返回一个生成器，生成器每次返回已完成的图片数量和总图片数量"""
        # 读取选项和进度
        self.ReadOptions()
        self.ReadProgress()
        # 将所有 "processing" 状态的图片改为 "waiting" 状态（上一次处理未完成），保持 "done" 状态的图片不变
        for image_name, status in self.progress.items():
            if status == "processing": self.progress[image_name] = "waiting"

        # 获取已完成的图片数量和总图片数量
        done_count = self.GetStatusCount("done")
        total_count = len(self.progress)
        yield (done_count, total_count)
        
        # 处理图片
        while self.ProcessOneImage(family):
            done_count += 1
            yield (done_count, total_count)

    def ProcessOneImage(self, family: Family) -> bool:
        """
        处理一张图片，返回是否还有下一张图片需要处理
        """
        image_name = self.GetOneWaitingImage()
        if image_name is None: return False
        self.progress[image_name] = "processing"
        self.WriteProgress()
        # 处理图片
        input_file  = f"{self.workbench_dir}/unpack/image/{image_name}"
        output_file = f"{self.workbench_dir}/himage/{image_name}"
        family.ProcessImage(input_file, output_file)
        self.ScaleAndCompress(output_file, output_file, self.options["scale"] / family.model_scale, self.options["quality"])

        self.progress[image_name] = "done"
        self.WriteProgress()
        return True
    
    @classmethod
    def ScaleAndCompress(cls, input_file: str, output_file: str, scale_ratio: float, quality_level: int):
        """
        缩放并压缩图片
        Args:
            input_file: 输入图片文件路径
            output_file: 输出图片文件路径
            scale_ratio: 缩放比例
            quality_level: 质量等级 (0-100)，值越大压缩越小
        """
        # 打开图片
        img = Image.open(input_file)
        
        if scale_ratio != 1.0:
            # 计算新的尺寸
            new_width = int(img.width * scale_ratio)
            new_height = int(img.height * scale_ratio)
            # 缩放图片（使用高质量的LANCZOS重采样）
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if quality_level < 100:
            match img.format:
                case "JPEG": img.save(output_file, quality=quality_level, optimize=True)
                case "PNG": img.save(output_file, compress_level=7, optimize=True)
                case _: img.save(output_file, quality=quality_level, optimize=True)

    def ReadOptions(self) -> dict:
        with open(f"{self.workbench_dir}/options.json", "r") as f:
            self.options = json.load(f)

    def WriteOptions(self):
        with open(f"{self.workbench_dir}/options.json", "w") as f:
            json.dump(self.options, f, indent=4)

    def ReadProgress(self) -> dict[str, str]:
        with open(f"{self.workbench_dir}/progress.json", "r") as f:
            self.progress = json.load(f)

    def WriteProgress(self):
        with open(f"{self.workbench_dir}/progress.json", "w") as f:
            json.dump(self.progress, f, indent=4)

    def GetOneWaitingImage(self) -> str | None:
        """
        获取一个等待处理的图片名称
        """
        for image_name, status in self.progress.items():
            if status == "waiting": return image_name
        return None
    
    def GetStatusCount(self, count_status: str) -> int:
        """
        统计当前进度中指定状态的图片数量
        count_status: 计数状态，"waiting", "processing", "done"
        """
        return len([image_name for image_name, status in self.progress.items() if status == count_status])


