use super::*;



pub struct GameCache {
    // update with self.update
    pub legal: BitGrid,
    pub cover: BitGrid,
    pub cover_comb: [BitBoard;2],
    pub legal_moves: Vec<Move>,
    pub king_pos: [Pos; 2],
    pub check: bool,
}


impl GameCache {
    pub fn new() -> Self {
        GameCache {
            check: false,
            king_pos: [64;2],
            cover: BitGrid::new(),
            legal: BitGrid::new(),
            cover_comb: [BitBoard::new(), BitBoard::new()],
            legal_moves: Vec::new(),
        }
    }
}