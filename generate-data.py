import os
import json

CONTENT_DIR = 'content'
IMAGE_EXTENSION = '.png'
DESCRIPTION_FILE = 'description.txt'

def find_png_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(IMAGE_EXTENSION):
            return os.path.join(folder_path, file_name).replace('\\', '/')
    return None

def read_description(folder_path):
    desc_path = os.path.join(folder_path, DESCRIPTION_FILE)
    if os.path.isfile(desc_path):
        with open(desc_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return ""

def generate_info_json(folder_name, folder_path, image_path, description):
    info_json_path = os.path.join(folder_path, "info.json")
    title = folder_name.replace("_", " ").replace("-", " ").title()
    info = {
        "title": title,
        "image": image_path,
        "description": description
    }
    with open(info_json_path, 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f"已生成并覆盖 {folder_name}/info.json")

def main():
    if not os.path.exists(CONTENT_DIR):
        print(f'目录 "{CONTENT_DIR}" 不存在，请检查路径')
        return

    items = []

    for folder_name in os.listdir(CONTENT_DIR):
        folder_path = os.path.join(CONTENT_DIR, folder_name)
        if os.path.isdir(folder_path):
            image_path = find_png_in_folder(folder_path)
            if image_path:
                description = read_description(folder_path)

                entry = {
                    "folder": folder_name,
                    "image": image_path
                }
                items.append(entry)

                generate_info_json(folder_name, folder_path, image_path, description)
            else:
                print(f'警告：文件夹 "{folder_name}" 中未找到 PNG 图片')

    output = {
        "infoPage": "info.html",
        "items": items
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f'\ndata.json 生成完成，包含 {len(items)} 条记录')

if __name__ == '__main__':
    main()
