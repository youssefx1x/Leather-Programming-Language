use std::collections::HashMap;
use std::fmt;
use std::time::Instant;

#[derive(Clone, Debug, PartialEq)]
pub enum Value {
    None,
    Bool(bool),
    Int(i64),
    Float(f64),
    Str(String),
    List(Vec<Value>),
    Map(HashMap<String, Value>),
}

impl Value {
    pub fn truthy(&self) -> bool {
        match self {
            Value::None => false,
            Value::Bool(v) => *v,
            Value::Int(v) => *v != 0,
            Value::Float(v) => *v != 0.0,
            Value::Str(v) => !v.is_empty(),
            Value::List(v) => !v.is_empty(),
            Value::Map(v) => !v.is_empty(),
        }
    }

    pub fn repr(&self) -> String {
        match self {
            Value::None => "None".to_string(),
            Value::Bool(v) => v.to_string(),
            Value::Int(v) => v.to_string(),
            Value::Float(v) => {
                if v.fract() == 0.0 {
                    format!("{:.1}", v)
                } else {
                    v.to_string()
                }
            }
            Value::Str(v) => format!("{:?}", v),
            Value::List(values) => {
                let body = values
                    .iter()
                    .map(Value::repr)
                    .collect::<Vec<_>>()
                    .join(", ");
                format!("[{}]", body)
            }
            Value::Map(values) => {
                let mut entries = values
                    .iter()
                    .map(|(k, v)| format!("{:?}: {}", k, v.repr()))
                    .collect::<Vec<_>>();
                entries.sort();
                format!("{{{}}}", entries.join(", "))
            }
        }
    }
}

impl fmt::Display for Value {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.repr())
    }
}

#[derive(Clone, Debug)]
pub enum Op {
    Nop,
    Const(usize),
    Load(usize),
    Store(usize),
    LoadMember(String),
    LoadIndex,
    BuildList(usize),
    BuildMap(usize),
    Unary(String),
    Binary(String),
    Call(String, usize),
    JumpIfFalse(usize),
    Jump(usize),
    Pop,
    Halt,
}

#[derive(Clone, Debug)]
pub struct Program {
    pub instructions: Vec<Op>,
    pub constants: Vec<Value>,
    pub names: Vec<String>,
}

impl Program {
    pub fn new() -> Self {
        Self {
            instructions: Vec::new(),
            constants: Vec::new(),
            names: Vec::new(),
        }
    }
}

#[derive(Clone, Debug, Default)]
pub struct Profile {
    pub instructions: u64,
    pub max_stack: usize,
    pub opcodes: HashMap<String, u64>,
    pub specialization_hits: u64,
    pub specialization_misses: u64,
}

impl Profile {
    fn record(&mut self, op: &Op, stack_size: usize) {
        self.instructions += 1;
        self.max_stack = self.max_stack.max(stack_size);

        let name = match op {
            Op::Nop => "NOP",
            Op::Const(_) => "CONST",
            Op::Load(_) => "LOAD",
            Op::Store(_) => "STORE",
            Op::LoadMember(_) => "LOAD_MEMBER",
            Op::LoadIndex => "LOAD_INDEX",
            Op::BuildList(_) => "BUILD_LIST",
            Op::BuildMap(_) => "BUILD_MAP",
            Op::Unary(_) => "UNARY",
            Op::Binary(_) => "BINARY",
            Op::Call(_, _) => "CALL",
            Op::JumpIfFalse(_) => "JUMP_IF_FALSE",
            Op::Jump(_) => "JUMP",
            Op::Pop => "POP",
            Op::Halt => "HALT",
        };

        *self.opcodes.entry(name.to_string()).or_insert(0) += 1;
    }
}

#[derive(Clone, Debug)]
pub struct ResultState {
    pub values: HashMap<String, Value>,
    pub profile: Profile,
}

pub struct Vm {
    step_limit: u64,
}

impl Vm {
    pub fn new(step_limit: u64) -> Self {
        Self { step_limit }
    }

    fn pop(stack: &mut Vec<Value>) -> Result<Value, String> {
        stack
            .pop()
            .ok_or_else(|| "stack underflow".to_string())
    }

