#include "../../src/lth06/lth06.hpp"

#include <cassert>
#include <cmath>
#include <iostream>

using namespace leather::lth06;

static void test_value_truthy() {
    assert(Value(false).truthy() == false);
    assert(Value(true).truthy() == true);
    assert(Value(0).truthy() == false);
    assert(Value(7).truthy() == true);
}

static void test_arithmetic() {
    Program program;

    program.names = {"price"};
    program.constants = {
        Value(150.5),
        Value(0.9)
    };

    program.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::LOAD, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BINARY, 0, "*"},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::HALT}
    };

    VM vm;
    auto result = vm.run(program);

    const auto& price = result.values.at("price").data;
    const auto* value = std::get_if<double>(&price);

    assert(value != nullptr);
    assert(std::fabs(*value - 135.45) < 1e-9);
}

static void test_context_is_not_output() {
    Program program;

    program.names = {"customer", "price"};
    program.constants = {Value(100.0), Value(0.9)};

    program.instructions = {
        {Instruction::Op::LOAD, 0},
        {Instruction::Op::LOAD_MEMBER, 0, "vip"},
        {Instruction::Op::JUMP_IF_FALSE, 7},
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BINARY, 0, "*"},
        {Instruction::Op::STORE, 1},
        {Instruction::Op::HALT}
    };

    Value::Map customer{{"vip", Value(true)}};

    VM vm;
    auto result = vm.run(
        program,
        {{"customer", Value(customer)}}
    );

    assert(result.values.count("customer") == 0);
    assert(result.values.count("price") == 1);
}

static void test_specialization() {
    Program program;

    program.constants = {
        Value(2),
        Value(3)
    };

    program.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BINARY, 0, "+"},
        {Instruction::Op::POP},
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BINARY, 0, "+"},
        {Instruction::Op::POP},
        {Instruction::Op::HALT}
    };

    VM vm;
    auto result = vm.run(program);

    assert(result.profile.specialization_hits >= 2);
}

int main() {
    test_value_truthy();
    test_arithmetic();
    test_context_is_not_output();
    test_specialization();

    std::cout << "LTH 0.6 C++ TESTS: PASS\n";
    return 0;
}
