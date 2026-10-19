use super::*;


#[derive(Clone, Copy, Debug)]
pub enum Eval {
    Value(f32),
    Mate(i8)
}


impl Eval {
    pub fn from_value(value: i32) -> Self {
        if value >= 1_000_000 {
            panic!()
        }
        match value.abs() {
            v if v >= 999_900 => Eval::Mate(((1_000_000 - v) * value.signum()) as i8),
            _ => Eval::Value((value as f32 / 400.0).tanh()),
        }
    }
}

use core::cmp::Ordering;

impl PartialEq for Eval {
    fn eq(&self, other: &Self) -> bool {
        self.cmp(other) == Ordering::Equal
    }
}

impl Eq for Eval {}

impl PartialOrd for Eval {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}


impl Ord for Eval {
    fn cmp(&self, other: &Self) -> Ordering {
        match (self, other) {
            // values
            (Eval::Value(a), Eval::Value(b)) => a.total_cmp(b),
            
            // mates 
            (Eval::Mate(a), Eval::Mate(b)) if *a > 0 && *b > 0 => a.cmp(b),
            
            // negative mates
            (Eval::Mate(a), Eval::Mate(b)) if *a < 0 && *b < 0 => b.cmp(a),
            
            // positive / negative mate
            (Eval::Mate(a), Eval::Mate(b)) => a.cmp(b),
            
            // positive mate / value
            (Eval::Mate(a), Eval::Value(_)) if *a > 0 => Ordering::Greater,
            (Eval::Value(_), Eval::Mate(b)) if *b > 0 => Ordering::Less,
            
            // negative mate / value
            (Eval::Mate(a), Eval::Value(_)) if *a < 0 => Ordering::Less,
            (Eval::Value(_), Eval::Mate(b)) if *b < 0 => Ordering::Greater,
                    
            _ => Ordering::Equal,
        }
    }
}




#[derive(Clone)]
pub struct SearchInfo {
    pub status: f32,
    pub moves: Vec<(Move, Eval, i32)>, // i32 - Iteration count
}

impl SearchInfo {
    pub fn new() -> Self {
        SearchInfo { 
            status: 0.0,
            moves: Vec::new(),
        }
    }

    pub fn eval(&self, color: Color) -> Option<Eval> {
        match color {
            Color::White => self.moves.first().map(|(_, eval, _)| *eval),
            Color::Black => self.moves.last().map(|(_, eval, _)| *eval)
        }
            
    }

    pub fn mv(&self, color: Color) -> Option<Move> {
        match color {
            Color::White => self.moves.first().map(|(mv, _, _)| *mv),
            Color::Black => self.moves.last().map(|(mv, _, _)| *mv)
        }
        
    }
}