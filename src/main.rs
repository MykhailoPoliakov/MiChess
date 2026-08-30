
pub mod core;
pub use core::{Game, timed};


fn play(game: &mut Game, mv: ((u8, u8),(u8, u8))) -> () {
   timed(|| game.play(((mv.0.0*8 + mv.0.1), (mv.1.0*8 + mv.1.1)))); 
}


fn main() -> () {

    let mut game = Game::new();

    // timed(|| game.play((52, 36))); // e2-e4
    // timed(|| game.play((12, 28))); // e7-e5
    // timed(|| game.play((62, 45))); // g1-f3
    // timed(|| game.play((1, 18)));  // b8-c6
    // timed(|| game.play((61, 34))); // f1-c4
    // timed(|| game.play((5, 26)));  // f8-c5
    
    // timed(|| game.undo());
    // timed(|| game.undo());
    // timed(|| game.undo());

    // timed(|| game.play((1, 18)));  // b8-c6
    // timed(|| game.play((61, 34))); // f1-c4
    // timed(|| game.play((5, 26)));  // f8-c5

    play(&mut game, ((6, 4), (4, 4)));
    play(&mut game, ((1, 4), (3, 4)));

    timed(|| game.autoplay());



    println!("\n\n\n");
    println!("Pl cover :\n{}", game.cover_comb[game.player as usize]);
    println!("Op cover :\n{}", game.cover_comb[game.player.opp() as usize]);
    println!("Board :\n{}", game.board);
    println!("Game history length : {}", game.history.len());
    println!("Updated moves :\n{}", game.dirty);
    println!("Mode : {:?}", game.mode);

}
