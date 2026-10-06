use super::*;

#[derive(Clone)]
pub struct SearchResult {
    pub mv: Move,
    pub eval: Eval,
} 


#[derive(Clone)]
pub enum SearchStatus {
    None,
    InProgress(f32),
    Finished,
}


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

impl PartialEq for Eval {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Eval::Value(a), Eval::Value(b)) => a == b,
            (Eval::Mate(a), Eval::Mate(b)) => a == b,
            _ => false,
        }
    }
}

impl Eq for Eval {}

impl PartialOrd for Eval {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Eval {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        match (self, other) {
            (Eval::Value(a), Eval::Value(b)) => a.total_cmp(b),
            (Eval::Mate(a), Eval::Mate(b)) => a.cmp(b),

            // Mate is better than any normal evaluation
            (Eval::Mate(_), Eval::Value(_)) => std::cmp::Ordering::Greater,
            (Eval::Value(_), Eval::Mate(_)) => std::cmp::Ordering::Less,
        }
    }
}




#[derive(Clone)]
pub struct SearchInfo {
    pub result: Option<SearchResult>,
    pub status: SearchStatus,
    pub moves: Vec<(Move, Eval, i32)>, // i32 - Iteration count
}

impl SearchInfo {
    pub fn new() -> Self {
        SearchInfo { 
            result: None,
            status: SearchStatus::None,
            moves: Vec::new(),
        }
    }
}