import os


def merge_txt_files(source_folder, output_filepath):
    """
    遍历文件夹合并txt文件
    :param source_folder: 源文件夹路径
    :param output_filepath: 输出文件的完整路径
    """

    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"❌ 错误：找不到文件夹路径 - {source_folder}")
        return

    count = 0

    # 使用 'w' 模式打开输出文件（如果文件存在则覆盖，不存在则创建）
    # encoding='utf-8' 确保中文正常显示
    with open(output_filepath, 'w', encoding='utf-8') as out_file:

        print(f"📂 开始扫描文件夹: {source_folder} ...")

        # os.walk 会自动递归遍历所有子文件夹
        for root, dirs, files in os.walk(source_folder):
            for filename in files:
                # 筛选 .txt 文件 (忽略大小写)
                if filename.lower().endswith('.txt'):

                    # 排除输出文件本身（如果输出文件也被保存在源文件夹中）
                    file_full_path = os.path.join(root, filename)
                    if os.path.abspath(file_full_path) == os.path.abspath(output_filepath):
                        continue

                    try:
                        # 读取源文件内容
                        # errors='ignore' 用于忽略编码错误（防止因某个文件编码特殊导致脚本崩溃）
                        with open(file_full_path, 'r', encoding='utf-8', errors='ignore') as in_file:
                            content = in_file.read()

                        # --- 写入格式 ---
                        # 1. 写入文件名
                        out_file.write(f"[{filename}]\n")
                        # 2. 写入文件内容
                        out_file.write(content)
                        # 3. 写入换行符作为分隔（这里加了两个换行，方便阅读）
                        out_file.write("\n\n")

                        count += 1
                        print(f"✅ 已合并: {filename}")

                    except Exception as e:
                        print(f"⚠️ 读取文件出错: {filename}, 原因: {e}")

    print("-" * 30)
    print(f"🎉 处理完成！")
    print(f"📊 共合并文件数: {count}")
    print(f"💾 结果已保存至: {output_filepath}")


if __name__ == "__main__":
    # 1. 设置源文件夹路径 (注意前面的 r 代表原始字符串，处理反斜杠)
    source_dir = r""

    # 2. 设置输出文件的保存位置和名称
    # 默认保存在脚本运行的当前目录下，名字叫 all_merged.txt
    output_file = r".\extracted\all_merged.txt"

    # 开始执行
    merge_txt_files(source_dir, output_file)