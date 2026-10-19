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
    EnPassant(Pos),
}


#[derive(Copy, Clone)]
pub struct PlayedMove {
    pub mv: Move,
    pub captured: Option<Piece>,
    pub old_en_passant: Option<u8>,
    pub old_castle: Castle,
    pub move_count: u8,
}


#[derive(Copy, Clone, PartialEq)]
pub enum MoveError {
    WrongMode,
    NoPiece,
    IlligalMove,
    NoPromotionPiece
}

#[derive(Copy, Clone, PartialEq)]
pub struct Move {
    pub start: Pos,
    pub end: Pos,
    pub tp: MoveType
}

impl Move {
    pub fn new(start: Pos, end: Pos) -> Self {
        Move {
            start,
            end,
            tp: MoveType::Basic
        }
    }

    pub fn to_str(&self) -> String {
        format!("{}{}", pos_to_str(self.start), pos_to_str(self.end))
    }
}

pub fn str_to_safemove(pos: &str) -> ((u8,u8), Option<Role>) {
    let bytes = pos.as_bytes();

    let role = bytes.get(4).map(|b| match b {
        b'r' => Role::Rook,
        b'b' => Role::Bishop,
        b'n' => Role::Knight,
        _    => Role::Queen,
    });
    (((b'8' - bytes[1])*8 + (bytes[0] - b'a'), (b'8' - bytes[3])*8 + (bytes[2] - b'a')), role)
}
    