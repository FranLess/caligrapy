from PIL import Image, ImageDraw, ImageFont

def to_pixels(size_in_mm:float, dpi:float) -> int:
    return int(size_in_mm * dpi / 25.4)


class Plantilla:
    class Mode:
        WORDS = True
        LETTERS = False

    VERTICAL_SPACING_MM = 15
    VERTICAL_SPACING_PX = to_pixels(VERTICAL_SPACING_MM, 300)

    def __init__(self):
        self.images: list[tuple[Image.Image, str]] = []
        self.words = False
        self.language = "es"
        # Convertir a píxeles

    def create_images(self):
        # Crear imagenes en blanco
        for letter in  self.letters if not self.words else [self.letters]:
            image = Image.new("RGB", (self.width_px, self.height_px), "white")
            draw = ImageDraw.Draw(image)
            self.draw_letter(letter, draw)
            self.images.append((image, letter))

    def draw_letter(self, letter: str, draw: ImageDraw):
        # Dibujar las letras en cuadricula
        vertical_spacing = self.letter_size_px
        horizontal_spacing = self.letter_size_px * len(letter)  
        vertical_spacing = int(vertical_spacing)
        horizontal_spacing = int(horizontal_spacing)
        for i, y in enumerate(range(self.margin_px, self.height_px - self.margin_px, vertical_spacing)): 
            for j, x in enumerate(range(self.margin_px, self.width_px - self.margin_px, horizontal_spacing)):
                draw.text(
                    (x, y),
                    letter, 
                    language="ru",
                    fill=self.font_color, 
                    font=self.font)
    
    def save_png(self):
        self.ensure_created()
        # Guardar la imagen
        for image, letter in self.images:
            image.save(f"./out/plantilla-{letter}.png")
            print(f"Imagen generada: ./out/plantilla-{letter}.png")

    def save_pdf(self):
        self.ensure_created()
        images_to_save = [image.convert("RGB") for image, _ in self.images]
        images_to_save[0].save(f"./out/{self.letters}-plantillas.pdf", 'PDF',resolution=100, save_all=True, append_images=images_to_save[1:])
        print(f"pdf guardado en ./out/{self.letters}-plantillas.pdf")
    
    def ensure_created(self):
        if len(self.images) < 1:
            self.create_images()

    def set_language(self, lang:str):
        self.language = lang

    def set_mode(self, mode:bool):
        self.words = mode

    def set_dpi(self, dpi):
        self.dpi = dpi

    def set_width(self, width_mm):
        self.width_px = to_pixels(width_mm, self.dpi) 

    def set_height(self, height_mm):
        self.height_px = to_pixels(height_mm, self.dpi) 

    def set_cell_size(self, cell_size_mm):
        self.cell_size_px = to_pixels(cell_size_mm, self.dpi)

    def set_letter_size(self, letter_size_mm):
        self.letter_size_px = to_pixels(letter_size_mm, self.dpi)
    
    def set_letters(self, letters:str):
        self.letters = letters

    def set_margin(self, margin_mm):
        self.margin_px = to_pixels(margin_mm, self.dpi)

    def set_font(self, font_path):
        # Cargar una fuente (ajusta la ruta según tu sistema)
        try:
            self.font = ImageFont.truetype(font_path, self.letter_size_px)
        except IOError:
            self.font = ImageFont.load_default(self.letter_size_px)
            print("Font not found.")

    def set_color(self, rgb:tuple[int, int, int]):
        self.font_color = rgb

    
    def set_vertical_spacing(self, vertical_spacing_mm):
        self.vertical_spacing_px = to_pixels(vertical_spacing_mm, self.dpi)
    
    def set_horizontal_spacing(self, horizontal_spacing_mm):
        self.horizontal_spacing_px = to_pixels(horizontal_spacing_mm, self.dpi)
