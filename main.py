import os
import tarfile
from tqdm import tqdm
import json
import chardet
from utils import list_tex_files, filter_tex_file
from pathlib import Path
import shutil
from loguru import logger

logger.add("log.log")

RAW_PATH = "/mnt/disk4/wangjunjie/proj/mnbvc/arxiv-test-data/arxiv-subset"
PARSE_PATH = "parse-files"
OUTPUT_TEX_PATH = "output-tex.jsonl"

def write_to_jsonl(tex_filelist):
    with open(OUTPUT_TEX_PATH, 'a', encoding='utf-8') as f_out:
        for tex_file in tex_filelist:
            with open(tex_file, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']
                
            with open(tex_file, 'r', encoding=encoding) as f_tex:
                content = f_tex.read()
                
                id_path = os.path.relpath(tex_file, PARSE_PATH)
                data = {
                    "id": id_path,
                    "text": content
                }
                
                json_line = json.dumps(data)
                f_out.write(json_line + '\n')

def extract_tex(arxiv_parse_path):
    # 找到所有.tex文件
    try:
        # 尝试找到所有.tex文件
        tex_filelist = list_tex_files(arxiv_parse_path)
    except Exception as e:
        # 如果发生异常，抛出新的异常
        raise RuntimeError(f"在处理 {arxiv_parse_path} 时发生错误: {e}")
    
    # 过滤有意义的.tex文件
    if len(tex_filelist) == 0:
        raise RuntimeError(f"在 {arxiv_parse_path} 没有找到.tex文件")
    if len(tex_filelist) > 1:
        tex_filelist = list(filter(filter_tex_file, tex_filelist))
    write_to_jsonl(tex_filelist)
    return tex_filelist


def extract_one_arxiv(id):
    """
    提取一个arxiv_id的所有内容
    """
    is_success = None
    arxiv_path = os.path.join(RAW_PATH, id)
    arxiv_parse_path = os.path.join(PARSE_PATH, id)
    os.makedirs(arxiv_parse_path, exist_ok=True)
    # pdf_path = os.path.join(arxiv_path, "pdf", id+".pdf")
    source_file_path = os.path.join(arxiv_path, "source", id)
    source_file_path_gz = source_file_path + ".tar.gz"

    # 重命名压缩包
    if os.path.exists(source_file_path):
        os.rename(source_file_path, source_file_path_gz)

    # 检查文件完整性
    # if (not os.path.exists(pdf_path)) or (not os.path.exists(source_file_path_gz)):
    if not os.path.exists(source_file_path_gz):
        logger.info(f"[Error] {id} 文件不完整，source文件丢失")
        is_success = False
        return is_success

    # 解压
    try:
        with tarfile.open(source_file_path_gz, 'r:gz') as tar_ref:
            # 这里会有一批古老的压缩包无法解压
            tar_ref.extractall(arxiv_parse_path)

        # 1.解析代码, 得到包含".tex"类型文件的list
        tex_filelist = extract_tex(arxiv_parse_path)
        is_success = True
    except Exception as e:
        logger.info(f"[Error] {id} 发生错误: {e}")
        is_success = False
    finally:
        # 复原压缩包
        if os.path.exists(source_file_path_gz):
            os.rename(source_file_path_gz, source_file_path)
        if os.path.exists(arxiv_parse_path):
            shutil.rmtree(arxiv_parse_path)
        return is_success


def main():
    # 检查并删除已存在的OUTPUT_TEX_PATH文件
    if os.path.exists(OUTPUT_TEX_PATH):
        os.remove(OUTPUT_TEX_PATH)
        logger.info(f"{OUTPUT_TEX_PATH} 已存在，已删除旧文件。")
        
    os.makedirs(PARSE_PATH, exist_ok=True)
    arxiv_ids = [d for d in os.listdir(RAW_PATH) if os.path.isdir(os.path.join(RAW_PATH, d))]
    arxiv_ids = arxiv_ids
    success = 0
    for arxiv_id in tqdm(arxiv_ids, ncols=100):
        if extract_one_arxiv(arxiv_id):
            success += 1
    
    logger.info("total: {}, success: {}, ratio: {}%,".format(len(arxiv_ids), success, success/len(arxiv_ids)*100.0))
    if os.path.exists(PARSE_PATH):
        shutil.rmtree(PARSE_PATH)

if __name__ == "__main__":
    main()