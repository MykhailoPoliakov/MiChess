mod update_fn;
mod types;
mod constants;
pub use types::*;
pub use constants::*;


#[derive(Clone, PartialEq)]
pub enum GameMode {
    Active,
    Finished(Option<Color>),
}



#[derive(Clone)]
pub struct Game {

    // game info
    pub board: Board,
    pub en_passant: Option<i8>,
    pub castle: [[bool; 2]; 2],
    pub check: bool,

    // kings
    pub king_pos: [Pos; 2],

    // info for stoping the game
    pub mode: GameMode,
    pub rule_50moves: u8,
    
    // players
    pub player: Color,

    // moves
    pub w_cover: Grid,
    pub b_cover: Grid,
    pub legal:   Grid,

}

impl Game {
    pub fn new() -> Self {
        let mut game = Game {
            // starting board
            board: Board([
                [BR, BH, BB, BQ, BK, BB, BH, BR],
                [BP, BP, BP, BP, BP, BP, BP, BP],
                [__, __, __, __, __, __, __, __],
                [__, __, __, __, __, __, __, __],
                [__, __, __, __, __, __, __, __],
                [__, __, __, __, __, __, __, __],
                [WP, WP, WP, WP, WP, WP, WP, WP],
                [WR, WH, WB, WQ, WK, WB, WH, WR],
            ]),
            
            // game info
            en_passant: None,
            castle: [[true,true],[true,true]],
            check: false,

            //kings
            king_pos: [(7,4), (0,4)],

            // info for stoping the game
            mode: GameMode::Active,
            rule_50moves: 0,

            // player
            player: Color::White, //attacker

            // moves
            w_cover: Grid::new(),
            b_cover: Grid::new(),
            legal:   Grid::new(),
        };
        game.update();
        game
    }


    // get player cover
    pub fn cover(&self, color: Color) -> &Grid {
        match color {
            Color::White => &self.w_cover,
            Color::Black => &self.b_cover
        }
    }
}

