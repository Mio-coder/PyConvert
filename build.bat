.venv/Scripts/activate.bat
pyinstaller -F --add-data "fileTypesData.json;." -p C:\Users\oparm\PycharmProjects\Pyconvert\.venv\Lib\site-packages -w converter.py file_dilog.py main.py ui.py