REQUIRED_CONCEPTS = (
    "value",
    "rule",
    "base",
    "flow",
    "system",
)


def verify_source_shape(source):
    return {
        name: name in source
        for name in REQUIRED_CONCEPTS
    }


def is_valid_source(source):
    return all(verify_source_shape(source).values())
