from openpyxl import load_workbook

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
