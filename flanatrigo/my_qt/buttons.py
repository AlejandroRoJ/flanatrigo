import pathlib

from PySide6 import QtCore, QtGui, QtWidgets

import constants


class TitleButton(QtWidgets.QPushButton):
    signal_resize = QtCore.Signal()

    def __init__(
        self,
        icon_path: str | pathlib.Path,
        parent: QtWidgets.QWidget,
        index: int,
        size=(constants.TITLE_BAR_HEIGHT, constants.TITLE_BAR_HEIGHT),
        top_margin=0,
        right_margin=0,
        icon_size=(16, 16),
        checkable=False
    ):
        super().__init__(icon=QtGui.QIcon(str(icon_path)), parent=parent)
        self.parent = parent
        self.index = index
        self.size = (size[0] - top_margin * 2, size[1] - top_margin * 2)
        self.top_margin = top_margin
        self.right_margin = right_margin

        self.setFlat(True)
        self.setIconSize(QtCore.QSize(*icon_size))
        self.setStyleSheet('QPushButton:checked{background-color: rgb(50, 50, 180)}')
        self.setCheckable(checkable)

        self.connect_signals()

        self.updateGeometry()

    def connect_signals(self):
        self.signal_resize.connect(
            lambda: self.setGeometry(
                self.parent.width() - self.size[0] * (self.index + 1) - self.right_margin,
                self.top_margin,
                self.size[0],
                self.size[1]
            ),
            QtCore.Qt.QueuedConnection
        )

    def enterEvent(self, event: QtGui.QEnterEvent):
        self.setFlat(False)

    def leaveEvent(self, event: QtCore.QEvent):
        self.setFlat(True)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        super().mouseMoveEvent(event)
        if self.rect().contains(event.pos()):
            self.setFlat(False)
        else:
            self.setFlat(True)

    def updateGeometry(self):
        super().updateGeometry()
        self.signal_resize.emit()


class Switch(QtWidgets.QAbstractButton):
    def __init__(self, parent=None, track_radius=10, thumb_radius=8, os_colors=True):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self._track_radius = track_radius
        self._thumb_radius = thumb_radius

        self._margin = max(0, self._thumb_radius - self._track_radius)
        self._base_offset = max(self._thumb_radius, self._track_radius)
        self._end_offset = {
            True: lambda: self.width() - self._base_offset,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset
        self._track_color: dict | None = None
        self._thumb_color: dict | None = None
        self._text_color: dict | None = None
        self._thumb_text: dict | None = None
        self._track_opacity: float | None = None
        self.default_highlight_color = self.palette().highlight().color()
        self.default_dark_color = self.palette().dark().color()
        self.default_light_color = self.palette().light().color()
        self.default_highlighted_text_color = self.palette().highlightedText().color()

        self.set_os_colors(os_colors)

    def click(self) -> None:
        super().click()
        self.offset = self._end_offset[self.isChecked()]()

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.PointingHandCursor)
        super().enterEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            anim = QtCore.QPropertyAnimation(self, b'offset', self)
            anim.setDuration(120)
            # noinspection PyPropertyAccess
            anim.setStartValue(self.offset)
            anim.setEndValue(self._end_offset[self.isChecked()]())
            anim.start()

    # noinspection PyCallingNonCallable
    @QtCore.Property(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def paintEvent(self, event):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setPen(QtCore.Qt.NoPen)
        track_opacity = self._track_opacity
        thumb_opacity = 1.0
        text_opacity = 1.0
        if self.isEnabled():
            track_brush = self._track_color[self.isChecked()]
            thumb_brush = self._thumb_color[self.isChecked()]
            text_color = self._text_color[self.isChecked()]
        else:
            track_opacity *= 0.8
            track_brush = self.palette().shadow()
            thumb_brush = self.palette().mid()
            text_color = self.palette().shadow().color()

        p.setBrush(track_brush)
        p.setOpacity(track_opacity)
        p.drawRoundedRect(
            self._margin,
            self._margin,
            self.width() - 2 * self._margin,
            self.height() - 2 * self._margin,
            self._track_radius,
            self._track_radius,
        )
        p.setBrush(thumb_brush)
        p.setOpacity(thumb_opacity)
        # noinspection PyPropertyAccess
        p.drawEllipse(
            self.offset - self._thumb_radius,
            self._base_offset - self._thumb_radius,
            2 * self._thumb_radius,
            2 * self._thumb_radius,
        )
        p.setPen(text_color)
        p.setOpacity(text_opacity)
        font = p.font()
        font.setPixelSize(1.5 * self._thumb_radius)
        p.setFont(font)
        # noinspection PyPropertyAccess
        p.drawText(
            QtCore.QRectF(
                self.offset - self._thumb_radius,
                self._base_offset - self._thumb_radius,
                2 * self._thumb_radius,
                2 * self._thumb_radius,
            ),
            QtCore.Qt.AlignCenter,
            self._thumb_text[self.isChecked()],
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.offset = self._end_offset[self.isChecked()]()

    def setChecked(self, checked):
        super().setChecked(checked)
        self.offset = self._end_offset[checked]()

    def set_os_colors(self, state=True):
        palette = self.palette()

        if state:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, self.default_highlight_color)
            palette.setColor(QtGui.QPalette.ColorRole.Dark, self.default_dark_color)
            palette.setColor(QtGui.QPalette.ColorRole.Light, self.default_light_color)
            palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, self.default_highlighted_text_color)
        else:
            palette.setColor(QtGui.QPalette.ColorRole.Highlight, QtGui.QColor.fromRgb(79, 114, 195))
            palette.setColor(QtGui.QPalette.ColorRole.Dark, QtGui.QColor.fromRgb(30, 30, 30))
            palette.setColor(QtGui.QPalette.ColorRole.Light, QtGui.QColor.fromRgb(120, 120, 120))
            palette.setColor(QtGui.QPalette.ColorRole.HighlightedText, QtGui.QColor.fromRgb(0, 0, 0))

        if self._thumb_radius > self._track_radius:
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._thumb_color = {
                True: palette.highlight(),
                False: palette.light(),
            }
            self._text_color = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: '',
                False: '',
            }
            self._track_opacity = 0.5
        else:
            self._thumb_color = {
                True: palette.highlightedText(),
                False: palette.light(),
            }
            self._track_color = {
                True: palette.highlight(),
                False: palette.dark(),
            }
            self._text_color = {
                True: palette.highlight().color(),
                False: palette.dark().color(),
            }
            self._thumb_text = {
                True: '✔',
                False: '✕',
            }
            self._track_opacity = 1

        self.setPalette(palette)

    def sizeHint(self):
        return QtCore.QSize(
            4 * self._track_radius + 2 * self._margin,
            2 * self._track_radius + 2 * self._margin,
        )
