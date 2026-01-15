from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    """Base class for all language parsers"""

    @abstractmethod
    def parse(self, code: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_ir(self) -> Dict[str, Any]:
        pass
