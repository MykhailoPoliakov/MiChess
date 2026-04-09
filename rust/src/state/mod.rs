mod game_class;
pub use self::game_class::Game;

// CONSTANTS

// const DRAW_PIECES: [&'static str;6] = ["br", "bq", "bp", "wr", "wq", "wp"];
pub const ALL_POS: [(i8, i8); 64] = [
    (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7),
    (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7),
    (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7),
    (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),
    (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7),
    (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7),
    (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7),
    (7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7),
];

// STATE class

pub struct State {
    pub histiry_bool: bool, 
}

// State functions
mod info_fn;
mod play_fn;
mod bot_fn;


impl State {
    pub fn new() -> Self {
        State {
            histiry_bool: false,
        }
    }

    pub fn opponent(&self, player: char) -> char {
        match player {
            'w' => return 'b',
            _   => return 'w',
        }
    }

    pub fn history_push(&self, game: &mut Game ) {
        game.history.push( game.board.clone());
    }
}



// INTERFACE class

pub struct Interface {
    state: State,
    game: Game,
}


impl Interface {
    pub fn new() -> Self {
        Interface {
            state: State::new(),
            game: Game::new(),
        }
    }

    pub fn init(&mut self) {
        self.state.info( &mut self.game);
        self.game.history.push(self.game.board.clone());
    }

    pub fn play(&mut self, start_pos: (i8,i8), end_pos: (i8,i8) ) {
        self.state.play(&mut self.game, start_pos, end_pos);
    }

    pub fn bot_play(&mut self) {
        self.state.bot_play(& mut self.game, 0 );
    }

    pub fn board(&self) -> [[(char,char);8];8] {
        println!("board");
        for row in self.game.board {
            for cell in row {
                print!("{} ", cell.0);
                print!("{} ", cell.1);
                print!(" ");
            }
            println!();
        }
        return self.game.board;
    } 

    pub fn cover_moves(&self) {
        println!("w_cover");
        for row in &self.game.w_cover {
            for cell in row {
                print!("{:?} ", cell);
            }
            println!();
        }

        println!("b_cover");
        for row in &self.game.b_cover {
            for cell in row {
                print!("{:?} ", cell);
            }
            println!();
        }
    }

    pub fn legal_moves(&self) {
        println!("legal");
        for row in &self.game.legal {
            for cell in row {
                print!("{:?} ", cell);
            }
            println!();
        }
    }
}

