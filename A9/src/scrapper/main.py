from .discover import discover
from .extract import extract

def main() -> None:
    extract(discover(3))