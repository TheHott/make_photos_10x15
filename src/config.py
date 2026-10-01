
from configparser import ConfigParser

config_filename = 'config.ini'

parser = ConfigParser()

def get_photos_path():
    return get_param(section='path', var_name='photo_directory')

def get_param(filename=config_filename, section=None, var_name=None):
    parser.read(filename, "utf-8")

    if parser.has_section(section):
        param = parser.get(section, var_name)
    else:
        raise Exception(f'Ошибка! Секция {section} не найдена в файле {filename}')

    return param