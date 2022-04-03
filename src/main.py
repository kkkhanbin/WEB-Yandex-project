import sys
sys.path.append('/home/usr/WEB-Yandex-project')

import os

from waitress import serve

from src import app


def main():
    port = int(os.getenv('PORT'))
    serve(app, host='127.0.0.1', port=port)


if __name__ == '__main__':
    main()
