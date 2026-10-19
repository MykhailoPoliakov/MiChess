use super::*;

mod analyze;
mod eval;
mod choose_move;

pub struct SearchContex {
    pub init_player: Color,
    pub depth: i8,
    pub iterated: i32,
}


impl Game {
    pub fn start_search(&mut self) {
        self.search = SearchInfo::new();
        let total_moves = self.cache.legal_moves.len() as f32;
        
        let mut ctx = SearchContex { init_player: self.state.player, depth: 1, iterated: 0};

        let mut game = Game::new(self.state.clone(), self.seed);

        // playing all legal moves and getting move value
        for mv in self.cache.legal_moves.clone() {
            game.play(mv);

            ctx.iterated = 0;
            let value = game.analyze(&mut ctx);
            
            self.search.moves.push((mv, Eval::from_value(value), ctx.iterated));
            self.search.status = self.search.moves.len() as f32 / total_moves;

            game.undo();
        }

        self.search.moves.sort_by(|a, b| b.1.cmp(&a.1));
        self.search.status = 1.1;
    }
}




