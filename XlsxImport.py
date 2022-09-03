from openpyxl import load_workbook
from docx import Document

from docx.enum.section import WD_ORIENT
from docx.shared import Mm

class Word_export:
    def form_docx():
        document = Document()
        section = document.sections[-1]
        # for section in sections:
        # change orientation to landscape
        # section.orientation = WD_ORIENT.LANDSCAPE
        # section.orientation = WD_ORIENT.LANDSCAPE
        # print(section.page_height, section.page_width)
        new_width, new_height = section.page_height, section.page_width
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Mm(297)
        section.page_height = Mm(210)

        table = document.add_table(rows=1, cols=10, style='Table Grid')
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '№ п/п'
        hdr_cells[1].text = 'Наименование объекта закупки (МНН)'
        hdr_cells[2].text = 'Лек. форма'
        hdr_cells[3].text = 'ОКПД / КТРУ'
        hdr_cells[4].text = 'Ед. изм.'
        hdr_cells[5].text = 'Доз-ка'
        hdr_cells[6].text = 'Кол-во'
        hdr_cells[
            7].text = 'Лекарственный препарат включен в перечень жизненно необходимых и важнейших лекарственных препаратов'
        hdr_cells[
            8].text = 'Наличие в лекарственном препарате наркотических средств, психотропных веществ и их прекурсоров'
        hdr_cells[9].text = 'Возможность взаимозаменяемости лекарственных препаратов'
        iterat = 1
        for KTRU, medicine, form, dose, mesure, is_GNVL, is_NSPV, interakt, total_q in inf_to_fill:
            row_cells = table.add_row().cells
            row_cells[0].text = str(iterat)
            row_cells[1].text = str(medicine)
            row_cells[2].text = form
            row_cells[3].text = KTRU
            row_cells[4].text = mesure
            row_cells[5].text = dose
            row_cells[6].text = total_q
            row_cells[7].text = is_GNVL
            row_cells[8].text = is_NSPV
            row_cells[9].text = interakt
            iterat += 1

        # sections = document.sections
        # for section in sections:
        #     # section.orientation = WD_ORIENT.PORTRAIT
        #     print(section.orientation)

        document.save('ТЗ.docx')

class XlsxImport:
    def __init__(self, file_name):
        self.file_name = file_name


    def import_into_list(self):
        wb2 = load_workbook(self.file_name)
        sheet = wb2.active
        rows = sheet.max_row
        # cols = sheet.max_column
        items = []
        for i in range(1, rows + 1):
            items_vals = []

            for j in range(2,5):
                items_vals.append(sheet.cell(row=i, column=j).value)
            items.append(items_vals)

        return items
