from PySide6 import QtCore, QtGui, QtWidgets

import constants
from models.config import Config
from models.salvable import Salvable
from my_qt.bases import MixinMeta
from my_qt.buttons import TitleButton
from my_qt.widgets import CentralWidget


class MainWindow(Salvable, QtWidgets.QMainWindow, metaclass=MixinMeta):
    def __init__(self, config: Config):
        super().__init__(config)
        self.last_position = None
        self.last_width = None
        self.was_maximized = False
        self.is_moving = False

        self.icon = QtGui.QIcon(constants.LOGO_PATH)
        self.setWindowTitle('TrigoMorao')
        self.setWindowIcon(self.icon)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.button_close = TitleButton(constants.CLOSE_PATH, self, 1, top_margin=3, right_margin=3)
        self.button_close.setStyleSheet('QPushButton:hover{background-color: darkred}')

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.setFixedSize(20, 20)
        self.button_maximize = TitleButton(constants.MAXIMIZE_PATH, self, 2, top_margin=3)
        self.button_minimize = TitleButton(constants.MINIMIZE_PATH, self, 3, top_margin=3)
        self.button_pin = TitleButton(constants.PIN_PATH, self, 4, icon_size=(12, 12), top_margin=3, checkable=True)

        self.resize(self.sizeHint())
        self.move_to_center()
        self.show()

    def connect_signals(self, *args):
        self.central_widget.connect_signals(*args)

        self.button_close.clicked.connect(self.close)
        self.button_maximize.clicked.connect(self.maximize)
        self.button_minimize.clicked.connect(self.minimize)
        self.button_pin.toggled.connect(self._on_pin_changed)

        self.central_widget.tab.currentChanged.connect(self._on_tab_changed)

    def _on_pin_changed(self, state: bool):
        self.set_on_top(state)
        self.config.pinned = state
        self.save_config()

    def _on_tab_changed(self, index: int):
        self.config.tab = index
        self.save_config()

    def close(self) -> bool:
        self.central_widget.close()
        return super().close()

    def load_config(self):
        self.config.load()

        self.button_pin.setChecked(self.config.pinned)
        self.central_widget.tab.setCurrentIndex(self.config.tab)

        self.config.release()

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.last_width = self.width()
            self.showMaximized()
        self.updateGeometry()
        self.was_maximized = not self.was_maximized

    def minimize(self):
        if self.isMinimized():
            self.show()
        else:
            self.showMinimized()
        self.updateGeometry()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        super().mouseDoubleClickEvent(event)
        if event.button() == QtCore.Qt.MouseButton.LeftButton and event.pos().y() <= constants.TITLE_BAR_HEIGHT:
            self.last_position = None
            self.maximize()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        super().mouseMoveEvent(event)
        if self.last_position is not None:
            self.is_moving = True
            if self.isMaximized():
                self.maximize()
                self.was_maximized = True
                horizontal_offset = self.last_width // 2
                vertical_offset = constants.TITLE_BAR_HEIGHT // 2
                self.move(QtGui.QCursor.pos().x() - horizontal_offset, QtGui.QCursor.pos().y() - vertical_offset)
                self.last_position = QtCore.QPoint(horizontal_offset, vertical_offset)
            else:
                self.move(self.mapToParent(self.mapFromGlobal(QtGui.QCursor.pos()) - self.last_position))

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        self.setFocus()
        if event.button() == QtCore.Qt.MouseButton.LeftButton and event.pos().y() <= constants.TITLE_BAR_HEIGHT:
            self.last_position = event.pos()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)
        cursor_pos = QtGui.QCursor.pos()
        current_screen = QtWidgets.QApplication.screenAt(cursor_pos)
        current_screen_top = QtWidgets.QApplication.primaryScreen().size().height() - current_screen.size().height()
        if self.is_moving:
            if not self.was_maximized and cursor_pos.y() <= current_screen_top + constants.TITLE_BAR_HEIGHT // 2:
                self.move(
                    current_screen.geometry().x() + (current_screen.size().width() - self.width()) // 2,
                    current_screen.geometry().y() + (current_screen.size().height() - self.height()) // 2
                )
                self.maximize()
            else:
                self.was_maximized = False
            self.is_moving = False
        self.last_position = None

    def move_to_center(self):
        current_screen = QtWidgets.QApplication.screenAt(QtGui.QCursor.pos())
        self.move(
            self.mapToGlobal(
                QtCore.QPoint(
                    current_screen.geometry().x() + current_screen.geometry().width() // 2 - self.size().width() // 2,
                    current_screen.geometry().y() + current_screen.geometry().height() // 2 - self.size().height() // 2
                )
            )
        )

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        self.updateGeometry()

    def set_on_top(self, activate: bool):
        size = self.size()
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint, activate)
        self.resize(size)
        self.show()

    def sizeHint(self):
        return QtCore.QSize(510, 600)

    def updateGeometry(self):
        super().updateGeometry()

        self.button_close.updateGeometry()
        self.button_maximize.updateGeometry()
        self.button_minimize.updateGeometry()
        self.button_pin.updateGeometry()

        self.grip.move(self.width() - self.grip.width(), self.height() - self.grip.height())


class CrosshairWindow(QtWidgets.QMainWindow):
    def __init__(self, color=(255, 0, 0), size=3, horizontal_offset=0, vertical_offset=0, screen_index=0):
        super().__init__()
        self.color = color
        self.screen_index = screen_index
        self.size = size
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset

        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTransparentForInput | QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(
            QtCore.Qt.BrushStyle.SolidPattern,
            constants.CROSSHAIR_PEN_WIDTH,
            QtCore.Qt.PenStyle.SolidLine,
            QtCore.Qt.PenCapStyle.SquareCap,
            QtCore.Qt.PenJoinStyle.MiterJoin
        )
        pen.setColor(QtGui.QColor.fromRgb(*self.color))
        pen.setWidth(constants.CROSSHAIR_PEN_WIDTH)
        painter.setPen(pen)
        painter.drawRect(
            (self.width() - self.size - constants.CROSSHAIR_PEN_WIDTH) // 2 + self.horizontal_offset,
            (self.height() - self.size - constants.CROSSHAIR_PEN_WIDTH) // 2 - self.vertical_offset,
            self.size + constants.CROSSHAIR_PEN_WIDTH,
            self.size + constants.CROSSHAIR_PEN_WIDTH
        )

    @property
    def screen_index(self) -> int:
        return QtWidgets.QApplication.screens().index(self.screen())

    @screen_index.setter
    def screen_index(self, index: int):
        self.setGeometry(QtWidgets.QApplication.screens()[index].geometry())
