from pathlib import Path

import src.img_tools as img_tools
import src.config as config

source_dir = Path(config.get_photos_path())

try:
    img_tools.create_print_images(source_dir)
except Exception as e:
    print(f"Произошла ошибка при печати. {e}")
finally:
    input("----------------------------------------------\n" \
      "Нажмите Enter, чтобы закрыть программу")