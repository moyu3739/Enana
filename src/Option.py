import argparse
from utility import *
from Error import *


def ParseOptions(args: list[str]):
    usage = f"{APP_NAME} -h | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY]"
    parser = argparse.ArgumentParser(prog=APP_NAME, usage=usage)
    # parser.add_argument("-c", "--continue", action="store_true",
    #                    dest="continue", 
    #                    help="continue work at interruption of last time. If you use this option, options except -i and -o will be ignored.")

    parser.add_argument("-lf", "--list-family", action="store_true",
                       dest="list_family",
                       help="list all available super-resolution model families")
    parser.add_argument("-lm", "--list-model", action="store_true",
                       dest="list_model",
                       help="list all available models in a specific family (use with -f)")

    parser.add_argument("-i", "--input", action="store", type=str,
                       dest="input_path",
                       help="input file path, or just input file name if you use -c option")
    parser.add_argument("-o", "--output", action="store", type=str,
                       dest="output_path",
                       help="output file path")
    parser.add_argument("-s", "--scale", action="store", type=float,
                       dest="scale",
                       help="scale factor (floating number), range and default depends on model")
    parser.add_argument("-f", "--family", action="store", type=str, default="realesrgan-ncnn-vulkan",
                       dest="family",
                       help="family name of super-resolution models, default=realesrgan-ncnn-vulkan")
    parser.add_argument("-m", "--model", action="store", type=str,
                       dest="model",
                       help="name of the super-resolution model, default depends on family")
    parser.add_argument("-q", "--quality", action="store", type=int, default=75,
                       dest="quality",
                       help="image quality level (0-100), default=75")
    
    # If no arguments are provided, show help information
    if len(args) == 0: 
        parser.print_help()
        parser.exit(0)

    # Parse command line arguments
    options = parser.parse_args(args)
    
    # Handle special modes
    if options.list_family or options.list_model:
        return vars(options)
    
    # Standard mode
    # In standard mode, -i parameter is required
    if options.input_path is None:
        parser.error("the following arguments are required: -i/--input")
    
    # Check the range of -q parameter
    if not 0 <= options.quality <= 100:
        raise ImageQualityValueInvalidError(f"Image quality level must be in range [0, 100], but got {options.quality}.")
    
    # If no output path is provided, use the directory of input path, output filename will be input filename with suffix "_hi"
    if options.output_path is None:
        options.output_path = f"{GetFileDir(options.input_path)}/{GetFileNameWithoutExt(options.input_path)}_hi{GetFileExt(options.input_path)}"
    
    return vars(options)


