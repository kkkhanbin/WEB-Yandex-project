import os

from waitress import serve

from src import app


def main():
    port = int(os.getenv('PORT'))
    serve(app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
