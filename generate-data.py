import os
import json

# 父目录名称，存放多个子文件夹
CONTENT_DIR = 'content'
# 只查找png格式图片
IMAGE_EXTENSION = '.png'

def find_png_in_folder(folder_path):
    """
    查找文件夹内第一个png图片，返回相对路径（项目根目录相对路径）
    """
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(IMAGE_EXTENSION):
            return os.path.join(folder_path, file_name).replace('\\', '/')
    return None

def main():
    # 判断目录是否存在
    if not os.path.exists(CONTENT_DIR):
        print(f'目录 "{CONTENT_DIR}" 不存在，请检查路径')
        return

    data = []

    # 遍历content目录下所有子目录
    for folder_name in os.listdir(CONTENT_DIR):
        folder_path = os.path.join(CONTENT_DIR, folder_name)
        if os.path.isdir(folder_path):
            image_path = find_png_in_folder(folder_path)
            if image_path:
                # 默认子文件夹里的页面是page.html
                page_path = os.path.join(folder_path, 'page.html').replace('\\', '/')
                entry = {
                    "folder": folder_name,
                    "image": image_path,
                    "page": page_path
                }
                data.append(entry)
            else:
                print(f'警告：文件夹 "{folder_name}" 中未找到 PNG 图片')

    # 写入 data.json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'data.json 生成完成，包含 {len(data)} 条记录')

if __name__ == '__main__':
    main()
