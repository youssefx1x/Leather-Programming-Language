#include "lth06.hpp"

#include <cassert>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace leather::lth06;

static Program arithmetic_program(
    const std::string& op
) {
    Program p;

    p.constants.emplace_back(std::int64_t(5));
    p.constants.emplace_back(std::int64_t(2));

    p.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BINARY, 0, op},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::HALT}
    };

    p.names = {"result"};
    return p;
}

static void test_arithmetic_semantics() {
    VM vm;

    {
        auto r = vm.run(arithmetic_program("/"));
        auto value = std::get<double>(r.values.at("result").data);
        assert(std::abs(value - 2.5) < 1e-12);
    }

    {
        auto r = vm.run(arithmetic_program("//"));
        assert(
            std::get<std::int64_t>(r.values.at("result").data) == 2
        );
    }

    {
        auto r = vm.run(arithmetic_program("%"));
        assert(
            std::get<std::int64_t>(r.values.at("result").data) == 1
        );
    }

    {
        Program p;
        p.constants.emplace_back(std::int64_t(2));
        p.constants.emplace_back(std::int64_t(3));
        p.names = {"result"};

        p.instructions = {
            {Instruction::Op::CONST, 0},
            {Instruction::Op::CONST, 1},
            {Instruction::Op::BINARY, 0, "**"},
            {Instruction::Op::STORE, 0},
            {Instruction::Op::HALT}
        };

        auto r = vm.run(p);
        auto value = std::get<double>(r.values.at("result").data);
        assert(std::abs(value - 8.0) < 1e-12);
    }
}

static void test_list_build_and_index() {
    Program p;
    p.names = {"result"};

    p.constants.emplace_back(std::int64_t(10));
    p.constants.emplace_back(std::int64_t(20));
    p.constants.emplace_back(std::int64_t(1));

    p.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BUILD_LIST, 2},
        {Instruction::Op::CONST, 2},
        {Instruction::Op::LOAD_INDEX},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::HALT}
    };

    VM vm;
    auto r = vm.run(p);

    assert(
        std::get<std::int64_t>(r.values.at("result").data) == 20
    );
}

static void test_map_build_and_index() {
    Program p;
    p.names = {"result"};

    p.constants.emplace_back(std::string("price"));
    p.constants.emplace_back(std::int64_t(150));
    p.constants.emplace_back(std::string("price"));

    p.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BUILD_MAP, 1},
        {Instruction::Op::CONST, 2},
        {Instruction::Op::LOAD_INDEX},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::HALT}
    };

    VM vm;
    auto r = vm.run(p);

    assert(
        std::get<std::int64_t>(r.values.at("result").data) == 150
    );
}

static void test_builtins() {
    VM vm;

    {
        Program p;
        p.names = {"result"};
        p.constants.emplace_back(std::string("Leather"));

        p.instructions = {
            {Instruction::Op::CONST, 0},
            {Instruction::Op::CALL, 1, "len"},
            {Instruction::Op::STORE, 0},
            {Instruction::Op::HALT}
        };

        auto r = vm.run(p);
        assert(
            std::get<std::int64_t>(r.values.at("result").data) == 7
        );
    }

    {
        Program p;
        p.names = {"result"};
        p.constants.emplace_back(std::int64_t(0));

        p.instructions = {
            {Instruction::Op::CONST, 0},
            {Instruction::Op::CALL, 1, "bool"},
            {Instruction::Op::STORE, 0},
            {Instruction::Op::HALT}
        };

        auto r = vm.run(p);
        assert(
            std::get<bool>(r.values.at("result").data) == false
        );
    }
}

static void test_structural_equality() {
    Program p;
    p.names = {"result"};

    p.constants.emplace_back(std::int64_t(1));
    p.constants.emplace_back(std::int64_t(2));

    p.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BUILD_LIST, 2},
        {Instruction::Op::CONST, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BUILD_LIST, 2},
        {Instruction::Op::BINARY, 0, "=="},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::HALT}
    };

    VM vm;
    auto r = vm.run(p);

    assert(
        std::get<bool>(r.values.at("result").data) == true
    );
}

static void test_error_paths() {
    VM vm;

    {
        Program p;
        p.instructions = {
            {Instruction::Op::BINARY, 0, "+"},
            {Instruction::Op::HALT}
        };

        bool failed = false;

        try {
            vm.run(p);
        } catch (const std::runtime_error&) {
            failed = true;
        }

        assert(failed);
    }

    {
        Program p;
        p.constants.emplace_back(std::int64_t(1));
        p.constants.emplace_back(std::int64_t(0));
        p.instructions = {
            {Instruction::Op::CONST, 0},
            {Instruction::Op::CONST, 1},
            {Instruction::Op::BINARY, 0, "/"},
            {Instruction::Op::HALT}
        };

        bool failed = false;

        try {
            vm.run(p);
        } catch (const std::runtime_error&) {
            failed = true;
        }

        assert(failed);
    }

    {
        Program p;
        p.constants.emplace_back(std::int64_t(1));
        p.instructions = {
            {Instruction::Op::CONST, 0},
            {Instruction::Op::JUMP, 0}
        };

        bool failed = false;

        try {
            VM limited(5);
            limited.run(p);
        } catch (const std::runtime_error&) {
            failed = true;
        }

        assert(failed);
    }
}

int main() {
    test_arithmetic_semantics();
    test_list_build_and_index();
    test_map_build_and_index();
    test_builtins();
    test_structural_equality();
    test_error_paths();

    std::cout << "LTH 0.6 EXTENDED TESTS: PASS\n";
    return 0;
}
