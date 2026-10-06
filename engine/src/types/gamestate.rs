use super::*;

#[derive(Clone)]
pub struct GameState {
    pub board: Board,
    pub en_passant: Option<u8>,
    pub castle: [[bool; 2]; 2],
    pub rule_50moves: u8,
    pub player: Color,
    pub mode: GameMode,
}

impl Default for GameState {
    fn default() -> Self {
        GameState { 
            board: Board::default(),
            en_passant: None,
            castle: [[true,true],[true,true]],
            rule_50moves: 0,
            player: Color::White,
            mode: GameMode::Active,
        }
    }
}