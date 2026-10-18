use engine::{Game, GameMode, Color};



#[test]
fn game_gufeld_bagirov_1973() {
    let mut game = Game::default();

    let moves = "
        d2d4 g7g6 c2c4 f8g7 b1c3 d7d6 e2e4 g8f6 f2f3 e8g8 c1e3 b8c6 g1e2 a8b8 d1d2 a7a6 e3h6 b7b5 h2h4 e7e5 h6g7 g8g7 h4h5 g7h8 c3d5 b5c4 h5g6 f7g6 d2h6 f6h5 g2g4 b8b2 g4h5 g6g5 h1g1 g5g4 e1c1 b2a2 e2f4 e5f4 d5f4 f8f4 h6f4 c4c3 f1c4 a2a3 f3g4 c6b4 c1b1 c8e6 c4e6 b4d3 f4f7 d8b8 e6b3 a3b3 b1c2 d3b4 c2b3 b4d5 b3c2 b8b2 c2d3 b2b5 d3c2 d5e3 c2c1 b5b2
    ";
    
    game.run(moves);
    game.unrun(5);
    game.run("b2b5 d3c2 d5e3 c2c1 b5b2");

    assert_eq!(game.state.mode, GameMode::Finished(Some(Color::Black)));

    println!("{}", game);
}


#[test]
fn game_mcdonnel_arblay_1830() {
    let mut game = Game::default();

    let moves = "
        e2e4 e7e5 f2f4 e5f4 g1f3 g7g5 f1c4 g5g4 b1c3 g4f3
        e1g1 d7d6 d1f3 c7c6 d2d4 f8h6 c4f7 e8f7 f3h5 f7g7 
        c1f4 h6f4 f1f4 g8f6 h5g5 g7f7 e4e5 d6e5 d4e5 b8d7 
        c3e4 h8g8 g5h5 f7g7 e5f6 g7h8 f4h4 d7f8 e4g5 g8g5 
        h5g5 f8e6 g5h5 d8g8 f6f7 g8g7 h4g4 g7f8 h5e5 e6g7 
        g4g7 f8g7 f7f8q
    ";
    
    game.run(moves);
    game.unrun(10);
    game.run("d8g8 f6f7 g8g7 h4g4 g7f8 h5e5 e6g7 g4g7 f8g7 f7f8q");

    assert_eq!(game.state.mode, GameMode::Finished(Some(Color::White)));

    println!("{}", game);
}


#[test]
fn game_carlsen_grischuk_2016() {
    let mut game = Game::default();

    let moves = "
        d2d4 g8f6 c2c4 e7e6 g1f3 f8b4 b1d2 e8g8 a2a3 b4e7 
        e2e4 d7d6 f1e2 b8d7 d1c2 e6e5 d2b1 c7c5 d4e5 d7e5 
        f3e5 d6e5 b1c3 c8e6 e1g1 d8c7 c1e3 f8d8 c3d5 e6d5 
        c4d5 a8c8 a1c1 f6e8 e2g4 c8b8 e3c5 c7c5 c2c5 e7c5 
        c1c5 e8d6 f2f3 g7g6 h2h4 f7f5 e4f5 g6f5 g4h3 d8d7 
        g2g4 g8f7 g4f5 f7f6 g1f2 b8d8 f2e3 d7g7 h4h5 g7g3 
        h3g4 d8g8 e3f2 g3g4 f3g4 d6e4 f2f3 e4c5 f1c1 c5b3 
        c1c7 b3d4 f3f2 g8g4 c7h7 g4f4 f2e1 e5e4 d5d6 f4f5 
        h5h6 e4e3 d6d7 f5d5 h7g7 d4f5 d7d8q d5d8 g7b7 f5h6 
        b7a7 h6f5
    ";
    
    game.run(moves);

    assert_eq!(game.state.mode, GameMode::Active);

    println!("{}", game);
}
