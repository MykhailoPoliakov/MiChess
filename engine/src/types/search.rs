use super::*;

#[derive(Clone, Copy)]
pub enum Eval {
    Value(f32),
    Mate(i8)
}

impl Eval {
    pub fn from_value(value: i32) -> Self {
        match value.abs() {
            v if v > 999_900 => Eval::Mate(((1_000_000 - v) * value.signum()) as i8),
            _ => Eval::Value((value as f32 / 100.0).tanh()),
        }
    }
}


#[derive(Clone)]
pub enum SearchStatus {
    None,
    InProgress(f32),
    Finished,
}

#[derive(Clone)]
pub struct SearchInfo {
    pub mv: Option<Move>,
    pub eval: Option<Eval>,
    pub status: SearchStatus,
    pub info: Vec<(Move, Eval, i32)>, // i32 - Iteration count
}

impl SearchInfo {
    pub fn new() -> Self {
        SearchInfo { 
            mv: None,
            eval: None,
            status: SearchStatus::None,
            info: Vec::new(),
        }
    }
}