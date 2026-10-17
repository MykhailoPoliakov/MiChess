use super::*;

pub struct GameLog {
    pub state: GameState,
    pub played: Option<PlayedMove>,
}
