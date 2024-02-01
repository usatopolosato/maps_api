import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
import move

SCREEN_SIZE = WIDTH, HEIGHT = 650, 400
SIZE_MAP = 650, 400


class RybSholMaps(QWidget):
    def __init__(self):
        super().__init__()
        self.z = 12
        self.lon = 37.530887
        self.lat = 55.703118
        self.ll = str(self.lon) + ',' + str(self.lat)
        self.fi, self.se = move.move(self.ll)
        self.getImage()
        self.initUI()

    def getImage(self):
        map_server = "http://static-maps.yandex.ru/1.x/?"
        params = {
            'll': self.ll,
            'z': str(self.z),
            'size': ','.join(map(str, SIZE_MAP)),
            'l': 'map',
        }
        response = requests.get(map_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.fi, self.se = move.move(self.ll)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SIZE_MAP)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            temp = self.z
            self.z += 1
            if not 0 <= self.z <= 21:
                self.z = temp
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.repaint()
        if event.key() == Qt.Key_PageDown:
            temp = self.z
            self.z -= 1
            if not 0 <= self.z <= 21:
                self.z = temp
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.repaint()
        if event.key() == Qt.Key_Up:
            self.lat += 0.01
        if event.key() == Qt.Key_Down:
            self.lat -= 0.01
        if event.key() == Qt.Key_Right:
            self.lon += 0.01
        if event.key() == Qt.Key_Left:
            self.lon -= 0.01
        keys = [Qt.Key_Down, Qt.Key_Left, Qt.Key_Up, Qt.Key_Right, Qt.Key_PageDown, Qt.Key_PageUp]
        if event.key() in keys:
            self.ll = str(self.lon) + ',' + str(self.lat)
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.repaint()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RybSholMaps()
    ex.show()
    sys.exit(app.exec())
