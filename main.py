import requests
import folium
import sys
import os
import pyautogui
import math
# Any widgets can be window
# QMainWindow - This is a pre-made widget which provides a lot of standard window features you'll make use of in your apps, including toolbars, menus, a statusbar, dockable widgets and more.
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLineEdit, QLabel
from PyQt5 import QtCore, QtWebEngineWidgets


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.label = QLabel("IP: ", self)
        self.find_button = QPushButton(self)
        self.ip_input = QLineEdit(self)

        self.size_x = 300
        self.size_y = 130
        self.window_title = 'My python GUI'
        self.init_UI()

    def init_UI(self):
        self.setup_main_window()
        self.setup_find_button()
        self.setup_ip_input()
        self.setup_label()

    def setup_main_window(self):
        window_width, window_height = pyautogui.size()

        move_x = math.floor((window_width / 2) - (self.size_x / 2))
        move_y = math.floor((window_height / 2) - (self.size_y / 2))

        self.setWindowTitle(self.window_title)
        self.resize(self.size_x, self.size_y)
        self.move(move_x, move_y)

    def setup_ip_input(self):
        self.ip_input.setFixedSize(150, 30)
        self.ip_input.move(self.calculate_middle_point_for_element(150), 30)

    def setup_find_button(self):
        self.find_button.setText("Find")
        self.find_button.setFixedSize(80, 30)
        self.find_button.move(self.calculate_middle_point_for_element(80), 70)
        self.find_button.clicked.connect(self.handle_ip_search)

    def setup_label(self):
        self.label.move(self.label.size().width(), 0)

    def setup_view(self):
        self.view.load(QtCore.QUrl().fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0] + r'\index.html'
        ))
        self.view.show()

    @QtCore.pyqtSlot()
    def handle_ip_search(self):
        ip = self.ip_input.text()

        try:
            info_from_ip = get_info_by_ip(ip)
            save_map_like_html(info_from_ip.get('lat'), info_from_ip.get('lon'))
        except ValueError:
            self.label.setText('Invalid IP address')
        except Exception as error:
            self.label.setText(error)
        else:
            self.setup_view()

    def calculate_middle_point_for_element(self, x, y=None):
        if x and not y:
            return math.floor((self.size_x / 2) - (x / 2))
        elif y and not x:
            return math.floor((self.size_y / 2) - (y / 2))
        else:
            return (
                math.floor((self.size_x / 2) - (x / 2)),
                math.floor((self.size_y / 2) - (y / 2))
            )


def get_info_by_ip(ip='127.0.0.1'):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}').json()

        return {
            'country': response.get('country'),
            'region': response.get('region'),
            'region_name': response.get('regionName'),
            'city': response.get('city'),
            'zip': response.get('zip'),
            'lat': response.get('lat'),
            'lon': response.get('lon'),
            'provider': response.get('isp'),
            'org': response.get('org'),
            'ip': response.get('query')
        }
    except requests.exceptions.ConnectionError:
        raise ConnectionError('Please check your connection!')
        print('[!] Please check your connection!')
    # except requests.exceptions.JSONDecodeError:
    #     print('[!] JSON encoding error')


def save_map_like_html(lat, lon):
    m = folium.Map(location=[lat, lon])
    m.add_child(folium.Marker(location=[lat, lon]))
    m.save(outfile='index.html')


def render_py_gui():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()


def main():
    render_py_gui()


if __name__ == '__main__':
    main()
