import os
import sys


def count_files(path):
    total = 0

    def handle_error(error):
        print(f"警告：无法访问目录 {error.filename}，跳过。", file=sys.stderr)

    for root, dirs, files in os.walk(path, onerror=handle_error):
        total += len(files)
    return total


def main():
    path = input("请输入要遍历的文件夹路径：").strip()

    if not os.path.isdir(path):
        print("错误：路径不存在或不是文件夹。", file=sys.stderr)
        sys.exit(1)

    file_count = count_files(path)
    print(f"文件夹 '{path}' 下的总文件数为：{file_count}")


if __name__ == "__main__":
    main()