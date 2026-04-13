from pathlib import Path
from pdf2image import convert_from_path
from docx2pdf import convert
import tempfile

# ================= 配置区域 =================
# 1. 你的项目文件所在的文件夹路径 (注意路径中的斜杠用反斜杠 / 或双斜杠 \\)
SOURCE_FOLDER = r""

# 2. 图片保存的文件夹
OUTPUT_FOLDER = r""

# 3. Poppler 的 bin 路径 (如果你没配环境变量，就在这里填，配了就留 None)
# 例如: r"C:\Software\poppler-24.02.0\Library\bin"
POPPLER_PATH = None


# ===========================================

def extract_cover(file_path, output_dir):
    filename = file_path.stem
    extension = file_path.suffix.lower()

    print(f"正在处理: {file_path.name} ...")

    try:
        if extension == '.pdf':
            # 直接处理 PDF
            images = convert_from_path(str(file_path), first_page=1, last_page=1, poppler_path=POPPLER_PATH)
            if images:
                save_path = output_dir / f"{filename}.png"
                images[0].save(save_path, 'PNG')
                print(f"  -> 封面已保存: {save_path.name}")

        elif extension in ['.docx', '.doc']:
            # 处理 Word: 先转 PDF (临时)，再转图片
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_pdf = Path(temp_dir) / f"{filename}.pdf"
                # Word 转 PDF
                convert(str(file_path), str(temp_pdf))

                # PDF 转图片
                images = convert_from_path(str(temp_pdf), first_page=1, last_page=1, poppler_path=POPPLER_PATH)
                if images:
                    save_path = output_dir / f"{filename}.png"
                    images[0].save(save_path, 'PNG')
                    print(f"  -> 封面已保存: {save_path.name}")

    except Exception as e:
        print(f"  !! 出错: {e}")


def main():
    src = Path(SOURCE_FOLDER)
    dst = Path(OUTPUT_FOLDER)
    dst.mkdir(parents=True, exist_ok=True)  # 自动创建输出目录

    # 遍历文件夹
    for file in src.iterdir():
        if file.suffix.lower() in ['.pdf', '.docx', '.doc']:
            extract_cover(file, dst)

    print("\n=== 全部完成！===")


if __name__ == "__main__":
    main()