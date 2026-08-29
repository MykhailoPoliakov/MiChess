use super::*;

#[derive(Copy, Clone, PartialEq)]
pub struct BitBoard(pub u64);

impl BitBoard {
    pub const fn new() -> Self {
        BitBoard(0)
    }

    pub fn set(&mut self, pos: Pos) -> () {
        self.0 |= 1u64 << pos;
    }

    pub fn set_all(&mut self) -> () {
        self.0 = u64::MAX;
    }

    pub fn clear(&mut self, pos: Pos) -> () {
        self.0 &= !(1u64 << pos);
    }

    pub fn get(&self, pos: Pos) -> bool {
        self.0 & (1u64 << pos) != 0
    }

    pub fn is_empty(&self) -> bool {
        self.0 == 0
    }

    pub fn count(&self) -> i32 {
        self.0.count_ones() as i32
    }

    pub fn iter_pos(&self) -> impl Iterator<Item = Pos> {
        let mut bits = self.0;
        std::iter::from_fn(move || {
            if bits == 0 {
                None
            } else {
                let pos = bits.trailing_zeros() as u8;
                bits &= bits - 1;
                Some(pos)
            }
        })
    }
}

impl std::ops::BitOrAssign for BitBoard {
    fn bitor_assign(&mut self, rhs: Self) {
        self.0 |= rhs.0;
    }
}

impl std::fmt::Display for BitBoard {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in 0..8 {
            for col in 0..8 {
                let bit = (self.0 >> (row * 8 + col)) & 1;
                write!(f, "{} ", bit)?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}





#[derive(Copy, Clone)]
pub struct BitGrid(pub [BitBoard; 64]);

impl BitGrid {
    pub const fn new() -> Self {
        BitGrid([BitBoard::new(); 64])
    }
}

impl std::ops::Index<Pos> for BitGrid {
    type Output = BitBoard;
    fn index(&self, pos: Pos) -> &Self::Output {
        &self.0[pos as usize]
    }
}

impl std::ops::IndexMut<Pos> for BitGrid {
    fn index_mut(&mut self, pos: Pos) -> &mut Self::Output {
        &mut self.0[pos as usize]
    }
}


