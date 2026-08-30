mod play;
mod update;
mod autoplay;
mod types;
pub use types::*;
mod undo;
pub use undo::GameLog;
mod nnue;



#[derive(Clone)]
pub struct Game {

    // game info
    pub board: Board,
    pub en_passant: Option<u8>,
    pub castle: [[bool; 2]; 2],
    pub rule_50moves: u8,

    // check
    pub check: bool,

    // players
    pub player: Color,
    
    // mode
    pub mode: GameMode,
    
    // king pos
    pub king_pos: [Pos; 2],

    // moves
    pub legal: BitGrid,
    pub cover: BitGrid,
    pub cover_comb: [BitBoard;2],
    pub legal_moves: Vec<Move>,

    // for dynamic update
    pub played: Option<PlayedMove>,
    pub dirty: BitBoard,

    // history
    pub history: Vec<GameLog>,

}

impl Game {
    pub fn new() -> Self {
        let mut game = Game {
            // main game info
            board: Board([
                BR, BH, BB, BQ, BK, BB, BH, BR,
                BP, BP, BP, BP, BP, BP, BP, BP,
                __, __, __, __, __, __, __, __,
                __, __, __, __, __, __, __, __,
                __, __, __, __, __, __, __, __,
                __, __, __, __, __, __, __, __,
                WP, WP, WP, WP, WP, WP, WP, WP,
                WR, WH, WB, WQ, WK, WB, WH, WR,
            ]),
            en_passant: None,
            castle: [[true,true],[true,true]],
            rule_50moves: 0,

            // player
            player: Color::White,

            // check
            check: false,

            // mode
            mode: GameMode::Active,
            
            //(filled by self.update)
            // king pos 
            king_pos: [7*8 + 4, 0*8 + 4],
            // moves
            cover: BitGrid::new(),
            legal: BitGrid::new(),
            cover_comb: [BitBoard::new(), BitBoard::new()],
            legal_moves: Vec::new(),

            // dynamic update
            played: None, 
            dirty: BitBoard::new(),

            // game history
            history: Vec::new(),

        };
        game.update(BitBoard(u64::MAX));
        game
    }
}



pub fn timed<F, T>(f: F) -> T 
where F: FnOnce() -> T {
    let start = std::time::Instant::now();
    let result = f();
    println!("took: {:?}", start.elapsed());
    result
}
