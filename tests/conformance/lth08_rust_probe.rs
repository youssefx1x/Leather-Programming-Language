use std::collections::BTreeMap;
use std::env;
use std::fs;

#[derive(Clone, Debug, PartialEq)]
enum Value {
    None,
    Bool(bool),
    Int(i64),
    Float(f64),
    Str(String),
    List(Vec<Value>),
    Map(BTreeMap<String, Value>),
}

#[derive(Debug)]
struct Lth08Error(String);

fn split_top(text: &str) -> Vec<String> {
    let mut result = Vec::new();
    let mut current = String::new();
    let mut depth = 0i32;
    let mut quote = false;
    let mut escape = false;

    for ch in text.chars() {
        if escape {
            current.push(ch);
            escape = false;
            continue;
        }

        if quote {
            current.push(ch);
            if ch == '\\' {
                escape = true;
            } else if ch == '"' {
                quote = false;
            }
            continue;
        }

        if ch == '"' {
            quote = true;
            current.push(ch);
            continue;
        }

        match ch {
            '(' | '[' | '{' => depth += 1,
            ')' | ']' | '}' => depth -= 1,
            _ => {}
        }

        if ch == ',' && depth == 0 {
            result.push(current.trim().to_string());
            current.clear();
        } else {
            current.push(ch);
        }
    }

    if !current.trim().is_empty() {
        result.push(current.trim().to_string());
    }

    result
}

fn parse_value(raw: &str) -> Result<Value, String> {
    let text = raw.trim();

    if text == "None" {
        return Ok(Value::None);
    }

    if text.starts_with("Int(") && text.ends_with(')') {
        return Ok(Value::Int(
            text[4..text.len() - 1]
                .parse()
                .map_err(|_| "bad int".to_string())?,
        ));
    }

    if text.starts_with("Float(") && text.ends_with(')') {
        return Ok(Value::Float(
            text[6..text.len() - 1]
                .parse()
                .map_err(|_| "bad float".to_string())?,
        ));
    }

    if text.starts_with("Str(") && text.ends_with(')') {
        let mut value = text[4..text.len() - 1].to_string();

        if value.len() >= 2 && value.starts_with('"') && value.ends_with('"') {
            value = value[1..value.len() - 1].to_string();
        }

        return Ok(Value::Str(value));
    }

    if text.starts_with("List(") && text.ends_with(')') {
        let inner = &text[5..text.len() - 1];

        if !inner.starts_with('[') || !inner.ends_with(']') {
            return Err("bad list".to_string());
        }

        let body = &inner[1..inner.len() - 1];

        let values = if body.trim().is_empty() {
            Vec::new()
        } else {
            split_top(body)
                .into_iter()
                .map(|x| parse_value(&x))
                .collect::<Result<Vec<_>, _>>()?
        };

        return Ok(Value::List(values));
    }

    if text.starts_with("Map(") && text.ends_with(')') {
        let inner = &text[4..text.len() - 1];

        if !inner.starts_with('{') || !inner.ends_with('}') {
            return Err("bad map".to_string());
        }

        let body = &inner[1..inner.len() - 1];
        let mut map = BTreeMap::new();

        if !body.trim().is_empty() {
            for item in split_top(body) {
                let (key, value) = item
                    .split_once(':')
                    .ok_or_else(|| "bad map item".to_string())?;

                let mut key = key.trim().to_string();

                if key.len() >= 2 && key.starts_with('"') && key.ends_with('"') {
                    key = key[1..key.len() - 1].to_string();
                }

                map.insert(key, parse_value(value)?);
            }
        }

        return Ok(Value::Map(map));
    }

    Err(format!("unsupported value: {text}"))
}

fn truth(value: &Value) -> bool {
    match value {
        Value::None => false,
        Value::Bool(v) => *v,
        Value::Int(v) => *v != 0,
        Value::Float(v) => *v != 0.0,
        Value::Str(v) => !v.is_empty(),
        Value::List(v) => !v.is_empty(),
        Value::Map(v) => !v.is_empty(),
    }
}

fn equal(left: &Value, right: &Value) -> bool {
    match (left, right) {
        (Value::Bool(a), Value::Bool(b)) => a == b,
        (Value::Bool(_), _) | (_, Value::Bool(_)) => false,

        (Value::Int(a), Value::Int(b)) => a == b,
        (Value::Float(a), Value::Float(b)) => a == b,
        (Value::Int(a), Value::Float(b)) => (*a as f64) == *b,
        (Value::Float(a), Value::Int(b)) => *a == (*b as f64),

        (Value::None, Value::None) => true,
        (Value::Str(a), Value::Str(b)) => a == b,
        (Value::List(a), Value::List(b)) => {
            a.len() == b.len() && a.iter().zip(b).all(|(x, y)| equal(x, y))
        }
        (Value::Map(a), Value::Map(b)) => {
            a.len() == b.len()
                && a.iter().all(|(key, value)| {
                    b.get(key).map(|other| equal(value, other)).unwrap_or(false)
                })
        }
        _ => false,
    }
}

