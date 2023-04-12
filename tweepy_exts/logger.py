from logging.handlers import RotatingFileHandler
import logging
import colorama
from typing import Iterable

colorama.init(autoreset=True)


max_filesize_in_mbs = 20
log_filename = "logs.log"
file_encoding = "UTF-8"

logging_format = logging.Formatter("%(levelname)s:[%(filename)s:%(lineno)s]:%(asctime)s: %(message)s")
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging_format)
file_handler = RotatingFileHandler(
    log_filename, mode="a", maxBytes=max_filesize_in_mbs * 1024 * 1024, backupCount=2, encoding=file_encoding,
    delay=False)
file_handler.setFormatter(logging_format)

logger.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
console_handler.setLevel(logging.DEBUG)

# logger.addHandler(console_handler)
logger.addHandler(file_handler)


class Console:
    @classmethod
    def j_args(cls, *args: Iterable[str]) -> str:
        j = [str(arg) for arg in args]
        return " ".join(j)

    @staticmethod
    def wait_for_shutdown() -> None:
        input(colorama.Fore.CYAN + colorama.Style.BRIGHT + "\n[#] Press Enter <- ")

    @staticmethod
    def error(*args: str, exc_info: bool = False, shutdown: bool = False) -> None:
        message = Console.j_args(*args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.RED + colorama.Style.BRIGHT + f"[-] {message}")
        if shutdown:
            return Console.wait_for_shutdown()

    @staticmethod
    def warn(*args: str, exc_info: bool = False, shutdown: bool = False) -> None:
        message = Console.j_args(args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"[*] {message}")
        if shutdown:
            return Console.wait_for_shutdown()

    @staticmethod
    def info(*args: str, exc_info: bool = False, shutdown: bool = False) -> None:
        message = Console.j_args(args)
        logger.debug(message, exc_info=exc_info)
        print(colorama.Fore.GREEN + colorama.Style.BRIGHT + f"[+] {message}")
        if shutdown:
            return Console.wait_for_shutdown()
