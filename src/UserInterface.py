from rich.progress import Progress, TextColumn, BarColumn, SpinnerColumn, TimeElapsedColumn
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from Family import Family
from Workbench import Workbench


class CmdUserInterface:
    def __init__(self, family: Family = None, workbench: Workbench = None):
        self.family = family
        self.workbench = workbench
        self.console = Console()

    def Print(self, *objs, **kwargs):
        self.console.print(*objs, **kwargs)

    def Bound(self, family: Family, workbench: Workbench):
        self.family = family
        self.workbench = workbench
        
    def InitWorkbench(self):
        # Display initialization prompt, add spinner icon
        spinner = Spinner('dots', text="[bold blue]Pre-processing the file...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.InitWorkbench(self.family.supported_image_exts)
            # Modify the final text, remove spinner icon
            live.update("[bold green]  Pre-processing finished![/bold green]\n")

    def ProcessAllImage(self):
        # Use rich.progress to create progress bar, add spinner icon (using default color)
        with Progress(
            SpinnerColumn(style="none"),
            TextColumn("{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TextColumn("{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),  # 添加时间显示组件
        ) as progress_bar:
            # Set the initial value of the progress bar to the number of completed images
            task = progress_bar.add_task("[bold blue]Images processing...[/bold blue]", total=1)
            # Process images
            for (done_count, total_count) in self.workbench.ProcessAllImage(self.family):
                progress_bar.update(task, completed=done_count, total=total_count) # Update progress bar
            progress_bar.update(task, description="[bold green]All images processing finished![/bold green]\n") # Update progress bar to completion status

    def GenerateEpubTarget(self):
        # Use rich to display post-processing prompt, add spinner icon
        spinner = Spinner('dots', text="[bold blue]Generating target file...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.GenerateEpubTarget()
            # Modify the final text, remove spinner icon
            live.update("[bold green]  Generating target file finished![/bold green]\n")

    def GeneratePreviewImage(self):
        # Use rich to display preview image prompt, add spinner icon
        spinner = Spinner('dots', text="[bold blue]Generating preview image...[/bold blue]")
        with Live(spinner, refresh_per_second=10, console=self.console) as live:
            self.workbench.GeneratePreviewImage(self.family)
            # Modify the final text, remove spinner icon
            live.update("[bold green]  Generating preview image finished![/bold green]\n")

