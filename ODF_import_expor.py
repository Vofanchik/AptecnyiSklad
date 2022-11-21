import datetime

from odf.opendocument import OpenDocumentText, load
from odf.style import ParagraphProperties, Style, TableColumnProperties, TextProperties
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.text import P


class OdtImport:
    def form_odt(self, inf_to_fill=None, file_name=None):
        textdoc = OpenDocumentText()

        tablecontents = Style(name="Table Contents", family="paragraph")
        tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
        textdoc.styles.addElement(tablecontents)

        widthshort = Style(name="Wshort", family="table-column")
        widthshort.addElement(TableColumnProperties(columnwidth="0.5cm"))
        textdoc.automaticstyles.addElement(widthshort)

        widthmed = Style(name="Wmed", family="table-column")
        widthmed.addElement(TableColumnProperties(columnwidth="2.0cm"))
        textdoc.automaticstyles.addElement(widthmed)

        widthwide = Style(name="Wwide", family="table-column")
        widthwide.addElement(TableColumnProperties(columnwidth="5.5cm"))
        textdoc.automaticstyles.addElement(widthwide)

        p = P(text=('Остатки по состоянию на {:%d.%m.%Y}'.format(datetime.date.today())))
        textdoc.text.addElement(p)

        table = Table()
        table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthshort))
        table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthwide))
        table.addElement(TableColumn(numbercolumnsrepeated=2, stylename=widthmed))

        col_names = ['№ п/п', 'Наименование', 'Ед. измерения', 'Кол-во']

        tr = TableRow()
        table.addElement(tr)

        for val in col_names:
            tc = TableCell()
            tr.addElement(tc)
            p = P(stylename=tablecontents, text=val)
            tc.addElement(p)

        for pp, lst in enumerate(inf_to_fill):
            tr = TableRow()
            table.addElement(tr)

            list_of_cols = [str(pp+1), lst[0], lst[1], lst[3]]

            for i in list_of_cols:
                tc = TableCell()
                tr.addElement(tc)
                p = P(stylename=tablecontents, text=i)
                tc.addElement(p)



        textdoc.text.addElement(table)
        textdoc.save(file_name)

class OdsExport:
    def export_from_ods(self, file_name):
        d = load(file_name)
        rows = d.getElementsByType(TableRow)
        items = []
        for row in rows:
            cells = row.getElementsByType(TableCell)
            for cell in cells:
                tps = cell.getElementsByType(P)
                for x in tps:
                    items.append(str(x.firstChild))

        res = list(zip(items[1::4], items[2::4], items[3::4]))
        print(res)
        return res


# p=OdtImport()
# p.form_odt()