from copy import deepcopy

from src.lth03.runner import LTH03Runner
from .runner import LTH05Runner


class EquivalenceError(AssertionError):
    pass


def run_equivalence(source, context=None):
    legacy = LTH03Runner().run(
        source,
        context=deepcopy(context),
    ).values

    result = LTH05Runner().run(
        source,
        context=deepcopy(context),
    )

    accelerated = dict(result.values)
    accelerated.pop("_lth05", None)

    if legacy != accelerated:
        raise EquivalenceError(
            "LTH 0.3 and LTH 0.5 results differ\n"
            f"LTH 0.3: {legacy}\n"
            f"LTH 0.5: {accelerated}"
        )

    return {
        "equivalent": True,
        "result": accelerated,
        "profile": result.profile.summary(),
    }
