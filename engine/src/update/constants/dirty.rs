use super::*;

pub(super) const fn combined_dirty() -> BitGrid {
    let mut bitgrid = BitGrid::new();

    
    let knight_offsets: [(i8, i8); 8] = [(1,-2),(-1,2),(-1,-2),(1,2),(2,-1),(-2,1),(-2,-1),(2,1)];

    let mut pos: u8 = 0;
    while pos < 64 {


        // KNIGHT
        let mut i = 0;
        while i < 8 {
            match offset(pos, knight_offsets[i]) {
                Some(legal_pos) => bitgrid.0[pos as usize].0 |= 1u64 << legal_pos,
                None => {}
            }
            i += 1;
        }



        // BISHOP
        let row = (pos / 8) as i8;
        let col = (pos % 8) as i8;

        // up left
        let mut r = row as i8 - 1;
        let mut c = col as i8 - 1;
        while r >= 0 && c >= 0{
            bitgrid.0[pos as usize].0 |= 1u64 << (r as u8 * 8 + c as u8);
            r -= 1; c -= 1;
        }

        // up right
        let mut r = row as i8 - 1;
        let mut c = col as i8 + 1;
        while r >= 0 && c < 8 {
            bitgrid.0[pos as usize].0 |= 1u64 << (r as u8 * 8 + c as u8);
            r -= 1; c += 1;
        }

        // down left
        let mut r = row as i8 + 1;
        let mut c = col as i8 - 1;
        while r < 8 && c >= 0 {
            bitgrid.0[pos as usize].0 |= 1u64 << (r as u8 * 8 + c as u8);
            r += 1; c -= 1; 
        }

        // down right
        let mut r = row as i8 + 1;
        let mut c = col as i8 + 1;
        while r < 8 && c < 8 {
            bitgrid.0[pos as usize].0 |= 1u64 << (r as u8 * 8 + c as u8);
            r += 1; c += 1;
        }



        // ROOK
        let row = (pos / 8) as i8;
        let col = (pos % 8) as i8;

        // up
        let mut r = row - 1;
        while r >= 0 {
            bitgrid.0[pos as usize].0 |= 1u64 << (r as u8 * 8 + col as u8);
            r -= 1;
        }

        // down
        let mut r = row + 1;
        while r < 8 {
            bitgrid.0[pos as usize].0 |= 1u64 << (r as u8 * 8 + col as u8);
            r += 1;
        }

        // left
        let mut c = col - 1;
        while c >= 0 {
            bitgrid.0[pos as usize].0 |= 1u64 << (row as u8 * 8 + c as u8);
            c -= 1;
        }

        // right
        let mut c = col + 1;
        while c < 8 {
            bitgrid.0[pos as usize].0 |= 1u64 << (row as u8 * 8 + c as u8);
            c += 1;
        }



        pos += 1;
    }
    bitgrid
}



pub(super) const fn pawn_dirty() -> BitGrid {
    let mut bitgrid = BitGrid::new();
    let mut pos: u8 = 0;
    while pos < 64 {
        let offsets: [i8; 4] = [8, 16, -8, -16];
        let mut i = 0;
        while i < 4 {
            let target = pos as i8 + offsets[i];
            if target >= 0 && target < 64 {
                bitgrid.0[pos as usize].0 |= 1u64 << target;
            }
            i += 1;
        }
        pos += 1;
    }
    bitgrid
}