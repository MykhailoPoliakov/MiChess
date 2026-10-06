use super::*;

mod analyze;
mod eval;
mod choose_move;


pub struct Contex {
    pub init_player: Color,
    pub depth: i8,
    pub iterated: i32,
}


impl Game {
    pub fn start_search(&mut self) {
        self.search = SearchInfo::new();
        let total_moves = self.cache.legal_moves.len() as f32;
        
        let mut ctx = Contex { init_player: self.state.player, depth: 1, iterated: 0};

        let mut game = Game::new(self.state.clone(), self.seed);

        // playing all legal moves and getting move value
        for mv in self.cache.legal_moves.clone() {
            game.play(mv);

            ctx.iterated = 0;
            let value = game.analyze(&mut ctx);
            
            self.search.moves.push((mv, Eval::from_value(value), ctx.iterated));
            self.search.status = SearchStatus::InProgress(self.search.moves.len() as f32 / total_moves);

            game.undo();
        }


        self.search.status = SearchStatus::Finished;
        self.search.result = Some( SearchResult { 
            mv: self.choose_move(),
            eval: match self.state.player {
                Color::White => self.search.moves.iter().max_by_key(|x| x.1),
                Color::Black => self.search.moves.iter().min_by_key(|x| x.1),
            }.unwrap().1
        });
    }
}




