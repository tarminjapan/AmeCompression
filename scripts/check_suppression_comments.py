import re
import sys
from pathlib import Path

# Regex for common error suppression comments
# Python: type: ignore, noqa, pyright: ignore, ruff: noqa, pylint: disable
# JS/TS: // eslint-disable, // @ts-ignore, // @ts-nocheck, /* eslint-disable */
SUPPRESSION_PATTERNS = [
    re.compile(r"#\s*type:\s*ignore", re.IGNORECASE),
    re.compile(r"#\s*pyright:\s*ignore", re.IGNORECASE),
    re.compile(r"#\s*ruff:\s*noqa", re.IGNORECASE),
    re.compile(r"#\s*noqa", re.IGNORECASE),
    re.compile(r"#\s*pylint:\s*disable", re.IGNORECASE),
    re.compile(r"//\s*eslint-disable", re.IGNORECASE),
    re.compile(r"/\*\s*eslint-disable", re.IGNORECASE),
    re.compile(r"//\s*@ts-(ignore|nocheck)", re.IGNORECASE),
    re.compile(r"@ts-(ignore|nocheck)", re.IGNORECASE),
]

# Files/Directories to ignore
IGNORE_PATHS = [
    ".git",
    ".venv",
    "node_modules",
    "dist",
    "__pycache__",
    "uv.lock",
    "package-lock.json",
    "CONTRIBUTING.md",  # Allowed to mention them here
    "scripts/check_suppression_comments.py",  # Ignore self
]


def should_ignore(path: Path) -> bool:
    return any(ignore_path in str(path.as_posix()) for ignore_path in IGNORE_PATHS)


def check_file(file_path: Path) -> int:
    errors = 0
    try:
        content = file_path.read_text(encoding="utf-8")
        for i, line in enumerate(content.splitlines(), 1):
            for pattern in SUPPRESSION_PATTERNS:
                if pattern.search(line):
                    print(f"Error: Suppression comment found in {file_path}:{i}")
                    print(f"  Line: {line.strip()}")
                    errors += 1
                    break
    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or inaccessible files
        pass
    return errors


def main():
    total_errors = 0
    files_to_check = sys.argv[1:]

    if not files_to_check:
        # If no files provided, check current directory recursively
        for path in Path().rglob("*"):
            if path.is_file() and not should_ignore(path):
                total_errors += check_file(path)
    else:
        for file_arg in files_to_check:
            path = Path(file_arg)
            if path.is_file() and not should_ignore(path):
                total_errors += check_file(path)

    if total_errors > 0:
        print(f"\nTotal errors found: {total_errors}")
        sys.exit(1)
    else:
        print("No suppression comments found.")
        sys.exit(0)


if __name__ == "__main__":
    main()
