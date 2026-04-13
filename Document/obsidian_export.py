import os
import re

# ================= 配置区域 =================
# 1. 你的 Document 仓库根目录
VAULT_PATH = r""

# 2. 是否要跳过 YAML Frontmatter (文档开头的 --- 元数据)
SKIP_YAML = False

# 3. 输出文件存放的目录
OUTPUT_DIR = "extracted"


# ===========================================

class ObsidianExporter:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.file_map = {}  # 映射:文件名 -> 完整路径
        self._index_files()

    def _index_files(self):
        """遍历仓库，建立文件名索引"""
        print(f"正在索引仓库: {self.vault_path} ...")
        for root, dirs, files in os.walk(self.vault_path):
            # 排除 .obsidian 和 .git 文件夹
            if '.obsidian' in dirs: dirs.remove('.obsidian')
            if '.git' in dirs: dirs.remove('.git')

            for file in files:
                if file.endswith(".md"):
                    # 存入不带后缀的文件名，方便匹配 [[Link]]
                    name_no_ext = file[:-3]
                    self.file_map[name_no_ext] = os.path.join(root, file)
        print(f"索引完成，共找到 {len(self.file_map)} 个 Markdown 文件。")

    @staticmethod
    def extract_links(content):
        """从内容中提取 [[链接]]"""
        # 正则匹配 [[链接]] 或 [[链接|别名]]
        # 排除包含 .png, .jpg 等附件链接
        links = []
        pattern = re.compile(r'\[\[(.*?)]]')
        matches = pattern.findall(content)

        for match in matches:
            # 处理别名: [[Name|Alias]] -> Name
            link_target = match.split('|')[0]
            # 处理锚点: [[Name#Header]] -> Name
            link_target = link_target.split('#')[0]

            # 简单过滤非 md 文件 (粗略过滤，主要靠 file_map 判断)
            if not any(link_target.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.pdf']):
                links.append(link_target)
        return links

    @staticmethod
    def clean_content(content):
        """清理内容（可选：去除 YAML 头）"""
        if SKIP_YAML and content.startswith('---'):
            second_dash_idx = content.find('\n---', 3)
            if second_dash_idx != -1:
                return content[second_dash_idx + 4:].strip()
        return content

    def export_all(self, output_path):
        """功能1：提取仓库下的所有笔记"""
        print(f"\n开始提取全库所有笔记...")
        count = 0

        with open(output_path, 'w', encoding='utf-8') as f_out:
            for note_name, file_path in self.file_map.items():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        raw_content = f_in.read()

                    # 清理并写入内容
                    clean_text = self.clean_content(raw_content)

                    # 写入分隔符和标题
                    f_out.write(f"{'=' * 50}\n")
                    f_out.write(f"笔记标题: {note_name}\n")
                    f_out.write(f"文件路径: {file_path}\n")
                    f_out.write(f"{'=' * 50}\n\n")
                    f_out.write(clean_text)
                    f_out.write("\n\n")  # 笔记间增加空行

                    count += 1
                except Exception as e:
                    print(f"读取文件出错 {note_name}: {e}")

        print(f"\n导出完成！")
        print(f"共导出 {count} 个笔记。")
        print(f"结果已保存至: {os.path.abspath(output_path)}")

    def export_branch(self, start_note, output_path):
        """功能2：根据起始笔记和 [[链接]] 递归提取分支"""
        if start_note not in self.file_map:
            print(f"错误: 找不到起始文件 '{start_note}'，请检查名称是否正确（无需 .md 后缀）。")
            return

        visited = set()  # 已处理的笔记集合
        queue = [start_note]  # 待处理队列

        print(f"\n开始从 '{start_note}' 递归导出...")

        with open(output_path, 'w', encoding='utf-8') as f_out:
            while queue:
                current_note_name = queue.pop(0)

                if current_note_name in visited:
                    continue

                if current_note_name not in self.file_map:
                    # print(f"警告: 链接指向的 '{current_note_name}' 文件不存在")
                    continue

                file_path = self.file_map[current_note_name]

                try:
                    with open(file_path, 'r', encoding='utf-8') as f_in:
                        raw_content = f_in.read()

                    # 1. 提取链接并加入队列
                    links = self.extract_links(raw_content)
                    for link in links:
                        if link not in visited and link not in queue:
                            queue.append(link)

                    # 2. 清理并写入内容
                    clean_text = self.clean_content(raw_content)

                    # 写入分隔符和标题
                    f_out.write(f"{'=' * 50}\n")
                    f_out.write(f"笔记标题: {current_note_name}\n")
                    f_out.write(f"文件路径: {file_path}\n")
                    f_out.write(f"{'=' * 50}\n\n")
                    f_out.write(clean_text)
                    f_out.write("\n\n")  # 笔记间增加空行

                    visited.add(current_note_name)
                    print(f"已处理: {current_note_name} (发现新链接: {len(links)})")

                except Exception as e:
                    print(f"读取文件出错 {current_note_name}: {e}")

        print(f"\n导出完成！")
        print(f"共导出 {len(visited)} 个笔记。")
        print(f"结果已保存至: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    # 1. 确保输出文件夹存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 2. 初始化 Exporter
    exporter = ObsidianExporter(VAULT_PATH)

    # 3. 打印终端菜单
    print("\n" + "=" * 40)
    print("      Obsidian 笔记合并提取工具")
    print("=" * 40)
    print("请选择提取模式:")
    print("  1. 提取所有笔记 (整个 Knowledge 文件夹)")
    print("  2. 提取特定分支 (基于 [[链接]] 递归提取)")
    print("=" * 40)

    # 4. 获取用户选择
    choice = input("请输入选项数字 (1 或 2): ").strip()

    if choice == '1':
        # 模式1：全量提取
        output_file = os.path.join(OUTPUT_DIR, "All_Knowledge_Notes.txt")
        exporter.export_all(output_file)

    elif choice == '2':
        # 模式2：分支提取
        start_note_input = input("\n请输入起始笔记名称: ").strip()
        if not start_note_input:
            print("输入为空，程序退出。")
        else:
            output_file = os.path.join(OUTPUT_DIR, f"{start_note_input}_分支提取.txt")
            exporter.export_branch(start_note_input, output_file)

    else:
        print("无效的输入，程序退出。")