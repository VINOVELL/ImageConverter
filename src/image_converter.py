import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                            QProgressBar, QListWidget)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PIL import Image
import webbrowser

class ImageConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Converter")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2D2D30; color: white;")

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной вертикальный макет
        main_layout = QVBoxLayout(central_widget)
        
        # Заголовок программы
        title_label = QLabel("Ren'Py Converter Image To WEBP")
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        title_label.setStyleSheet("color: #FF5252;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Создаем виджет для контента
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        
        # Левая панель - список файлов
        file_list_layout = QVBoxLayout()
        file_list_label = QLabel("Выбранные файлы:")
        file_list_label.setFont(QFont('Arial', 10))
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("background-color: #3E3E42; color: white;")
        
        file_list_layout.addWidget(file_list_label)
        file_list_layout.addWidget(self.file_list)
        
        # Правая панель - кнопки и прогресс
        control_layout = QVBoxLayout()
        
        select_button = QPushButton("Выбрать изображения")
        select_button.setStyleSheet("background-color: #0078D7; padding: 10px;")
        select_button.clicked.connect(self.select_images)
        
        convert_button = QPushButton("Конвертировать в WEBP")
        convert_button.setStyleSheet("background-color: #107C10; padding: 10px;")
        convert_button.clicked.connect(self.convert_images)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("text-align: center;")
        self.status_label = QLabel("Готов к работе")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        control_layout.addWidget(select_button)
        control_layout.addWidget(convert_button)
        control_layout.addWidget(self.progress_bar)
        control_layout.addWidget(self.status_label)
        control_layout.addStretch()
        
        # Добавляем левую и правую панель в контент
        content_layout.addLayout(file_list_layout, 2)  # 2/3 ширины
        content_layout.addLayout(control_layout, 1)    # 1/3 ширины
        
        main_layout.addWidget(content_widget)
        
        # Нижняя панель с информацией о разработчике
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.addStretch()
        
        # Правая часть футера
        github_link = QLabel("<a href='https://github.com/VINOVELL'>@VINOVELL</a>")
        github_link.setOpenExternalLinks(True)
        github_link.setStyleSheet("color: #0078D7;")
        github_link.setFont(QFont('Arial', 9))
        github_link.setTextInteractionFlags(Qt.TextBrowserInteraction)
        github_link.linkActivated.connect(self.open_github)
        
        made_by = QLabel("Made By VINOVELL")
        made_by.setStyleSheet("color: #777;")
        made_by.setFont(QFont('Arial', 8))
        
        footer_right = QVBoxLayout()
        footer_right.addWidget(github_link, alignment=Qt.AlignRight)
        footer_right.addWidget(made_by, alignment=Qt.AlignRight)
        
        footer_layout.addLayout(footer_right)
        
        main_layout.addWidget(footer_widget)
        
        # Список для хранения выбранных файлов
        self.images = []
        
    def select_images(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        
        if file_dialog.exec_():
            self.images = file_dialog.selectedFiles()
            self.file_list.clear()
            for image_path in self.images:
                self.file_list.addItem(os.path.basename(image_path))
            
            self.status_label.setText(f"Выбрано {len(self.images)} файлов")
    
    def convert_images(self):
        if not self.images:
            self.status_label.setText("Сначала выберите изображения")
            return
            
        output_dir = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if not output_dir:
            return
            
        self.progress_bar.setMaximum(len(self.images))
        self.progress_bar.setValue(0)
        
        converted_count = 0
        for idx, image_path in enumerate(self.images):
            try:
                with Image.open(image_path) as img:
                    output_filename = os.path.splitext(os.path.basename(image_path))[0] + ".webp"
                    output_path = os.path.join(output_dir, output_filename)
                    img.save(output_path, "WEBP")
                    converted_count += 1
            except Exception as e:
                print(f"Ошибка при конвертации {image_path}: {e}")
            
            self.progress_bar.setValue(idx + 1)
            QApplication.processEvents()
        
        self.status_label.setText(f"Конвертировано {converted_count} из {len(self.images)} файлов")
    
    def open_github(self, link):
        QDesktopServices.openUrl(QUrl(link))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverter()
    window.show()
    sys.exit(app.exec_()) 