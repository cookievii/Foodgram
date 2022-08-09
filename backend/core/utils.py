from django.http.response import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def download(ingredients):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'
    p = canvas.Canvas(response)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    p.setFont("FreeSans", 20)
    WIDTH = 60
    HEIGHT = 770
    p.drawString(WIDTH, HEIGHT, '  Ингредиенты: ')
    for add_new_string in ingredients:
        HEIGHT -= 30
        name = add_new_string['ingredients__name']
        measurement_unit = add_new_string['ingredients__measurement_unit']
        amount = add_new_string['ingredient_total']
        string = f'{name}({measurement_unit}) - {amount} шт.'
        p.drawString(WIDTH, HEIGHT, string)
    p.showPage()
    p.save()
    return response