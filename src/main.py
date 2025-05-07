import sys
import re
from Option import ParseOptions
from Error import *
from Family import *
import FamilyList
import WorkbenchList
from UserInterface import CmdUserInterface


def Work(ui, options: dict):
    # preview a image
    if options["preview"]:
        ui.InitWorkbench()
        ui.GeneratePreviewImage()
    # process images
    else:
        if options["restart"]:
            ui.Print("[bold blue][Info][/bold blue] Restart progress", end="\n\n")
            ui.InitWorkbench()
        elif not ui.workbench.WorkbenchInitialized():
            ui.Print("[bold blue][Info][/bold blue] Checkpoint not found, start progress from scratch", end="\n\n")
            ui.InitWorkbench()
        else:
            ui.Print("[bold blue][Info][/bold blue] Checkpoint found, continue progress from last time (if you want to restart, use -r option)", end="\n\n")
        ui.ProcessAllImage()
        ui.GenerateTarget()

def GetOutputPath(input_path: str, output_format: str):
    # replace "?" with input filename without extension
    output_filename = output_format.replace("?", GetFileNameWithoutExt(input_path))
    # replace "*" with input filename with extension (without "." prefix)
    output_filename = output_filename.replace("*", GetFileExt(input_path)[1:])
    return f"{GetFileDir(input_path)}/{output_filename}"

def CmdMain(args: list[str] = sys.argv[1:]):
    # Create rich console object
    ui = CmdUserInterface()
    
    try:
        options = ParseOptions(args)
        # List all families
        if options["list_family"]:
            family_list = FamilyList.GetAllFamilies()
            ui.Print("[bold blue]All available families:[/bold blue]")
            for family in family_list:
                ui.Print(f"  - [green]{family}[/green]")
        # List all models of specified family
        elif options["list_model"]:
            model_list = FamilyList.GetFamilyClass(options["family"]).GetAllModels()
            ui.Print(f"[bold blue]All available models of family '{options['family']}':[/bold blue]")
            for model in model_list:
                ui.Print(f"  - [green]{model}[/green]")
        # Process
        else:
            # get Family class from family name
            FamilyType = FamilyList.GetFamilyClass(options["family"])
            # If Family is derived from CommonFamilyBase, alert the user
            if issubclass(FamilyType, CommonFamilyBase):
                ui.Print(f"[bold yellow][Warning][/bold yellow] local family '{options['family']}' "\
                          "is not adapted specifically, so it may fail or cause some problems in output file.")

            input_format: str = options["input_path"]
            # If output path is not provided, set the default output
            if options["output_path"] is None:
                output_format = f"? {APP_NAME}.*"
            else:
                output_format = options["output_path"]

            if options["batch"]:
                input_paths = SearchFilesRegex(".", input_format, True)

                io_paths = {input_path: GetOutputPath(input_path, output_format) for input_path in input_paths}

                if len(io_paths) == 0:
                    ui.Print(f"[bold magenta]No files matched![/bold magenta]")
                else:
                    ui.Print(f"[bold magenta]Matched files:[/bold magenta]")
                    for input_path, output_path in io_paths.items():
                        ui.Print(f"  - [cyan]'{input_path}'[/cyan] [yellow]->[/yellow] [cyan]'{output_path}'[/cyan]")
                    input("Press Enter to start...")
            else:
                input_paths = [input_format]
                io_paths = {input_format: GetOutputPath(input_format, output_format)}

            records = {input_path: False for input_path in input_paths}
            for i, input_path in enumerate(input_paths):
                try:
                    ui.Print(f"[bold magenta]Processing file:[/bold magenta] [magenta]'{input_path}'[/magenta] [yellow]({i+1}/{len(input_paths)})[/yellow]")
                    options_i = options.copy()
                    options_i["input_path"] = input_path
                    options_i["output_path"] = io_paths[input_path]

                    WorkbenchType = WorkbenchList.GetWorkbenchClass(options_i["input_path"])
                    family = FamilyType(options_i)
                    workbench = WorkbenchType(options_i)
                    ui.Bound(family, workbench)

                    Work(ui, options_i)
                    records[input_path] = True

                # Runtime errors (after workbench initialization)
                except FileCorruptedError as e:
                    workbench.CleanupWorkbench() # Clean up workbench
                    ui.Print(f"[bold red]Runtime error:[/bold red] {e}")
                    exit_code = 51
                except ModelRuntimeError as e:
                    workbench.CleanupWorkbench() # Clean up workbench
                    ui.Print(f"[bold red]Runtime error:[/bold red] {e}")
                    exit_code = 52

            if options["batch"]:
                ui.Print("[bold magenta]All matched files processed.[/bold magenta]")
                success = [input_path for input_path, flag in records.items() if flag]
                failed  = [input_path for input_path, flag in records.items() if not flag]
                if len(success) > 0:
                    ui.Print(f"[bold green]Success:[/bold green]")
                    for input_path in success:
                        ui.Print(f"  - [green]'{input_path}'[/green] [yellow]->[/yellow] [green]'{io_paths[input_path]}'[/green]")
                if len(failed) > 0:
                    ui.Print(f"[bold red]Failed:[/bold red]")
                    for input_path in failed:
                        ui.Print(f"  - [red]'{input_path}'[/red] [yellow]->[/yellow] [red]'{io_paths[input_path]}'[/red]")

        exit_code = 0

    # Command line option errors
    except InputFileNotFoundError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 11
    except UnsupportedSourceTypeError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 12
    except OutputPathIsDirError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 13
    except FamilyNotFoundError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 14
    except ModelNotFoundError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 15
    except ScaleValueInvalidError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 16
    except PreScaleValueInvalidError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 17
    except ImageQualityValueInvalidError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 18
    except JobsValueInvalidError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 19

    # # Runtime errors (after workbench initialization)
    # except FileCorruptedError as e:
    #     workbench.CleanupWorkbench() # Clean up workbench
    #     ui.Print(f"[bold red]Runtime error:[/bold red] {e}")
    #     exit_code = 51
    # except ModelRuntimeError as e:
    #     workbench.CleanupWorkbench() # Clean up workbench
    #     ui.Print(f"[bold red]Runtime error:[/bold red] {e}")
    #     exit_code = 52

    # Other exceptions
    except KeyboardInterrupt:
        ui.Print("\n[bold red]Process interrupted by user.[/bold red]")
        exit_code = 2
    # except Exception as e:
    #     if workbench.progress.GetTaskNumOfStatus("done") == 0:
    #         workbench.CleanupWorkbench() # Clean up workbench
    #     ui.Print(f"[bold red]Error:[/bold red] {e}")
    #     exit_code = 1
    
    sys.exit(exit_code)


