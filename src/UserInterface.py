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
        # Display initialization prompt, add spinner icon
        spinner = Spinner('dots', text="[bold blue]文件预处理...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.InitWorkbench()
            # Modify the final text, remove spinner icon
            live.update("[bold green]  文件预处理完成！[/bold green]\n")

    def ProcessAllImage(self):
        # Use rich.progress to create progress bar, add spinner icon (using default color)
        with Progress(
            SpinnerColumn(style="none"),
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TextColumn("{task.percentage:>3.0f}%")
        ) as progress_bar:
            # Set the initial value of the progress bar to the number of completed images
            task = progress_bar.add_task("[bold blue]图片放大中...[/bold blue]", total=1)
            # Process images
            for (done_count, total_count) in self.workbench.ProcessAllImage(self.family):
                progress_bar.update(task, completed=done_count, total=total_count) # Update progress bar
            progress_bar.update(task, description="[bold green]全部图片放大完成！[/bold green]\n") # Update progress bar to completion status

    def GenerateTarget(self):
        # Use rich to display post-processing prompt, add spinner icon
        spinner = Spinner('dots', text="[bold blue]生成目标文件...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.GenerateTarget()
            # Modify the final text, remove spinner icon
            live.update("[bold green]  生成目标文件完成！[/bold green]\n")

