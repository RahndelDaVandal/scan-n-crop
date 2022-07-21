from pathlib import Path
from rich.traceback import install
from app import App
from cropper.scan_croppers import SinglePhotoScanCropper

install()

app = App()
app.cropper = SinglePhotoScanCropper()

scans_dir = Path(__file__).parent.parent / 'imgs-test'
files = []
for file in scans_dir.iterdir():
    files.append(file)

app.crop(str(files[2]))
