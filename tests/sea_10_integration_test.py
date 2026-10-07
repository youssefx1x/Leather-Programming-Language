from src.sea_1_0 import build_final_report


def main():
    report = build_final_report()

    assert report.valid
    assert report.arithmetic_ok
    assert report.graph_ok
    assert report.optimization_ok
    assert report.benchmark_ok
    assert report.certificate_ok

    print("SEA 1.0 COMPLETE INTEGRATION: PASS")


if __name__ == "__main__":
    main()
