import os
import PyInstaller.__main__

# Запускаем PyInstaller
PyInstaller.__main__.run([
    'src/image_converter.py',
    '--name=RenpyImageConverter',
    '--onefile',
    '--windowed',
    '--clean',
    '--icon=NONE',  # Можно заменить на путь к иконке, если она будет
    '--add-data=src;src'
])

print("Сборка завершена! Исполняемый файл находится в папке dist/") 