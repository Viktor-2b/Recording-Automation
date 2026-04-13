import os
import re
import shutil
from datetime import datetime


def modify_files_name(filename):
    list_path = os.listdir(filename)  # 读取文件夹里面的名字
    for index in list_path:  # list_path返回的是一个列表   通过for循环遍历提取元素
        if index[0] == '[':
            number = index.split(' ')[2]
            no = number.split('.')[1]
            path = filename + '\\' + index
            new_path = filename + '\\' + 'XIUREN No.' + no + ' 鱼子酱Fish'
            os.rename(path, new_path)  # 重新命名


def modify_files_postfix(filepath):  # 修改文件夹中所有特定后缀名的文件为指定后缀名
    list_name = os.listdir(filepath)  # 读取文件夹里面的名字
    for name in list_name:
        filename = os.path.splitext(name)[0]  # 文件名
        postfix = os.path.splitext(name)[-1]  # 后缀
        if postfix == '.pdf':  # 待修改后缀
            path = filepath + '\\' + name
            new_path = filepath + '\\' + filename + '.rar'  # 指定后缀
            os.rename(path, new_path)  # 重新命名


def delete_chinese_files_postfix(filepath):  # 删除文件夹中所有后缀名的中文字符
    list_name = os.listdir(filepath)  # 读取文件夹里面的名字
    for name in list_name:
        filename, postfix = os.path.splitext(name)  # 分割文件名和后缀
        new_postfix = re.sub(r'[\u4e00-\u9fa5]', '', postfix)
        # 构造新的文件路径
        new_path = os.path.join(filepath, filename + new_postfix)
        old_path = os.path.join(filepath, name)
        os.rename(old_path, new_path)  # 重命名文件


def delete_old_files(base_folder):  # 只保留英雄配置的最新一个
    # 遍历base_folder下的所有一级子文件夹
    for subdir in os.listdir(base_folder):
        subdir_path = os.path.join(base_folder, subdir)

        # 检查子目录是否是文件夹
        if os.path.isdir(subdir_path):
            recommend_path = os.path.join(subdir_path, 'Recommended')

            # 检查recommend文件夹是否存在
            if os.path.exists(recommend_path) and os.path.isdir(recommend_path):
                print(f'Checking directory: {recommend_path}')

                # 获取recommend文件夹下的所有文件
                recommend_files = [os.path.join(recommend_path, f) for f in os.listdir(recommend_path) if
                                   os.path.isfile(os.path.join(recommend_path, f))]

                if recommend_files:
                    # 按照文件的修改时间排序，最新的文件排在最前面
                    recommend_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

                    # 保留最新的文件，删除其他文件
                    for file_to_delete in recommend_files[1:]:
                        print(f'Deleting file: {file_to_delete}')
                        os.remove(file_to_delete)
                else:
                    print(f'No files found in {recommend_path}')
            else:
                print(f'No recommend directory found in {subdir_path}')


if __name__ == '__main__':
    delete_old_files()
    print('修改完成')
