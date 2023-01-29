import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging


"""
    Test usage
    python sorter_threads.py -s picture -o dist
"""


# User CLI based on argparse library
parser = argparse.ArgumentParser(description='Application for sorting files to folder by extension. Use threads.')
parser.add_argument('-s', '--source', help="Source folder for sorting", required=True)
parser.add_argument('-o', '--output', help="Destination folder for sorting", default='dist')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')

FOLDERS = []

base_folder = Path(source)
output_folder = Path(output)


def grabs_folder(path: Path) -> None:
    """Function recursively collect folders to sort in base folder to FOLDERS"""
    for el in path.iterdir():
        if el.is_dir():
            FOLDERS.append(el)
            grabs_folder(el)


def sort_file(path: Path) -> None:
    """Function copy files to destination folders by extensions"""
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as err:
                logging.error(err)


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")

    FOLDERS.append(base_folder)
    grabs_folder(base_folder)
    logging.debug(FOLDERS)
    threads = []
    for folder in FOLDERS:
        th = Thread(target=sort_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f'Work is done. You can delete source folder.')


if __name__ == '__main__':
    main()
