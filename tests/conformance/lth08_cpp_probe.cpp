#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Value {
    enum class Kind {
        None,
        Bool,
        Int,
        Float,
        Str,
        List,
        Map
    };

    Kind kind = Kind::None;
    bool b = false;
    std::int64_t i = 0;
    double f = 0.0;
    std::string s;
    std::vector<Value> list;
    std::map<std::string, Value> map;

    static Value none() {
        return Value{};
    }

    static Value boolean(bool value) {
        Value result;
        result.kind = Kind::Bool;
        result.b = value;
        return result;
    }

    static Value integer(std::int64_t value) {
        Value result;
        result.kind = Kind::Int;
        result.i = value;
        return result;
    }

    static Value real(double value) {
        Value result;
        result.kind = Kind::Float;
        result.f = value;
        return result;
    }

    static Value str(std::string value) {
        Value result;
        result.kind = Kind::Str;
        result.s = std::move(value);
        return result;
    }
};

struct LTH08Error : std::runtime_error {
    using std::runtime_error::runtime_error;
};


static std::vector<std::string> split_top(const std::string& text) {
    std::vector<std::string> result;
    std::string current;

    int depth = 0;
    bool quote = false;
    bool escape = false;

    for (char ch : text) {
        if (escape) {
            current += ch;
            escape = false;
            continue;
        }

        if (quote) {
            current += ch;

            if (ch == '\\')
                escape = true;
            else if (ch == '"')
                quote = false;

            continue;
        }

        if (ch == '"') {
            quote = true;
            current += ch;
            continue;
        }

        if (ch == '(' || ch == '[' || ch == '{')
            ++depth;

        if (ch == ')' || ch == ']' || ch == '}')
            --depth;

        if (ch == ',' && depth == 0) {
            result.push_back(current);
            current.clear();
        } else {
            current += ch;
        }
    }

    if (!current.empty())
        result.push_back(current);

    for (auto& item : result) {
        const auto first = item.find_first_not_of(" \t");
        const auto last = item.find_last_not_of(" \t");

        if (first == std::string::npos) {
            item.clear();
        } else {
            item = item.substr(first, last - first + 1);
        }
    }

    return result;
}


static Value parse_value(const std::string& raw) {
    const auto first = raw.find_first_not_of(" \t");
    const auto last = raw.find_last_not_of(" \t");

    const std::string text =
        first == std::string::npos
            ? ""
            : raw.substr(first, last - first + 1);

    if (text == "None")
        return Value::none();

    if (text.rfind("Int(", 0) == 0 && text.back() == ')')
        return Value::integer(
            std::stoll(text.substr(4, text.size() - 5))
        );

    if (text.rfind("Float(", 0) == 0 && text.back() == ')')
        return Value::real(
            std::stod(text.substr(6, text.size() - 7))
        );

    if (text.rfind("Str(", 0) == 0 && text.back() == ')') {
        std::string value = text.substr(4, text.size() - 5);

        if (value.size() >= 2 &&
            value.front() == '"' &&
            value.back() == '"') {
            value = value.substr(1, value.size() - 2);
        }

        return Value::str(value);
    }

    if (text.rfind("List(", 0) == 0 && text.back() == ')') {
        std::string body = text.substr(5, text.size() - 6);

        if (body.size() < 2 ||
            body.front() != '[' ||
            body.back() != ']') {
            throw std::runtime_error("bad list");
        }

        body = body.substr(1, body.size() - 2);

        Value result;
        result.kind = Value::Kind::List;

        if (body.find_first_not_of(" \t") != std::string::npos) {
            for (const auto& item : split_top(body))
                result.list.push_back(parse_value(item));
        }

        return result;
    }

    if (text.rfind("Map(", 0) == 0 && text.back() == ')') {
        std::string body = text.substr(4, text.size() - 5);

        if (body.size() < 2 ||
            body.front() != '{' ||
            body.back() != '}') {
            throw std::runtime_error("bad map");
        }

        body = body.substr(1, body.size() - 2);

        Value result;
        result.kind = Value::Kind::Map;

        if (body.find_first_not_of(" \t") != std::string::npos) {
            for (const auto& item : split_top(body)) {
                const auto colon = item.find(':');

                if (colon == std::string::npos)
                    throw std::runtime_error("bad map item");

                std::string key = item.substr(0, colon);
                const std::string value = item.substr(colon + 1);

                const auto first_key =
                    key.find_first_not_of(" \t");
                const auto last_key =
                    key.find_last_not_of(" \t");

                if (first_key != std::string::npos)
                    key = key.substr(
                        first_key,
                        last_key - first_key + 1
                    );

                if (key.size() >= 2 &&
                    key.front() == '"' &&
                    key.back() == '"') {
                    key = key.substr(1, key.size() - 2);
                }

                result.map[key] = parse_value(value);
            }
        }

        return result;
    }

    throw std::runtime_error("bad value: " + text);
}


