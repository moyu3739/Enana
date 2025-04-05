# Enana

<div align="center">
<a href="README.md">English</a> | <a href="README.zh.md">简体中文</a>
</div>

----

一个用于优化 EPUB 电子书中图像质量的工具，使用先进的超分辨率神经网络技术提升图像清晰度。名字 Enana 来源于：
- Epub NAtive Neural Amplifier
- Eikón (图像) NAtive Neural Amplifier
- Enana's NAtive Neural Amplifier

## 功能特点

- 支持多种超分辨率模型系列，目前专门适配了 "realesrgan-ncnn-vulkan" 系列，并对其他系列做了通用性适配（通用性适配不保证程序能正确运行）
- 可调整图像缩放比例和质量
- 简单易用的命令行界面
- 自动处理 EPUB 文件中的所有图像
- 支持中断恢复，当正常处理图片时被外部中断，下次遇到同名输入文件时自动加载上次中断前已完成的工作

## 支持模型
- "realesrgan-ncnn-vulkan": 做了专门适配，基本不会出错
- "realcugan-ncnn-vulkan": 通用适配可用，基本不会出错
- "waifu2x-ncnn-vulkan": 通用适配可用，基本不会出错

### 模型性能和适用图像风格

|模型系列|模型名称|速度|画质|适用动漫风格|适用写实风格|
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

评价仅供参考。

## 添加额外模型或模型系列
为一个已有模型系列添加新模型时，请按照相应模型系列的目录规则添加模型文件；添加一个新的模型系列时，请将该模型系列的目录添加到 `family` 目录下，并确保该系列的可执行文件在系列目录下且与系列目录同名。`family` 目录结构如下：

```
family
 ├─realcugan-ncnn-vulkan
 │  ├─models-nose
 │  │  └─...
 │  ├─models-pro
 │  │  └─...
 │  ├─models-se
 │  │  └─...
 │  ├─realcugan-ncnn-vulkan.exe    // 与所在目录同名
 │  └─(其他文件...)
 │
 ├─realesrgan-ncnn-vulkan
 │  ├─models
 │  │  └─...
 │  ├─realesrgan-ncnn-vulkan.exe    // 与所在目录同名
 │  └─(其他文件...)
 │
 ├─waifu2x-ncnn-vulkan
 │  ├─models-cunet
 │  │  └─...
 │  ├─models-upconv_7_anime_style_art_rgb
 │  │  └─...
 │  ├─models-upconv_7_photo
 │  │  └─...
 │  ├─waifu2x-ncnn-vulkan.exe    // 与所在目录同名
 │  └─(其他文件...)
 │
 └─(其他系列...)
```

## Python 脚本用法

**请确保目录 `src` 和 `family` 在同一个目录下！**

```bash
cd src
python main.py -h | -v | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-p] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY] [-r]
```

### 参数说明

- `-h, --help`: 显示帮助信息
- `-v, --version`: 打印版本信息
- `-lf, --list-family`: 列出所有可用的超分辨率模型系列
- `-lm, --list-model`: 列出特定系列中所有可用的模型（需配合 -f 使用）
- `-i, --input`: 输入文件路径（必需）
- `-o, --output`: 输出文件路径（可选，默认为输入文件名添加 "_enana" 后缀）
- `-p, --preview`: 输出预览图片。如果使用此选项，程序将从您的 EPUB 文件中选择一张图像，并将其原始版本和处理后的版本输出到输出目录
- `-ps, --pre-scale`: 预缩放系数（浮点数），预缩放应用于超分辨率模型放大之前，默认值为 1.0
- `-s, --scale`: 缩放因子（浮点数，范围和默认值取决于所选模型）
- `-f, --family`: 超分辨率模型系列名称（默认为 "realesrgan-ncnn-vulkan"）
- `-m, --model`: 超分辨率模型名称（默认值取决于所选系列）
- `-q, --quality`: 图像压缩质量级别（0-100，默认为 75）
- `-r, --restart`: 强制重新处理全部图片，**否则将从上次中断处继续**

### 示例

列出所有可用的模型系列：
```bash
python main.py -lf
```

列出 realesrgan-ncnn-vulkan 系列中的所有模型：
```bash
python main.py -lm -f realesrgan-ncnn-vulkan
```

使用默认设置生成预览图片：
```bash
python main.py -i book.epub -p
```

使用自定义设置生成预览图片：
```bash
python main.py -i book.epub -p -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
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

从 [releases](https://github.com/moyu3739/Enana/releases) 获取可执行程序。

```bash
enana -h | -v | -lf | -lm [-f FAMILY] | -i INPUT_PATH [-o OUTPUT_PATH] [-p] [-s SCALE] [-f FAMILY] [-m MODEL] [-q QUALITY] [-r]
```

### 参数说明

- `-h, --help`: 显示帮助信息
- `-v, --version`: 打印版本信息
- `-lf, --list-family`: 列出所有可用的超分辨率模型系列
- `-lm, --list-model`: 列出特定系列中所有可用的模型（需配合 -f 使用）
- `-i, --input`: 输入文件路径（必需）
- `-o, --output`: 输出文件路径（可选，默认为输入文件名添加 "_enana" 后缀）
- `-p, --preview`: 输出预览图片。如果使用此选项，程序将从您的 EPUB 文件中选择一张图像，并将其原始版本和处理后的版本输出到输出目录
- `-ps, --pre-scale`: 预缩放系数（浮点数），预缩放应用于超分辨率模型放大之前，默认值为 1.0
- `-s, --scale`: 缩放因子（浮点数，范围和默认值取决于所选模型）
- `-f, --family`: 超分辨率模型系列名称（默认为 "realesrgan-ncnn-vulkan"）
- `-m, --model`: 超分辨率模型名称（默认值取决于所选系列）
- `-q, --quality`: 图像压缩质量级别（0-100，默认为 75）
- `-r, --restart`: 强制重新处理全部图片，**否则将从上次中断处继续**

### 示例

列出所有可用的模型系列：
```bash
enana -lf
```

列出 realesrgan-ncnn-vulkan 系列中的所有模型：
```bash
enana -lm -f realesrgan-ncnn-vulkan
```

使用默认设置生成预览图片：
```bash
enana -i book.epub -p
```

使用自定义设置生成预览图片：
```bash
enana -i book.epub -p -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
```

使用默认设置处理 EPUB 文件：
```bash
enana -i book.epub -o book_enhanced.epub
```

使用自定义设置处理 EPUB 文件：
```bash
enana -i book.epub -o book_enhanced.epub -s 2.0 -f realesrgan-ncnn-vulkan -m realesrgan-x4plus -q 60
```

## 许可证

[本项目许可证 MIT License](LICENSE)

[本项目中使用的超分辨率模型许可证](Licenses)

