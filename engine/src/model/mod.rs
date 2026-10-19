mod base;
pub use base::*;
mod search;
pub use search::{SearchInfo, Eval};
mod gamecache;
pub use gamecache::GameCache;
mod gamestate;
pub use gamestate::{GameState, GameMode};





pub struct Game {
    pub state: GameState,
    pub cache: GameCache,

    pub history: Vec<PlayedMove>,
    pub seed: u64,
    pub search: SearchInfo,
}

impl Game {
    pub fn new(state: GameState, seed: u64) -> Self {
        let mut game = Game {
            state,
            cache: GameCache::new(),
            history: Vec::new(),
            seed,
            search: SearchInfo::new(),
        };
        game.update();
        game
    }
}

impl Default for Game {
    fn default() -> Self {
        Game::new(GameState::default(), 0x71F2_9A3C_5B44)
    }
}