"""
python src/main.py -h
python src/main.py -v
python src/main.py -lf
python src/main.py -lm
python src/main.py -i "test.jpg"
python src/main.py -i "ha.epub"
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f ha
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -m ha
python src/main.py -i "[安達與島村(重製版)]卷01 损坏.epub"
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -m Omni-MiniV2-W2xEX -s 4

python src/main.py -i "[安達與島村(重製版)]卷01.epub" -s 2 -j 4
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -o "../[HD] ?.*" -s 2 -j 2
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -o "an.epub" -m realesrgan-x4plus-anime -s 1.5 -q 60
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -p
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -ps 0.1 -p
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -s 4 -m RealESRGANv2-animevideo-xsx4
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f waifu2x-ncnn-vulkan -m models-upconv_7_anime_style_art_rgb -s 4
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f realcugan-ncnn-vulkan -m models-se -s 5 -r -j 4
python src/main.py -i "a.pdf" -s 2 -j 2
python src/main.py -i "zjuthesis.pdf" -s 2 -j 2


python src/main.py -i "[終將成為妳]卷04.epub" -s 2

python src/main.py -i ".*安達與島村.*卷0[1-9].*" -o "../HD ? ENANA.*" -s 2 -j 2 -b
python src/main.py -i ".*安達與島村.*卷0[1-9].epub" -s 2 -j 2 -b
"""
if __name__ == "__main__":
    # args = [
    #     "-i", ".*安達與島村.*卷0[1-9].epub",
    #     # "-o", "% HD.epub",
    #     "-s", "2",
    #     "-j", "2",
    # ]
    # CmdMain(args)

    CmdMain()
