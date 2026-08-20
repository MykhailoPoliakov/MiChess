mod update_fn;
mod types;
mod constants;
pub use types::*;
pub use constants::*;


mod log;
pub use log::GameLog;





#[derive(Clone, Copy, PartialEq)]
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

    // move logs

}

impl Game {
    pub fn new() -> Self {
        let mut game = Game {
            // game info
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
            en_passant: None,
            castle: [[true,true],[true,true]],
            check: false,

            // player
            player: Color::White,

            // info for stoping the game
            mode: GameMode::Active,
            rule_50moves: 0,

            // moves and king pos (filled by self.update)
            king_pos: [(7,4), (0,4)],
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

