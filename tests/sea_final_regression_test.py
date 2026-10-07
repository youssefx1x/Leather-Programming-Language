from src.sea_1_0 import build_final_report
from src.sea_final_benchmark import run_recursive_benchmark


def main():
    report = build_final_report()
    benchmark = run_recursive_benchmark(18)

    assert report.valid
    assert benchmark.valid

    print("SEA FINAL REGRESSION: PASS")


if __name__ == "__main__":
    main()
