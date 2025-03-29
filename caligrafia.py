from PIL import Image, ImageDraw, ImageFont

def to_pixels(size_in_mm:float, dpi:float) -> int:
    return int(size_in_mm * dpi / 25.4)

class Plantilla:
    def __init__(self):
        self.images: list[tuple[Image.Image, str]] = []
        # Convertir a píxeles
    
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
    
    def set_letters(self, letters):
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
    
    def create_images(self):
        # Crear imagenes en blanco
        for letter in self.letters:
            image = Image.new("RGB", (self.width_px, self.height_px), "white")
            draw = ImageDraw.Draw(image)
            self.draw_letter(letter, draw)
            self.images.append((image, letter))

    def draw_letter(self, letter: str, draw: ImageDraw):
        # Dibujar las letras en cuadricula
        for y in range(self.margin_px, self.height_px - self.margin_px, self.cell_size_px):
            for x in range(self.margin_px, self.width_px - self.margin_px, self.cell_size_px):
                draw.text((x + self.cell_size_px // 4, y + self.cell_size_px // 4), letter, fill=self.font_color, font=self.font)

    def save_png(self):
        self.ensure_created()
        # Guardar la imagen
        for image, letter in self.images:
            image.save(f"plantilla_caligrafia-{letter}.png")
            print(f"Imagen generada: plantilla_caligrafia-{letter}.png")

    def save_pdf(self):
        self.ensure_created()
        images_to_save = [image.convert("RGB") for image, _ in self.images]
        images_to_save[0].save("plantillas.pdf", 'PDF',resolution=100, save_all=True, append_images=images_to_save[1:])
    
    def ensure_created(self):
        if len(self.images) < 1:
            self.create_images()

# Generar la cuadrícula de letras
abecedario = "abcdefqhijklmnñopqrstuvwxyz"
abecedario = abecedario + str.upper(abecedario)
letter_color = (0,0,0,100)





plantilla = Plantilla()

plantilla.set_dpi(300)
plantilla.set_width(215.9)
plantilla.set_height(279.4)
plantilla.set_margin(20)
plantilla.set_cell_size(15)
plantilla.set_letter_size(10)
plantilla.set_letters(abecedario)
plantilla.set_font("/usr/share/fonts/tex-gyre/texgyreadventor-regular.otf")
plantilla.set_color((216, 216, 216))

plantilla.save_png()
plantilla.save_pdf()




