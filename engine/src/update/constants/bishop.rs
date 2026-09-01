pub(super) const fn bishop_rays() -> [[[u8 ; 7]; 4]; 64] {
    let mut attacks = [[[64; 7]; 4]; 64];
    
    let mut i: u8 = 0;
    while i < 64 {

        let row = (i / 8) as u8;
        let col = (i % 8) as u8; 

        // up left
        let mut r = row as i8 - 1;
        let mut c = col as i8 - 1;
        let mut count = 0;
        while r >= 0 && c >= 0{
            attacks[i as usize][0][count] = (r*8) as u8 + c as u8;

            r -= 1; c -= 1; count += 1;
        }

        // up right
        let mut r = row as i8 - 1;
        let mut c = col as i8 + 1;
        let mut count = 0;
        while r >= 0 && c < 8 {
            attacks[i as usize][1][count] = (r*8) as u8 + c as u8;

            r -= 1; c += 1; count += 1;
        }


        // down left
        let mut r = row as i8 + 1;
        let mut c = col as i8 - 1;
        let mut count = 0;
        while r < 8 && c >= 0 {
            attacks[i as usize][2][count] = (r*8) as u8 + c as u8;

            r += 1; c -= 1; count += 1;
        }

        // down right
        let mut r = row as i8 + 1;
        let mut c = col as i8 + 1;
        let mut count = 0;
        while r < 8 && c < 8 {
            attacks[i as usize][3][count] = (r*8) as u8 + c as u8;

            r += 1; c += 1; count += 1;
        }
        i += 1;

    }
    attacks

}