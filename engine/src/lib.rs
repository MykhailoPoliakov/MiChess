mod play;
mod update;
mod search;
mod types;
pub use types::*;
mod with_std;


pub struct Game {
    pub state: GameState,
    pub played: Option<PlayedMove>,
    pub cache: GameCache,

    pub history: Vec<GameLog>,
    pub seed: u64,
    pub search: SearchInfo,
}



impl Game {
    pub fn new(state: GameState, seed: u64) -> Self {
        let mut game = Game {
            state,
            played: None,
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




// for testing
pub fn timed<F, T>(f: F) -> T 
where F: FnOnce() -> T {
    let start = std::time::Instant::now();
    let result = f();
    println!("took: {:?}", start.elapsed());
    result
}
