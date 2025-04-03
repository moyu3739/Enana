# Enana

<div align="center">
<a href="readme.md">English</a> | <a href="readme.zh.md">简体中文</a>
</div>

----

A tool for optimizing image quality in EPUB e-books, using advanced super-resolution neural network technology to enhance image clarity. The name *Enana* comes from:
- Epub NAtive Neural Amplifier
- Eikón (icon) NAtive Neural Amplifier
- Enana's NAtive Neural Amplifier

## Features

- Supports multiple super-resolution model families, with specialized adaptation for the "realesrgan-ncnn-vulkan" model and general adaptation for other models (general adaptation does not guarantee correct program operation)
- Adjustable image scaling ratio and quality
- Simple and easy-to-use command line interface
- Automatically processes all images in EPUB files

## Supported Models
- "realesrgan-ncnn-vulkan": Specially adapted, generally error-free
- "realcugan-ncnn-vulkan": General adaptation available, generally error-free
- "waifu2x-ncnn-vulkan": General adaptation available, generally error-free

### Model Performance and Style Suitability

|Model Family|Model Name|Speed|Quality|Suitable for Anime|Suitable for Realistic|
|-|-|-|-|-|-|
|realesrgan-ncnn-vulkan|realesr-animevideov3            |⭐⭐️⭐️⭐️ |⭐️⭐️⭐️   |✅|❌|
|realesrgan-ncnn-vulkan|realesrgan-x4plus               |⭐️         |⭐️⭐️⭐️⭐️|❌|✅|
|realesrgan-ncnn-vulkan|realesrgan-x4plus-anime         |⭐️         |⭐️⭐️⭐️⭐️|✅|❌|
|realesrgan-ncnn-vulkan|RealESRGANv2-animevideo-xsx2    |⭐️⭐️⭐️⭐️ |⭐️        |✅|❌|
|realesrgan-ncnn-vulkan|RealESRGANv2-animevideo-xsx4    |⭐️⭐️      |⭐️⭐️      |✅|❌|
|realesrgan-ncnn-vulkan|realesr-general-wdn-x4v3        |⭐️⭐️      |⭐️⭐️⭐️   |✅|✅|
|realesrgan-ncnn-vulkan|realesr-general-x4v3            |⭐️⭐️      |⭐️⭐️⭐️   |✅|✅|
|realcugan-ncnn-vulkan|models-se                        |⭐️⭐️      |⭐️⭐️⭐️⭐️ |✅|❌|
|realcugan-ncnn-vulkan|models-pro                       |⭐️⭐️      |⭐️⭐️⭐️⭐️ |✅|❌|
|waifu2x-ncnn-vulkan|models-cunet                       |⭐️⭐️      |⭐️⭐️      |✅|❌|
|waifu2x-ncnn-vulkan|models-upconv_7_anime_style_art_rgb|⭐️⭐️      |⭐️⭐️      |✅|❌|
|waifu2x-ncnn-vulkan|models-upconv_7_photo              |⭐️⭐️      |⭐️⭐️      |❌|✅|

Ratings are for reference only.

## Adding Additional Models or Model Families
To add a new model to an existing model family, please add model files according to the directory rules of the corresponding model family. To add a new model family, add the model family directory to the `family` directory, and ensure that the executable file of the family is in the family directory and has the same name as the family directory. The structure of the `family` directory is as follows:

```
family
 ├─realcugan-ncnn-vulkan
 │  ├─models-nose
 │  │  └─...
 │  ├─models-pro
 │  │  └─...
 │  ├─models-se
 │  │  └─...
 │  ├─realcugan-ncnn-vulkan.exe    // Same name as the directory
 │  └─(other files...)
 │
 ├─realesrgan-ncnn-vulkan
 │  ├─models
 │  │  └─...
 │  ├─realesrgan-ncnn-vulkan.exe    // Same name as the directory
 │  └─(other files...)
 │
 ├─waifu2x-ncnn-vulkan
 │  ├─models-cunet
 │  │  └─...
 │  ├─models-upconv_7_anime_style_art_rgb
 │  │  └─...
 │  ├─models-upconv_7_photo
 │  │  └─...
 │  ├─waifu2x-ncnn-vulkan.exe    // Same name as the directory
 │  └─(other files...)
 │
 └─(other families...)
```

## Python Script Usage

**Please ensure that the directories `src` and `family` are in the same directory!**

```bash
cd src
python main.py -h | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY]
```

### Parameter Description

- `-h, --help`: Display help information
- `-lf, --list-family`: List all available super-resolution model families
- `-lm, --list-model`: List all available models in a specific family (must be used with -f)
- `-i, --input`: Input file path (required)
- `-o, --output`: Output file path (optional, default is the input filename with "_hi" suffix)
- `-s, --scale`: Scaling factor (float, range and default value depend on the selected model)
- `-f, --family`: Super-resolution model family name (default is "realesrgan-ncnn-vulkan")
- `-m, --model`: Super-resolution model name (default value depends on the selected family)
- `-q, --quality`: Image quality level (0-100, default is 75)

### Examples

List all available model families:
```bash
python main.py -lf
```

List all models in the realesrgan-ncnn-vulkan family:
```bash
python main.py -lm -f realesrgan-ncnn-vulkan
```

Process an EPUB file with default settings:
```bash
python main.py -i book.epub -o book_enhanced.epub
```

Process an EPUB file with custom settings:
```bash
python main.py -i book.epub -o book_enhanced.epub -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
```

## Executable Program Usage

**Please ensure that the file `himage-epub.exe` and the directory `family` are in the same directory!**

```bash
./himage-epub -h | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY]
```

### Parameter Description

- `-h, --help`: Display help information
- `-lf, --list-family`: List all available super-resolution model families
- `-lm, --list-model`: List all available models in a specific family (must be used with -f)
- `-i, --input`: Input file path (required)
- `-o, --output`: Output file path (optional, default is the input filename with "_hi" suffix)
- `-s, --scale`: Scaling factor (float, range and default value depend on the selected model)
- `-f, --family`: Super-resolution model family name (default is "realesrgan-ncnn-vulkan")
- `-m, --model`: Super-resolution model name (default value depends on the selected family)
- `-q, --quality`: Image quality level (0-100, default is 75)

### Examples

List all available model families:
```bash
./himage-epub -lf
```

List all models in the realesrgan-ncnn-vulkan family:
```bash
./himage-epub -lm -f realesrgan-ncnn-vulkan
```

Process an EPUB file with default settings:
```bash
./himage-epub -i book.epub -o book_enhanced.epub
```

Process an EPUB file with custom settings:
```bash
./himage-epub -i book.epub -o book_enhanced.epub -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
```

## License

[This project's license - MIT License](LICENSE)

[License for super-resolution models used in this project](Licenses)
