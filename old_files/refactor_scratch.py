from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, TypeVar

IMG = TypeVar("IMG")


@dataclass
class Scan:
    file_path: str
    img: IMG = None

    def __post_init__(self):
        self.img = self._load_img(self.file_path)

    def _load_img(self):
        ...

    @property
    def img(self) -> IMG:
        return self.img

    @img.setter
    def img(self, img: IMG) -> None:
        self.img = img


class Scan(ABC):
    def __init__(self) -> None:
        self.file_path: str = None
        self._img: IMG = None

    @property
    def img(self) -> IMG:
        return self._img

    @abstractmethod
    def load(self, file_path: str) -> None:
        ...

    @abstractmethod
    def save(self, file_path: str) -> None:
        ...


class Cropper(Protocol):
    def crop(self, img: IMG) -> IMG:
        ...


class ScanHandler(Protocol):
    def load(self, file_path: str) -> IMG:
        ...

    def save(self, file_path, img: IMG) -> None:
        ...


class App:
    def __init__(self) -> None:
        self._cropper = None
        self._scanner_handler = None

    @property
    def cropper(self) -> Cropper:
        return self._cropper

    @cropper.setter
    def cropper(self, cropper: Cropper) -> None:
        self._cropper = cropper

    @property
    def scanner(self) -> ScanHandler:
        return self._scanner_handler

    @scanner.setter
    def scanner(self, scan_handler: ScanHandler) -> None:
        self._scanner = scan_handler

    def crop(self, file_path) -> None:
        scan = self._scanner_handler.load(file_path)
        cropped = self._cropper.crop(scan)
        self._scanner_handler.save(cropped)


app = App()
print(app)
