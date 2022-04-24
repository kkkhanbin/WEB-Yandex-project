from src.search import Results, Result
from src.data import session
from src.data.models import User


class UserResult(Result):
    TEMPLATE_PATH = Result.TEMPLATES_TYPES_PATH + 'user/user.html'

    @classmethod
    def search(cls, text: str) -> Results:
        """
        Процесс поиска по тексту

        :param text: поисковая строка
        :return: src.search.Results - список найденных объектов
        """

        # Поиск пользователей по никнейму, имени и фамилии
        users = session.query(User).filter(
            User.nickname.ilike(f'%{text.lower()}%') |
            User.name.ilike(f'%{text.lower()}%') |
            User.surname.ilike(f'%{text.lower()}%') |

            User.nickname.ilike(f'%{text.upper()}%') |
            User.name.ilike(f'%{text.upper()}%') |
            User.surname.ilike(f'%{text.upper()}%') |

            User.nickname.ilike(f'%{text}%') |
            User.name.ilike(f'%{text}%') |
            User.surname.ilike(f'%{text}%')
        ).distinct().all()

        return cls.pack_results(text, users, lambda user: cls({'user': user}))
