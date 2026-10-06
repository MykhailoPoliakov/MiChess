use std::collections::HashMap;
use eframe::egui;
use super::*;

const TEXTURES_NAME: [&str; 12] = [
    "w_pawn", "w_knight", "w_bishop", "w_rook", "w_queen", "w_king",
    "b_pawn", "b_knight", "b_bishop", "b_rook", "b_queen", "b_king",
];


impl App {
    pub fn load_textures(cc: &eframe::CreationContext) -> HashMap<String, egui::TextureHandle> {
        // upload textures on init
        let mut textures = HashMap::new();

        for texture_name in TEXTURES_NAME {
            let path = format!("{}/textures/{}.png", env!("CARGO_MANIFEST_DIR"), texture_name);
            let image = image::open(path).unwrap();
            let size = [image.width() as usize, image.height() as usize];
            let pixels = image.to_rgba8();
            let texture = cc.egui_ctx.load_texture(
                texture_name,
                egui::ColorImage::from_rgba_unmultiplied(size, &pixels),
                egui::TextureOptions::default(),
            );
            textures.insert(texture_name.to_string(), texture);
        }

        textures
    }
}
