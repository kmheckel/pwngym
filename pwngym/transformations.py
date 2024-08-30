from utils import winpath_escaper

def escape_windows_paths(text: str) -> str:
    if "meterpreter" in text:
        return winpath_escaper(text)