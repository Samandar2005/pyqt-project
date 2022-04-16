import os
from cx_Freeze import setup, Executable
import sys

import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

base = "Win32GUI"
#base = None

os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [Executable(
    "main.py",
    base = base,
    icon="icon.ico"
    )]

packages = ["os", "numpy", "matplotlib", "random", "sklearn", "scipy", "multiprocessing", 
    "multiprocessing.pool", "tkinter", "encodings", "datetime", "win32api","encodings"]
include_files = [
            r"C:\Users\IDTM\AppData\Local\Programs\Python\Python39\tcl\tcl8.6",
            r"C:\Users\IDTM\AppData\Local\Programs\Python\Python39\tcl\tk8.6",
            r"C:\Users\IDTM\AppData\Local\Programs\Python\Python39\Lib\site-packages\PyQt5\Qt\plugins\platforms",
            r"images",
            r"helper",
            r"css",
]
options = {
    'build_exe': {
        "include_files": include_files,
        'packages': packages,
    },    
}

setup(
    name = "Moliyaviy berilganlarni tahlil qilish",
    options = options,
    version = "1.2.3.1",
    description = 'Dastur Moliyaviy Berilganlarni tahlil qilish uchun',
    executables = executables
)