    fn equal(left: &Value, right: &Value) -> bool {
        match (left, right) {
            (Value::Int(a), Value::Float(b)) => *a as f64 == *b,
            (Value::Float(a), Value::Int(b)) => *a == *b as f64,
            (Value::List(a), Value::List(b)) => {
                a.len() == b.len()
                    && a.iter()
                        .zip(b)
                        .all(|(x, y)| Self::equal(x, y))
            }
            (Value::Map(a), Value::Map(b)) => {
                a.len() == b.len()
                    && a.iter().all(|(k, v)| {
                        b.get(k)
                            .is_some_and(|other| Self::equal(v, other))
                    })
            }
            _ => left == right,
        }
    }

    fn floor_div(a: i64, b: i64) -> Result<(i64, i64), String> {
        if b == 0 {
            return Err("division by zero".to_string());
        }

        let mut q = a / b;
        let mut r = a % b;

        if r != 0 && (r < 0) != (b < 0) {
            q -= 1;
            r = a - q * b;
        }

        Ok((q, r))
    }

    fn binary(
        &self,
        op: &str,
        left: Value,
        right: Value,
        profile: &mut Profile,
    ) -> Result<Value, String> {
        match (&left, &right) {
            (Value::Int(a), Value::Int(b)) => {
                profile.specialization_hits += 1;

                match op {
                    "+" => Ok(Value::Int(a + b)),
                    "-" => Ok(Value::Int(a - b)),
                    "*" => Ok(Value::Int(a * b)),
                    "/" => {
                        if *b == 0 {
                            Err("division by zero".to_string())
                        } else {
                            Ok(Value::Float(*a as f64 / *b as f64))
                        }
                    }
                    "//" => Ok(Value::Int(Self::floor_div(*a, *b)?.0)),
                    "%" => Ok(Value::Int(Self::floor_div(*a, *b)?.1)),
                    "**" => Ok(Value::Float((*a as f64).powf(*b as f64))),
                    "==" => Ok(Value::Bool(a == b)),
                    "!=" => Ok(Value::Bool(a != b)),
                    "<" => Ok(Value::Bool(a < b)),
                    "<=" => Ok(Value::Bool(a <= b)),
                    ">" => Ok(Value::Bool(a > b)),
                    ">=" => Ok(Value::Bool(a >= b)),
                    "and" => Ok(if *a != 0 { right } else { left }),
                    "or" => Ok(if *a != 0 { left } else { right }),
                    _ => Err(format!("unsupported binary operator: {}", op)),
                }
            }

            (Value::Float(a), Value::Float(b)) => {
                profile.specialization_hits += 1;

                match op {
                    "+" => Ok(Value::Float(a + b)),
                    "-" => Ok(Value::Float(a - b)),
                    "*" => Ok(Value::Float(a * b)),
                    "/" => {
                        if *b == 0.0 {
                            Err("division by zero".to_string())
                        } else {
                            Ok(Value::Float(a / b))
                        }
                    }
                    "//" => {
                        if *b == 0.0 {
                            Err("division by zero".to_string())
                        } else {
                            Ok(Value::Float((a / b).floor()))
                        }
                    }
                    "%" => {
                        if *b == 0.0 {
                            Err("modulo by zero".to_string())
                        } else {
                            Ok(Value::Float(a - (*b * (a / b).floor())))
                        }
                    }
                    "**" => Ok(Value::Float(a.powf(*b))),
                    "==" => Ok(Value::Bool(a == b)),
                    "!=" => Ok(Value::Bool(a != b)),
                    "<" => Ok(Value::Bool(a < b)),
                    "<=" => Ok(Value::Bool(a <= b)),
                    ">" => Ok(Value::Bool(a > b)),
                    ">=" => Ok(Value::Bool(a >= b)),
                    "and" => Ok(if *a != 0.0 { right } else { left }),
                    "or" => Ok(if *a != 0.0 { left } else { right }),
                    _ => Err(format!("unsupported binary operator: {}", op)),
                }
            }

            (Value::Int(a), Value::Float(b)) | (Value::Float(b), Value::Int(a)) => {
                profile.specialization_misses += 1;

                let (left_number, right_number) =
                    if matches!(left, Value::Int(_)) {
                        (*a as f64, *b)
                    } else {
                        (*b, *a as f64)
                    };

                match op {
                    "+" => Ok(Value::Float(left_number + right_number)),
                    "-" => Ok(Value::Float(left_number - right_number)),
                    "*" => Ok(Value::Float(left_number * right_number)),
                    "/" => {
                        if right_number == 0.0 {
                            Err("division by zero".to_string())
                        } else {
                            Ok(Value::Float(left_number / right_number))
                        }
                    }
                    "//" => {
                        if right_number == 0.0 {
                            Err("division by zero".to_string())
                        } else {
                            Ok(Value::Float(
                                (left_number / right_number).floor(),
                            ))
                        }
                    }
                    "%" => {
                        if right_number == 0.0 {
                            Err("modulo by zero".to_string())
                        } else {
                            Ok(Value::Float(
                                left_number
                                    - right_number
                                        * (left_number / right_number).floor(),
                            ))
                        }
                    }
                    "**" => Ok(Value::Float(
                        left_number.powf(right_number),
                    )),
                    "==" => Ok(Value::Bool(
                        left_number == right_number,
                    )),
                    "!=" => Ok(Value::Bool(
                        left_number != right_number,
                    )),
                    "<" => Ok(Value::Bool(
                        left_number < right_number,
                    )),
                    "<=" => Ok(Value::Bool(
                        left_number <= right_number,
                    )),
                    ">" => Ok(Value::Bool(
                        left_number > right_number,
                    )),
                    ">=" => Ok(Value::Bool(
                        left_number >= right_number,
                    )),
                    _ => Err(format!("unsupported binary operator: {}", op)),
                }
            }

            (Value::Str(a), Value::Str(b)) => {
                profile.specialization_hits += 1;

                match op {
                    "+" => Ok(Value::Str(format!("{}{}", a, b))),
                    "==" => Ok(Value::Bool(a == b)),
                    "!=" => Ok(Value::Bool(a != b)),
                    "<" => Ok(Value::Bool(a < b)),
                    "<=" => Ok(Value::Bool(a <= b)),
                    ">" => Ok(Value::Bool(a > b)),
                    ">=" => Ok(Value::Bool(a >= b)),
                    "and" => Ok(if !a.is_empty() { right } else { left }),
                    "or" => Ok(if !a.is_empty() { left } else { right }),
                    _ => Err(format!("unsupported string operator: {}", op)),
                }
            }

            _ => {
                profile.specialization_misses += 1;

                match op {
                    "==" => Ok(Value::Bool(Self::equal(&left, &right))),
                    "!=" => Ok(Value::Bool(!Self::equal(&left, &right))),
                    "and" => Ok(if left.truthy() { right } else { left }),
                    "or" => Ok(if left.truthy() { left } else { right }),
                    _ => Err(format!("unsupported operands for {}", op)),
                }
            }
        }
    }

