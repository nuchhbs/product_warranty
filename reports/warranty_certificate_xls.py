from odoo import models


class WarrantyCertificateXLS(models.AbstractModel):
    _name = 'report.product_warranty.report_warranty_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, product_warranty):
        row = 2
        col = 0
        format1 = workbook.add_format({'font_size': 20, 'bold': True, 'align': 'center',
                                       'bg_color': '#D6EAF8'})
        format2 = workbook.add_format({'font_size': 16, 'align': 'vcenter', })
        format3 = workbook.add_format({'font_size': 23, 'bold': True, 'align': 'center'})
        format4 = workbook.add_format({'font_size': 16, 'align': 'right'})
        date_format = workbook.add_format({'font_size': 16, 'num_format': 'dd/mm/yyyy'})
        date_format2 = workbook.add_format({'font_size': 16, 'num_format': 'dd/mm/yyyy', 'align': 'left'})
        sheet = workbook.add_worksheet('Warranty Product Report')
        sheet.set_column('A:A', 70)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 30)
        sheet.set_column('G:G', 25)
        sheet.set_column('H:H', 20)
        for line in product_warranty:
            sheet.merge_range(0, 0, 0, 7, 'Warranty Product Report', format3)
            sheet.merge_range(1, 0, 1, 6, 'Date of issue:', format4)
            sheet.write(1, 7, line.date_action, date_format2)

            sheet.write(2, 0, 'Warranty Number', format1)
            sheet.write(2, 1, 'Product Name', format1)
            sheet.write(2, 2, 'Sale Order', format1)
            sheet.write(2, 3, 'Customer Name', format1)
            sheet.write(2, 4, 'Warranty Start Date', format1)
            sheet.write(2, 5, 'Warranty End Date', format1)
            sheet.write(2, 6, 'Warranty Type', format1)
            sheet.write(2, 7, 'Status', format1)

            row += 1
            sheet.write(row, col, line.warranty_seq, format2)
            sheet.write(row, col + 1, line.product_id.name, format2)
            sheet.write(row, col + 2, line.order_id.name, format2)
            sheet.write(row, col + 3, line.customer_id.name, format2)
            sheet.write(row, col + 4, line.date_start, date_format)
            sheet.write(row, col + 5, line.date_end, date_format)
            sheet.write(row, col + 6, line.type_id.name_period, format2)
            sheet.write(row, col + 7, line.state, format2)