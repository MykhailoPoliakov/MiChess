
pub mod game;
pub use game::Game;

fn timed<F, T>(f: F) -> T 
where F: FnOnce() -> T {
    let start = std::time::Instant::now();
    let result = f();
    println!("took: {:?}", start.elapsed());
    result
}


fn main() -> () {

    let mut game = Game::new();

    timed(|| game.play(((6,0), (4,0))));
    // timed(|| game.undo());
    // timed(|| game.play(((6,4), (4,4))));
    
    // timed(|| game.play(((1,4), (3,4))));
    // timed(|| game.play(((7,6), (5,5))));
    // timed(|| game.play(((0,1), (2,2))));
    // timed(|| game.play(((7,5), (4,2))));

    // timed(|| game.autoplay());



    println!("\n\n\n");
    println!("Pl cover :\n{}", game.cover_comb[game.player as usize]);
    println!("Op cover :\n{}", game.cover_comb[game.player.opp() as usize]);
    println!("Board :\n{}", game.board);
    println!("Game history length : {}", game.history.len());
    println!("Updated moves :\n{}", game.dirty);
    println!("Mode : {:?}", game.mode);

}
