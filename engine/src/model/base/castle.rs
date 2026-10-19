use super::{Color};

pub type Castle = u8;

pub trait CastleExt {
    fn get(&self, color: Color, side: usize) -> bool;
    fn set(&mut self, color: Color, side: usize, value: bool);
    fn set_side(&mut self, color: Color, value: bool);
}

impl CastleExt for Castle {
    fn get(&self, color: Color, side: usize) -> bool {
        self & (1 << (color as u8 * 2 + side as u8)) != 0
    }
    fn set(&mut self, color: Color, side: usize, value: bool) {
        let bit = 1 << (color as u8 * 2 + side as u8);
        if value { *self |= bit; } else { *self &= !bit; }
    }
    fn set_side(&mut self, color: Color, value: bool) {
        let mask = 0b11 << (color as u8 * 2);
        if value { *self |= mask; } else { *self &= !mask; }
    }
}