use super::Game;
use super::ALL_POS;

// constants of how pieces move
const ROOK_MOVES: [(i8, i8); 4] = [(1, 0), (-1, 0), (0, -1), (0, 1)];
const BISHOP_MOVES: [(i8, i8); 4] = [(1, -1), (-1, 1), (-1, -1), (1, 1)];
const KNIGHT_MOVES: [(i8, i8); 8] = [(1, -2), (-1, 2), (-1, -2), (1, 2), (2, -1), (-2, 1), (-2, -1), (2, 1)];
const KING_MOVES: [(i8, i8); 8] = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, -1), (-1, 1), (-1, -1), (1, 1)];


// Analyses the board, saves all the legal moves and covers for exact board position.
// Changes: game.legal , game.w_cover , game.b_cover
pub fn info(game: &mut Game) -> () {

    // cleaning
    game.w_cover = std::array::from_fn(|_| std::array::from_fn(|_| Vec::new()));
    game.b_cover = std::array::from_fn(|_| std::array::from_fn(|_| Vec::new()));
    game.legal   = std::array::from_fn(|_| std::array::from_fn(|_| Vec::new()));

    // get variables 
    let legal = &mut game.legal;
    let board: &[[(char, char); 8]; 8] = &game.board;

    // other quenue for kings, iterate through them after the other pieces
    let mut kings_places: Vec<(i8, i8)> = Vec::new();
    
    // start iteration
    for place in ALL_POS {
        if board[place.0 as usize][place.1 as usize].0 == ' ' {
            continue;
        };

        // get variables 
        let player: char = board[place.0 as usize][place.1 as usize].0;
        let opponent: char = if player == 'w' {'b'} else {'w'};
        let p_cover = if player == 'w' { &mut game.w_cover } else { &mut game.b_cover };

        // match the piece
        match board[place.0 as usize][place.1 as usize].1 {

            'p' => {let direction = if player == 'w' { -1 } else { 1 };
                    if !(place.0 + direction >= 0 || place.0 + direction < 8)  {
                        continue;
                    }

                    // cover
                    if place.1 - 1 >= 0 && place.1 - 1 < 8 {
                        p_cover[(place.0 + direction) as usize][(place.1 - 1) as usize].push( place );
                    }
                    if place.1 + 1 >= 0 && place.1 + 1 < 8 {
                        p_cover[(place.0 + direction) as usize][(place.1 + 1) as usize].push( place );
                    }

                    // one move ahead
                    if game.board[(place.0 + direction) as usize ][place.1 as usize] == (' ',' ') {
                        legal[place.0 as usize][place.1 as usize].push((place.0 + direction,place.1));
                        // two moves ahead
                        if (place.0 + direction*2 >= 0 && place.0 + direction*2 < 8) &&
                        game.board[(place.0 + direction*2) as usize ][place.1 as usize].0 == ' ' &&
                        ((player == 'w' && place.0 == 6) || (player == 'b' && place.0 == 1)) {
                            legal[place.0 as usize][place.1 as usize].push((place.0 + direction*2,place.1));
                        }
                    }

                    //capture
                    if place.1 - 1 >= 0 && place.1 - 1 < 8 && board[(place.0 + direction) as usize][(place.1 - 1) as usize].0 == opponent {
                        legal[place.0 as usize][place.1 as usize].push((place.0 + direction,place.1 - 1));
                    }
                    if place.1 + 1 >= 0 && place.1 + 1 < 8 && board[(place.0 + direction) as usize][(place.1 + 1) as usize].0 == opponent {
                        legal[place.0 as usize][place.1 as usize].push((place.0 + direction,place.1 + 1));
                    }

                    // en passant
                    if (player == 'w' && place.0 == 3) || (player == 'b' && place.0 == 4) {
                        if place.1 - 1 >= 0 && place.1 - 1 < 8 && board[place.0 as usize][(place.1 - 1) as usize] == (opponent, 'p') &&
                        game.en_passant == (place.1 - 1) {
                            legal[place.0 as usize][place.1 as usize].push((place.0 + direction,place.1 - 1));
                        }
                        if place.1 + 1 >= 0 && place.1 + 1 < 8 && board[place.0 as usize][(place.1 + 1) as usize] == (opponent, 'p') &&
                        game.en_passant == (place.1 + 1) {
                            legal[place.0 as usize][place.1 as usize].push((place.0 + direction,place.1 + 1));
                        }
                    }
                },

            'h' => {for num in KNIGHT_MOVES {
                        let num1: i8 = place.0 + num.0;
                        let num2: i8 = place.1 + num.1;
                        if num1 >= 0 && num1 < 8 && num2 >= 0 && num2 < 8 {
                            p_cover[num1 as usize][num2 as usize].push( place );
                            if board[num1 as usize][num2 as usize].0 != player {
                                legal[place.0 as usize][place.1 as usize].push((num1, num2));
                            }
                        }
                    }
                },
                    
            'b' => {for direction in BISHOP_MOVES {
                        for i in 1..8 {
                            let num1 = place.0 + i*direction.0;
                            let num2 = place.1 + i*direction.1;
                            if num1 >= 0 && num1 < 8 && num2 >= 0 && num2 < 8 {
                                // cover 
                                p_cover[num1 as usize][num2 as usize].push( place );
                                // legal
                                if board[num1 as usize][num2 as usize].0 == player {
                                    break
                                }
                                legal[place.0 as usize][place.1 as usize].push((num1, num2));
                                // stop
                                if ![(' ',' '),(opponent,'k')].contains(&board[num1 as usize][num2 as usize]) {
                                    break
                                }
                            }
                        } 
                    }
                },

            'r' => {for direction in ROOK_MOVES {
                        for i in 1..8 {
                            let num1 = place.0 + i*direction.0;
                            let num2 = place.1 + i*direction.1;
                            if num1 >= 0 && num1 < 8 && num2 >= 0 && num2 < 8 {
                                // cover 
                                p_cover[num1 as usize][num2 as usize].push( place );
                                // legal
                                if board[num1 as usize][num2 as usize].0 == player {
                                    break
                                }
                                legal[place.0 as usize][place.1 as usize].push((num1, num2));
                                // stop
                                if ![(' ',' '),(opponent,'k')].contains(&board[num1 as usize][num2 as usize]) {
                                    break
                                }
                            }
                        } 
                    }
                },

            'q' => {for direction in KING_MOVES {
                        for i in 1..8 {
                            let num1 = place.0 + i*direction.0;
                            let num2 = place.1 + i*direction.1;
                            if num1 >= 0 && num1 < 8 && num2 >= 0 && num2 < 8 {
                                // cover 
                                p_cover[num1 as usize][num2 as usize].push( place );
                                // legal
                                if board[num1 as usize][num2 as usize].0 == player {
                                    break
                                }
                                legal[place.0 as usize][place.1 as usize].push((num1, num2));
                                // stop
                                if ![(' ',' '),(opponent,'k')].contains(&board[num1 as usize][num2 as usize]) {
                                    break
                                }
                            }
                        } 
                    }
                },
            
            'k' => kings_places.push(place),

            _   => (),
        }
    }


    // iterate through kings (cover)
    for place in kings_places.clone() {

        // get variables 
        let player: char = board[place.0 as usize][place.1 as usize].0;
        let p_cover = if player == 'w' { &mut game.w_cover } else { &mut game.b_cover };

        // check all moves
        for num in KING_MOVES {
            let num1: i8 = place.0 + num.0;
            let num2: i8 = place.1 + num.1;
            if num1 >= 0 && num1 < 8 && num2 >= 0 && num2 < 8 {
                p_cover[num1 as usize][num2 as usize].push( place );
            }
        }
    }
    // iterate through kings (legal)
    for place in kings_places {

        // get variables 
        let player: char = board[place.0 as usize][place.1 as usize].0;
        let (p_cover, op_cover) = if player == 'w' {
            (&mut game.w_cover, &mut game.b_cover)
        } else {
            (&mut game.b_cover, &mut game.w_cover)
        };

        // check all moves
        for num in KING_MOVES {
            let num1: i8 = place.0 + num.0;
            let num2: i8 = place.1 + num.1;
            if num1 >= 0 && num1 < 8 && num2 >= 0 && num2 < 8 {
                p_cover[num1 as usize][num2 as usize].push( place );
                if board[num1 as usize][num2 as usize].0 != player && op_cover[num1 as usize][num2 as usize].is_empty() {
                    legal[place.0 as usize][place.1 as usize].push((num1, num2));
                }
            }
        }

        // castle
        let s: usize = if player == 'w' {7} else {0};
        let direction: usize = if player == 'w' {0} else {1};

        if place == (s as i8,4) {
            // left
            if game.castle[direction][0] {
                if board[s][3] == (' ',' ') && op_cover[s][3].is_empty() &&
                    board[s][2] == (' ',' ') && op_cover[s][2].is_empty() &&
                    board[s][1] == (' ',' ') && op_cover[s][1].is_empty() &&
                    board[s][0] == (player,'r') {
                        legal[place.0 as usize][place.1 as usize].push((s as i8, 2));
                }
            } 
            // right
            if game.castle[direction][1] {
                if board[s][5] == (' ',' ') && op_cover[s][5].is_empty() &&
                    board[s][6] == (' ',' ') && op_cover[s][6].is_empty() &&
                    board[s][7] == (player,'r') {
                        legal[place.0 as usize][place.1 as usize].push((s as i8, 6));
                }
            }
        }
    }
}
