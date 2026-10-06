use super::*;
use eframe::egui;


mod render_board;
mod render_search;
mod load_textures;


impl App {
    pub fn render(&self, ui: &mut egui::Ui) -> () {
        self.render_board(ui);
        self.render_search(ui, egui::Pos2 { x: self.square_size * 8.5, y: 0.0 });
    }

}