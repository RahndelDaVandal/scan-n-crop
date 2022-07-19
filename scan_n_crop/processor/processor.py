# scan_n_crop.processor.processor
from abc import ABC, abstractmethod

import numpy as np


class Processor(ABC):
    @abstractmethod
    def process(img: np.ndarray) -> np.ndarray:
        pass
