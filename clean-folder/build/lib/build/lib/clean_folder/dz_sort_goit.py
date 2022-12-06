import os
import re
from pathlib import Path
from zipfile import ZipFile
from sys import argv

#path_dir = '/Users/aleksandrseryj/Documents/Мой компьютер/Программирование/python/GO_IT/sort programm/хлам/'
dir_suff_dict = {"Images": ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.ico', '.bmp', '.webp', '.svg'],
                 "Documents": [".md", ".epub", ".txt", ".docx", ".doc", ".ods", ".odt", ".dotx", ".docm", ".dox",
                               ".rvg", ".rtf", ".rtfd", ".wpd", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".xml"],
                 "Archives": [".iso", ".tar", ".gz", ".7z", ".dmg", ".rar", ".zip"],
                 "Audio": [".aac", ".m4a", ".mp3", "ogg", ".raw", ".wav", ".wma"],
                 "Video": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mpg", ".mpeg", ".3gp"],
                 "PDF": [".pdf"],
                 "HTML": [".html", ".htm", ".xhtml"],
                 "EXE_MSI": [".exe", ".msi"],
                 "PYTHON": [".py", ".pyw"]}


def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


def sort_func(path_dir: Path):
    cur_dir = path_dir
    dir_path = []

    for root, dirs, files in os.walk(path_dir):
        for d in dirs:
            dir_path.append(os.path.join(root, d))
        for file in files:
            try:
                p_file = Path(root) / file
                name_normalize = f"{normalize(p_file.name[0:-len(p_file.suffix)])}{p_file.suffix}"
                p_file.rename(Path(root) / name_normalize)
                p_file = Path(root) / name_normalize
            except IsADirectoryError:
                continue
            for suff in dir_suff_dict:
                if p_file.suffix.lower() in dir_suff_dict[suff]:
                    dir_img = cur_dir / suff
                    dir_img.mkdir(exist_ok=True)
                    try:
                        p_file.rename(dir_img.joinpath(p_file.name))
                    except FileExistsError:
                        p_file.rename(dir_img.joinpath(f'{p_file.name.split(".")[0]}_c{p_file.suffix}'))
                        print(f"Возможно дубликат: {p_file.name}")

    for dir_p in reversed(dir_path):
        if os.path.split(dir_p)[1] in dir_suff_dict or os.stat(dir_p).st_size != 0:
            continue
        else:
            os.rmdir(dir_p)

    for archive in os.listdir(fr"{path_dir}/Archives"):
        os.mkdir(fr"{path_dir}/Archives/{os.path.splitext(archive)[0]}")
        extract_dir = fr"{path_dir}/Archives/{os.path.splitext(archive)[0]}"
        with ZipFile(fr"{path_dir}/Archives/{archive}") as arch:
            arch.extractall(extract_dir)


def main():
    try:
        path = Path(argv[1])
    except IndexError:
        print('Type path to folder')
        return None
    if not path.exists():
        print('Folder is not exist. Try again.')
        return None
    sort_func(path)

if __name__ == "__main__":
    path_d = input('[+] Введите путь к директории для сортировки: ')
    if not Path(path_d).exists():
        print('[-] Директории не существует')
    else:
        sort_func(path_d)
    print('[!] Сортировка завершена')