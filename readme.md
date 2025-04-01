# Himage-Epub

一个用于优化 EPUB 电子书中图像质量的工具，使用先进的超分辨率技术提升图像清晰度。

## 功能特点

- 支持多种超分辨率模型系列，目前专门适配了 "realesrgan-ncnn-vulkan" 模型，并对其他模型做了通用性适配（通用性适配不保证程序能正确运行）
- 可调整图像缩放比例和质量
- 简单易用的命令行界面
- 自动处理 EPUB 文件中的所有图像

## 支持模型
- "realesrgan-ncnn-vulkan": 做了专门适配，基本不会出错
- "realcugan-ncnn-vulkan": 通用适配可用，基本不会出错
- "waifu2x-ncnn-vulkan": 通用适配可用，基本不会出错

## 添加额外模型
请按照相应模型系列的目录规则添加模型文件

## Python 脚本用法

**请确保目录 `src` 和 `family` 在同一个目录下！**

```bash
cd src
python main.py -h | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY]
```

### 参数说明

- `-h, --help`: 显示帮助信息
- `-lf, --list-family`: 列出所有可用的超分辨率模型系列
- `-lm, --list-model`: 列出特定系列中所有可用的模型（需配合 -f 使用）
- `-i, --input`: 输入文件路径（必需）
- `-o, --output`: 输出文件路径（可选，默认为添加"_hi"后缀的输入文件名）
- `-s, --scale`: 缩放因子（浮点数，范围和默认值取决于所选模型）
- `-f, --family`: 超分辨率模型系列名称（默认为"realesrgan-ncnn-vulkan"）
- `-m, --model`: 超分辨率模型名称（默认值取决于所选系列）
- `-q, --quality`: 图像质量级别（0-100，默认为75）

### 示例

列出所有可用的模型系列：
```bash
python main.py -lf
```

列出 realesrgan-ncnn-vulkan 系列中的所有模型：
```bash
python main.py -lm -f realesrgan-ncnn-vulkan
```

使用默认设置处理 EPUB 文件：
```bash
python main.py -i book.epub -o book_enhanced.epub
```

使用自定义设置处理 EPUB 文件：
```bash
python main.py -i book.epub -o book_enhanced.epub -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
```

## 可执行程序用法

**请确保文件 `himage-epub.exe` 和 目录 `family` 在同一个目录下！**

```bash
./himage-epub -h | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY]
```

### 参数说明

- `-h, --help`: 显示帮助信息
- `-lf, --list-family`: 列出所有可用的超分辨率模型系列
- `-lm, --list-model`: 列出特定系列中所有可用的模型（需配合 -f 使用）
- `-i, --input`: 输入文件路径（必需）
- `-o, --output`: 输出文件路径（可选，默认为添加"_hi"后缀的输入文件名）
- `-s, --scale`: 缩放因子（浮点数，范围和默认值取决于所选模型）
- `-f, --family`: 超分辨率模型系列名称（默认为"realesrgan-ncnn-vulkan"）
- `-m, --model`: 超分辨率模型名称（默认值取决于所选系列）
- `-q, --quality`: 图像质量级别（0-100，默认为75）

### 示例

列出所有可用的模型系列：
```bash
./himage-epub -lf
```

列出 realesrgan-ncnn-vulkan 系列中的所有模型：
```bash
./himage-epub -lm -f realesrgan-ncnn-vulkan
```

使用默认设置处理 EPUB 文件：
```bash
./himage-epub -i book.epub -o book_enhanced.epub
```

使用自定义设置处理 EPUB 文件：
```bash
./himage-epub -i book.epub -o book_enhanced.epub -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
```

## 许可证

[本项目许可证 MIT License](LICENSE)

[本项目中使用的超分辨率模型许可证](Licenses)

