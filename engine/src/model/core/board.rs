use super::*;


#[derive(Clone, Copy)]
pub struct Board( pub [Option<Piece>; 64] );

impl Board {
    pub fn default() -> Self {
        Board([
            BR, BH, BB, BQ, BK, BB, BH, BR,
            BP, BP, BP, BP, BP, BP, BP, BP,
            __, __, __, __, __, __, __, __,
            __, __, __, __, __, __, __, __,
            __, __, __, __, __, __, __, __,
            __, __, __, __, __, __, __, __,
            WP, WP, WP, WP, WP, WP, WP, WP,
            WR, WH, WB, WQ, WK, WB, WH, WR,
        ])
    } 

    pub fn get_king_pos(&self) -> [u8; 2] {
        let mut king_pos = [64;2];
        for pos in 0..64 {
            match self[pos] {
                Some(Piece {color: Color::White, role: Role::King}) => {
                    if king_pos[0] != 64 {panic!("Too many white kings.")}

                    king_pos[0] = pos;
                },
                Some(Piece {color: Color::Black, role: Role::King}) => {
                    if king_pos[1] != 64 {panic!("Too many black kings.")}

                    king_pos[1] = pos;
                },
                _ => {},
            }
        };

        if king_pos[0] == 64 { panic!("Missing white king.") }
        if king_pos[1] == 64 { panic!("Missing black king.") }
        
        king_pos
    }

    pub fn to_bitboards(&mut self) -> [BitBoard; 2] {
        let mut bitboards = [BitBoard(0); 2];
        let mut i: u64 = 0;
        for square in &self.0 {
            if let Some(piece) = square {
                bitboards[piece.color as usize].0 |= 1u64 << i;
            }
            i += 1;
        }
        bitboards
    }



}



impl core::ops::Index<Pos> for Board {
    type Output = Option<Piece>;
    fn index(&self, pos: Pos) -> &Self::Output {
        &self.0[pos as usize]
    }
}

impl core::ops::IndexMut<Pos> for Board {
    fn index_mut(&mut self, pos: Pos) -> &mut Self::Output {
        &mut self.0[pos as usize]
    }
}


