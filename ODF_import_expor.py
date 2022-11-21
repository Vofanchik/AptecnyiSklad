from odf.opendocument import OpenDocumentText
from odf.style import ParagraphProperties, Style, TableColumnProperties
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

# p=OdtImport()
# p.form_odt()