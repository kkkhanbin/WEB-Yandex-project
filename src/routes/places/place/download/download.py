import os
import shutil
import io

from flask import abort, send_from_directory, send_file
from werkzeug.exceptions import NotFound

from src.routes import routes_bp
from src.data.models import Place
from src.data import session


@routes_bp.route(
    '/places/<login>/download/<int:place_id>', defaults={'path': '/'})
@routes_bp.route('/places/<login>/download/<int:place_id>/<path:path>')
def place_media_download(login, place_id, path):
    user, place, file_path, media_path, path = \
        Place.get_view_config(session, login, place_id, path)

    file_path_split = os.path.split(file_path)

    try:
        if os.path.isdir(file_path):
            shutil.make_archive(file_path_split[-1], 'zip', root_dir=file_path)
            archive_path = file_path_split[-1] + '.zip'

            with open(archive_path, mode='rb') as archive:
                data = io.BytesIO(archive.read())
            os.remove(archive_path)

            return send_file(
                data, as_attachment=True, download_name=archive_path)
        else:
            response = send_from_directory(
                os.path.join(*file_path_split[:-1]), file_path_split[-1],
                as_attachment=True)

            return response

    except FileNotFoundError:
        abort(NotFound.code, description='Файл не найден')
