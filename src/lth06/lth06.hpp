#pragma once

#include <cstdint>
#include <functional>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <variant>
#include <utility>
#include <vector>

namespace leather::lth06 {

using Number = double;

struct Value {
    using Map = std::unordered_map<std::string, Value>;
    using List = std::vector<Value>;

    std::variant<
        std::monostate,
        bool,
        std::int64_t,
        Number,
        std::string,
        List,
        Map
    > data;

    Value() = default;
    Value(bool v) : data(v) {}
    Value(std::int64_t v) : data(v) {}
    Value(int v) : data(static_cast<std::int64_t>(v)) {}
    Value(Number v) : data(v) {}
    Value(const char* v) : data(std::string(v)) {}
    Value(std::string v) : data(std::move(v)) {}
    Value(List v) : data(std::move(v)) {}
    Value(Map v) : data(std::move(v)) {}

    bool truthy() const;
    std::string repr() const;
};

struct Instruction {
    enum class Op {
        NOP,
        CONST,
        LOAD,
        STORE,
        LOAD_MEMBER,
        LOAD_INDEX,
        BUILD_LIST,
        BUILD_MAP,
        UNARY,
        BINARY,
        CALL,
        JUMP_IF_FALSE,
        JUMP,
        POP,
        HALT
    };

    Op op;
    std::int64_t arg = 0;
    std::string text;

    Instruction(Op op_, std::int64_t arg_ = 0, std::string text_ = {})
        : op(op_), arg(arg_), text(std::move(text_)) {}
};

struct Program {
    std::vector<Instruction> instructions;
    std::vector<Value> constants;
    std::vector<std::string> names;
};

struct Profile {
    std::uint64_t instructions = 0;
    std::uint64_t max_stack = 0;
    std::unordered_map<std::string, std::uint64_t> opcodes;
    std::uint64_t specialization_hits = 0;
    std::uint64_t specialization_misses = 0;

    void record(const Instruction& instruction, std::size_t stack_size);
};

struct Result {
    std::unordered_map<std::string, Value> values;
    Profile profile;
};

class VM {
public:
    explicit VM(std::uint64_t step_limit = 1'000'000);

    Result run(
        const Program& program,
        const std::unordered_map<std::string, Value>& context = {}
    );

private:
    std::uint64_t step_limit_;

    Value binary(
        const std::string& op,
        const Value& left,
        const Value& right,
        Profile& profile
    );

    Value unary(
        const std::string& op,
        const Value& value
    );
};

class Compiler {
public:
    Program make_demo_program();
};

class Optimizer {
public:
    Program optimize(const Program& input);
};

class Runner {
public:
    explicit Runner(std::uint64_t step_limit = 1'000'000);

    Result run(
        const Program& program,
        const std::unordered_map<std::string, Value>& context = {}
    );

private:
    Optimizer optimizer_;
    VM vm_;
};

} // namespace leather::lth06
