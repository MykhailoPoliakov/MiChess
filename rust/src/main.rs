
pub mod state;
pub use state::{Game, autoplay};

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

    timed(|| game.play(((6, 3), (5, 3))));


    println!("Legal :\n{}", game.legal);
    println!("Pl cover :\n{}", game.cover(game.player));

    // timed(|| autoplay(&mut game, 0));

    println!("Board :\n{}", game.board);
    println!("Game history length : {}", game.history.len());
}
