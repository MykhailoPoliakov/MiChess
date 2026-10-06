use super::*;

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


pub fn move_to_str(mv: Move) -> String {
    format!("{} {}", pos_to_str(mv.0), pos_to_str(mv.1))
}

pub fn pos_to_str(pos: Pos) -> String {
    let col = (b'a' + pos % 8) as char;
    let row = 8 - pos / 8;
    format!("{}{}", col, row)
}


#[derive(Copy, Clone)]
pub struct PlayedMove {
    pub mv: Move,
    pub tp: MoveType,
    pub captured: Option<Piece>,
    pub old_en_passant: Option<u8>,
    pub old_castle: [[bool; 2]; 2],
}


#[derive(Copy, Clone, PartialEq)]
pub enum MoveType {
    Basic,
    Promotion,
    Castle(Move),
    EnPassant,
}


#[derive(Copy, Clone, PartialEq)]
pub enum MoveError {
    WrongMode,
    NoPiece,
    IlligalMove,
    KingInDanger,
}
    