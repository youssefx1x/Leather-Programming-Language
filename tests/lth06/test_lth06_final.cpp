#include "lth06.hpp"

#include <cassert>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

using namespace leather::lth06;

static std::string run_binary(
    const Value& left,
    const Value& right,
    const std::string& op
) {
    Program program;
    program.constants = {left, right};
    program.names = {"result"};

    program.instructions = {
        Instruction(Instruction::Op::CONST, 0),
        Instruction(Instruction::Op::CONST, 1),
        Instruction(Instruction::Op::BINARY, 0, op),
        Instruction(Instruction::Op::STORE, 0),
        Instruction(Instruction::Op::HALT),
    };

    VM vm;
    const auto result = vm.run(program);

    const auto it = result.values.find("result");
    assert(it != result.values.end());
    return it->second.repr();
}

static void test_python_floor_semantics() {
    assert(run_binary(Value(std::int64_t(-5)), Value(std::int64_t(2)), "//") == "-3");
    assert(run_binary(Value(std::int64_t(-5)), Value(std::int64_t(2)), "%") == "1");
    assert(run_binary(Value(std::int64_t(5)), Value(std::int64_t(-2)), "//") == "-3");
    assert(run_binary(Value(std::int64_t(5)), Value(std::int64_t(-2)), "%") == "-1");
    assert(run_binary(Value(std::int64_t(5)), Value(std::int64_t(2)), "//") == "2");
    assert(run_binary(Value(std::int64_t(5)), Value(std::int64_t(2)), "%") == "1");
}

static void test_optimizer_preserves_result() {
    Program program;
    program.constants = {
        Value(std::int64_t(2)),
        Value(std::int64_t(3)),
    };
    program.names = {"x"};

    program.instructions = {
        Instruction(Instruction::Op::NOP),
        Instruction(Instruction::Op::CONST, 0),
        Instruction(Instruction::Op::CONST, 1),
        Instruction(Instruction::Op::BINARY, 0, "+"),
        Instruction(Instruction::Op::STORE, 0),
        Instruction(Instruction::Op::HALT),
    };

    VM vm;
    Optimizer optimizer;

    const auto before = vm.run(program);
    const auto optimized = optimizer.optimize(program);
    const auto after = vm.run(optimized);

    assert(optimized.instructions.size() < program.instructions.size());

    for (const auto& instruction : optimized.instructions) {
        assert(instruction.op != Instruction::Op::NOP);
    }

    assert(before.values.at("x").repr() == "5");
    assert(after.values.at("x").repr() == "5");
}

static void test_optimizer_does_not_touch_control_flow() {
    Program program;
    program.constants = {
        Value(true),
    };

    program.instructions = {
        Instruction(Instruction::Op::CONST, 0),
        Instruction(Instruction::Op::JUMP_IF_FALSE, 3),
        Instruction(Instruction::Op::NOP),
        Instruction(Instruction::Op::HALT),
    };

    Optimizer optimizer;
    const auto optimized = optimizer.optimize(program);

    assert(optimized.instructions.size() == program.instructions.size());
}

static void test_benchmark_path() {
    Compiler compiler;
    Runner runner;

    const auto program = compiler.make_demo_program();

    const auto start = std::chrono::steady_clock::now();

    Result last;
    for (int i = 0; i < 20000; ++i) {
        last = runner.run(program);
    }

    const auto end = std::chrono::steady_clock::now();
    const auto elapsed_us =
        std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();

    assert(!last.profile.opcodes.empty());
    assert(last.profile.instructions > 0);

    std::cout << "BENCHMARK ITERATIONS: 20000\n";
    std::cout << "BENCHMARK TIME US: " << elapsed_us << "\n";
}

int main() {
    test_python_floor_semantics();
    test_optimizer_preserves_result();
    test_optimizer_does_not_touch_control_flow();
    test_benchmark_path();

    std::cout << "LTH 0.6 FINAL TESTS: PASS\n";
    return 0;
}
