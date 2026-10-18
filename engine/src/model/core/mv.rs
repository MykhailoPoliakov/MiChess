use super::{Piece, Role, Castle};

pub type Pos = u8;

pub trait PosExt {
    fn row(self) -> u8;
    fn col(self) -> u8;
}

impl PosExt for u8 {
    fn row(self) -> u8 { self / 8 }
    fn col(self) -> u8 { self % 8 }
}


pub type Move = (Pos, Pos);

pub fn str_to_move(pos: &str) -> (u8, u8) {
    let bytes = pos.as_bytes();
    ((b'8' - bytes[1])*8 + (bytes[0] - b'a'), (b'8' - bytes[3])*8 + (bytes[2] - b'a'))
}

pub fn move_to_str(mv: Move) -> String {
    format!("{} {}", pos_to_str(mv.0), pos_to_str(mv.1))
}

pub fn pos_to_str(pos: Pos) -> String {
    let col = (b'a' + pos % 8) as char;
    let row = 8 - pos / 8;
    format!("{}{}", col, row)
}


#[derive(Copy, Clone, PartialEq)]
pub enum MoveType {
    Basic,
    Promotion(Role),
    Castle((Pos,Pos)),
    EnPassant,
}


#[derive(Copy, Clone)]
pub struct PlayedMove {
    pub mv: Move,
    pub tp: MoveType,
    pub captured: Option<Piece>,
    pub old_en_passant: Option<u8>,
    pub old_castle: Castle,
}


#[derive(Copy, Clone, PartialEq)]
pub enum MoveError {
    WrongMode,
    NoPiece,
    IlligalMove,
    NoPromotionPiece
}


pub struct Mv {
    pub st: Pos,
    pub end: Pos,
    pub tp: MoveType
}

impl Mv {
    pub fn new(st: Pos, end: Pos) -> Self {
        Mv {
            st,
            end,
            tp: MoveType::Basic
        }
    }


    pub fn from_str(pos: &str) -> Self {
        let bytes = pos.as_bytes();
        Mv::new((b'8' - bytes[1])*8 + (bytes[0] - b'a'), (b'8' - bytes[3])*8 + (bytes[2] - b'a'))
    }

    pub fn to_str(&self) -> String {
        format!("{} {}", pos_to_str(self.st), pos_to_str(self.end))
    }
}
    