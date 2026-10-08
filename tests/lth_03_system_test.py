from src.lth03.final_runner import LTH03FinalRunner


source = """
flow a {
    x = 10
}

flow b {
    y = x * 2
}

system Demo {
    use flow a
    use flow b
}

run system Demo
"""

state = LTH03FinalRunner().run(source)

assert state.values["x"] == 10
assert state.values["y"] == 20

print("LTH 0.3-H SYSTEM: PASS")
