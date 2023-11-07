from PySide6.QtWidgets import QMainWindow, QMessageBox, QHeaderView

from ui.main_window import Ui_MainWindow
from data.list_devices import Devices
from utils.convert_subnet import cidr_to_subnetmask
from utils.ip_scaner import scan_ports
from utils import table

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow() # инициализация окна
        self.ui.setupUi(self) 
        self.msg = QMessageBox() # инициализация окна сообщений
        self.devices = Devices.get_devices()
        for device in self.devices:
            self.ui.comboBox_devices.addItem(device)
        self.current_device:dict = self.devices[self.ui.comboBox_devices.currentText()]
        self.current_device['name'] = self.ui.comboBox_devices.currentText()
        self.ui.port_enter.setText('3306')
        self.set_text_for_labels_device()
        self.ui.comboBox_devices.currentIndexChanged.connect(self.change_device)
        self.ui.skanport_button.clicked.connect(self.run_scan_port)
        self.ui.devices_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def set_text_for_labels_device(self) -> None:
        self.ui.label_info_mac_adress.setText(self.current_device['MAC'])
        self.ui.label_info_ip_adress.setText(self.current_device['IP'])
        self.ui.label_info_mask.setText(cidr_to_subnetmask(self.current_device['NETWORK PREFIX']))

    def change_device(self) -> None:
        self.current_device = self.devices[self.ui.comboBox_devices.currentText()]
        self.current_device['name'] = self.ui.comboBox_devices.currentText()
        self.set_text_for_labels_device()

    def run_scan_port(self) -> None:
        port = int(self.ui.port_enter.text())
        ip:str = self.current_device['IP']
        ip_mask = ip.split('.')[0]+'.'+ip.split('.')[1]+'.'+ip.split('.')[2]+'.'
        ip_adreses = list()
        self.msg.warning(self, 'Сканирование портов', 'Сканирование портов началось')
        ip_adreses = scan_ports(ip_mask, port)
        self.msg.warning(self, 'Сканирование портов', 'Сканирование портов завершено')
        table.data_table = table.get_devices_table(ip_adreses)
        model = table.TableModel_MainWindow(table.data_table, self.ui.devices_view)
        self.ui.devices_view.setModel(model)
        self.ui.devices_view.resizeColumnsToContents()
        