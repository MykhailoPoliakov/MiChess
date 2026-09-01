use engine::*;
use eframe::egui;


// mod render;

struct App {
    game: Game,
}

impl App {
    fn new() -> Self {
        App {
            game: Game::new(),
        }
    }
}

impl eframe::App for App {
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        let painter = ui.painter();
        
        painter.rect_filled(
            egui::Rect::from_min_size(
                egui::pos2(0.0, 0.0),
                egui::vec2(100.0, 100.0)
            ),
            0.0,
            egui::Color32::from_rgb(255, 0, 0),
        );
    }
}

pub fn run() {
    let _ = eframe::run_native(
        "MiChess",
        eframe::NativeOptions::default(),
        Box::new(|_| Ok(Box::new(App::new()))),
    );
}