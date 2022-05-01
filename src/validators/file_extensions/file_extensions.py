from src.validators.validator import Validator


class FileExtensions(Validator):
    """
    Валидатор, предназначенный для проверки расширения файла
    """

    # Сообщения ошибок
    FORBIDDEN_EXTENSION_MESSAGE = \
        'Запрещенное расширение файла: {forbidden_filename}'

    def __init__(
            self, extensions: iter, must_be: bool = True, *args, **kwargs):
        """
        :param extensions: коллекция из типов форматов
        :param must_be: указывает на то, должен ли быть формат файла в
        extensions, True - должен, False - нет
        """

        self.extensions = extensions
        self.must_be = must_be

        super().__init__(*args, **kwargs)

    def __call__(self, *args):
        super().__call__(*args)

        # Переданные файлы на валидацию
        files = self.get_validation_data(*args)

        for file in files:
            filename = file.filename.strip()

            if not filename:
                # Если название файла пустое - это значит что файл не был
                # передан в форму и нет смысла выбрасывать ошибку
                continue

            # Если условия проверки не совпали. Например: формат .exe есть в
            # списке, но must_be = False, значит ошибка
            extension = filename.split('.')[-1]
            if extension in self.extensions != self.must_be:
                self.stop_validation(
                    self.FORBIDDEN_EXTENSION_MESSAGE.format(
                        forbidden_filename=filename))
