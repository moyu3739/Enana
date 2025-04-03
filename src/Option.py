import argparse
from utility import *
from Error import *


def ParseOptions(args: list[str]):
    usage = f"{USAGE_PROG} -h | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-p] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY] [-r]"
    parser = argparse.ArgumentParser(prog=APP_NAME, usage=usage)

    parser.add_argument("-lf", "--list-family", action="store_true",
                       dest="list_family",
                       help="to list all available super-resolution model families")
    parser.add_argument("-lm", "--list-model", action="store_true",
                       dest="list_model",
                       help="to list all available models in a specific family (use with -f)")
    parser.add_argument("-i", "--input", action="store", type=str,
                       dest="input_path",
                       help="input file path (required)")
    parser.add_argument("-o", "--output", action="store", type=str,
                       dest="output_path",
                       help="output file path (optional, default is the input filename with \"_enana\" suffix)")
    parser.add_argument("-p", "--preview", action="store_true",
                       dest="preview",
                       help="to output preview image. If you use this option, the program will choose an image in your EPUB file and output its original and processed copy to the output directory.")
    parser.add_argument("-s", "--scale", action="store", type=float,
                       dest="scale",
                       help="scaling factor (floating number), range and default value depends on the selected model")
    parser.add_argument("-f", "--family", action="store", type=str, default="realesrgan-ncnn-vulkan",
                       dest="family",
                       help="family name of super-resolution models, default=realesrgan-ncnn-vulkan")
    parser.add_argument("-m", "--model", action="store", type=str,
                       dest="model",
                       help="name of the super-resolution model, default value depends on the selected family")
    parser.add_argument("-q", "--quality", action="store", type=int, default=75,
                       dest="quality",
                       help="image quality level (0-100), default=75")
    parser.add_argument("-r", "--restart", action="store_true",
                       dest="restart",
                       help="to force reprocessing all images, otherwise continue from interruption of the last time")
    
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
    
    # If no output path is provided, use the directory of input path,
    # output filename will be input filename with suffix "_enana"
    if options.output_path is None:
        output_dir = GetFileDir(options.input_path)
        output_file_name = f"{GetFileNameWithoutExt(options.input_path)}_{APP_NAME}"
        output_ext = GetFileExt(options.input_path)
        options.output_path = f"{output_dir}/{output_file_name}{output_ext}"
    
    return vars(options)


