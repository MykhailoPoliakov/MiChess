mod piece;
pub use piece::*;
mod board;
pub use board::Board;
mod bitgrid;
pub use bitgrid::BitGrid;
mod bitboard;
pub use bitboard::BitBoard;
mod search;
pub use search::*;
mod mv;
pub use mv::*;
mod gamelog;
pub use gamelog::GameLog;
mod gamecache;
pub use gamecache::GameCache;
mod gamestate;
pub use gamestate::GameState;



#[derive(Clone, Copy, PartialEq)]
pub enum GameMode {
    Active,
    Finished(Option<Color>),
}