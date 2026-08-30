use super::*;



mod analyze;
use analyze::{analyze};
mod evaluate;
mod choose_move;
use choose_move::choose_move;



struct Config {
    init_player: Color,
    max_depth: i8
}

struct MoveInfo {
    liquidity: i8,
    depth: i8,
    way: Vec<Move>,
}


impl Game {
    pub fn autoplay(&mut self) -> () {
        // clone for safety
        let game = &mut self.clone(); 

        let mut moves_iterated: Vec<i32> = Vec::new();

        let config = Config { init_player: game.player, max_depth: 2 };

        let mut moves: Vec<(Move, i32)> = Vec::new(); 

        // iterating through all legal moves
        for &mv in &self.legal_moves {
            if game.play(mv) {
                let mut iterated = 0;
                
                let info = MoveInfo { liquidity: 2, depth: 1, way: vec![mv] };
                let value = 0; //analyze(&config, game, &info, &mut iterated);

                moves_iterated.push(iterated);

                moves.push((mv, value));
                game.undo();
            } 
        }

        // make move
        let mv: Move = choose_move(&mut moves);
        self.play(mv);

        // console ouput
        println!("\nIteratrions done : {:?}", moves_iterated);
        println!("\n---Bot makes move!---\nchosen move: {mv:?}\n");
    }
}








fn print_visual_horisontal() {
    println!("\n          Autoplay");
    println!("{}{}{}", "┌───","───┬───".repeat(18), "───┐" );
}




