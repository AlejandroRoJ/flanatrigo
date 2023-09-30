import sys

from my_qt.apps import UpdaterApp

if __name__ == '__main__' and len(sys.argv) > 1:
    app = UpdaterApp('sys.argv[1]')
    app.exec()
