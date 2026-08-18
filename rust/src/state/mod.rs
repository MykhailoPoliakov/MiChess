pub mod game;
pub use game::{Game, Piece};

pub mod play_fn;
pub use play_fn::play;

pub mod autoplay_fn;
pub use autoplay_fn::autoplay;



pub struct GameState {
   pub history: Vec<[[Option<Piece>;8];8]>,
   pub game: Game,
}

impl GameState {
    pub fn new() -> Self {
        GameState {
            history: Vec::new(),
            game: Game::new(),
        }
    }
}

