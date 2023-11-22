from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH

class TableSetupUtils():
    def set_cell_center(table):
        for row in table.rows:
            cells = row.cells
            # Set the alignment of text in each cell to center
            for cell in cells:
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

                for paragraph in cell.paragraphs:
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    def set_header_bold(table):
        hdr_row = table.rows[0]
        for cell in hdr_row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.bold = True