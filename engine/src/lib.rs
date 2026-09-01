mod play;
mod update;
mod autoplay;
mod types;
pub use types::*;
mod state;
pub use state::State;
mod undo;
pub use undo::GameLog;
mod nnue;



#[derive(Clone)]
pub struct Game {

    // game info
    pub(crate) board: Board,
    pub(crate) en_passant: Option<u8>,
    pub(crate) castle: [[bool; 2]; 2],
    pub(crate) rule_50moves: u8,

    // check
    pub(crate) check: bool,

    // players
    pub(crate) player: Color,
    
    // mode
    pub(crate) mode: GameMode,
    
    // king pos
    pub(crate) king_pos: [Pos; 2],

    // moves
    pub(crate) legal: BitGrid,
    pub(crate) cover: BitGrid,
    pub(crate) cover_comb: [BitBoard;2],
    pub(crate) legal_moves: Vec<Move>,

    // for dynamic update
    pub(crate) played: Option<PlayedMove>,
    pub(crate) dirty: BitBoard,

    // history
    pub(crate) history: Vec<GameLog>,

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
