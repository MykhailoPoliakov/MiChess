pub use super::types::*;
pub use super::{Game, GameMode};


#[derive(Clone)]
pub struct GameLog {
    pub board: Board,
    pub en_passant: Option<i8>,
    pub castle: [[bool;2];2],
    pub player: Color,
    pub mode: GameMode,
    pub rule_50moves: u8,
}


impl Game {
    pub fn save(&self) -> GameLog {
        GameLog {
            board: self.board.clone(),
            en_passant: self.en_passant,
            castle: self.castle,
            player: self.player,
            mode: self.mode,
            rule_50moves: self.rule_50moves,
        }
    }

    pub fn load(&mut self, log: GameLog) -> () {
        self.board = log.board;
        self.en_passant = log.en_passant;
        self.castle = log.castle;
        self.player = log.player;
        self.mode = log.mode;
        self.rule_50moves = log.rule_50moves;

    }

    pub fn undo(&mut self) -> bool {
        if !self.history.is_empty() {
            let log = self.history.pop().unwrap();
            self.load(log);
            self.update();
            true
        } else {
            false
        }
        
        
    }
}