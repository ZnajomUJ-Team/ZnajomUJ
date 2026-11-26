import json
from pathlib import Path

from research.errors import FieldValidationError
from .validation import validate_questions


def load_questions(path: str | Path) -> tuple[list[dict], list[FieldValidationError]]:
    """Read UTF-8 JSON and return valid questions together with record errors.

    File errors and JSONDecodeError propagate. An invalid dataset envelope
    raises FieldValidationError. Invalid records are reported and filtered.
    """
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_questions(data)
