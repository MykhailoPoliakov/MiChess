mod piece;
pub use piece::{Color,Role,Piece};
mod board;
pub use board::Board;
mod bitgrid;
pub use bitgrid::{BitBoard,BitGrid};


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


#[derive(Copy, Clone)]
pub struct PlayedMove {
    pub mv: Move,
    pub tp: MoveType,
    pub captured: Option<Piece>,

}

#[derive(Copy, Clone)]
pub enum MoveType {
    Basic,
    Promotion,
    Castle(Move),
    EnPassant,
}








#[derive(Clone, Copy, PartialEq, Debug)]
pub enum GameMode {
    Active,
    Finished(Option<Color>),
}