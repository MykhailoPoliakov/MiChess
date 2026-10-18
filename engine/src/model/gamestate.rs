use super::*;





#[derive(Clone, Copy, PartialEq, Debug)]
pub enum GameMode {
    Active,
    Finished(Option<Color>),
}


#[derive(Clone)]
pub struct GameState {
    pub board: Board,
    pub en_passant: Option<u8>,
    pub castle: u8,
    pub rule_50moves: u8,
    pub player: Color,
    pub mode: GameMode,
}

impl Default for GameState {
    fn default() -> Self {
        GameState { 
            board: Board::default(),
            en_passant: None,
            castle: 0b1111,
            rule_50moves: 0,
            player: Color::White,
            mode: GameMode::Active,
        }
    }
}