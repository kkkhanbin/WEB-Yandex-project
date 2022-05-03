ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'svg', 'mp3', 'mp4', 'mpeg-1', 'mpeg-2', 'mpeg-3', 'mpeg-4',
    'txt', 'csv', 'db', 'py', 'js', 'html'
}
FORBIDDEN_EXTENSIONS = {
    'exe'
}
MAX_PLACE_MEDIA_SIZE = 16 * 1024 * 1024  # 16 мегабайт

# Пути
STATIC_PATH = ['static']
UPLOAD_PATH = STATIC_PATH + ['upload']
PROFILES_PATH = UPLOAD_PATH + ['profiles']
PROFILE_PATH = PROFILES_PATH + ['{profile_id}']
AVATAR_PATH = PROFILE_PATH + ['avatar.png']
PLACES_PATH = PROFILE_PATH + ['places']
PLACE_PATH = PLACES_PATH + ['{place_id}']
PLACE_MEDIA_FILES_PATH = PLACE_PATH + ['media']
