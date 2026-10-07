class UnifiedValueNormalizer:
    """Convert semantic values into LTH IR primitive values."""

    def normalize(self, value):
        if hasattr(value, "kind") and hasattr(value, "value"):
            return value.value

        return value

    def kind(self, value):
        if hasattr(value, "kind") and hasattr(value, "value"):
            return value.kind

        if isinstance(value, bool):
            return "boolean"

        if isinstance(value, (int, float)):
            return "number"

        if isinstance(value, str):
            return "string"

        return "unknown"
