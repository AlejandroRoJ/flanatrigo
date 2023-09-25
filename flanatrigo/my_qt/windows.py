from PySide6 import QtCore, QtGui, QtWidgets

import constants
from models.config import Config
from models.enums import WindowBorder
from models.salvable import Salvable
from my_qt.bases import MixinMeta
from my_qt.buttons import TitleButton
from my_qt.widgets import CentralWidget


class MainWindow(Salvable, QtWidgets.QMainWindow, metaclass=MixinMeta):
    def __init__(self, config: Config):
        super().__init__(config)
        self.last_position: QtCore.QPoint | None = None
        self.last_width = None
        self.was_maximized = False
        self.is_moving = False
        self.current_border: WindowBorder | None = None
        self.grabbed_border: WindowBorder | None = None

        self.icon = QtGui.QIcon(constants.LOGO_PATH)
        self.setWindowTitle('TrigoMorao')
        self.setWindowIcon(self.icon)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.central_widget = CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.button_close = TitleButton(constants.CLOSE_PATH, self, 1, top_margin=3, right_margin=3)
        self.button_close.setStyleSheet('QPushButton:hover{background-color: darkred}')
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

    def _drag(self):
        if self.last_position.y() > constants.TITLE_BAR_HEIGHT:
            return

        if self.isMaximized():
            self.maximize()
            self.was_maximized = True
            horizontal_offset = self.last_width // 2
            vertical_offset = constants.TITLE_BAR_HEIGHT // 2
            self.move(self.cursor().pos().x() - horizontal_offset, self.cursor().pos().y() - vertical_offset)
            self.last_position = QtCore.QPoint(horizontal_offset, vertical_offset)
        else:
            self.move(self.pos() + self.mapFromGlobal(self.cursor().pos()) - self.last_position)

    def _get_current_border(self, position: QtCore.QPoint) -> WindowBorder | None:
        if self.isMaximized():
            return
        elif (
            position.x() <= constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR
            and
            position.y() <= constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR
        ):
            return WindowBorder.LEFT_TOP
        elif (
            self.width() - constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR <= position.x()
            and
            position.y() <= constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR
        ):
            return WindowBorder.RIGHT_TOP
        elif (
            position.x() <= constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR
            and
            self.height() - constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR <= position.y()
        ):
            return WindowBorder.LEFT_BOTTOM
        elif (
            self.width() - constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR <= position.x()
            and
            self.height() - constants.RESIZE_AREA_SIZE * constants.RESIZE_AREA_CORNER_FACTOR <= position.y()
        ):
            return WindowBorder.RIGHT_BOTTOM
        elif position.x() <= constants.RESIZE_AREA_SIZE:
            return WindowBorder.LEFT
        elif self.width() - constants.RESIZE_AREA_SIZE <= position.x():
            return WindowBorder.RIGHT
        elif position.y() <= constants.RESIZE_AREA_SIZE:
            return WindowBorder.TOP
        elif self.height() - constants.RESIZE_AREA_SIZE <= position.y():
            return WindowBorder.BOTTOM

    def _on_pin_changed(self, state: bool):
        self.set_on_top(state)
        self.config.pinned = state
        self.save_config()

    def _on_tab_changed(self, index: int):
        self.config.tab = index
        self.save_config()

    def _resize(self):
        local_cursor_position = self.mapFromGlobal(self.cursor().pos())
        x_distance = local_cursor_position.x() - self.last_position.x()
        y_distance = local_cursor_position.y() - self.last_position.y()

        match self.grabbed_border:
            case WindowBorder.LEFT:
                if (new_width := self.width() - x_distance) >= self.minimumWidth():
                    self.setGeometry(self.x() + x_distance, self.y(), new_width, self.height())
            case WindowBorder.RIGHT:
                self.resize(local_cursor_position.x(), self.height())
            case WindowBorder.TOP:
                if (new_height := self.height() - y_distance) >= self.minimumHeight():
                    self.setGeometry(self.x(), self.y() + y_distance, self.width(), new_height)
            case WindowBorder.BOTTOM:
                self.resize(self.width(), local_cursor_position.y())
            case WindowBorder.LEFT_TOP:
                if (new_width := self.width() - x_distance) >= self.minimumWidth():
                    new_x = self.x() + x_distance
                else:
                    new_x = self.x()
                if (new_height := self.height() - y_distance) >= self.minimumHeight():
                    new_y = self.y() + y_distance
                else:
                    new_y = self.y()
                self.setGeometry(new_x, new_y, new_width, new_height)
            case WindowBorder.RIGHT_TOP:
                if (new_height := self.height() - y_distance) >= self.minimumHeight():
                    new_y = self.y() + y_distance
                else:
                    new_y = self.y()
                self.setGeometry(self.x(), new_y, local_cursor_position.x(), new_height)
            case WindowBorder.LEFT_BOTTOM:
                if (new_width := self.width() - x_distance) >= self.minimumWidth():
                    new_x = self.x() + x_distance
                else:
                    new_x = self.x()
                self.setGeometry(new_x, self.y(), new_width, local_cursor_position.y())
            case WindowBorder.RIGHT_BOTTOM:
                self.resize(local_cursor_position.x(), local_cursor_position.y())

    def _update_cursor(self):
        if self.current_border in (WindowBorder.LEFT_TOP, WindowBorder.RIGHT_BOTTOM):
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif self.current_border in (WindowBorder.RIGHT_TOP, WindowBorder.LEFT_BOTTOM):
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif self.current_border in (WindowBorder.LEFT, WindowBorder.RIGHT):
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif self.current_border in (WindowBorder.TOP, WindowBorder.BOTTOM):
            self.setCursor(QtCore.Qt.SizeVerCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)

    def close(self) -> bool:
        self.central_widget.close()
        return super().close()

    def event(self, event: QtCore.QEvent) -> bool:
        if isinstance(event, QtGui.QHoverEvent) and not self.is_moving:
            self.current_border = self._get_current_border(event.pos())
            self._update_cursor()

        return super().event(event)

    def load_config(self):
        self.config.load()

        self.resize(self.sizeHint())
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
            self.grabbed_border = None
            self.maximize()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        super().mouseMoveEvent(event)
        if self.last_position is None:
            return

        self.is_moving = True
        if self.grabbed_border:
            self._resize()
        else:
            self._drag()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        super().mousePressEvent(event)
        self.setFocus()
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.last_position = event.pos()
            self.grabbed_border = self.current_border

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        super().mouseReleaseEvent(event)
        cursor_pos = self.cursor().pos()
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
        self.grabbed_border = None

    def move_to_center(self):
        current_screen = QtWidgets.QApplication.screenAt(self.cursor().pos())
        self.move(
            self.mapToGlobal(
                QtCore.QPoint(
                    current_screen.geometry().x() + (current_screen.geometry().width() - self.size().width()) // 2,
                    current_screen.geometry().y() + (current_screen.geometry().height() - self.size().height()) // 2
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
        return QtCore.QSize(600, 600)

    def updateGeometry(self):
        super().updateGeometry()

        self.button_close.updateGeometry()
        self.button_maximize.updateGeometry()
        self.button_minimize.updateGeometry()
        self.button_pin.updateGeometry()


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
