ALLOWED_EXTENSIONS = {'png', 'jpg', 'svg'}

# Пути
STATIC_PATH = ['static']
UPLOAD_PATH = STATIC_PATH + ['upload']
PROFILES_PATH = UPLOAD_PATH + ['profiles']
PROFILE_PATH = PROFILES_PATH + ['{profile_id}']
AVATAR_PATH = PROFILE_PATH + ['avatar.png']