    fn unary(&self, op: &str, value: Value) -> Result<Value, String> {
        match op {
            "not" | "!" => Ok(Value::Bool(!value.truthy())),
            "+" => match value {
                Value::Int(v) => Ok(Value::Int(v)),
                Value::Float(v) => Ok(Value::Float(v)),
                _ => Err("unsupported unary +".to_string()),
            },
            "-" => match value {
                Value::Int(v) => Ok(Value::Int(-v)),
                Value::Float(v) => Ok(Value::Float(-v)),
                _ => Err("unsupported unary -".to_string()),
            },
            _ => Err(format!("unsupported unary operator: {}", op)),
        }
    }

    pub fn run(
        &self,
        program: &Program,
        context: &HashMap<String, Value>,
    ) -> Result<ResultState, String> {
        let mut stack: Vec<Value> = Vec::new();
        let mut values: HashMap<String, Value> = HashMap::new();
        let mut profile = Profile::default();
        let mut ip = 0usize;
        let mut steps = 0u64;

        while ip < program.instructions.len() {
            steps += 1;
            if steps > self.step_limit {
                return Err("step limit exceeded".to_string());
            }

            let instruction = &program.instructions[ip];
            profile.record(instruction, stack.len());

            match instruction {
                Op::Nop => {
                    ip += 1;
                }

                Op::Const(index) => {
                    let value = program
                        .constants
                        .get(*index)
                        .ok_or_else(|| "constant index out of range".to_string())?
                        .clone();

                    stack.push(value);
                    ip += 1;
                }

                Op::Load(index) => {
                    let name = program
                        .names
                        .get(*index)
                        .ok_or_else(|| "name index out of range".to_string())?;

                    let value = values
                        .get(name)
                        .or_else(|| context.get(name))
                        .cloned()
                        .ok_or_else(|| format!("unknown name: {}", name))?;

                    stack.push(value);
                    ip += 1;
                }

                Op::Store(index) => {
                    let name = program
                        .names
                        .get(*index)
                        .ok_or_else(|| "name index out of range".to_string())?
                        .clone();

                    let value = Self::pop(&mut stack)?;
                    values.insert(name, value);
                    ip += 1;
                }

                Op::LoadMember(name) => {
                    let object = Self::pop(&mut stack)?;

                    match object {
                        Value::Map(map) => {
                            let value = map
                                .get(name)
                                .cloned()
                                .ok_or_else(|| {
                                    format!("missing member: {}", name)
                                })?;
                            stack.push(value);
                        }
                        _ => {
                            return Err(
                                "member access requires a map".to_string()
                            );
                        }
                    }

                    ip += 1;
                }

                Op::LoadIndex => {
                    let index = Self::pop(&mut stack)?;
                    let object = Self::pop(&mut stack)?;

                    match (object, index) {
                        (Value::List(values), Value::Int(i)) => {
                            if i < 0 {
                                return Err(
                                    "negative list index unsupported in 0.7"
                                        .to_string(),
                                );
                            }

                            let value = values
                                .get(i as usize)
                                .cloned()
                                .ok_or_else(|| {
                                    "list index out of range".to_string()
                                })?;

                            stack.push(value);
                        }

                        (Value::Map(map), Value::Str(key)) => {
                            let value = map
                                .get(&key)
                                .cloned()
                                .ok_or_else(|| {
                                    format!("missing map key: {}", key)
                                })?;

                            stack.push(value);
                        }

                        (Value::Str(value), Value::Int(i)) => {
                            if i < 0 {
                                return Err(
                                    "negative string index unsupported in 0.7"
                                        .to_string(),
                                );
                            }

                            let value = value
                                .chars()
                                .nth(i as usize)
                                .ok_or_else(|| {
                                    "string index out of range".to_string()
                                })?;

                            stack.push(Value::Str(value.to_string()));
                        }

                        _ => {
                            return Err(
                                "unsupported index operands".to_string()
                            );
                        }
                    }

                    ip += 1;
                }

                Op::BuildList(count) => {
                    if stack.len() < *count {
                        return Err("stack underflow".to_string());
                    }

                    let start = stack.len() - *count;
                    let values = stack.drain(start..).collect::<Vec<_>>();
                    stack.push(Value::List(values));
                    ip += 1;
                }

                Op::BuildMap(count) => {
                    if stack.len() < count * 2 {
                        return Err("stack underflow".to_string());
                    }

                    let start = stack.len() - count * 2;
                    let entries = stack.drain(start..).collect::<Vec<_>>();

                    let mut map = HashMap::new();

                    for pair in entries.chunks_exact(2) {
                        let key = match &pair[0] {
                            Value::Str(v) => v.clone(),
                            _ => {
                                return Err(
                                    "map keys must be strings".to_string()
                                );
                            }
                        };

                        map.insert(key, pair[1].clone());
                    }

                    stack.push(Value::Map(map));
                    ip += 1;
                }

                Op::Unary(op) => {
                    let value = Self::pop(&mut stack)?;
                    stack.push(self.unary(op, value)?);
                    ip += 1;
                }

                Op::Binary(op) => {
                    let right = Self::pop(&mut stack)?;
                    let left = Self::pop(&mut stack)?;
                    stack.push(self.binary(
                        op,
                        left,
                        right,
                        &mut profile,
                    )?);
                    ip += 1;
                }

                Op::Call(name, count) => {
                    if stack.len() < *count {
                        return Err("stack underflow".to_string());
                    }

                    let start = stack.len() - *count;
                    let args = stack.drain(start..).collect::<Vec<_>>();

                    let result = match name.as_str() {
                        "len" => {
                            if args.len() != 1 {
                                return Err(
                                    "len expects one argument".to_string()
                                );
                            }

                            let len = match &args[0] {
                                Value::Str(v) => v.chars().count(),
                                Value::List(v) => v.len(),
                                Value::Map(v) => v.len(),
                                _ => {
                                    return Err(
                                        "len unsupported for value"
                                            .to_string(),
                                    );
                                }
                            };

                            Value::Int(len as i64)
                        }

                        "bool" => {
                            if args.len() != 1 {
                                return Err(
                                    "bool expects one argument".to_string()
                                );
                            }

                            Value::Bool(args[0].truthy())
                        }

                        "repr" => {
                            if args.len() != 1 {
                                return Err(
                                    "repr expects one argument".to_string()
                                );
                            }

                            Value::Str(args[0].repr())
                        }

                        _ => {
                            return Err(format!(
                                "unknown builtin: {}",
                                name
                            ));
                        }
                    };

                    stack.push(result);
                    ip += 1;
                }

                Op::JumpIfFalse(target) => {
                    let condition = Self::pop(&mut stack)?;

                    if !condition.truthy() {
                        ip = *target;
                    } else {
                        ip += 1;
                    }
                }

                Op::Jump(target) => {
                    ip = *target;
                }

                Op::Pop => {
                    Self::pop(&mut stack)?;
                    ip += 1;
                }

                Op::Halt => break,
            }
        }

        Ok(ResultState { values, profile })
    }
}

