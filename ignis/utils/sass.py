import os
import subprocess
from ignis.logging import logger

TEMP_DIR = "/tmp/ignis"
COMPILED_CSS = f"{TEMP_DIR}/compiled.css"
os.makedirs(TEMP_DIR, exist_ok=True)


class DartSassNotFoundError(Exception):
    """
    Raised when Dart Sass is not found.
    """

    def __init__(self, *args: object) -> None:
        super().__init__(
            "Dart Sass not found! To compile SCSS/SASS, install dart-sass", *args
        )


def compile_file(path: str) -> str:
    result = subprocess.run(["sass", path, COMPILED_CSS], capture_output=True)

    if result.returncode != 0:
        logger.error(f"SASS compilation error:\n{result.stderr.decode()}")
        return

    with open(COMPILED_CSS) as file:
        return file.read()


def compile_string(string: str) -> str:
    process = subprocess.Popen(
        ["sass", "--stdin"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=string.encode())

    if process.returncode != 0:
        logger.error(f"SASS compilation error:\n{stderr.decode()}")
        return
    else:
        return stdout.decode()


def sass_compile(path: str = None, string: str = None) -> str:
    """
    Compile a SASS/SCSS file or string.
    Requires ``dart-sass``.

    Args:
        path (``str``, optional): The path to the SASS/SCSS file.
        string (``str``, optional): A string with SASS/SCSS style.

    Raises:
        TypeError: If neither of the arguments is provided.
    """
    if not os.path.exists("/bin/sass"):
        raise DartSassNotFoundError()

    if string:
        return compile_string(string)

    elif path:
        return compile_file(path)

    else:
        raise TypeError("sass_compile() requires at least one positional argument")