fn floor_div(left: i64, right: i64) -> Result<i64, Lth08Error> {
    if right == 0 {
        return Err(Lth08Error("division by zero".to_string()));
    }

    let mut q = left / right;
    let r = left % right;

    if r != 0 && ((r < 0) != (right < 0)) {
        q -= 1;
    }

    Ok(q)
}

fn modulo(left: i64, right: i64) -> Result<i64, Lth08Error> {
    if right == 0 {
        return Err(Lth08Error("modulo by zero".to_string()));
    }

    let q = floor_div(left, right)?;
    Ok(left - q * right)
}

fn evaluate(
    operation: &str,
    left: &Value,
    right: &Value,
) -> Result<Value, Lth08Error> {
    match operation {
        "add" => match (left, right) {
            (Value::Str(a), Value::Str(b)) => Ok(Value::Str(format!("{a}{b}"))),

            (Value::Int(a), Value::Int(b)) => Ok(Value::Int(a + b)),

            (Value::Int(a), Value::Float(b)) => Ok(Value::Float(*a as f64 + b)),

            (Value::Float(a), Value::Int(b)) => Ok(Value::Float(a + *b as f64)),

            (Value::Float(a), Value::Float(b)) => Ok(Value::Float(a + b)),

            _ => Err(Lth08Error("unsupported add".to_string())),
        },

        "floor_div" => match (left, right) {
            (Value::Int(a), Value::Int(b)) => floor_div(*a, *b).map(Value::Int),
            _ => Err(Lth08Error("unsupported floor_div".to_string())),
        },

        "mod" => match (left, right) {
            (Value::Int(a), Value::Int(b)) => modulo(*a, *b).map(Value::Int),
            _ => Err(Lth08Error("unsupported mod".to_string())),
        },

        "eq" => Ok(Value::Bool(equal(left, right))),

        "truth" => Ok(Value::Bool(truth(left))),

        "and" => {
            if truth(left) {
                Ok(right.clone())
            } else {
                Ok(left.clone())
            }
        }

        "or" => {
            if truth(left) {
                Ok(left.clone())
            } else {
                Ok(right.clone())
            }
        }

        _ => Err(Lth08Error(format!("unsupported op: {operation}"))),
    }
}

fn format_float(value: f64) -> String {
    let mut text = format!("{value:.17}");

    while text.contains('.') && text.ends_with('0') {
        text.pop();
    }

    if text.ends_with('.') {
        text.push('0');
    }

    text
}

fn format_value(value: &Value) -> String {
    match value {
        Value::None => "None".to_string(),

        Value::Bool(v) => {
            if *v {
                "Bool(true)".to_string()
            } else {
                "Bool(false)".to_string()
            }
        }

        Value::Int(v) => format!("Int({v})"),

        Value::Float(v) => format!("Float({})", format_float(*v)),

        Value::Str(v) => format!("Str(\"{v}\")"),

        Value::List(values) => {
            let body = values
                .iter()
                .map(format_value)
                .collect::<Vec<_>>()
                .join(",");

            format!("List([{body}])")
        }

        Value::Map(map) => {
            let body = map
                .iter()
                .map(|(key, value)| {
                    format!("\"{key}\":{}", format_value(value))
                })
                .collect::<Vec<_>>()
                .join(",");

            format!("Map({{{body}}})")
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let path = args
        .get(1)
        .map(String::as_str)
        .unwrap_or("tests/conformance/lth08_cases.tsv");

    let content = fs::read_to_string(path)
        .unwrap_or_else(|error| panic!("cannot open {path}: {error}"));

    for (line_no, line) in content.lines().enumerate() {
        if line.trim().is_empty() || line.starts_with('#') {
            continue;
        }

        let fields: Vec<&str> = line.split('\t').collect();

        if fields.len() != 6 {
            panic!("bad case line {}", line_no + 1);
        }

        let case_id = fields[0];
        let operation = fields[2];

        let left =
            parse_value(fields[3])
                .unwrap_or_else(|e| panic!("bad left value: {e}"));

        let right = if fields[4] == "-" {
            Value::None
        } else {
            parse_value(fields[4])
                .unwrap_or_else(|e| panic!("bad right value: {e}"))
        };

        let actual = match evaluate(operation, &left, &right) {
            Ok(value) => format_value(&value),
            Err(error) => format!("Error(\"{}\")", error.0),
        };

        println!("{case_id}\t{actual}");
    }
}