pub struct Optimizer;

impl Optimizer {
    pub fn optimize(input: &Program) -> Program {
        let has_control_flow = input.instructions.iter().any(|op| {
            matches!(op, Op::Jump(_) | Op::JumpIfFalse(_))
        });

        if has_control_flow {
            return input.clone();
        }

        let mut output = input.clone();
        let mut compact = Vec::new();
        let mut i = 0usize;

        while i < input.instructions.len() {
            if matches!(input.instructions[i], Op::Nop) {
                i += 1;
                continue;
            }

            if i + 2 < input.instructions.len() {
                if let (
                    Op::Const(a),
                    Op::Const(b),
                    Op::Binary(op),
                ) = (
                    &input.instructions[i],
                    &input.instructions[i + 1],
                    &input.instructions[i + 2],
                ) {
                    let left = input.constants.get(*a);
                    let right = input.constants.get(*b);

                    if let (Some(left), Some(right)) = (left, right) {
                        if let Some(value) =
                            Self::fold_numeric(left, right, op)
                        {
                            let index = output.constants.len();
                            output.constants.push(value);
                            compact.push(Op::Const(index));
                            i += 3;
                            continue;
                        }
                    }
                }
            }

            compact.push(input.instructions[i].clone());
            i += 1;
        }

        output.instructions = compact;
        output
    }

