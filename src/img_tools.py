from pathlib import Path
from PIL import Image, ImageFilter, ImageOps

def create_print_images(source_dir: Path):
    save_dir = str(source_dir) + "\\Для печати\\"
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    print(f"Папка с фотографиями - {source_dir}")
    print(f"Отредактированные фото будут сохранены в папку {save_dir}")
    
    for image_path in get_images_paths(source_dir):
        create_print_image(image_path, save_dir)


def create_print_image(image_path, save_dir: Path):
    print(f"\nРедактирую фото - {image_path.name}")
    img = open_image(image_path)
    
    background = create_blur_background(img)

    if background is not None:
        paste_img_on_blurred_background(img=img, background=background)

    new_image_path = save_dir + image_path.name

    if background is not None:
        background.save(new_image_path)
    else:
        img.save(new_image_path)

    print(f"Фото сохранено по пути {new_image_path}")

def paste_img_on_blurred_background(img, background):
    img_w, img_h = img.size
    bg_w, bg_h = background.size
    
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(img, offset)

def open_image(image_path):
    img = Image.open(image_path)
    return ImageOps.exif_transpose(img)

def create_blur_background(img: Image):
    size_10_by_15 = get_10_by_15_size(img)
    if size_10_by_15 == img.size:
        print(f"Не нужно редактировать - фото и так 10x15")
        return None
    
    blur = img.filter(ImageFilter.GaussianBlur(67))
    blur = blur.resize(size_10_by_15)
    return blur

def get_10_by_15_size(img: Image):
    og_width, og_height = img.size
    new_width, new_height = img.size

    if og_width <= og_height:
        new_width = (og_height / 15 * 10)
        if new_width < og_width: # we want to expand image, not make it shorter. change height instead of width
            new_width = og_width
            new_height = (og_width / 10 * 15)
    else:
        new_height = (og_width / 15 * 10)
        if new_height < og_height: # we want to expand image, not make it shorter. change width instead of height
            new_height = og_height
            new_width = (og_height / 10 * 15)

    return int(new_width), int(new_height)


def get_images_paths(source_dir: Path):
    allowed_extensions = Image.registered_extensions()
    files = []

    for extension in allowed_extensions:
        files.extend(source_dir.glob('*' + extension))

    return files