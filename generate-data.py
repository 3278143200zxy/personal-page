import os
import json

CONTENT_DIR = 'content'
DESCRIPTION_FILE = 'description.txt'

VIDEO_EXTENSIONS = {'.mp4', '.webm', '.mov', '.avi', '.mkv'}
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}

def find_main_image(folder_path):
    """查找项目主封面图：优先找同文件夹下的第一张 png/jpg/jpeg/webp"""
    for file_name in os.listdir(folder_path):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            return os.path.join(folder_path, file_name).replace('\\', '/')
    return None

def read_description(folder_path):
    """读取 description.txt，返回非空行列表"""
    desc_path = os.path.join(folder_path, DESCRIPTION_FILE)
    if os.path.isfile(desc_path):
        with open(desc_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            return lines
    return []

def read_gallery_files(folder_path):
    """读取 gallery 文件夹内视频和图片文件，视频路径放前，图片路径放后"""
    gallery_path = os.path.join(folder_path, "gallery")
    if not os.path.isdir(gallery_path):
        return []

    videos = []
    images = []

    for file_name in os.listdir(gallery_path):
        ext = os.path.splitext(file_name)[1].lower()
        full_path = os.path.join(gallery_path, file_name).replace('\\', '/')
        if ext in VIDEO_EXTENSIONS:
            videos.append(full_path)
        elif ext in IMAGE_EXTENSIONS:
            images.append(full_path)

    videos.sort()
    images.sort()

    return videos + images

def generate_info_json(folder_name, folder_path, main_image_path, description_lines, gallery_files):
    title_line = description_lines[0] if description_lines else folder_name.replace("_", " ").replace("-", " ").title()
    description_text = "\n".join(description_lines[1:]) if len(description_lines) > 1 else ""

    info = {
        "title": title_line,
        "image": main_image_path,
        "gallery": gallery_files,
        "description": description_text
    }

    info_json_path = os.path.join(folder_path, "info.json")
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

            main_image = find_main_image(folder_path)
            if not main_image:
                print(f'警告："{folder_name}" 无封面图片，跳过')
                continue

            description_lines = read_description(folder_path)
            gallery_files = read_gallery_files(folder_path)

            generate_info_json(folder_name, folder_path, main_image, description_lines, gallery_files)

            title_line = description_lines[0] if description_lines else folder_name.replace("_", " ").replace("-", " ").title()

            items.append({
                "folder": folder_name,
                "image": main_image,
                "title": title_line
            })

    output = {
        "infoPage": "info.html",
        "items": items
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\ndata.json 生成完成，共 {len(items)} 条记录")

if __name__ == '__main__':
    main()
