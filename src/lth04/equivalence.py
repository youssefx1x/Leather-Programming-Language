from .runner import LTH04Runner


def state_values(state):
    values = getattr(
        state,
        "values",
        None,
    )

    if values is None:
        raise TypeError(
            "runtime result does not expose "
            "State.values"
        )

    return values


def equivalent(
    source,
    context=None,
):
    reference = LTH04Runner(
        use_cache=False
    )
    accelerated = LTH04Runner(
        use_cache=True
    )

    expected = state_values(
        reference.run(
            source,
            context=context,
        )
    )

    actual = state_values(
        accelerated.run(
            source,
            context=context,
        )
    )

    return expected == actual
