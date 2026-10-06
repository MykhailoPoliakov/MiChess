mod play;
mod update;
mod search;
mod types;
pub use types::*;
mod with_std;
mod undo;
pub use undo::GameLog;
mod nnue;
pub use nnue::{Nnue, Transformer};
mod nnue_file;
pub use nnue_file::NNUE;




pub struct Game {
    pub state: GameState,
    pub played: Option<PlayedMove>,
    pub cache: GameCache,

    pub history: Vec<GameLog>,
    pub transformer: Transformer,
    pub seed: u64,
    pub search: SearchInfo,
}





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


pub struct GameCache {
    // update with self.update
    pub legal: BitGrid,
    pub cover: BitGrid,
    pub cover_comb: [BitBoard;2],
    pub legal_moves: Vec<Move>,
    pub king_pos: [Pos; 2],
    pub check: bool,
}



impl Game {
    pub fn new(state: GameState, seed: u64) -> Self {
        let transformer = Transformer::new(&NNUE, &state.board, state.board.king_pos());

        let mut game = Game {
            state,
            played: None,
            cache: GameCache {
                check: false,
                king_pos: [64;2],
                cover: BitGrid::new(),
                legal: BitGrid::new(),
                cover_comb: [BitBoard::new(), BitBoard::new()],
                legal_moves: Vec::new(),
            },
            history: Vec::new(),
            transformer,
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
