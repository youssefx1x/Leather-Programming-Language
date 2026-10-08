from src.lth03.final_runner import LTH03FinalRunner
from src.lth03.flow import FlowError
from src.lth03.system_syntax import SystemSyntaxError


try:
    LTH03FinalRunner().run(
        """
        flow a {
            x = 1
        }

        system Broken {
            use flow missing
        }

        run system Broken
        """
    )
except FlowError:
    pass
except SystemSyntaxError:
    pass
else:
    raise AssertionError(
        "unknown flow must fail"
    )


try:
    LTH03FinalRunner().run(
        """
        flow a {
            run flow b
        }

        flow b {
            run flow a
        }

        run flow a
        """
    )
except FlowError:
    pass
else:
    raise AssertionError(
        "flow cycle must fail"
    )


print("LTH 0.3-H SYSTEM ERRORS: PASS")
