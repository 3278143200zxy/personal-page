import os
import json

CONTENT_DIR = 'content'
DESCRIPTION_FILE = 'description.txt'
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}

def find_main_image(folder_path):
    """查找项目主封面图：优先找同文件夹下的第一张 png/jpg/jpeg/webp"""
    for file_name in os.listdir(folder_path):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            return os.path.join(folder_path, file_name).replace('\\', '/')
    return None

def read_description(folder_path):
    desc_path = os.path.join(folder_path, DESCRIPTION_FILE)
    if os.path.isfile(desc_path):
        with open(desc_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            return lines
    return []

def read_gallery_images(folder_path):
    """读取内容文件夹内 gallery/ 里的所有图片，返回图片相对路径数组"""
    gallery_path = os.path.join(folder_path, "gallery")
    if not os.path.isdir(gallery_path):
        return []

    images = []
    for file_name in os.listdir(gallery_path):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in IMAGE_EXTENSIONS:
            img_path = os.path.join(gallery_path, file_name).replace('\\', '/')
            images.append(img_path)

    # 排序保证稳定顺序
    images.sort()
    return images

def generate_info_json(folder_name, folder_path, main_image_path, description_lines, gallery_images):
    title_line = description_lines[0] if description_lines else folder_name.replace("_", " ").replace("-", " ").title()
    description_text = "\n".join(description_lines[1:]) if len(description_lines) > 1 else ""

    info = {
        "title": title_line,
        "image": main_image_path,
        "gallery": gallery_images,   # ⭐ 新增：子图片数组
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
            gallery_images = read_gallery_images(folder_path)

            # 生成单独 info.json
            generate_info_json(folder_name, folder_path, main_image, description_lines, gallery_images)

            # 获取标题（显示在 index 页面）
            title_line = description_lines[0] if description_lines else folder_name.replace("_", " ").replace("-", " ").title()

            items.append({
                "folder": folder_name,
                "image": main_image,
                "title": title_line
            })

    # 写入 index 页的数据
    output = {
        "infoPage": "info.html",
        "items": items
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\ndata.json 生成完成，共 {len(items)} 条记录")

if __name__ == '__main__':
    main()
