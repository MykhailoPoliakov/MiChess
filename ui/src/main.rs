use engine::*;

mod app;


fn play(game: &mut Game, mv: ((u8, u8),(u8, u8))) -> () {
   game.play(((mv.0.0*8 + mv.0.1), (mv.1.0*8 + mv.1.1))); 
}


fn main() -> () {

    let mut game = Game::new();
    
    app::run();

    play(&mut game, ((6, 4), (4, 4)));
    play(&mut game, ((1, 4), (3, 4)));

    timed(|| game.autoplay());

    println!("{}", game);

}
