use super::*;


pub const WP: Option<Piece> = Some(Piece { color: Color::White, role: Role::Pawn   });
pub const WR: Option<Piece> = Some(Piece { color: Color::White, role: Role::Rook   });
pub const WH: Option<Piece> = Some(Piece { color: Color::White, role: Role::Knight });
pub const WB: Option<Piece> = Some(Piece { color: Color::White, role: Role::Bishop });
pub const WQ: Option<Piece> = Some(Piece { color: Color::White, role: Role::Queen  });
pub const WK: Option<Piece> = Some(Piece { color: Color::White, role: Role::King   });
pub const BP: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Pawn   });
pub const BR: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Rook   });
pub const BH: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Knight });
pub const BB: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Bishop });
pub const BQ: Option<Piece> = Some(Piece { color: Color::Black, role: Role::Queen  });
pub const BK: Option<Piece> = Some(Piece { color: Color::Black, role: Role::King   });
pub const __: Option<Piece> = None;


