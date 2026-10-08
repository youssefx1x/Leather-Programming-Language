from src.lth09.engine import AcceleratedEngine


def test_integer_fast_path():
    engine = AcceleratedEngine()
    assert engine.add(2, 3) == 5
    assert engine.stats.fast_path_hits == 1


def test_float_semantics():
    engine = AcceleratedEngine()
    assert abs(engine.add(2, 0.5) - 2.5) < 1e-12


def test_string_semantics():
    engine = AcceleratedEngine()
    assert engine.add("hello ", "world") == "hello world"


def test_cache_path():
    engine = AcceleratedEngine()

    first = engine.add(2.5, 0.5)
    second = engine.add(2.5, 0.5)

    assert first == 3.0
    assert second == 3.0
    assert engine.stats.cache_hits == 1


def test_bool_is_not_integer_fast_path():
    engine = AcceleratedEngine()

    result = engine.add(True, 2)

    assert result == 3
    assert engine.stats.fast_path_hits == 0
