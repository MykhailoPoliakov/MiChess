use super::*;


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


