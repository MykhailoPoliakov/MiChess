pub mod state;
pub use state::{Game, info, movement, check_move, bot_play, evaluate};

fn test() -> () {
    let  mut game = Game::new();
    game.board = [
                [('b','r'), ('b','h'), ('b','b'), (' ',' '), ('b','k'), ('b','b'), ('b','h'), ('b','r')],
                [('b','p'), ('b','p'), ('b','p'), (' ',' '), ('b','p'), ('b','p'), ('b','p'), ('b','p')],
                [(' ',' '), (' ',' '), (' ',' '), (' ',' '), ('b','q'), (' ',' '), (' ',' '), (' ',' ')],
                [(' ',' '), (' ',' '), (' ',' '), ('b','p'), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [(' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [(' ',' '), (' ',' '), (' ',' '), ('w','p'), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [('w','p'), ('w','p'), ('w','p'), (' ',' '), ('w','r'), ('w','p'), ('w','p'), ('w','p')],
                [('w','p'), ('w','h'), ('w','b'), ('w','q'), ('w','k'), ('w','b'), ('w','h'), ('w','r')],
    ];

    movement(&mut game, &(6,4), &(4,4), false);

    // info(&mut game);

    println!("w_cover");
    for i in &game.w_cover {
        println!("{:?}", i);
    }

    println!("b_cover");
    for i in &game.b_cover {
        println!("{:?}", i);
    }

    let pos_value = evaluate( &game);
    println!("{:?}", pos_value)
}


fn main() -> () {
    test();
}
