from _typeshed import Incomplete
from typing import Iterable

max_filesize_in_mbs: int
log_filename: str
file_encoding: str
logging_format: Incomplete
logger: Incomplete
console_handler: Incomplete
file_handler: Incomplete

class Console:
    @classmethod
    def j_args(cls, *args: Iterable[str]) -> str: ...
    @staticmethod
    def wait_for_shutdown() -> None: ...
    @staticmethod
    def error(*args: str, exc_info: bool = ..., shutdown: bool = ...) -> None: ...
    @staticmethod
    def warn(*args: str, exc_info: bool = ..., shutdown: bool = ...) -> None: ...
    @staticmethod
    def info(*args: str, exc_info: bool = ..., shutdown: bool = ...) -> None: ...
