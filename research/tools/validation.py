from collections import Counter

from research.errors import FieldValidationError


def _validate_answer(
    answer: object,
    duplicate_ids: set[str],
    field: str,
) -> None:
    """Raise the first validation error for one answer."""
    if not isinstance(answer, dict):
        raise FieldValidationError(
            field, answer, "Answer must be a dictionary"
        )

    for name in ("id", "text"):
        if name not in answer:
            raise FieldValidationError(
                f"{field}.{name}", None, "Missing required field"
            )
        value = answer[name]
        if not isinstance(value, str) or not value.strip():
            raise FieldValidationError(
                f"{field}.{name}", value, "Must be a non-empty string"
            )

    if answer["id"] in duplicate_ids:
        raise FieldValidationError(
            f"{field}.id", answer["id"], "Repeated answer id"
        )
        

def _validate_question(
    question: object,
    duplicate_ids: set[str],
    errors: list[FieldValidationError],
    field: str,
) -> list[dict]:
    """Return valid answers, or raise if the question cannot be compared."""
    if not isinstance(question, dict):
        raise FieldValidationError(
            field, question, "Question must be a dictionary"
        )

    for name in ("id", "text", "answers"):
        if name not in question:
            raise FieldValidationError(
                f"{field}.{name}", None, "Missing required field"
            )

    for name in ("id", "text"):
        value = question[name]
        if not isinstance(value, str) or not value.strip():
            raise FieldValidationError(
                f"{field}.{name}", value, "Must be a non-empty string"
            )

    if question["id"] in duplicate_ids:
        raise FieldValidationError(
            f"{field}.id", question["id"], "Repeated question id"
        )

    answers = question["answers"]
    if not isinstance(answers, list):
        raise FieldValidationError(
            f"{field}.answers", answers, "Answers must be a list"
        )

    id_counts = Counter(
        answer["id"]
        for answer in answers
        if isinstance(answer, dict) and isinstance(answer.get("id"), str)
    )
    duplicate_answer_ids = {
        answer_id for answer_id, count in id_counts.items() if count > 1
    }
    valid_answers = []
    for index, answer in enumerate(answers):
        try:
            _validate_answer(answer, duplicate_answer_ids, f"{field}.answers[{index}]")
        except FieldValidationError as error:
            errors.append(error)
        else:
            valid_answers.append(answer)

    if len(valid_answers) < 2:
        raise FieldValidationError(
            f"{field}.answers", answers, "Each question needs at least 2 valid answers"
        )

    return valid_answers


def validate_questions(data: object) -> tuple[list[dict], list[FieldValidationError]]:
    """Return valid questions and record errors; raise for an invalid root structure."""
    if not isinstance(data, dict):
        raise FieldValidationError(
            "data", data, "Data must be a dictionary"
        )
    if "questions" not in data:
        raise FieldValidationError(
            "questions", None, "Missing required field"
        )

    questions = data["questions"]
    if not isinstance(questions, list) or not questions:
        raise FieldValidationError(
            "questions", questions, "Questions must be a non-empty list"
        )

    errors = []
    id_counts = Counter(
        question["id"]
        for question in questions
        if isinstance(question, dict) and isinstance(question.get("id"), str)
    )
    duplicate_question_ids = {
        question_id for question_id, count in id_counts.items() if count > 1
    }
    valid_questions = []
    for index, question in enumerate(questions):
        try:
            valid_answers = _validate_question(question, duplicate_question_ids, errors, f"questions[{index}]")
        except FieldValidationError as error:
            errors.append(error)
        else:
            valid_question = question.copy()
            valid_question["answers"] = valid_answers
            valid_questions.append(valid_question)

    return valid_questions, errors
