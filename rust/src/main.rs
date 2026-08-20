
pub mod state;
pub use state::{Game, play, autoplay};

fn timed<F, T>(f: F) -> T 
where F: FnOnce() -> T {
    let start = std::time::Instant::now();
    let result = f();
    println!("took: {:?}", start.elapsed());
    result
}

fn main() -> () {

    let mut game = Game::new();

    // timed(|| game.update());

    timed(|| play(&mut game, ((6, 3), (5, 3)), true));

    // game.legal.print("Legal");
    // game.w_cover.print("Cover w");

    // timed(|| autoplay(&mut game, 0));

    println!("{}", game.board);
}
