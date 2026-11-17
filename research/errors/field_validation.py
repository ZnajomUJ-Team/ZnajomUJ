class FieldValidationError(ValueError):
    """A field does not satisfy the expected data contract."""

    def __init__(self, field: str, value: object, reason: str):
        super().__init__(f"{field}={value!r}: {reason}")
        self.field = field
        self.value = value
        self.reason = reason
