# Пути
STATIC_PATH = ('static',)
UPLOAD_PATH = STATIC_PATH + ('upload',)
PROFILES_PATH = UPLOAD_PATH + ('profiles',)
PROFILE_PATH = PROFILES_PATH + ('{profile_id}',)
AVATAR_PATH = PROFILE_PATH + ('avatar.png',)
PLACES_PATH = PROFILE_PATH + ('places',)
PLACE_PATH = PLACES_PATH + ('{place_id}',)
PLACE_MEDIA_FILES_PATH = PLACE_PATH + ('media',)
