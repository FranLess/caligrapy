from fonts import Fonts
from caligrafia import Plantilla
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
plantilla.accurate_cell_size_y(30)
plantilla.accurate_cell_size_x(50)
plantilla.set_language("ru")
#SI SE QUIEREN PLANTILLAS DE PALABRAS, USAR words
# plantilla.set_words(["HOLA", "MANOLA", "COLA"])
#SI SE QUIEREN PLANTILLAS DE LETRAS, USAR letters
plantilla.set_letters("adfñlk")
plantilla.set_font(Fonts.OPENSANS)
plantilla.set_color(helpers.Colors.GREY)


# Guardar plantillas como png o en un pdf
# plantilla.save_png()
plantilla.save_pdf()



