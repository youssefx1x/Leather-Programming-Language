#include "lth06.hpp"

#include <cmath>
#include <sstream>
#include <utility>

namespace leather::lth06 {

bool Value::truthy() const {
    if (std::holds_alternative<std::monostate>(data))
        return false;

    if (auto p = std::get_if<bool>(&data))
        return *p;

    if (auto p = std::get_if<std::int64_t>(&data))
        return *p != 0;

    if (auto p = std::get_if<Number>(&data))
        return *p != 0.0;

    if (auto p = std::get_if<std::string>(&data))
        return !p->empty();

    if (auto p = std::get_if<List>(&data))
        return !p->empty();

    if (auto p = std::get_if<Map>(&data))
        return !p->empty();

    return false;
}

std::string Value::repr() const {
    if (std::holds_alternative<std::monostate>(data))
        return "null";

    if (auto p = std::get_if<bool>(&data))
        return *p ? "true" : "false";

    if (auto p = std::get_if<std::int64_t>(&data))
        return std::to_string(*p);

    if (auto p = std::get_if<Number>(&data)) {
        std::ostringstream out;
        out << *p;
        return out.str();
    }

    if (auto p = std::get_if<std::string>(&data))
        return "\"" + *p + "\"";

    if (auto p = std::get_if<List>(&data)) {
        std::string out = "[";
        for (std::size_t i = 0; i < p->size(); ++i) {
            if (i) out += ", ";
            out += (*p)[i].repr();
        }
        return out + "]";
    }

    const auto& map = std::get<Map>(data);
    std::string out = "{";
    bool first = true;
    for (const auto& [key, value] : map) {
        if (!first) out += ", ";
        first = false;
        out += key + ": " + value.repr();
    }
    return out + "}";
}

void Profile::record(
    const Instruction& instruction,
    std::size_t stack_size
) {
    ++instructions;

    if (stack_size > max_stack)
        max_stack = stack_size;

    std::string name;

    switch (instruction.op) {
        case Instruction::Op::NOP: name = "NOP"; break;
        case Instruction::Op::CONST: name = "CONST"; break;
        case Instruction::Op::LOAD: name = "LOAD"; break;
        case Instruction::Op::STORE: name = "STORE"; break;
        case Instruction::Op::LOAD_MEMBER: name = "LOAD_MEMBER"; break;
        case Instruction::Op::LOAD_INDEX: name = "LOAD_INDEX"; break;
        case Instruction::Op::BUILD_LIST: name = "BUILD_LIST"; break;
        case Instruction::Op::BUILD_MAP: name = "BUILD_MAP"; break;
        case Instruction::Op::UNARY: name = "UNARY"; break;
        case Instruction::Op::BINARY: name = "BINARY"; break;
        case Instruction::Op::CALL: name = "CALL"; break;
        case Instruction::Op::JUMP_IF_FALSE: name = "JUMP_IF_FALSE"; break;
        case Instruction::Op::JUMP: name = "JUMP"; break;
        case Instruction::Op::POP: name = "POP"; break;
        case Instruction::Op::HALT: name = "HALT"; break;
    }

    ++opcodes[name];
}

Value VM::unary(
    const std::string& op,
    const Value& value
) {
    if (op == "not" || op == "!")
        return Value(!value.truthy());

    if (op == "+") {
        if (auto p = std::get_if<std::int64_t>(&value.data))
            return Value(*p);
        if (auto p = std::get_if<Number>(&value.data))
            return Value(*p);
    }

    if (op == "-") {
        if (auto p = std::get_if<std::int64_t>(&value.data))
            return Value(-*p);
        if (auto p = std::get_if<Number>(&value.data))
            return Value(-*p);
    }

    throw std::runtime_error("unsupported unary operator: " + op);
}

namespace {

bool value_equal(const Value& left, const Value& right) {
    if (left.data.index() != right.data.index()) {
        const auto li = std::get_if<std::int64_t>(&left.data);
        const auto ri = std::get_if<std::int64_t>(&right.data);
        const auto lf = std::get_if<Number>(&left.data);
        const auto rf = std::get_if<Number>(&right.data);

        if ((li || lf) && (ri || rf)) {
            const double l = li
                ? static_cast<double>(*li)
                : *lf;
            const double r = ri
                ? static_cast<double>(*ri)
                : *rf;
            return l == r;
        }

        return false;
    }

    if (std::holds_alternative<std::monostate>(left.data))
        return true;

    if (const auto l = std::get_if<bool>(&left.data))
        return *l == std::get<bool>(right.data);

    if (const auto l = std::get_if<std::int64_t>(&left.data))
        return *l == std::get<std::int64_t>(right.data);

    if (const auto l = std::get_if<Number>(&left.data))
        return *l == std::get<Number>(right.data);

    if (const auto l = std::get_if<std::string>(&left.data))
        return *l == std::get<std::string>(right.data);

    if (const auto l = std::get_if<Value::List>(&left.data)) {
        const auto& r = std::get<Value::List>(right.data);
        if (l->size() != r.size())
            return false;

        for (std::size_t i = 0; i < l->size(); ++i) {
            if (!value_equal((*l)[i], r[i]))
                return false;
        }

        return true;
    }

    const auto& l = std::get<Value::Map>(left.data);
    const auto& r = std::get<Value::Map>(right.data);

    if (l.size() != r.size())
        return false;

    for (const auto& [key, value] : l) {
        const auto it = r.find(key);
        if (it == r.end() || !value_equal(value, it->second))
            return false;
    }

    return true;
}

} // namespace

Value VM::binary(
    const std::string& op,
    const Value& left,
    const Value& right,
    Profile& profile
) {
    const auto li = std::get_if<std::int64_t>(&left.data);
    const auto ri = std::get_if<std::int64_t>(&right.data);
    const auto lf = std::get_if<Number>(&left.data);
    const auto rf = std::get_if<Number>(&right.data);

    if (li && ri) {
        ++profile.specialization_hits;

        if (op == "+") return Value(*li + *ri);
        if (op == "-") return Value(*li - *ri);
        if (op == "*") return Value(*li * *ri);

        if (op == "/") {
            if (*ri == 0)
                throw std::runtime_error("division by zero");
            return Value(
                static_cast<double>(*li) / static_cast<double>(*ri)
            );
        }

        if (op == "//" || op == "%") {
            if (*ri == 0)
                throw std::runtime_error(
                    op == "//" ? "division by zero" : "modulo by zero"
                );

            std::int64_t quotient = *li / *ri;
            std::int64_t remainder = *li % *ri;

            // Python floor-division semantics:
            // -5 // 2 == -3
            // -5 % 2  == 1
            if (remainder != 0 && ((remainder < 0) != (*ri < 0))) {
                --quotient;
                remainder = *li - quotient * *ri;
            }

            if (op == "//")
                return Value(quotient);

            return Value(remainder);
        }

        if (op == "**")
            return Value(std::pow(
                static_cast<double>(*li),
                static_cast<double>(*ri)
            ));

        if (op == "==") return Value(*li == *ri);
        if (op == "!=") return Value(*li != *ri);
        if (op == "<") return Value(*li < *ri);
        if (op == ">") return Value(*li > *ri);
        if (op == "<=") return Value(*li <= *ri);
        if (op == ">=") return Value(*li >= *ri);
    }

    if ((li || lf) && (ri || rf)) {
        ++profile.specialization_hits;

        const double l = li ? static_cast<double>(*li) : *lf;
        const double r = ri ? static_cast<double>(*ri) : *rf;

        if (op == "+") return Value(l + r);
        if (op == "-") return Value(l - r);
        if (op == "*") return Value(l * r);

        if (op == "/") {
            if (r == 0.0)
                throw std::runtime_error("division by zero");
            return Value(l / r);
        }

        if (op == "//") {
            if (r == 0.0)
                throw std::runtime_error("division by zero");
            return Value(std::floor(l / r));
        }

        if (op == "%") {
            if (r == 0.0)
                throw std::runtime_error("modulo by zero");
            return Value(std::fmod(l, r));
        }

        if (op == "**")
            return Value(std::pow(l, r));

        if (op == "==") return Value(l == r);
        if (op == "!=") return Value(l != r);
        if (op == "<") return Value(l < r);
        if (op == ">") return Value(l > r);
        if (op == "<=") return Value(l <= r);
        if (op == ">=") return Value(l >= r);
    }

    if (auto ls = std::get_if<std::string>(&left.data)) {
        if (auto rs = std::get_if<std::string>(&right.data)) {
            ++profile.specialization_hits;

            if (op == "+") return Value(*ls + *rs);
            if (op == "==") return Value(*ls == *rs);
            if (op == "!=") return Value(*ls != *rs);
            if (op == "<") return Value(*ls < *rs);
            if (op == ">") return Value(*ls > *rs);
            if (op == "<=") return Value(*ls <= *rs);
            if (op == ">=") return Value(*ls >= *rs);
        }
    }

    ++profile.specialization_misses;

    if (op == "and")
        return Value(left.truthy() && right.truthy());

    if (op == "or")
        return Value(left.truthy() || right.truthy());

    if (op == "==")
        return Value(value_equal(left, right));

    if (op == "!=")
        return Value(!value_equal(left, right));

    throw std::runtime_error("unsupported binary operator: " + op);
}

VM::VM(std::uint64_t step_limit)
    : step_limit_(step_limit) {}

Result VM::run(
    const Program& program,
    const std::unordered_map<std::string, Value>& context
) {
    std::unordered_map<std::string, Value> values;
    std::vector<Value> stack;

    auto name_at = [&](std::int64_t index) -> const std::string& {
        if (index < 0 ||
            static_cast<std::size_t>(index) >= program.names.size()) {
            throw std::runtime_error("invalid name index");
        }
        return program.names[static_cast<std::size_t>(index)];
    };

    auto constant_at = [&](std::int64_t index) -> const Value& {
        if (index < 0 ||
            static_cast<std::size_t>(index) >= program.constants.size()) {
            throw std::runtime_error("invalid constant index");
        }
        return program.constants[static_cast<std::size_t>(index)];
    };

    Profile profile;
    std::size_t ip = 0;
    std::uint64_t steps = 0;

    while (ip < program.instructions.size()) {
        if (steps++ >= step_limit_)
            throw std::runtime_error("step limit exceeded");

        const Instruction& ins = program.instructions[ip];
        profile.record(ins, stack.size());

        switch (ins.op) {
            case Instruction::Op::NOP:
                ++ip;
                break;

            case Instruction::Op::CONST:
                stack.push_back(constant_at(ins.arg));
                ++ip;
                break;

            case Instruction::Op::LOAD: {
                const std::string& name = name_at(ins.arg);

                auto own = values.find(name);
                if (own != values.end()) {
                    stack.push_back(own->second);
                    ++ip;
                    break;
                }

                auto external = context.find(name);
                if (external != context.end()) {
                    stack.push_back(external->second);
                    ++ip;
                    break;
                }

                throw std::runtime_error("unknown variable: " + name);
            }

            case Instruction::Op::STORE: {
                if (stack.empty())
                    throw std::runtime_error("empty stack on STORE");

                values[name_at(ins.arg)] = stack.back();
                stack.pop_back();
                ++ip;
                break;
            }

            case Instruction::Op::LOAD_MEMBER: {
                if (stack.empty())
                    throw std::runtime_error("empty stack on LOAD_MEMBER");

                Value object = stack.back();
                stack.pop_back();

                auto map = std::get_if<Value::Map>(&object.data);
                if (!map)
                    throw std::runtime_error("member access requires map");

                auto it = map->find(ins.text);
                if (it == map->end())
                    throw std::runtime_error("member not found: " + ins.text);

                stack.push_back(it->second);
                ++ip;
                break;
            }

            case Instruction::Op::LOAD_INDEX: {
                if (stack.size() < 2)
                    throw std::runtime_error(
                        "stack underflow on LOAD_INDEX"
                    );

                Value index = stack.back();
                stack.pop_back();

                Value object = stack.back();
                stack.pop_back();

                if (auto list = std::get_if<Value::List>(&object.data)) {
                    auto position = std::get_if<std::int64_t>(&index.data);
                    if (!position)
                        throw std::runtime_error(
                            "list index must be integer"
                        );

                    if (*position < 0 ||
                        static_cast<std::size_t>(*position) >= list->size()) {
                        throw std::runtime_error("list index out of range");
                    }

                    stack.push_back(
                        (*list)[static_cast<std::size_t>(*position)]
                    );
                    ++ip;
                    break;
                }

                if (auto map = std::get_if<Value::Map>(&object.data)) {
                    auto key = std::get_if<std::string>(&index.data);
                    if (!key)
                        throw std::runtime_error(
                            "map index must be string"
                        );

                    auto it = map->find(*key);
                    if (it == map->end())
                        throw std::runtime_error("map key not found");

                    stack.push_back(it->second);
                    ++ip;
                    break;
                }

                throw std::runtime_error(
                    "index access requires list or map"
                );
            }

            case Instruction::Op::BUILD_LIST: {
                if (ins.arg < 0 ||
                    static_cast<std::size_t>(ins.arg) > stack.size()) {
                    throw std::runtime_error(
                        "invalid BUILD_LIST count"
                    );
                }

                const std::size_t count =
                    static_cast<std::size_t>(ins.arg);

                Value::List list(count);

                for (std::size_t i = 0; i < count; ++i) {
                    list[count - 1 - i] = stack.back();
                    stack.pop_back();
                }

                stack.push_back(Value(std::move(list)));
                ++ip;
                break;
            }

            case Instruction::Op::BUILD_MAP: {
                if (ins.arg < 0)
                    throw std::runtime_error("invalid BUILD_MAP count");

                const std::size_t count =
                    static_cast<std::size_t>(ins.arg);

                if (stack.size() < count * 2)
                    throw std::runtime_error(
                        "stack underflow on BUILD_MAP"
                    );

                Value::Map map;

                for (std::size_t i = 0; i < count; ++i) {
                    Value value = stack.back();
                    stack.pop_back();

                    Value key = stack.back();
                    stack.pop_back();

                    auto key_string =
                        std::get_if<std::string>(&key.data);

                    if (!key_string)
                        throw std::runtime_error(
                            "map key must be string"
                        );

                    map[*key_string] = std::move(value);
                }

                stack.push_back(Value(std::move(map)));
                ++ip;
                break;
            }

            case Instruction::Op::CALL: {
                if (ins.arg < 0 ||
                    static_cast<std::size_t>(ins.arg) > stack.size()) {
                    throw std::runtime_error("invalid CALL arity");
                }

                const std::size_t argc =
                    static_cast<std::size_t>(ins.arg);

                if (stack.size() < argc)
                    throw std::runtime_error(
                        "stack underflow on CALL"
                    );

                std::vector<Value> args(argc);

                for (std::size_t i = 0; i < argc; ++i) {
                    args[argc - 1 - i] = std::move(stack.back());
                    stack.pop_back();
                }

                if (ins.text == "len") {
                    if (argc != 1)
                        throw std::runtime_error(
                            "len expects one argument"
                        );

                    const Value& value = args[0];

                    if (const auto list =
                            std::get_if<Value::List>(&value.data))
                        stack.push_back(
                            Value(static_cast<std::int64_t>(list->size()))
                        );
                    else if (const auto map =
                                 std::get_if<Value::Map>(&value.data))
                        stack.push_back(
                            Value(static_cast<std::int64_t>(map->size()))
                        );
                    else if (const auto text =
                                 std::get_if<std::string>(&value.data))
                        stack.push_back(
                            Value(static_cast<std::int64_t>(text->size()))
                        );
                    else
                        throw std::runtime_error(
                            "len unsupported for value"
                        );

                    ++ip;
                    break;
                }

                if (ins.text == "bool") {
                    if (argc != 1)
                        throw std::runtime_error(
                            "bool expects one argument"
                        );

                    stack.push_back(Value(args[0].truthy()));
                    ++ip;
                    break;
                }

                if (ins.text == "repr") {
                    if (argc != 1)
                        throw std::runtime_error(
                            "repr expects one argument"
                        );

                    stack.push_back(Value(args[0].repr()));
                    ++ip;
                    break;
                }

                throw std::runtime_error(
                    "unknown builtin: " + ins.text
                );
            }

            case Instruction::Op::BINARY: {
                if (stack.size() < 2)
                    throw std::runtime_error("stack underflow on BINARY");

                Value right = stack.back();
                stack.pop_back();

                Value left = stack.back();
                stack.pop_back();

                stack.push_back(binary(ins.text, left, right, profile));
                ++ip;
                break;
            }

            case Instruction::Op::UNARY: {
                if (stack.empty())
                    throw std::runtime_error("stack underflow on UNARY");

                Value value = stack.back();
                stack.pop_back();
                stack.push_back(unary(ins.text, value));
                ++ip;
                break;
            }

            case Instruction::Op::JUMP_IF_FALSE: {
                if (stack.empty())
                    throw std::runtime_error(
                        "stack underflow on JUMP_IF_FALSE"
                    );

                Value condition = stack.back();
                stack.pop_back();

                if (!condition.truthy())
                    ip = static_cast<std::size_t>(ins.arg);
                else
                    ++ip;

                break;
            }

            case Instruction::Op::JUMP:
                ip = static_cast<std::size_t>(ins.arg);
                break;

            case Instruction::Op::POP:
                if (stack.empty())
                    throw std::runtime_error("stack underflow on POP");
                stack.pop_back();
                ++ip;
                break;

            case Instruction::Op::HALT:
                return Result{std::move(values), profile};

            default:
                throw std::runtime_error("opcode not implemented in 0.6");
        }
    }

    return Result{std::move(values), profile};
}

Program Compiler::make_demo_program() {
    Program program;

    program.names = {"price"};

    program.constants.emplace_back(Number(150.5));
    program.constants.emplace_back(Number(0.9));

    program.instructions = {
        {Instruction::Op::CONST, 0},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::LOAD, 0},
        {Instruction::Op::CONST, 1},
        {Instruction::Op::BINARY, 2, "*"},
        {Instruction::Op::STORE, 0},
        {Instruction::Op::HALT, 0}
    };