static bool truthy(const Value& value) {
    switch (value.kind) {
        case Value::Kind::None:
            return false;

        case Value::Kind::Bool:
            return value.b;

        case Value::Kind::Int:
            return value.i != 0;

        case Value::Kind::Float:
            return value.f != 0.0;

        case Value::Kind::Str:
            return !value.s.empty();

        case Value::Kind::List:
            return !value.list.empty();

        case Value::Kind::Map:
            return !value.map.empty();
    }

    return false;
}


static bool equal_value(
    const Value& left,
    const Value& right
) {
    if (left.kind == Value::Kind::Bool ||
        right.kind == Value::Kind::Bool) {
        return left.kind == right.kind &&
               left.b == right.b;
    }

    const auto numeric = [](Value::Kind kind) {
        return kind == Value::Kind::Int ||
               kind == Value::Kind::Float;
    };

    if (numeric(left.kind) && numeric(right.kind)) {
        const double a =
            left.kind == Value::Kind::Int
                ? static_cast<double>(left.i)
                : left.f;

        const double b =
            right.kind == Value::Kind::Int
                ? static_cast<double>(right.i)
                : right.f;

        return a == b;
    }

    if (left.kind != right.kind)
        return false;

    switch (left.kind) {
        case Value::Kind::None:
            return true;

        case Value::Kind::Str:
            return left.s == right.s;

        case Value::Kind::List:
            if (left.list.size() != right.list.size())
                return false;

            for (std::size_t i = 0; i < left.list.size(); ++i) {
                if (!equal_value(left.list[i], right.list[i]))
                    return false;
            }

            return true;

        case Value::Kind::Map:
            if (left.map.size() != right.map.size())
                return false;

            for (const auto& [key, value] : left.map) {
                const auto found = right.map.find(key);

                if (found == right.map.end())
                    return false;

                if (!equal_value(value, found->second))
                    return false;
            }

            return true;

        default:
            return false;
    }
}


