pub mod game;
pub use game::{Game, Piece};

pub mod play_fn;
pub use play_fn::play;

pub mod autoplay_fn;
pub use autoplay_fn::autoplay;
