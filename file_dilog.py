"""
from : https://stackoverflow.com/a/54120628/15451952
"""

from PyQt5 import QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog, QDialog
from pathlib import Path


def FileDialog(directory: str = '', forOpen: bool = True, fmt: dict[str, str] = None, isFolder: bool = False):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    options |= QFileDialog.DontUseCustomDirectoryIcons
    dialog = QFileDialog()
    dialog.setOptions(options)

    dialog.setFilter(dialog.filter() | QDir.Hidden)

    # ARE WE TALKING ABOUT FILES OR FOLDERS
    if isFolder:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
    else:
        dialog.setFileMode(QFileDialog.AnyFile)

    # OPENING OR SAVING
    dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)

    # SET FORMAT, IF SPECIFIED
    if fmt is not None and isFolder is False:
        dialog.setDefaultSuffix(next(iter(fmt.values())))
        dialog.setNameFilters([f"{name} (*.{ext})" for name, ext in fmt.items()])

    # SET THE STARTING DIRECTORY
    if directory != '':
        dialog.setDirectory(str(directory))
    else:
        dialog.setDirectory(str(Path.home()))

    if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]  # returns a list
        return path
    else:
        return ''