static Value evaluate(
    const std::string& operation,
    const Value& left,
    const Value& right
) {
    if (operation == "add") {
        if (left.kind == Value::Kind::Str &&
            right.kind == Value::Kind::Str) {
            return Value::str(left.s + right.s);
        }

        const bool left_numeric =
            left.kind == Value::Kind::Int ||
            left.kind == Value::Kind::Float;

        const bool right_numeric =
            right.kind == Value::Kind::Int ||
            right.kind == Value::Kind::Float;

        if (left_numeric && right_numeric) {
            const double a =
                left.kind == Value::Kind::Int
                    ? static_cast<double>(left.i)
                    : left.f;

            const double b =
                right.kind == Value::Kind::Int
                    ? static_cast<double>(right.i)
                    : right.f;

            if (left.kind == Value::Kind::Float ||
                right.kind == Value::Kind::Float) {
                return Value::real(a + b);
            }

            return Value::integer(left.i + right.i);
        }

        throw LTH08Error("unsupported add");
    }

    if (operation == "floor_div") {
        if (left.kind != Value::Kind::Int ||
            right.kind != Value::Kind::Int) {
            throw LTH08Error("unsupported floor_div");
        }

        if (right.i == 0)
            throw LTH08Error("division by zero");

        std::int64_t quotient = left.i / right.i;
        const std::int64_t remainder = left.i % right.i;

        if (remainder != 0 &&
            ((remainder < 0) != (right.i < 0))) {
            --quotient;
        }

        return Value::integer(quotient);
    }

    if (operation == "mod") {
        if (left.kind != Value::Kind::Int ||
            right.kind != Value::Kind::Int) {
            throw LTH08Error("unsupported mod");
        }

        if (right.i == 0)
            throw LTH08Error("modulo by zero");

        std::int64_t quotient = left.i / right.i;
        const std::int64_t remainder = left.i % right.i;

        if (remainder != 0 &&
            ((remainder < 0) != (right.i < 0))) {
            --quotient;
        }

        return Value::integer(
            left.i - quotient * right.i
        );
    }

    if (operation == "eq")
        return Value::boolean(equal_value(left, right));

    if (operation == "truth")
        return Value::boolean(truthy(left));

    if (operation == "and")
        return truthy(left) ? right : left;

    if (operation == "or")
        return truthy(left) ? left : right;

    throw LTH08Error("unsupported op: " + operation);
}


static std::string format_value(const Value& value) {
    std::ostringstream out;

    switch (value.kind) {
        case Value::Kind::None:
            return "None";

        case Value::Kind::Bool:
            return value.b
                ? "Bool(true)"
                : "Bool(false)";

        case Value::Kind::Int:
            out << "Int(" << value.i << ")";
            return out.str();

        case Value::Kind::Float: {
            out << std::setprecision(17) << value.f;
            std::string text = out.str();

            if (text.find('.') == std::string::npos &&
                text.find('e') == std::string::npos &&
                text.find('E') == std::string::npos) {
                text += ".0";
            }

            return "Float(" + text + ")";
        }

        case Value::Kind::Str:
            return "Str(\"" + value.s + "\")";

        case Value::Kind::List: {
            out << "List([";

            for (std::size_t i = 0; i < value.list.size(); ++i) {
                if (i)
                    out << ",";

                out << format_value(value.list[i]);
            }

            out << "])";
            return out.str();
        }

        case Value::Kind::Map: {
            out << "Map({";

            bool first = true;

            for (const auto& [key, item] : value.map) {
                if (!first)
                    out << ",";

                first = false;

                out << "\"" << key << "\":"
                    << format_value(item);
            }

            out << "})";
            return out.str();
        }
    }

    throw std::runtime_error("unknown value");
}


int main(int argc, char** argv) {
    const std::string path =
        argc > 1
            ? argv[1]
            : "tests/conformance/lth08_cases.tsv";

    std::ifstream input(path);

    if (!input) {
        std::cerr << "cannot open " << path << "\n";
        return 2;
    }

    std::string line;
    std::size_t line_no = 0;

    while (std::getline(input, line)) {
        ++line_no;

        if (line.empty() || line[0] == '#')
            continue;

        std::vector<std::string> fields;
        std::stringstream stream(line);
        std::string field;

        while (std::getline(stream, field, '\t'))
            fields.push_back(field);

        if (fields.size() != 6) {
            std::cerr << "bad case line "
                      << line_no << "\n";
            return 3;
        }

        const std::string& case_id = fields[0];
        const std::string& operation = fields[2];

        const Value left = parse_value(fields[3]);

        const Value right =
            fields[4] == "-"
                ? Value::none()
                : parse_value(fields[4]);

        std::string actual;

        try {
            actual = format_value(
                evaluate(operation, left, right)
            );
        } catch (const LTH08Error& error) {
            actual =
                "Error(\"" +
                std::string(error.what()) +
                "\")";
        }

        std::cout << case_id
                  << "\t"
                  << actual
                  << "\n";
    }

    return 0;
}
