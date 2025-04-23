from PIL import Image, ImageDraw, ImageFont
from enum import Enum

from enum import Enum
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional, Union
import os


def to_pixels(size_in_mm: float, dpi: float) -> int:
    """Convert millimeters to pixels based on DPI."""
    return int(size_in_mm * dpi / 25.4)


class Mode(Enum):
    WORDS = 1
    LETTERS = 2
    SINGLE_PAGE_WORDS = 3


class Plantilla:
    """Class to create template images with text for printing."""

    # Class constants
    DEFAULT_VERTICAL_SPACING_MM = 15
    DEFAULT_DPI = 300
    DEFAULT_FONT_COLOR = (0, 0, 0)  # Black
    OUTPUT_DIR = "./out"

    def __init__(self):
        # Initialize basic properties
        self.images: List[Tuple[Image.Image, str]] = []
        self.mode: Mode = Mode.WORDS
        self.language: str = "es"
        self.dpi: int = self.DEFAULT_DPI

        # Sizing properties (will be set later)
        self.width_px: int = 0
        self.height_px: int = 0
        self.margin_px: int = 0
        self.letter_size_px: int = 0
        self.accurate_cell_size_x_px: int = 0
        self.accurate_cell_size_y_px: int = 0
        self.vertical_spacing_px: int = 0
        self.horizontal_spacing_px: int = 0

        # Content properties
        self.letters: str = ""
        self.words: List[str] = []
        self.font = None
        self.font_color = self.DEFAULT_FONT_COLOR

        # Create output directory if it doesn't exist
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

    def create_images(self) -> None:
        """Create images based on the current mode."""
        if self.mode == Mode.LETTERS:
            self.create_layouts([self.letters])
        elif self.mode in (Mode.WORDS, Mode.SINGLE_PAGE_WORDS):
            self.create_layouts(self.words)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")

    def create_layouts(self, characters: List[str]) -> None:
        """Create layout images for the given characters."""
        if self.mode == Mode.SINGLE_PAGE_WORDS:
            self._create_single_page_layout(characters)
        else:
            self._create_individual_layouts(characters)

    def _create_single_page_layout(self, words: List[str]) -> None:
        """Create a single page with multiple words."""
        if len(words) > 5:
            raise ValueError(
                "Single page words only supports five (5) words at once")

        image = Image.new("RGB", (self.width_px, self.height_px), "white")
        draw = ImageDraw.Draw(image)
        self._draw_single_page_words(words, draw)
        self.images.append((image, ' '.join(words)))

    def _create_individual_layouts(self, characters: List[str]) -> None:
        """Create individual layouts for each character."""
        for char in characters:
            image = Image.new("RGB", (self.width_px, self.height_px), "white")
            draw = ImageDraw.Draw(image)
            self._draw_text(char, draw)
            self.images.append((image, char))

    def _draw_single_page_words(self, words: List[str], draw: ImageDraw.Draw) -> None:
        """Draw multiple words on a single page."""
        counter = 0
        vertical_position = self.margin_px

        for word in words:
            # Calculate spacing
            vertical_spacing = self.letter_size_px + self.accurate_cell_size_y_px
            horizontal_spacing = (self.letter_size_px *
                                  len(word)) + self.accurate_cell_size_x_px

            for i, y in enumerate(
                range(vertical_position, self.height_px -
                      self.margin_px, vertical_spacing)
            ):
                if counter > 0 and counter % 5 + (5 - len(words)) == 0:
                    vertical_position = y
                    counter += 1
                    break

                counter += 1
                for j, x in enumerate(
                    range(self.margin_px, self.width_px -
                          self.margin_px, horizontal_spacing)
                ):
                    if x + horizontal_spacing > self.width_px:
                        continue

                    draw.text(
                        (x, y), word, language=self.language, fill=self.font_color, font=self.font
                    )

    def _draw_text(self, text: str, draw: ImageDraw.Draw) -> None:
        """Draw repeated text on the image."""
        vertical_spacing = self.letter_size_px + self.accurate_cell_size_y_px
        horizontal_spacing = (self.letter_size_px * len(text)
                              ) + self.accurate_cell_size_x_px

        for y in range(self.margin_px, self.height_px - self.margin_px, vertical_spacing):
            for x in range(self.margin_px, self.width_px - self.margin_px, horizontal_spacing):
                if x + horizontal_spacing > self.width_px:
                    continue

                draw.text(
                    (x, y), text, language=self.language, fill=self.font_color, font=self.font
                )

    def save_png(self) -> None:
        """Save each image as a PNG file."""
        self.ensure_created()

        for image, text in self.images:
            filepath = os.path.join(self.OUTPUT_DIR, f"plantilla-{text}.png")
            image.save(filepath)
            print(f"Image generated: {filepath}")

    def save_pdf(self) -> None:
        """Save all images as a single PDF file."""
        self.ensure_created()

        images_to_save = [image.convert("RGB") for image, _ in self.images]

        if not images_to_save:
            print("No images to save")
            return

        name = self.letters if self.mode == Mode.LETTERS else '-'.join(
            self.words)
        pdf_path = os.path.join(self.OUTPUT_DIR, f"{name}-plantillas.pdf")

        images_to_save[0].save(
            pdf_path,
            "PDF",
            resolution=100,
            save_all=True,
            append_images=images_to_save[1:],
        )
        print(f"PDF saved at: {pdf_path}")

    def ensure_created(self) -> None:
        """Ensure images are created before saving."""
        if not self.images:
            self.create_images()

    # Configuration methods
    def set_language(self, lang: str) -> 'Plantilla':
        """Set the language for text rendering."""
        self.language = lang
        return self

    def set_mode(self, mode: Mode) -> 'Plantilla':
        """Set the mode for template generation."""
        self.mode = mode
        return self

    def set_dpi(self, dpi: int) -> 'Plantilla':
        """Set the DPI for image generation."""
        self.dpi = dpi
        return self

    def set_width(self, width_mm: float) -> 'Plantilla':
        """Set the width in millimeters."""
        self.width_px = to_pixels(width_mm, self.dpi)
        return self

    def set_height(self, height_mm: float) -> 'Plantilla':
        """Set the height in millimeters."""
        self.height_px = to_pixels(height_mm, self.dpi)
        return self

    def set_letter_size(self, letter_size_mm: float) -> 'Plantilla':
        """Set the letter size in millimeters."""
        self.letter_size_px = to_pixels(letter_size_mm, self.dpi)
        return self

    def set_margin(self, margin_mm: float) -> 'Plantilla':
        """Set the margin size in millimeters."""
        self.margin_px = to_pixels(margin_mm, self.dpi)
        return self

    def set_vertical_spacing(self, vertical_spacing_mm: float) -> 'Plantilla':
        """Set the vertical spacing in millimeters."""
        self.vertical_spacing_px = to_pixels(vertical_spacing_mm, self.dpi)
        return self

    def set_horizontal_spacing(self, horizontal_spacing_mm: float) -> 'Plantilla':
        """Set the horizontal spacing in millimeters."""
        self.horizontal_spacing_px = to_pixels(horizontal_spacing_mm, self.dpi)
        return self

    def accurate_cell_size_x(self, cell_size_mm: float) -> 'Plantilla':
        """Set the accurate cell size X in millimeters."""
        self.accurate_cell_size_x_px = to_pixels(cell_size_mm, self.dpi)
        return self

    def accurate_cell_size_y(self, cell_size_mm: float) -> 'Plantilla':
        """Set the accurate cell size Y in millimeters."""
        self.accurate_cell_size_y_px = to_pixels(cell_size_mm, self.dpi)
        return self

    def set_letters(self, letters: str) -> 'Plantilla':
        """Set letters and change mode to LETTERS."""
        self.letters = letters
        self.mode = Mode.LETTERS
        return self

    def set_words(self, words: List[str]) -> 'Plantilla':
        """Set words and change mode to WORDS."""
        self.words = words
        self.mode = Mode.WORDS
        return self

    def set_single_page_words(self, words: List[str]) -> 'Plantilla':
        """Set words and change mode to SINGLE_PAGE_WORDS."""
        self.words = words
        self.mode = Mode.SINGLE_PAGE_WORDS
        return self

    def set_font(self, font_path: str) -> 'Plantilla':
        """Load and set the font for text rendering."""
        try:
            self.font = ImageFont.truetype(font_path, self.letter_size_px)
        except IOError:
            print(f"Font not found at: {font_path}. Using default font.")
            self.font = ImageFont.load_default()
        return self

    def set_color(self, rgb: Tuple[int, int, int]) -> 'Plantilla':
        """Set the font color as RGB tuple."""
        self.font_color = rgb
        return self

    # Helper methods for checking mode
    def are_words(self) -> bool:
        """Check if mode is WORDS."""
        return self.mode == Mode.WORDS

    def are_letters(self) -> bool:
        """Check if mode is LETTERS."""
        return self.mode == Mode.LETTERS

    def are_single_page_words(self) -> bool:
        """Check if mode is SINGLE_PAGE_WORDS."""
        return self.mode == Mode.SINGLE_PAGE_WORDS
