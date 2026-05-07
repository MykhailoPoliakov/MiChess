// Saves all the info about the game
#[derive(Clone)]
pub struct Game {

    // game info
    pub board: [[(char,char);8];8],
    pub en_passant: i8,
    pub castle: [[bool;2];2],
    pub check: bool,

    // info for stoping the game
    pub mode: char,
    pub moves_amount: i16,
    
    // players
    pub player: char,
    pub opponent: char,

    // moves
    pub w_cover: [[Vec<(i8,i8)>;8];8],
    pub b_cover: [[Vec<(i8,i8)>;8];8],
    pub legal:   [[Vec<(i8,i8)>;8];8],

    // history
    pub captured: Vec<(char,char)>,
    pub history: Vec<[[(char,char);8];8]>,

}

impl Game {
    pub fn new() -> Self {
        Game {
            // starting board
            board: [
                [('b','r'), ('b','h'), ('b','b'), ('b','q'), ('b','k'), ('b','b'), ('b','h'), ('b','r')],
                [('b','p'), ('b','p'), ('b','p'), ('b','p'), ('b','p'), ('b','p'), ('b','p'), ('b','p')],
                [(' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [(' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [(' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [(' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' '), (' ',' ')],
                [('w','p'), ('w','p'), ('w','p'), ('w','p'), ('w','p'), ('w','p'), ('w','p'), ('w','p')],
                [('w','r'), ('w','h'), ('w','b'), ('w','q'), ('w','k'), ('w','b'), ('w','h'), ('w','r')],
            ],
            
            // game info
            en_passant: -1,
            castle: [[true,true],[true,true]],
            check: false,

            // info for stoping the game
            mode: 'g',
            moves_amount: 0,

            // players
            player: 'w',
            opponent: 'b',

            // moves
            w_cover: std::array::from_fn(|_| std::array::from_fn(|_| Vec::new())),
            b_cover: std::array::from_fn(|_| std::array::from_fn(|_| Vec::new())),
            legal:   std::array::from_fn(|_| std::array::from_fn(|_| Vec::new())),
            
            // history
            captured: Vec::new(),
            history: Vec::new(),
        }
    }


    // get player cover
    pub fn pl_cover(&mut self) -> &mut [[Vec<(i8,i8)>;8];8] {
        if self.player == 'w' {
            return &mut self.w_cover;
        } else {
            return &mut self.b_cover;
        }
    }

    // get opponent cover
    pub fn op_cover(&mut self) -> &mut [[Vec<(i8,i8)>;8];8] {
        if self.player == 'b' {
            return &mut self.w_cover;
        } else {
            return &mut self.b_cover;
        }
    }
}



