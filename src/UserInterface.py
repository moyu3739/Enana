from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from Family import Family
from Workbench import Workbench


class CmdUserInterface:
    def __init__(self, family: Family, workbench: Workbench):
        self.family = family
        self.workbench = workbench
        self.console = Console()
        
    def InitWorkbench(self):
        # 显示初始化提示，添加旋转图标
        spinner = Spinner('dots', text="[bold blue]文件预处理...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.InitWorkbench()
            # 修改最后的文本，去掉旋转图标
            live.update("[bold green]  文件预处理完成！[/bold green]\n")

    def ProcessAllImage(self):
        # 使用 rich.progress 创建进度条，添加旋转图标（使用默认颜色）
        with Progress(
            SpinnerColumn(style="none"),
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TextColumn("{task.percentage:>3.0f}%")
        ) as progress_bar:
            # 设置进度条的初始值为已完成的图片数量
            task = progress_bar.add_task("[bold blue]图片放大中...[/bold blue]", total=1)
            # 处理图片
            for (done_count, total_count) in self.workbench.ProcessAllImage(self.family):
                progress_bar.update(task, completed=done_count, total=total_count) # 更新进度条
            progress_bar.update(task, description="[bold green]全部图片放大完成！[/bold green]\n") # 更新进度条到完成状态

    def GenerateTarget(self):
        # 使用rich显示后处理提示，添加旋转图标
        spinner = Spinner('dots', text="[bold blue]生成目标文件...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.GenerateTarget()
            # 修改最后的文本，去掉旋转图标
            live.update("[bold green]  生成目标文件完成！[/bold green]\n")

