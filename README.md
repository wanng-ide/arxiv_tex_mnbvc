# arxiv_tex_mnbvc

这是[MNBVC项目](https://github.com/esbatmop/MNBVC)的一部分，致力于实现从 arXiv 的研究论文中提取和处理 `.tex` 文件的自动化。

本项目从arxiv原始文件 (注，下载脚本来自[arxivSpider_mnbvc](https://github.com/wanng-ide/arxivSpider_mnbvc)) 中收集`.tex`语料:

以.tex为对象的纯文本数据集 (本项目的目标)

数据流程:

source files -> .tex -> jsonline

## 特点

- 专注于 .tex 文件的提取：从 arXiv 的研究论文的压缩包中提取 .tex 文件。
- 转换为 JSON Line 格式：将 .tex 文件转换为 .jsonl 格式。
- 错误处理和日志记录

## 开始使用

### 安装

克隆本仓库：
```bash
git clone https://github.com/yourusername/arxiv_tex_mnbvc.git
cd arxiv_tex_mnbvc
```

安装所需的依赖：

```bash
pip install tqdm chardet loguru
```

### 使用方法

提前完善`main.py`中的变量路径：

```python
RAW_PATH = "arxiv-subset"
PARSE_PATH = "parse-files"
OUTPUT_TEX_PATH = "output-tex.jsonl"
```

注：假如不需要log，可以把带有logger的所有行直接注释掉。

运行主脚本开始提取和转换：

```bash
python main.py
```

### 其他

具体来说，代码流程为：

1. 本脚本会先扫描source文件，然后解压到`parse-files`文件夹。
2. 扫描解压后的文件夹中的tex文件
3. 抽取tex文件并且存储到jsonline中
4. 删除解压后的文件夹，恢复source文件到原来的样子

## 许可证

本项目根据 Apache-2.0 许可证授权 - 详见 LICENSE 文件。
