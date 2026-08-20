use super::*;

// constants of how pieces move
const ROOK_MOVES: [Pos; 4] = [(1, 0), (-1, 0), (0, -1), (0, 1)];
const BISHOP_MOVES: [Pos; 4] = [(1, -1), (-1, 1), (-1, -1), (1, 1)];
const KNIGHT_MOVES: [Pos; 8] = [(1, -2), (-1, 2), (-1, -2), (1, 2), (2, -1), (-2, 1), (-2, -1), (2, 1)];
const KING_MOVES: [Pos; 8] = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, 1), (-1, -1), (1, 1)];


// Analyses the board, saves all the game.legal moves and covers for exact board position.
// Changes: game.game.legal , game.w_cover , game.b_cover

impl Game {
    pub fn update(&mut self) -> () {

        // cleaning
        self.w_cover.clean();
        self.b_cover.clean();
        self.legal.clean();

        // start iteration
        for pos in ALL_POS {
            match self.board[pos] {
                Some(piece) => {
                    // get variables 
                    let pl_cover = match piece.color {Color::White => &mut self.w_cover, Color::Black => &mut self.b_cover};

                    // match every piece
                    match piece.role {
                        Role::Pawn => {

                            let direction: i8 = match piece.color { Color::White => -1, Color::Black =>  1 };

                            if !valid_int(pos.0 + direction) {
                                continue;
                            }

                            // cover
                            for side in [1 as i8,-1 as i8] {
                                let target = (pos.0 + direction, pos.1 + side);
                                if valid_int(target.1) {
                                    pl_cover[target].push( pos );
                                }
                            }


                            // one move ahead
                            let target: Pos = (pos.0 + direction, pos.1);
                            if self.board[target].is_none() {
                                self.legal[pos].push(target);
                                // two moves ahead
                                let target: Pos = (pos.0 + direction*2, pos.1);
                                if valid_int(target.1) && self.board[target].is_none() &&
                                match piece.color { Color::White => pos.0 == 6, Color::Black => pos.0 == 1 } {
                                    self.legal[pos].push(target);
                                }
                            }

                            // capture
                            for side in [1 as i8,-1 as i8] {
                                let target: Pos = (pos.0 + direction, pos.1 + side);

                                if valid_int(target.1) &&
                                self.board[target].is_some_and(|p| p.color == piece.color.opp()) {
                                    self.legal[pos].push(target);
                                }
                            }

                            // en passant
                            if match piece.color { Color::White => pos.0 == 3, Color::Black => pos.0 == 4 } {
                                for side in [1 as i8,-1 as i8] {
                                    let target = (pos.0 + direction, pos.1 + side);

                                    if valid_int(target.1) &&
                                    self.board[target].is_some_and(|p| p.color == piece.color.opp()) &&
                                    self.en_passant == Some(target.1) {
                                        self.legal[pos].push(target);
                                    }
                                }
                            }
                        }
                        Role::Knight => {

                            for num in KNIGHT_MOVES {
                                let target: Pos = (pos.0 + num.0, pos.1 + num.1);
                                if target.0 >= 0 && target.0 < 8 && target.1 >= 0 && target.1 < 8 {
                                    // cover
                                    pl_cover[target].push( pos );
                                    // game.legal
                                    if !self.board[target].is_some_and(|p| p.color == piece.color) {
                                        self.legal[pos].push(target);
                                    }
                                }
                            }
                        }
                        Role::Bishop => {

                            for direction in BISHOP_MOVES {
                                for i in 1..8 {
                                    let target = (pos.0 + i*direction.0, pos.1 + i*direction.1);
                                    if valid(target) {
                                        // cover 
                                        pl_cover[target].push( pos );
                                        // game.legal
                                        if self.board[target].is_some_and(|p| p.color == piece.color) {
                                            break
                                        }
                                        self.legal[pos].push( target );
                                        // stop
                                        if !self.board[target].is_some_and(|p| p.color == piece.color.opp() && p.role == Role::King) {
                                            break
                                        }
                                    }
                                } 
                            }
                        }
                        Role::Rook => {

                            for direction in ROOK_MOVES {
                                for i in 1..8 {
                                    let target = (pos.0 + i*direction.0, pos.1 + i*direction.1);
                                    if valid(target) {
                                        // cover 
                                        pl_cover[target].push( pos );
                                        // game.legal
                                        if self.board[target].is_some_and(|p| p.color == piece.color) {
                                            break
                                        }
                                        self.legal[pos].push( target );
                                        // stop
                                        if !self.board[target].is_some_and(|p| p.color == piece.color.opp() && p.role == Role::King) {
                                            break
                                        }
                                    }
                                } 
                            }
                        }
                        Role::Queen => {

                            for direction in KING_MOVES {
                                for i in 1..8 {
                                    let target = (pos.0 + i*direction.0, pos.1 + i*direction.1);
                                    if valid(target) {
                                        // cover 
                                        pl_cover[target].push( pos );
                                        // game.legal
                                        if self.board[target].is_some_and(|p| p.color == piece.color) {
                                            break
                                        }
                                        self.legal[pos].push( target );
                                        // stop
                                        if !self.board[target].is_some_and(|p| p.color == piece.color.opp() && p.role == Role::King) {
                                            break
                                        }
                                    }
                                } 
                            }
                        }
                        Role::King => {
                            self.king_pos[piece.color as usize] = pos;
                        }
                    }
                }
                None => {}
            }
        }


        // iterate through kings (cover)
        for pos in self.king_pos {
            // get variables 
            let piece = self.board[pos].unwrap();
            let pl_cover = match piece.color {Color::White => &mut self.w_cover, Color::Black => &mut self.b_cover};
            // check all moves
            for num in KING_MOVES {
                let target = (pos.0 + num.0,pos.1 + num.1);
                if valid(target) {
                    pl_cover[target].push( pos );
                }
            }
        }

        // iterate through kings (game.legal)
        for pos in self.king_pos {
            // get variables 
            let piece = self.board[pos].unwrap();
            let op_cover = match piece.color.opp() {Color::White => &mut self.w_cover, Color::Black => &mut self.b_cover};
            // check all moves
            for num in KING_MOVES {
                let target = (pos.0 + num.0,pos.1 + num.1);
                if valid(target) {
                    if !self.board[target].is_some_and(|p| p.color == piece.color) && 
                    op_cover[target].is_empty() {
                        self.legal[pos].push(target);
                    }
                }
            }

            // castle
            let row: i8 = match piece.color { Color::White => 7, Color::Black => 0 };

            if pos == (row as i8,4) {
                // left
                if self.castle[piece.color as usize][0] {
                    if self.board[(row,3)].is_none() && op_cover[(row,3)].is_empty() &&
                        self.board[(row,2)].is_none() && op_cover[(row,3)].is_empty() &&
                        self.board[(row,1)].is_none() && op_cover[(row,3)].is_empty() &&
                        self.board[(row,0)] == Some(Piece{color: piece.color.clone(), role: Role::Rook}) {
                            self.legal[pos].push((row as i8, 2));
                    }
                } 
                // right
                if self.castle[piece.color as usize][1] {
                    if self.board[(row,5)].is_none() && op_cover[(row,5)].is_empty() &&
                        self.board[(row,6)].is_none() && op_cover[(row,6)].is_empty() &&
                        self.board[(row,7)] == Some(Piece{color: piece.color.clone(), role: Role::Rook}) {
                            self.legal[pos].push((row as i8, 6));
                    }
                }
            }
        }
    }
}





fn valid_int(int: i8) -> bool {
    if int >= 0 && int < 8 {
        true
    } else {
        false
    }
}

fn valid(pos: Pos) -> bool {
    if pos.0 >= 0 && pos.0 < 8 && pos.1 >= 0 && pos.1 < 8{
        true
    } else {
        false
    }
}