    fn fold_numeric(
        left: &Value,
        right: &Value,
        op: &str,
    ) -> Option<Value> {
        match (left, right) {
            (Value::Int(a), Value::Int(b)) => match op {
                "+" => Some(Value::Int(a + b)),
                "-" => Some(Value::Int(a - b)),
                "*" => Some(Value::Int(a * b)),
                "/" if *b != 0 => {
                    Some(Value::Float(*a as f64 / *b as f64))
                }
                "//" if *b != 0 => {
                    let (q, _) = Vm::floor_div(*a, *b).ok()?;
                    Some(Value::Int(q))
                }
                "%" if *b != 0 => {
                    let (_, r) = Vm::floor_div(*a, *b).ok()?;
                    Some(Value::Int(r))
                }
                _ => None,
            },

            (Value::Float(a), Value::Float(b)) => match op {
                "+" => Some(Value::Float(a + b)),
                "-" => Some(Value::Float(a - b)),
                "*" => Some(Value::Float(a * b)),
                "/" if *b != 0.0 => Some(Value::Float(a / b)),
                "//" if *b != 0.0 => {
                    Some(Value::Float((a / b).floor()))
                }
                "%" if *b != 0.0 => {
                    Some(Value::Float(
                        a - b * (a / b).floor(),
                    ))
                }
                _ => None,
            },

            _ => None,
        }
    }
}

pub struct Compiler;

impl Compiler {
    pub fn demo_program() -> Program {
        let mut program = Program::new();

        program.constants = vec![
            Value::Float(150.5),
            Value::Float(0.9),
        ];

        program.names = vec!["price".to_string()];

        program.instructions = vec![
            Op::Const(0),
            Op::Const(1),
            Op::Binary("*".to_string()),
            Op::Store(0),
            Op::Halt,
        ];

        program
    }
}

pub struct Runner {
    vm: Vm,
}

impl Runner {
    pub fn new(step_limit: u64) -> Self {
        Self {
            vm: Vm::new(step_limit),
        }
    }

    pub fn run(
        &self,
        program: &Program,
        context: &HashMap<String, Value>,
    ) -> Result<ResultState, String> {
        let optimized = Optimizer::optimize(program);
        self.vm.run(&optimized, context)
    }
}

pub fn benchmark(iterations: usize) -> u128 {
    let program = Compiler::demo_program();
    let runner = Runner::new(1_000_000);
    let context = HashMap::new();

    let start = Instant::now();

    for _ in 0..iterations {
        let result = runner.run(&program, &context);
        assert!(result.is_ok());
    }

    start.elapsed().as_micros()
}