    return program;
}

Program Optimizer::optimize(const Program& input) {
    Program out = input;

    bool has_control_flow = false;
    for (const auto& instruction : input.instructions) {
        if (instruction.op == Instruction::Op::JUMP ||
            instruction.op == Instruction::Op::JUMP_IF_FALSE) {
            has_control_flow = true;
            break;
        }
    }

    // Keep jump-bearing programs structurally unchanged in 0.6.
    // This makes the optimizer conservative and semantics-preserving.
    if (has_control_flow) {
        return out;
    }

    std::vector<Instruction> compact;
    compact.reserve(input.instructions.size());

    auto numeric_value = [](const Value& value, double& number, bool& is_integer) {
        if (const auto* p = std::get_if<std::int64_t>(&value.data)) {
            number = static_cast<double>(*p);
            is_integer = true;
            return true;
        }

        if (const auto* p = std::get_if<double>(&value.data)) {
            number = *p;
            is_integer = false;
            return true;
        }

        return false;
    };

    std::size_t i = 0;
    while (i < input.instructions.size()) {
        if (input.instructions[i].op == Instruction::Op::NOP) {
            ++i;
            continue;
        }

        // Constant-fold:
        // CONST a
        // CONST b
        // BINARY op
        if (i + 2 < input.instructions.size() &&
            input.instructions[i].op == Instruction::Op::CONST &&
            input.instructions[i + 1].op == Instruction::Op::CONST &&
            input.instructions[i + 2].op == Instruction::Op::BINARY) {

            const auto a_index = input.instructions[i].arg;
            const auto b_index = input.instructions[i + 1].arg;

            if (a_index >= 0 &&
                b_index >= 0 &&
                static_cast<std::size_t>(a_index) < out.constants.size() &&
                static_cast<std::size_t>(b_index) < out.constants.size()) {

                const auto& a = out.constants[static_cast<std::size_t>(a_index)];
                const auto& b = out.constants[static_cast<std::size_t>(b_index)];

                double da = 0.0;
                double db = 0.0;
                bool ai = false;
                bool bi = false;

                if (numeric_value(a, da, ai) && numeric_value(b, db, bi)) {
                    const auto& op = input.instructions[i + 2].text;
                    bool folded = true;
                    Value result;

                    if (op == "+") {
                        if (ai && bi) {
                            result = Value(static_cast<std::int64_t>(da + db));
                        } else {
                            result = Value(da + db);
                        }
                    } else if (op == "-") {
                        if (ai && bi) {
                            result = Value(static_cast<std::int64_t>(da - db));
                        } else {
                            result = Value(da - db);
                        }
                    } else if (op == "*") {
                        if (ai && bi) {
                            result = Value(static_cast<std::int64_t>(da * db));
                        } else {
                            result = Value(da * db);
                        }
                    } else if (op == "/") {
                        if (db == 0.0) {
                            folded = false;
                        } else {
                            result = Value(da / db);
                        }
                    } else {
                        folded = false;
                    }

                    if (folded) {
                        const auto new_index =
                            static_cast<std::int64_t>(out.constants.size());
                        out.constants.push_back(result);
                        compact.emplace_back(
                            Instruction::Op::CONST,
                            new_index
                        );
                        i += 3;
                        continue;
                    }
                }
            }
        }

        compact.push_back(input.instructions[i]);
        ++i;
    }

    out.instructions = std::move(compact);
    return out;
}

Runner::Runner(std::uint64_t step_limit)
    : vm_(step_limit) {}

Result Runner::run(
    const Program& program,
    const std::unordered_map<std::string, Value>& context
) {
    return vm_.run(optimizer_.optimize(program), context);
}

} // namespace leather::lth06
