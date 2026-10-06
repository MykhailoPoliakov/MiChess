use super::*;

mod constants;
use constants::*;




impl Game {
    pub fn eval(&self) -> i32 {
        let mut value = 0;
        let phase = self.get_phase();

        for pos in 0..64 {
            if let Some(piece) = self.state.board[pos] {
                match piece.color {
                    Color::White => {
                        value += eval_material(piece.role);
                        value += eval_value_grid(pos, piece, phase);
                        value += eval_mobility(&self.cache.legal[pos], piece);
                        value += eval_king_attack(pos, self.cache.king_pos[1]);
                        // if pawns protecting the king
                        if phase[1] > 10 && piece.role == Role::Pawn && self.cache.cover[self.cache.king_pos[0]].get(pos) {
                            value += 30
                        }
                    }
                    Color::Black => {
                        value -= eval_material(piece.role);
                        value -= eval_value_grid(pos, piece, phase);
                        value -= eval_mobility(&self.cache.legal[pos], piece);
                        value -= eval_king_attack(pos, self.cache.king_pos[0]);
                        // if pawns protecting the king
                        if phase[0] > 10 && piece.role == Role::Pawn && self.cache.cover[self.cache.king_pos[1]].get(pos) {
                            value -= 30
                        }
                    }
                }
            }
        }

        value += self.eval_pawn_struct();
        value += self.eval_king_safety();
        
        value
    }



    fn get_phase(&self) -> [i8; 2] {
        let mut phase: [i8; 2] = [0; 2];
        for pos in 0..64 {
            if let Some(piece) = self.state.board[pos] {
                match piece.role {
                    Role::Knight => phase[piece.color as usize] += 3,
                    Role::Bishop => phase[piece.color as usize] += 3,
                    Role::Rook   => phase[piece.color as usize] += 5,
                    Role::Queen  => phase[piece.color as usize] += 9,
                    _ => {},
                }
            }
        }
        phase
    }



    fn eval_pawn_struct(&self) -> i32 {
        0
    }



    fn eval_king_safety(&self) -> i32 {
        0
    }



}



// get how much a piece is worth
fn eval_material(role : Role) -> i32 {
    match role {
        Role::Pawn   =>  100,
        Role::Knight =>  300,
        Role::Bishop =>  300,
        Role::Rook   =>  500,
        Role::Queen  =>  900,
        Role::King   => 1500,
    }
}


// use piece grids to get piece pos worth
fn eval_value_grid(pos: Pos, piece: Piece, phase: [i8; 2]) -> i32 {
    match piece.role {
        Role::Pawn   =>  PAWN_VALUE_GRID[piece.color as usize][pos as usize],
        Role::Knight =>  KNIGHT_VALUE_GRID[pos as usize],
        Role::Bishop =>  BISHOP_VALUE_GRID[pos as usize],
        Role::Rook   =>  ROOK_VALUE_GRID[piece.color as usize][pos as usize],
        Role::Queen  =>  QUEEN_VALUE_GRID[pos as usize],
        Role::King   =>  {
            if phase[piece.color.opp() as usize] < 10 {
                KING_ENDGAME_VALUE_GRID[pos as usize]
            } else {
                KING_MIDGAME_VALUE_GRID[piece.color as usize][pos as usize]
            }
        }
    }
}


// the more legal moves the better value
fn eval_mobility(pos_legal: &BitBoard, piece: Piece) -> i32 {
    if piece.role == Role::King || piece.role == Role::Pawn {
        return 0;
    }
    let moves_amount = pos_legal.count();
    if moves_amount == 0 {
        -(30 + eval_material(piece.role) / 50)
    } else {
        moves_amount * 4
    }
}


// the closer to op king the better value
fn eval_king_attack(pos: Pos, enemy_king: Pos) -> i32 {
    let row_dist = (pos / 8) as i32 - (enemy_king / 8) as i32;
    let col_dist = (pos % 8) as i32 - (enemy_king % 8) as i32;
    let distance = row_dist.abs() + col_dist.abs();
    (14 - distance) * 4
}

