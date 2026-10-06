use super::*;


// chooses move out of all given moves
impl Game {
    pub fn choose_move(&mut self) -> Move {

        let min_value = self.search.moves.iter()
            .map(|(_, _, value)| if self.state.player == Color::White { *value } else { -*value })
            .min().unwrap();

        let total: u64 = self.search.moves.iter()
            .map(|(_, _, value)| {
                let score = if self.state.player == Color::White { *value } else { -*value };
                let diff = (score as i64 - min_value as i64 + 1) as u64;
                diff.pow(3)
            })
            .sum();

        let mut rnd = self.seed_update() % total;

        for (mv,_ , value) in &self.search.moves {
            let score = if self.state.player == Color::White { *value } else { -*value };
            let weight = ((score - min_value + 1) as u64).pow(3);

            if rnd < weight {
                return *mv;
            }

            rnd -= weight;
        }

        unreachable!()
    }



    fn seed_update(&mut self) -> u64 {
        if self.seed == 0 {
            self.seed = 0x9E37_79B9_7F4A_7C15;
        }
        self.seed ^= self.seed << 13;
        self.seed ^= self.seed >> 7;
        self.seed ^= self.seed << 17;
        self.seed
    }
}
