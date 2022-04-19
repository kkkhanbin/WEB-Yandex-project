from .search.search import SearchForm
from .login.login import LoginForm
from .profile.edit.edit import EditProfileForm
from .profile.delete.delete import DeleteProfileForm
from .register.register import RegisterForm
from .profile.develop.apikey.add.add import AddEditApikeyForm

# Разветвление форм для того, чтобы в будущем можно было легко разделить эти
# две формы, но сейчас они полностью идентичны, поэтому нет смысла создавать
# лишнюю форму
AddApikeyForm = EditApikeyForm = AddEditApikeyForm

__all__ = (
    'SearchForm', 'LoginForm', 'EditProfileForm', 'AddApikeyForm',
    'DeleteProfileForm', 'RegisterForm', 'EditApikeyForm'
)
