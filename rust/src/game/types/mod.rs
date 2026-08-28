mod piece;
pub use piece::{Color,Role,Piece};
mod board;
pub use board::Board;
mod bitgrid;
pub use bitgrid::{BitBoard,BitGrid};
mod pos;



pub type Pos = (i8,i8);
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