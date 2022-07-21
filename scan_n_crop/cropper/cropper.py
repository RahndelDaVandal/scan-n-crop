# img_cropper.py
from typing import Protocol, TypeVar

IMG = TypeVar("IMG")


class Cropper(Protocol):
    def crop(self, img: IMG) -> list[IMG]:
        ...
