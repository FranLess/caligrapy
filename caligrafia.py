from PIL import Image, ImageDraw, ImageFont
from enum import Enum

def to_pixels(size_in_mm: float, dpi: float) -> int:
    return int(size_in_mm * dpi / 25.4)

class Mode(Enum):
    WORDS = 1
    LETTERS = 2
    SINGLE_PAGE_WORDS = 3

class Plantilla:
    VERTICAL_SPACING_MM = 15
    VERTICAL_SPACING_PX = to_pixels(VERTICAL_SPACING_MM, 300)

    def __init__(self):
        self.images: list[tuple[Image.Image, str]] = []
        self.mode:Mode
        self.language = "es"
        self.accurate_cell_size_x_px = 0
        self.accurate_cell_size_y_px = 0
        self.single_page_words:bool = False
        # Convertir a píxeles

    def create_images(self):
        # Crear imagenes en blanco
        if self.are_letters():
            self.create_layouts(self.letters)
        elif self.are_words():
            self.create_layouts(self.words)
        else:
            self.create_layouts(self.words)

    def create_layouts(self, characters: list):
        if self.are_single_page_words():
            if len(characters) > 5:
                raise ValueError("single page words only suport five (5) words at once")
            image = Image.new("RGB", (self.width_px, self.height_px), "white")
            draw = ImageDraw.Draw(image)
            self.draw_single_page_words(characters, draw)
            self.images.append((image, ' '.join(characters)))
        else:
            for letter in characters:
                image = Image.new("RGB", (self.width_px, self.height_px), "white")
                draw = ImageDraw.Draw(image)
                self.draw_letter(letter, draw)  
                self.images.append((image, letter))

    def draw_single_page_words(self, words: list[str, str, str, str, str], draw: ImageDraw):
        counter = 0
        vertical_spacing_check_point = self.margin_px
        for word in words:
            vertical_spacing = self.letter_size_px
            horizontal_spacing = self.letter_size_px * len(word)
            vertical_spacing = int(vertical_spacing) + self.accurate_cell_size_y_px
            horizontal_spacing = int(horizontal_spacing) + self.accurate_cell_size_x_px

            for i, y in enumerate(
                range(vertical_spacing_check_point, self.height_px - self.margin_px, vertical_spacing)
            ):
                if counter > 0 and counter % 5 == 0:
                    vertical_spacing_check_point = y
                    counter += 1
                    break
                counter += 1
                for j, x in enumerate(
                    range(
                        self.margin_px, self.width_px - self.margin_px, horizontal_spacing
                    )
                ):
                    if x + horizontal_spacing > self.width_px:
                        continue
                    draw.text(
                        (x, y), word, language="ru", fill=self.font_color, font=self.font
                    )

    def draw_letter(self, characters: list[str], draw: ImageDraw):
        vertical_spacing = self.letter_size_px
        horizontal_spacing = self.letter_size_px * len(characters)
        vertical_spacing = int(vertical_spacing) + self.accurate_cell_size_y_px
        horizontal_spacing = int(horizontal_spacing) + self.accurate_cell_size_x_px
        for i, y in enumerate(
            range(self.margin_px, self.height_px - self.margin_px, vertical_spacing)
        ):
            for j, x in enumerate(
                range(
                    self.margin_px, self.width_px - self.margin_px, horizontal_spacing
                )
            ):
                draw.text(
                    (x, y), characters, language="ru", fill=self.font_color, font=self.font
                )

    def save_png(self):
        self.ensure_created()
        # Guardar la imagen
        for image, letter in self.images:
            image.save(f"./out/plantilla-{letter}.png")
            print(f"Imagen generada: ./out/plantilla-{letter}.png")

    def save_pdf(self):
        self.ensure_created()
        images_to_save = [image.convert("RGB") for image, _ in self.images]
        name = self.letters if self.are_letters() else '-'.join(self.words)
        images_to_save[0].save(
            f"./out/{name}-plantillas.pdf",
            "PDF",
            resolution=100,
            save_all=True,
            append_images=images_to_save[1:],
        )
        print(f"pdf guardado en ./out/{name}-plantillas.pdf")

    def ensure_created(self):
        if len(self.images) < 1:
            self.create_images()

    def set_language(self, lang: str):
        self.language = lang

    def set_mode(self, mode: Mode):
        self.mode = mode

    def are_words(self) -> bool:
        return True if self.mode == Mode.WORDS else False

    def are_letters(self) -> bool:
        return True if self.mode == Mode.LETTERS else False
    
    def are_single_page_words(self) -> bool:
        return True if self.mode == Mode.SINGLE_PAGE_WORDS else False

    def set_dpi(self, dpi):
        self.dpi = dpi

    def set_width(self, width_mm):
        self.width_px = to_pixels(width_mm, self.dpi)

    def set_height(self, height_mm):
        self.height_px = to_pixels(height_mm, self.dpi)

    def accurate_cell_size_x(self, cell_size_mm):
        self.accurate_cell_size_x_px = to_pixels(cell_size_mm, self.dpi)

    def accurate_cell_size_y(self, cell_size_mm):
        self.accurate_cell_size_y_px = to_pixels(cell_size_mm, self.dpi)

    def set_letter_size(self, letter_size_mm):
        self.letter_size_px = to_pixels(letter_size_mm, self.dpi)

    def set_letters(self, letters: str):
        self.letters = letters
        self.set_mode(Mode.LETTERS)

    def set_words(self, words: list[str]):
        self.words = words
        self.set_mode(Mode.WORDS)

    def set_margin(self, margin_mm):
        self.margin_px = to_pixels(margin_mm, self.dpi)

    def set_font(self, font_path):
        # Cargar una fuente (ajusta la ruta según tu sistema)
        try:
            self.font = ImageFont.truetype(font_path, self.letter_size_px)
        except IOError:
            self.font = ImageFont.load_default(self.letter_size_px)
            print("Font not found.")

    def set_color(self, rgb: tuple[int, int, int]):
        self.font_color = rgb

    def set_vertical_spacing(self, vertical_spacing_mm):
        self.vertical_spacing_px = to_pixels(vertical_spacing_mm, self.dpi)

    def set_horizontal_spacing(self, horizontal_spacing_mm):
        self.horizontal_spacing_px = to_pixels(horizontal_spacing_mm, self.dpi)
