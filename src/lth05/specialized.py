import operator


_GENERIC = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
    "and": lambda a, b: a and b,
    "or": lambda a, b: a or b,
}


def generic_binary(op, left, right):
    if op not in _GENERIC:
        raise ValueError(f"unsupported binary operator: {op}")
    return _GENERIC[op](left, right)


def _specialized_function(op, left_type, right_type):
    if left_type is int and right_type is int:
        table = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "//": lambda a, b: a // b,
            "%": lambda a, b: a % b,
            "**": lambda a, b: a ** b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "<=": lambda a, b: a <= b,
            ">=": lambda a, b: a >= b,
        }
        if op in table:
            return table[op]

    if left_type is float and right_type is float:
        table = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "//": lambda a, b: a // b,
            "%": lambda a, b: a % b,
            "**": lambda a, b: a ** b,
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            "<": lambda a, b: a < b,
            ">": lambda a, b: a > b,
            "<=": lambda a, b: a <= b,
            ">=": lambda a, b: a >= b,
        }
        if op in table:
            return table[op]

    if left_type is str and right_type is str and op == "+":
        return lambda a, b: a + b

    if op in ("==", "!="):
        return _GENERIC[op]

    return _GENERIC.get(op)


class SpecializationCache:
    def __init__(self):
        self.cache = {}

    def execute(self, op, left, right, profile=None):
        key = (op, type(left), type(right))
        function = self.cache.get(key)

        if function is None:
            if profile is not None:
                profile.specialization_misses += 1

            function = _specialized_function(
                op,
                type(left),
                type(right),
            )

            if function is None:
                function = lambda a, b: generic_binary(op, a, b)

            self.cache[key] = function
        else:
            if profile is not None:
                profile.specialization_hits += 1

        return function(left, right)

    def size(self):
        return len(self.cache)
