import subprocess
from src.utility import APP_NAME, VERSION, MoveFile, CopyDir, PackZip

"""
Pack the enana program with Nuitka
"""

# pack with Nuitka
args = [
    "python", "-m", "nuitka",
    "--standalone",
    "--show-memory",
    "--show-progress",
    "--mingw64",
    "--no-deployment-flag=self-execution",
    "--remove-output",
    "--output-dir=release",
    "--lto=yes",
    "--windows-icon-from-ico=icon/icon.png",
    "src/main.py",
]
subprocess.run(args)

# rename 'main.exe' as 'enana.exe'
MoveFile(f"release/main.dist/main.exe",
          f"release/main.dist/{APP_NAME}.exe")

# copy directory 'family' to release/main.dist
CopyDir(f"family", f"release/main.dist/family")

# pack zip
PackZip(f"release/main.dist", f"release/{APP_NAME}-{VERSION}.zip")
