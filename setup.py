from cx_Freeze import setup, Executable
import os

with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

build_exe_options = {
    "packages": [],
    "include_files": [("icons", "icons")],  # includes entire folder
}
base = "Win32GUI" if os.name == "nt" else None

setup(
    name="Sortly",
    version="1.0",
    description="My PySide6 App",
    options={"build_exe": build_exe_options},
    executables=[Executable("app.py", base=base, target_name="sortly.exe")],
)
