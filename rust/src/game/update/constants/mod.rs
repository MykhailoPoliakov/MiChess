use super::*;

mod rook;
use rook::rook_rays;
mod bishop;
use bishop::bishop_rays;

pub const KNIGHT_ATTACKS: BitGrid = knight_attacks();
pub const KING_ATTACKS: BitGrid = king_attacks();
pub const PAWN_ATTACKS: [BitGrid; 2] = pawn_attacks();
pub const ROOK_RAYS: [[[Pos; 7]; 4]; 64] = rook_rays();
pub const BISHOP_RAYS: [[[Pos; 7]; 4]; 64] = bishop_rays();  



const fn knight_attacks() -> BitGrid {
    let offsets: [(i8, i8); 8] = [(1,-2),(-1,2),(-1,-2),(1,2),(2,-1),(-2,1),(-2,-1),(2,1)];
    let mut bitgrid = BitGrid::new();

    let mut pos: u8 = 0;
    while pos < 64 {
        let mut i = 0;
        while i < 8 {
            match offset(pos, offsets[i]) {
                Some(legal_pos) => bitgrid.0[pos as usize].0 |= 1u64 << legal_pos,
                None => {}
            }
            i += 1;
        }
        pos += 1;
    }
    bitgrid
}



const fn king_attacks() -> BitGrid {
    let offsets: [(i8, i8); 8] = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, 1), (-1, -1), (1, 1)];
    let mut bitgrid = BitGrid::new();

    let mut pos: u8 = 0;
    while pos < 64 {
        let mut i = 0;
        while i < 8 {
            match offset(pos, offsets[i]) {
                Some(legal_pos) => bitgrid.0[pos as usize].0 |= 1u64 << legal_pos,
                None => {}
            }
            i += 1;
        }
        pos += 1;
    }
    bitgrid
}


const fn pawn_attacks() -> [BitGrid; 2] {
    let mut white_bitgrid = BitGrid::new();
    let mut black_bitgrid = BitGrid::new();

    let white_offsets: [(i8, i8); 2] = [(-1, 1), (-1, -1)];
    let black_offsets: [(i8, i8); 2] = [( 1, 1), ( 1, -1)];
    
    let mut pos: u8 = 0;
    while pos < 64 {
        let mut i = 0;
        while i < 2 {
            match offset(pos, white_offsets[i]) {
                Some(legal_pos) => white_bitgrid.0[pos as usize].0 |= 1u64 << legal_pos,
                None => {}
            }
            match offset(pos, black_offsets[i]) {
                Some(legal_pos) => black_bitgrid.0[pos as usize].0 |= 1u64 << legal_pos,
                None => {}
            }
            i += 1;
        }

        pos += 1;
    };

    [white_bitgrid, black_bitgrid]
}



const fn offset(pos: Pos, offset: (i8, i8)) -> Option<Pos> {
    let row = (pos / 8) as i8 + offset.0;
    let col = (pos % 8) as i8 + offset.1;
    if row >= 0 && row < 8 && col >= 0 && col < 8 {
        Some(row as u8 * 8 + col as u8)
    } else {
        None
    }
}