from importlib import import_module


def discover():
    result = {}

    candidates = {
        "lexer": (
            "src.lexer.lexer",
            "src.lexer",
        ),
        "parser": (
            "src.parser.parser",
            "src.parser",
        ),
        "semantic": (
            "src.semantic",
            "src.semantic.analyzer",
            "src.semantic.semantic_analyzer",
        ),
        "ir": (
            "src.ir",
            "src.compiler.ir",
            "src.compiler",
        ),
        "runtime": (
            "src.runtime",
            "src.runtime.unified",
        ),
    }

    for component, modules in candidates.items():
        found = None

        for name in modules:
            try:
                module = import_module(name)
                found = module
                break
            except ImportError:
                continue

        result[component] = found

    return result
