pub mod state;
pub use state::{GameState, play, autoplay};



fn main() -> () {
    let mut gamestate = GameState::new();

    gamestate.game.legal.print("Legal");
    gamestate.game.w_cover.print("Cover w");
    autoplay(&mut gamestate.game, 0);

    println!("{}", gamestate.game.board);
}
