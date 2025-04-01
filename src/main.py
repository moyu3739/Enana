import sys
from rich.console import Console
from Option import ParseOptions
from Error import *
from Family import *
import FamilyList
from Workbench import Workbench
from UserInterface import CmdUserInterface


def main(args: list[str] = sys.argv[1:]):
    # Create rich console object
    console = Console()
    
    try:
        options = ParseOptions(args)
        # List all families
        if options["list_family"]:
            family_list = FamilyList.GetAllFamilies()
            console.print("[bold blue]All available families:[/bold blue]")
            for family in family_list:
                console.print(f"  - [green]{family}[/green]")
        # List all models of specified family
        elif options["list_model"]:
            model_list = FamilyList.GetFamilyClass(options["family"]).GetAllModels()
            console.print(f"[bold blue]All available models of family '{options['family']}':[/bold blue]")
            for model in model_list:
                console.print(f"  - [green]{model}[/green]")
        # Process EPUB file
        else:
            family = FamilyList.GetFamilyClass(options["family"])(options)

            # If family is CommonFamily, alert the user
            if isinstance(family, CommonFamilyBase):
                console.print(f"[bold yellow]Warning:[/bold yellow] local family '{options['family']}' "\
                               "is not implemented specifically, so be careful using it.")

            workbench = Workbench(options)
            ui = CmdUserInterface(family, workbench)
                
            ui.InitWorkbench()
            ui.ProcessAllImage()
            ui.GenerateTarget()

        exit_code = 0

    # Command line option errors
    except FileNotFoundError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 11
    except NotEpubFileError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 12
    except OutputPathIsDirError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 13
    except FamilyNotFoundError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 14
    except ModelNotFoundError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 15
    except ScaleValueInvalidError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 16
    except ImageQualityValueInvalidError as e:
        console.print(f"[bold red]Options error:[/bold red] {e}")
        exit_code = 17

    # Runtime errors (after workbench initialization)
    except FileCorruptedError as e:
        workbench.CleanupWorkbench() # Clean up workbench
        console.print(f"[bold red]Runtime error:[/bold red] {e}")
        exit_code = 51
    except ModelRuntimeError as e:
        workbench.CleanupWorkbench() # Clean up workbench
        console.print(f"[bold red]Runtime error:[/bold red] {e}")
        exit_code = 52

    # Other exceptions
    except Exception as e:
        workbench.CleanupWorkbench() # Clean up workbench
        console.print(f"[bold red]Error:[/bold red] {e}")
        exit_code = 1
    except KeyboardInterrupt:
        console.print("\n[bold red]Process interrupted by user.[/bold red]")
        exit_code = 2
    
    sys.exit(exit_code)


"""
python src/main.py -h
python src/main.py -lf
python src/main.py -lm
python src/main.py -c
python src/main.py -i "test.jpg"
python src/main.py -i "ha.epub"
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f ha
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -m ha
python src/main.py -i "[安達與島村(重製版)]卷01 损坏.epub"
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -m Omni-MiniV2-W2xEX -s 4
python src/main.py -i "test.epub" -o "test"

python src/main.py -i "[安達與島村(重製版)]卷01.epub" -s 2
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f realcugan-ncnn-vulkan -s 4
python src/main.py -i "[安達與島村(重製版)]卷01.epub" -f waifu2x-ncnn-vulkan -s 4 -m models-upconv_7_anime_style_art_rgb

python src/main.py -i "[終將成為妳]卷04.epub" -m Omni-MiniV2-W2xEX
"""
if __name__ == "__main__":
    # args = [
    #     "-i", "[安達與島村(重製版)]卷01.epub",
    #     "-s", "2",
    #     "-f", "realcugan-ncnn-vulkan",
    #     "-m", "models-se"
    # ]
    # main(args)

    main()
