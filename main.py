import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
from move import search_coord, postal_index, scale_m, get_address

SCREEN_SIZE = WIDTH, HEIGHT = 650, 400
SIZE_MAP = 650, 400


class RybSholMaps(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/first.ui', self)
        self.z = 12
        self.index = 0
        self.dothis = False
        self.lon = 37.530887
        self.lat = 55.703118
        self.ll = str(self.lon) + ',' + str(self.lat)
        self.pt = self.ll + ',vkbkm'
        self.map = 'map'
        self.fi, self.se = scale_m(self.ll)
        self.image.setFocus()
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SIZE_MAP)
        self.image.setPixmap(self.pixmap)
        self.take_btn.clicked.connect(self.postal)
        self.leave_btn.clicked.connect(self.postal)
        self.map_btn.clicked.connect(self.select_map)
        self.sputnic_btn.clicked.connect(self.select_map)
        self.search_btn.clicked.connect(self.run)
        self.gibrid_btn.clicked.connect(self.select_map)
        self.clear_btn.clicked.connect(self.clear)

    def clear(self):
        self.dothis = False
        self.index = 0
        self.address.setPlainText('')
        self.search.setText('')
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.repaint()
        self.image.setFocus()

    def postal(self):
        if self.sender().text() == 'ДА':
            self.index = 1
        else:
            self.index = 0
        if self.dothis:
            if self.index:
                self.get_postal_code()
            else:
                self.address.setPlainText(self.p_address)

    def get_postal_code(self):
        self.address.setPlainText(self.p_address +
                                  f'. Почтовый индекс: {postal_index(self.ll)}')

    def getImage(self):
        map_server = "http://static-maps.yandex.ru/1.x/?"
        if self.dothis:
            if self.index:
                self.get_postal_code()
            else:
                self.address.setPlainText(self.p_address)
            params = {
                'll': self.ll,
                'pt': self.pt,
                'z': str(self.z),
                'size': ','.join(map(str, SIZE_MAP)),
                'l': self.map,
            }
        else:
            params = {
                'll': self.ll,
                'z': str(self.z),
                'size': ','.join(map(str, SIZE_MAP)),
                'l': self.map,
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
            self.lat += 0.01 * (21 - self.z)
        if event.key() == Qt.Key_Down:
            self.lat -= 0.01 * (21 - self.z)
        if event.key() == Qt.Key_Right:
            self.lon += 0.01 * (21 - self.z)
        if event.key() == Qt.Key_Left:
            self.lon -= 0.01 * (21 - self.z)
        keys = [Qt.Key_Down, Qt.Key_Left, Qt.Key_Up, Qt.Key_Right,
                Qt.Key_PageDown, Qt.Key_PageUp]
        if event.key() in keys:
            self.ll = str(self.lon) + ',' + str(self.lat)
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.repaint()
            self.image.setFocus()

    def select_map(self):
        if self.sender().text() == 'Карта':
            self.map = 'map'
        elif self.sender().text() == 'Спутник':
            self.map = 'sat'
        elif self.sender().text() == 'Гибрид':
            self.map = 'skl'
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.repaint()
        self.image.setFocus()

    def run(self):
        try:
            ll = search_coord(self.search.text())
            if ll:
                self.lon, self.lat = map(float, ll[0].split())
                self.ll = str(self.lon) + ',' + str(self.lat)
                self.pt = self.ll + ',vkbkm'
                self.p_address = ll[1]
                self.address.setPlainText(ll[1])
                self.dothis = True
                self.getImage()
                self.pixmap = QPixmap(self.map_file)
                self.image.setPixmap(self.pixmap)
                self.repaint()
                self.image.setFocus()
        except Exception:
            ...

    def mousePressEvent(self, event):
        coor = [int(x) for x in str(event.pos())[20:-1].split(",")]

        if 0 <= coor[1] <= 400 and 0 <= coor[0] <= 650:
            first = self.lat - 0.08 * (coor[1] - 200) / 400
            second = self.lon + 0.218 * (coor[0] - 325) / 650
            self.pt = f'{second},{first},vkbkm'
            self.p_address = get_address(first, second)
            self.dothis = True
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.repaint()
            self.image.setFocus()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RybSholMaps()
    ex.show()
    sys.exit(app.exec())
