from fonts import Fonts
from caligrafia import Plantilla, Mode
import palabras
import helpers

# Ejemplo de uso

#Crear una plantilla
plantilla = Plantilla()

#Configurar paramétros
plantilla.set_dpi(300)
plantilla.set_width(helpers.Sheets.Carta.WIDTH)
plantilla.set_height(helpers.Sheets.Carta.HEIGHT)
plantilla.set_margin(20)
#PARA ESPAÑOL Y LETRAS SEPARADAS
# plantilla.set_cell_size(15)
plantilla.set_letter_size(10)
# plantilla.set_letters("gG")

#PARA PALABRAS (habrá que cambiar el cell_size según la longitud de la palabra)
plantilla.accurate_cell_size_y(1)
# plantilla.accurate_cell_size_x(50)
plantilla.set_language("ru")
#SI SE QUIEREN PLANTILLAS DE PALABRAS, USAR words
# words = [word.name.capitalize() for word in palabras.CursoRuso.Lesion1]
# words5 = [words[i: i + 5] for i in range(0, len(words), 5)]
palabras1 = ['карандаш', 'ручка', 'журнал', 'газета', 'вода']
palabras2 = ['чай', 'кофе', 'молоко', 'кефир']
palabras3 = ['люди', 'внук', 'внучка', 'браслет', 'часы']
palabras4 = ['книга', 'класс', 'библиотека', 'алгебра', 'стол']
plantilla.set_words(palabras4)
plantilla.set_mode(Mode.SINGLE_PAGE_WORDS)
#SI SE QUIEREN PLANTILLAS DE LETRAS, USAR letters
# plantilla.set_letters("hola")
plantilla.set_font(Fonts.OPENSANS)
plantilla.set_color(helpers.Colors.GREY)


# Guardar plantillas como png o en un pdf
# plantilla.save_png()
plantilla.save_pdf()
