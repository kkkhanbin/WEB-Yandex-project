import os
import shutil

from PIL import Image


class UseFiles:
    @staticmethod
    def create_dir(*paths: str) -> None:
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    @staticmethod
    def save_image(data, destiny: str) -> None:
        """
        Сохранение фотографии

        Пришлось прибегнуть к способу через библиотеку PIL, так как встроенный
        во flask метод data.save() работал неккоректно, т.е. изображение
        сохранялось побитым и ни я, ни flask не могли его открыть

        :param data: любые данные фото, которые можно открыть через
        PIL.Image.open()
        :param destiny: путь до сохраняемого файла
        :return: None
        """

        img = Image.open(data)
        img.save(destiny)

    @staticmethod
    def secure_path(path: str) -> str:
        path_split = path.split('/')
        for i, filename in enumerate(path_split):
            if filename.count('.') == len(filename):
                del path_split[i]
        path_split = os.path.join(*path_split)

        return path_split

    @staticmethod
    def get_size(dir_path: str) -> int:
        """
        Получение размера директория

        :param dir_path: путь к директорию
        :return float: количество байт - размер директория
        """

        total_size = 0

        # Проходимся по всем директориям директория
        for dir_path, dir_names, filenames in os.walk(dir_path):

            # По всем файлам директория
            for filename in filenames:
                file_path = os.path.join(dir_path, filename)
                if not os.path.islink(file_path):
                    total_size += os.path.getsize(file_path)

        return total_size

    @staticmethod
    def delete_file(path: str) -> None:
        """
        Удаление файла по заданному пути вне зависимости от того,
        директория это или файл

        :param path: путь до удаляемого файла
        :return: None
        """

        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
