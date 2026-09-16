use super::*;

impl Game { 
    pub(super) fn update_legal_moves(&mut self, pieces: [BitBoard; 2]) {
        // clear 
        self.cache.legal_moves.clear();
        let pins = self.get_pins(pieces);

        // amount of pieces to attack the king
        let mut king_attakers: u8 = 0;
        let mut attacker_pos: u8 = 64;
        let king_pos = self.cache.king_pos[self.state.player as usize];

        // fill
        for pos in 0..64u8 {
            match self.state.board[pos] {
                Some(piece) if piece.color == self.state.player => {
                    let mut bits = self.cache.legal[pos].0;
                    bits &= pins[pos as usize];

                    while bits != 0 {
                        let end_pos = bits.trailing_zeros() as u8;
                        self.cache.legal_moves.push((pos, end_pos));
                        bits &= bits - 1;
                    }
                },
                Some(piece) if piece.color == self.state.player.opp() => {
                    if self.cache.cover[pos].get(king_pos) {
                        king_attakers += 1;
                        attacker_pos = pos;
                    }
                },
                _ => {}
            }
        }

        match king_attakers {
            0 => self.cache.check = false,
            1 => {
                self.cache.check = true;
                // remove moves that cause check
                let block_mask = match self.state.board[attacker_pos] {
                    Some(Piece { role: Role::Bishop | Role::Rook | Role::Queen, .. }) => {
                        ray_between(attacker_pos, king_pos)
                    }
                    _ => 1u64 << attacker_pos,
                };
                self.cache.legal_moves.retain(|(start, end)| {
                    *start == king_pos || (block_mask & (1u64 << end)) != 0
                });
            }
            _ => {
                self.cache.check = true;
                // recalculate legal only for king
                self.cache.legal_moves.clear();
                let mut bits = self.cache.legal[king_pos].0;
                while bits != 0 {
                    let end_pos = bits.trailing_zeros() as u8;
                    self.cache.legal_moves.push((king_pos, end_pos));
                    bits &= bits - 1;
                };
            }
        }

    }



    fn get_pins(&mut self, pieces: [BitBoard; 2]) -> [u64; 64] {
        let mut pins = [u64::MAX; 64];
        // for each piece, is it pinned and what ray can it move on

        for dir in 0..4 {
            let mut found_pinned: Option<Pos> = None;
            let mut ray_mask: BitBoard = BitBoard(0);

            for &pos in &ROOK_RAYS[self.cache.king_pos[self.state.player as usize] as usize][dir] {
                if pos == 64 { break; }
                ray_mask.set(pos);  // save visited squares

                // friendly pieces
                if pieces[self.state.player as usize].get(pos) {
                    if found_pinned.is_some() { break; }
                    found_pinned = Some(pos);
                }
                // opponent pieces
                else if pieces[self.state.player.opp() as usize].get(pos) {
                    if let Some(pinned_pos) = found_pinned {
                        if let Some(piece) = self.state.board[pos] {
                            if piece.role == Role::Rook || piece.role == Role::Queen {
                                pins[pinned_pos as usize] &= ray_mask.0 | (1u64 << pos);
                            }
                        }
                    }
                    break;
                }
            }
        }



        for dir in 0..4 {
            let mut found_pinned: Option<Pos> = None;
            let mut ray_mask: BitBoard = BitBoard(0);

            for &pos in &BISHOP_RAYS[self.cache.king_pos[self.state.player as usize] as usize][dir] {
                if pos == 64 { break; }
                ray_mask.set(pos);  // save visited squares

                // friendly pieces
                if pieces[self.state.player as usize].get(pos) {
                    if found_pinned.is_some() { break; }
                    found_pinned = Some(pos);
                }
                // opponent pieces
                else if pieces[self.state.player.opp() as usize].get(pos) {
                    if let Some(pinned_pos) = found_pinned {
                        if let Some(piece) = self.state.board[pos] {
                            if piece.role == Role::Bishop || piece.role == Role::Queen {
                                pins[pinned_pos as usize] &= ray_mask.0 | (1u64 << pos);
                            }
                        }
                    }
                    break;
                }
            }
        }
        pins
    }
}



fn ray_between(attacker_pos: Pos, king_pos: Pos) -> u64 {
    let mut mask: u64 = 1 << attacker_pos; 

    if attacker_pos.row() == king_pos.row() {
        let min_col = king_pos.col().min(attacker_pos.col()) + 1;
        let max_col = king_pos.col().max(attacker_pos.col());
        for col in min_col..max_col {
            mask |= 1u64 << (king_pos.row() * 8 + col);
        }
    } else if attacker_pos.col() == king_pos.col() {
        let min_row = king_pos.row().min(attacker_pos.row()) + 1;
        let max_row = king_pos.row().max(attacker_pos.row());
        for row in min_row..max_row {
            mask |= 1u64 << (row*8 + king_pos.col());
        }
    } else {
        let step_row = (attacker_pos.row() as i8 - king_pos.row() as i8).signum();
        let step_col = (attacker_pos.col() as i8 - king_pos.col() as i8).signum();
        let mut r = king_pos.row() as i8 + step_row;
        let mut c = king_pos.col() as i8 + step_col;
        while r as u8 != attacker_pos.row() || c as u8 != attacker_pos.col() {
            mask |= 1u64 << (r as u8 * 8 + c as u8);
            r += step_row;
            c += step_col;
        }
    }
    mask
}


