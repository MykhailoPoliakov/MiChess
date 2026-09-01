pub(super) const fn rook_rays() -> [[[u8; 7]; 4]; 64] {
    let mut attacks = [[[64; 7]; 4]; 64];
    
    let mut i: u8 = 0;
    while i < 64 {

        let row = (i / 8) as u8;
        let col = (i % 8) as u8; 

        // up
        let mut r = row as i8 - 1;
        let mut count = 0;
        while r >= 0 {
            attacks[i as usize][0][count] = (r*8) as u8 + col;

            r -= 1; count += 1;
        }

        // down
        let mut r = row + 1;
        let mut count = 0;
        while r < 8 {
            attacks[i as usize][1][count] = r*8 + col;

            r += 1; count += 1;
        }

        // right
        let mut c = col + 1;
        let mut count = 0;
        while c < 8 {
            attacks[i as usize][2][count] = row*8 + c;

            c += 1; count += 1;
        }

        // left
        let mut c = col as i8 - 1;
        let mut count = 0;
        while c >= 0 {
            attacks[i as usize][3][count] = row*8 + c as u8;

            c -= 1; count += 1;
        }

        i += 1;
    }

    attacks

}