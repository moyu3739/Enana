import sys
from Option import ParseOptions
from Error import *
from Family import *
import FamilyList
from Workbench import Workbench
from UserInterface import CmdUserInterface


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
        # Process EPUB file
        else:
            family = FamilyList.GetFamilyClass(options["family"])(options)

            # If family is CommonFamily, alert the user
            if isinstance(family, CommonFamilyBase):
                ui.Print(f"[bold yellow][Warning][/bold yellow] local family '{options['family']}' "\
                          "is not adapted specifically, so it may fail or cause some problems in output file.")

            workbench = Workbench(options)
            ui.Bound(family, workbench)

            # preview a image
            if options["preview"]:
                ui.InitWorkbench()
                ui.GeneratePreviewImage()
            # process images
            else:
                if options["restart"]:
                    ui.Print("[bold blue][Info][/bold blue] Restart progress", end="\n\n")
                    ui.InitWorkbench()
                elif not workbench.WorkbenchExist():
                    ui.Print("[bold blue][Info][/bold blue] Checkpoint not found, start progress from scratch", end="\n\n")
                    ui.InitWorkbench()
                else:
                    ui.Print("[bold blue][Info][/bold blue] Checkpoint found, continue progress from last time (if you want to restart, use -r option)", end="\n\n")
                ui.ProcessAllImage()
                ui.GenerateEpubTarget()

        exit_code = 0

    # Command line option errors
    except FileNotFoundError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 11
    except NotEpubFileError as e:
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
    except ImageQualityValueInvalidError as e:
        ui.Print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 17

    # Runtime errors (after workbench initialization)
    except FileCorruptedError as e:
        workbench.CleanupWorkbench() # Clean up workbench
        ui.Print(f"[bold red]Runtime error:[/bold red] {e}")
        exit_code = 51
    except ModelRuntimeError as e:
        workbench.CleanupWorkbench() # Clean up workbench
        ui.Print(f"[bold red]Runtime error:[/bold red] {e}")
        exit_code = 52

    # Other exceptions
    except KeyboardInterrupt:
        ui.Print("\n[bold red]Process interrupted by user.[/bold red]")
        exit_code = 2
    except Exception as e:
        workbench.CleanupWorkbench() # Clean up workbench
        ui.Print(f"[bold red]Error:[/bold red] {e}")
        exit_code = 1
    
    sys.exit(exit_code)


"""
python src/main.py -h
python src/main.py -lf
python src/main.py -lm
python src/main.py -i "test.jpg"
python src/main.py -i "ha.epub"
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f ha
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -m ha
python src/main.py -i "[安達與島村(重製版)]卷01 损坏.epub"
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -m Omni-MiniV2-W2xEX -s 4

python src/main.py -i "[安達與島村(重製版)]卷01.epub" -s 2 -r
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -o "an.epub" -m realesrgan-x4plus-anime -s 1.5 -q 60
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -p
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -s 4 -m RealESRGANv2-animevideo-xsx4
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f waifu2x-ncnn-vulkan -m models-upconv_7_anime_style_art_rgb -s 4
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f realcugan-ncnn-vulkan -m models-se -s 2

python src/main.py -i "[終將成為妳]卷04.epub" -m Omni-MiniV2-W2xEX
"""
if __name__ == "__main__":
    # args = [
    #     "-i", "[安達與島村(重製版)]卷01.epub",
    #     "-s", "2",
    #     "-f", "realcugan-ncnn-vulkan",
    #     "-m", "models-se"
    # ]
    # CmdMain(args)

    CmdMain()
