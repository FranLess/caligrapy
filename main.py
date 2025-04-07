from fonts import Fonts
from caligrafia import Plantilla
import palabras
import sheet

# Ejemplo de uso

#Crear una plantilla
plantilla = Plantilla()

#Configurar paramétros
plantilla.set_dpi(300)
plantilla.set_width(sheet.Carta.WIDTH)
plantilla.set_height(sheet.Carta.HEIGHT)
plantilla.set_margin(20)
#PARA ESPAÑOL Y LETRAS SEPARADAS
# plantilla.set_cell_size(15)
plantilla.set_letter_size(10)
# plantilla.set_letters("gG")

#PARA PALABRAS (habrá que cambiar el cell_size según la longitud de la palabra)
plantilla.set_mode(Plantilla.Mode.WORDS)
plantilla.set_cell_size(50)
plantilla.set_language("ru")
plantilla.set_letters(palabras.Palabras.Ruso.Существительные.человек.capitalize())
plantilla.set_font(Fonts.ROBOTO)
plantilla.set_color((216, 216, 216))


# Guardar plantillas como png o en un pdf
# plantilla.save_png()
plantilla.save_pdf()



