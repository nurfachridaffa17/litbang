############################################################################
#
#  Model Name: satker_rengar.headKertasKerjaInherit
#  Description: Field dan method untuk entitas headKertasKerjaInherit
#  File Name: print_xlsx_rengar.py
#  Created On: 07/01/2019, 14:27
#  Snipet: tp_model_generic
#  Author: Matrica
#
############################################################################
import base64
import locale

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import tools
from odoo.exceptions import Warning
from odoo import api, fields , models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from itertools import izip

import xlwt
from cStringIO import StringIO

class headKertasKerjaInherit(models.Model):
    # ORM ------------------------------------------------------------------------------------ ORM #
    _translate = True
    _inherit = ['head.kertas.kerja']                 # ['mail.thread','other.model'] for oppenchatter


    # FIELDS ------------------------------------------------------------------------------- FIELD #


    # METHOD ------------------------------------------------------------------------------ METHOD #
    @api.multi
    def button_excel(self):
        cr, uid, context = self.env.args
        if context is None:
            context = {}
        context = dict(context)
        data = self.read()[0]
        get_date = data.get('date', False)
        # res_user = self.env["res.users"].browse(uid)
        # Create bank summary report in Excel file.
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')
        # today = datetime.now()
        # =============Date Style============
        # context.update({'date_act': get_date})
        # # locale.setlocale(locale.LC_ALL, 'deu_deu')
        # post_date = datetime.strptime(context.get("date_act"),
        #                               DEFAULT_SERVER_DATE_FORMAT)
        # post_date_footer_formate = post_date.strftime('%d %B %Y')
        # sign_date_formate = today.strftime('Jakarta,  %d %B %Y')
        # post_day_formate = post_date.strftime('%A')
        # post_year_formate = post_date.strftime('%Y')
        # posting_year_formate = 'TAHUN ANGGARAN : ' + tools.ustr(post_year_formate)
        # post_month_formate = post_date.strftime('%B')
        # posting_month_formate = 'BULAN : ' + tools.ustr(post_month_formate)
        # footer1 = 'Pada hari ini ' + tools.ustr(post_day_formate) + ' tanggal ' + tools.ustr(post_date_footer_formate) + \
        #           ' untuk keperluan Buku kas - Bank ditutup dengan sisa sebesar'
        # sign_date = tools.ustr(sign_date_formate)
        # =============Font Style============
        font1 = 'Arial Narrow'
        size1 = 200
        kegiatan_height = 1000
        penelitian_height = 500
        # header = xlwt.easyxf('font: bold 1, height 280')
        kop = xlwt.easyxf('font: height 160; align: horiz center')
        kop.font.name = font1
        kop_u = xlwt.easyxf('font: underline 1, height 160; align: horiz center')
        kop_u.font.name = font1
        judul1 = xlwt.easyxf('font: underline 1, height 340; align: horiz center')
        judul1.font.name = font1
        judul2 = xlwt.easyxf('font: height 160; align: horiz center')
        judul2.font.name = font1

        # style = xlwt.easyxf('align: wrap yes')
        align_ment = xlwt.Alignment()
        align_ment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        # =============Border Style============
        borders = xlwt.Borders()
        borders.top = xlwt.Borders.MEDIUM
        borders.bottom = xlwt.Borders.MEDIUM
        borders.left = xlwt.Borders.MEDIUM
        borders.right = xlwt.Borders.MEDIUM

        header_border_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')  # Create Style
        header_border_style.borders = borders
        header_border_style.font.name = font1
        header_border_style.font.bold = True
        header_border_style.font.height = size1
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
        header_border_style.pattern = pattern

        borders1 = xlwt.Borders()
        borders1.top = xlwt.Borders.THIN
        borders1.bottom = xlwt.Borders.THIN
        borders1.left = xlwt.Borders.THIN
        borders1.right = xlwt.Borders.THIN

        normal_border_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')  # Create Style
        normal_border_style.borders = borders1
        normal_border_style.font.name = font1
        normal_border_style.font.height = size1

        normal_left_border_style = xlwt.easyxf('align: wrap yes, horiz left, vert center')  # Create Style
        normal_left_border_style.borders = borders1
        normal_left_border_style.font.name = font1
        normal_left_border_style.font.height = size1

        normal_style = xlwt.easyxf('align: wrap yes, horiz left, vert center')
        normal_style.font.name = font1
        normal_style.font.height = size1

        bold_style = xlwt.easyxf('align: wrap yes, horiz left, vert center')
        bold_style.font.name = font1
        bold_style.font.height = size1
        bold_style.font.bold = True

        bold_border_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')
        bold_border_style.borders = borders1
        bold_border_style.font.name = font1
        bold_border_style.font.height = size1
        bold_border_style.font.bold = True

        bold_left_border_style = xlwt.easyxf('align: wrap yes, horiz left, vert center')
        bold_left_border_style.borders = borders1
        bold_left_border_style.font.name = font1
        bold_left_border_style.font.height = size1
        bold_left_border_style.font.bold = True

        bold_border_kegiatan_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')
        bold_border_kegiatan_style.borders = borders1
        # bold_border_kegiatan_style.font.name = font1
        # bold_border_kegiatan_style.font.height = size1 +20
        bold_border_kegiatan_style.font.bold = True

        bold_big_border_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')
        bold_big_border_style.borders = borders1
        bold_big_border_style.font.name = font1
        bold_big_border_style.font.height = size1 + 50
        bold_big_border_style.font.bold = True

        italic_border_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')  # Create Style
        italic_border_style.borders = borders1
        italic_border_style.font.name = font1
        italic_border_style.font.height = size1
        italic_border_style.font.italic = True


        footer_border_style = xlwt.easyxf('align: wrap yes, horiz left, vert center')
        footer_border_style.font.name = font1
        footer_border_style.font.height = size1

        footer_saldo_border_style = xlwt.easyxf('align: wrap yes, horiz left, vert center')
        footer_saldo_border_style.font.name = font1
        footer_saldo_border_style.font.height = size1
        footer_saldo_border_style.borders.top = xlwt.Borders.MEDIUM
        footer_saldo_border_style.borders.bottom = xlwt.Borders.MEDIUM

        footer_under_border_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')  # Create Style
        footer_under_border_style.font.name = font1
        footer_under_border_style.font.height = size1
        footer_under_border_style.font.underline = True

        footer_sign_style = xlwt.easyxf('align: wrap yes, horiz center, vert center')  # Create Style
        footer_sign_style.font.name = font1
        footer_sign_style.font.height = size1
        # =============Money Style ============
        normal_just_money_border_style = xlwt.easyxf('align: wrap yes, horiz distributed, vert center')  # Create Style
        normal_just_money_border_style.borders = borders1
        normal_just_money_border_style.font.name = font1
        normal_just_money_border_style.font.height = size1
        normal_just_money_border_style.num_format_str = '"Rp. "#,##0_);("Rp. "#,##'

        bold_just_money_border_style = xlwt.easyxf('align: wrap yes, horiz distributed, vert center')  # Create Style
        bold_just_money_border_style.borders = borders1
        bold_just_money_border_style.font.name = font1
        bold_just_money_border_style.font.height = size1
        bold_just_money_border_style.num_format_str = '"Rp. "#,##0_);("Rp. "#,##'
        bold_just_money_border_style.font.bold = True

        italic_just_money_border_style = xlwt.easyxf('align: wrap yes, horiz distributed, vert center')  # Create Style
        italic_just_money_border_style.borders = borders1
        italic_just_money_border_style.font.name = font1
        italic_just_money_border_style.font.height = size1
        italic_just_money_border_style.num_format_str = '"Rp. "#,##0_);("Rp. "#,##'
        italic_just_money_border_style.font.italic = True

        bold_big_money_border_style = xlwt.easyxf('align: wrap yes, horiz distributed, vert center')
        bold_big_money_border_style.borders = borders1
        bold_big_money_border_style.font.name = font1
        bold_big_money_border_style.font.height = size1 + 50
        bold_big_money_border_style.font.bold = True
        bold_big_money_border_style.num_format_str = '"Rp. "#,##0_);("Rp. "#,##'
        # =============Header size ============
        worksheet.col(0).width = 3500  # Rincian
        worksheet.col(1).width = 1500  # Rincian 2
        worksheet.col(2).width = 9000  # Rincian 3
        worksheet.col(3).width = 4000  # Volume Sub Output
        worksheet.col(4).width = 5000  # Jenis Komponen (Utama/Pendukung)
        worksheet.col(5).width = 4000  # Rincian Perhitungan ( Uraian )
        worksheet.col(6).width = 2000  # Rincian Perhitungan ( Jumlah )
        worksheet.col(7).width = 3000  # Harga Satuan
        worksheet.col(8).width = 5000  # Jumlah

        worksheet.row(0).height = 500
        worksheet.row(1).height = 500
        worksheet.row(2).height = 500
        # =============KOP ============
        worksheet.write_merge(0, 0, 0, 2, "MARKAS BESAR", kop)
        worksheet.write_merge(1, 1, 0, 2, "KEPOLISIAN NEGARA REPUBLIK INDONESIA", kop)
        worksheet.write_merge(2, 2, 0, 2, "PUSAT PENELITIAN DAN PENGEMBANGAN", kop_u)
        # =============Judul============
        # keluaran_output = "Keluaran (Output) " + self.rengar_program.name
        worksheet.write_merge(5, 5, 3, 5, "RINCIAN ANGGARAN BIAYA (RAB)", judul1)
        # worksheet.write_merge(6, 6, 3, 5, "RINCIAN ANGGARAN BIAYA (RAB)", judul1)
        # worksheet.write_merge(7, 7, 3, 5, "RINCIAN ANGGARAN BIAYA (RAB)", judul1)
        row = 6
        # =============Header============
        nama_program = ": " + self.rengar_program.name
        # nama_output = ": " + self.rengar_program.name
        total_amount_expense = ": Rp." + str('{0:,.0f}'.format(int(self.total_amount_expense))) + ",-"
        #satuan ukur static
        #volume di compute
        #jenis komponen tidak tau
        #volume rincian tidak jelas
        #monetary satuan
        #wrap test

        # =============Formula Header============
        volume = 0
        for kertas in self.advance_expense_line_ids:
            volume += len(kertas.advance_expense_line_ids)
            # volume[kertas.rengar_kegiatan.name] += kertas.rengar_kegiatan.name

        row += 1
        worksheet.write_merge(row, row, 0, 1, "Kementrian Negara/Lembaga", normal_style)
        worksheet.write_merge(row, row, 2, 3, ": Kepolisian Negara Republik Indonesia", normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Unit Eselon II/ Satker ", normal_style)
        worksheet.write_merge(row, row, 2, 3, ": Puslitbang Polri", normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Program", normal_style)
        worksheet.write_merge(row, row, 2, 3, nama_program , normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Kegiatan", normal_style)
        worksheet.write_merge(row, row, 2, 3, ": nama kegiatan", normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Keluaran (Output)", normal_style)
        worksheet.write_merge(row, row, 2, 3, ": nama keluaran", normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Volume", normal_style)
        worksheet.write_merge(row, row, 2, 3, ": " + volume", normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Satuan Ukur", normal_style)
        worksheet.write_merge(row, row, 2, 3, ": Dokumen", normal_style)
        row += 1
        worksheet.write_merge(row, row, 0, 1, "Alokasi Dana", normal_style)
        worksheet.write_merge(row, row, 2, 3, total_amount_expense, normal_style)
        row += 3

        # =============Table Header============
        worksheet.write_merge(row, row + 1, 0, 0, "KODE", header_border_style)
        worksheet.write_merge(row, row + 1, 1, 2, "URAIAN SUBOUTPUT/KOMPONEN /SUBKOMPONEN/AKUN/DETIL", header_border_style)
        worksheet.write_merge(row, row + 1, 3, 3, "VOLUME SUB OUTPUT", header_border_style)
        worksheet.write_merge(row, row + 1, 4, 4, "JENIS KOMPONEN UTAMA/PENDUKUNG", header_border_style)
        worksheet.write_merge(row, row , 5, 6, "RINCIAN PERHITUNGAN", header_border_style)
        worksheet.write_merge(row + 1, row + 1, 5, 5, "URAIAN", header_border_style)
        worksheet.write_merge(row +1, row + 1, 6, 6, "JUMLAH", header_border_style)
        worksheet.write_merge(row, row + 1, 7, 7, "HARGA SATUAN", header_border_style)
        worksheet.write_merge(row, row + 1, 8, 8, "JUMLAH", header_border_style)
        row +=2
        worksheet.write(row, 0, "1", header_border_style)
        worksheet.write_merge(row, row, 1, 2, "2", header_border_style)
        for x in range(3,5):
            worksheet.write(row, x, x, header_border_style)
        worksheet.write_merge(row, row, 5, 6, "5", header_border_style)
        worksheet.write(row, 7, "6", header_border_style)
        worksheet.write(row, 8, "7", header_border_style)
        # =============Programe Table============
        row += 1

        kegiatan_compare = ""
        output_compare = ""
        suboutput_compare = ""
        komponen_compare = ""
        subkomponen_compare = ""
        for kertas in self.advance_expense_line_ids :
            if kegiatan_compare != kertas.rengar_kegiatan.name:
                worksheet.write(row, 0, kertas.rengar_kegiatan.code, bold_big_border_style)
                worksheet.write_merge(row, row, 1, 2, kertas.rengar_kegiatan.name, bold_big_border_style)
                worksheet.write(row, 3, "", bold_big_border_style)
                worksheet.write(row, 4, "Utama", bold_big_border_style)
                worksheet.write(row, 5, "", bold_big_border_style)
                worksheet.write(row, 6, volume, bold_big_border_style)
                worksheet.write(row, 7, "", bold_big_border_style)
                worksheet.write(row, 8, kertas.total_amount_expense, bold_big_money_border_style)
                kegiatan_compare = kertas.rengar_kegiatan.name
                row += 1

            for rengar_output in kertas.rengar_output:
                if output_compare != rengar_output.name:
                    worksheet.write(row, 0, rengar_output.code, italic_border_style)
                    worksheet.write_merge(row, row, 1, 2, rengar_output.name, italic_border_style)
                    for x in range(3, 8):
                        worksheet.write(row, x, "", italic_border_style)
                    worksheet.write(row, 8, kertas.total_amount_expense, italic_just_money_border_style)
                    output_compare = rengar_output.name
                    row += 1

                for rengar_suboutput in kertas.rengar_suboutput:
                    if suboutput_compare != rengar_suboutput.name:
                        worksheet.write(row, 0, rengar_suboutput.code, italic_border_style)
                        worksheet.write_merge(row, row, 1, 2, rengar_suboutput.name, italic_border_style)
                        for x in range(3, 8):
                            worksheet.write(row, x, "", italic_border_style)
                        worksheet.write(row, 8, kertas.total_amount_expense, italic_just_money_border_style)
                        suboutput_compare = rengar_suboutput.name
                        row += 1

                    for rengar_komponen in kertas.rengar_komponen:
                        if komponen_compare != rengar_komponen.name:
                            worksheet.write(row, 0, rengar_komponen.code, bold_border_style)
                            worksheet.write_merge(row, row, 1, 2, rengar_komponen.name, bold_border_style)
                            for x in range(3, 8):
                                worksheet.write(row, x, "", bold_border_style)
                            worksheet.write(row, 8, kertas.total_amount_expense, bold_just_money_border_style)
                            komponen_compare = rengar_komponen.name
                            row += 1

                        # for advance_expese in kertas.advance_expense_line_ids:
                            # volume += 1

                        for rengar_subkomponen in kertas.rengar_subkomponen:
                            if subkomponen_compare != rengar_subkomponen.name:
                                worksheet.write(row, 0, rengar_subkomponen.code, bold_border_style)
                                worksheet.write_merge(row, row, 1, 2, rengar_subkomponen.name, bold_border_style)
                                worksheet.write(row, 3, len(kertas.advance_expense_line_ids), italic_border_style)
                                for x in range(4, 8):
                                    worksheet.write(row, x, "", bold_border_style)
                                worksheet.write(row, 8, kertas.total_amount_expense, bold_just_money_border_style)
                                subkomponen_compare = rengar_subkomponen.name
                                row += 1


        row += 2
        # =============Komponen Table============
        for paper in self.advance_expense_line_ids:
            for rengar_subkomponen in paper.rengar_subkomponen:
                row += 1
                # =============Table Header============
                worksheet.write_merge(row, row + 1, 0, 0, "KODE", header_border_style)
                worksheet.write_merge(row, row + 1, 1, 2, "URAIAN SUBOUTPUT/KOMPONEN /SUBKOMPONEN/AKUN/DETIL",
                                      header_border_style)
                worksheet.write_merge(row, row + 1, 3, 3, "VOLUME SUB OUTPUT", header_border_style)
                worksheet.write_merge(row, row + 1, 4, 4, "JENIS KOMPONEN UTAMA/PENDUKUNG", header_border_style)
                worksheet.write_merge(row, row, 5, 6, "RINCIAN PERHITUNGAN", header_border_style)
                worksheet.write_merge(row + 1, row + 1, 5, 5, "URAIAN", header_border_style)
                worksheet.write_merge(row + 1, row + 1, 6, 6, "JUMLAH", header_border_style)
                worksheet.write_merge(row, row + 1, 7, 7, "HARGA SATUAN", header_border_style)
                worksheet.write_merge(row, row + 1, 8, 8, "JUMLAH", header_border_style)
                row += 2
                worksheet.write(row, 0, "1", header_border_style)
                worksheet.write_merge(row, row, 1, 2, "2", header_border_style)
                for x in range(3, 5):
                    worksheet.write(row, x, x, header_border_style)
                worksheet.write_merge(row, row, 5, 6, "5", header_border_style)
                worksheet.write(row, 7, "6", header_border_style)
                worksheet.write(row, 8, "7", header_border_style)
                row += 1
                #================Nama kegiatan===========
                worksheet.row(row).height_mismatch = True
                worksheet.row(row).height = kegiatan_height
                worksheet.write(row, 0,  rengar_subkomponen.code, bold_border_kegiatan_style)
                worksheet.write_merge(row, row, 1, 2, rengar_subkomponen.name , bold_border_kegiatan_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", bold_border_kegiatan_style)
                worksheet.write(row, 8, "", bold_border_kegiatan_style)
                row += 1


                worksheet.write(row, 0, "", normal_border_style)
                worksheet.write_merge(row, row, 1, 2, "", normal_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", normal_border_style)
                worksheet.write(row, 8, "", normal_border_style)
                row += 1
                worksheet.write(row, 0, "", header_border_style)
                worksheet.write_merge(row, row, 1, 2, "", header_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", header_border_style)
                worksheet.write(row, 8, "", header_border_style)
                row += 1
            #=================== Judul Penelitian-adv========
            for paper_adv in paper.advance_expense_line_ids:
                worksheet.row(row).height_mismatch = True
                worksheet.row(row).height = penelitian_height
                worksheet.write(row, 0, "", bold_border_style)
                worksheet.write_merge(row, row, 1, 2,paper_adv.note, bold_border_style)
                worksheet.write(row, 3,paper_adv.time_volume, bold_border_style)
                for x in range(4, 8):
                    worksheet.write(row, x, "", bold_border_style)
                worksheet.write(row, 8, paper_adv.total_amount, bold_just_money_border_style)
                row += 1

                worksheet.write(row, 0, "", normal_border_style)
                worksheet.write_merge(row, row, 1, 2, "", normal_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", normal_border_style)
                worksheet.write(row, 8, "", normal_border_style)
                row += 1
                #========================================================PERENCANAAN=========================
                worksheet.write(row, 0, "", bold_border_style)
                worksheet.write(row, 1, "I.", bold_border_style)
                worksheet.write(row, 2, "TAHAP PERENCANAAN", bold_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", bold_border_style)
                worksheet.write(row, 8, paper_adv.subtotal1, bold_just_money_border_style)
                row += 1
                #========detail1
                jml_detail1 = 0
                ur_item = 0
                header_1 = ""
                header_2 = ""
                ur_abj = chr(ord('a'))
                for hitung_ttl in paper_adv.advance_expense_line_ids:
                    jml_detail1 += hitung_ttl.unit_amount * hitung_ttl.quantity

                for paper_adv_adv in paper_adv.advance_expense_line_ids:
                    if header_1 != paper_adv_adv.detail1.name:
                        worksheet.write(row, 0, paper_adv_adv.detail1.account_id.code or '', bold_border_style)
                        worksheet.write(row, 1, ur_abj + ".", bold_border_style)
                        worksheet.write(row, 2, paper_adv_adv.detail1.name or '', bold_left_border_style)
                        for x in range(3, 8):
                            worksheet.write(row, x, "", bold_border_style)
                        # worksheet.write(row, 8, jml_detail1, bold_just_money_border_style) # Angka total Header 1 belum benar
                        header_1 = paper_adv_adv.detail1.name
                        ur_abj = chr(ord(ur_abj) + 1)
                        row += 1

                    # ========header2
                    if header_2 != paper_adv_adv.detail2.name:
                        worksheet.write(row, 0, '', bold_border_style)
                        worksheet.write(row, 1, '', bold_border_style)
                        worksheet.write(row, 2, paper_adv_adv.detail2.name or '', bold_left_border_style)
                        for x in range(3, 9):
                            worksheet.write(row, x, '', bold_border_style)
                        # worksheet.write(row, 8, jml_detail1, bold_just_money_border_style) # Angka total Header 1 belum benar
                        header_2 = paper_adv_adv.detail2.name
                        row += 1

                    #===============================detail komponen===================
                    ur_item += 1
                    worksheet.write(row, 0, "", normal_left_border_style)
                    worksheet.write(row, 1, str(ur_item) + ".", normal_border_style)
                    worksheet.write(row, 2, paper_adv_adv.detail3.name, normal_left_border_style)
                    for x in range(3, 5):
                        worksheet.write(row, x, "", normal_left_border_style)
                    #worksheet.write(row, 5, tools.ustr(int(paper_adv_adv.quantity)) + paper_adv_adv.product_uom_id.name, normal_left_border_style)
                    worksheet.write(row, 5, paper_adv_adv.uraian or '', normal_border_style)
                    worksheet.write(row, 6, paper_adv_adv.quantity, normal_border_style)
                    worksheet.write(row, 7, paper_adv_adv.unit_amount, normal_just_money_border_style)
                    worksheet.write(row, 8, paper_adv_adv.unit_amount * paper_adv_adv.quantity, normal_just_money_border_style)
                    row += 1


                # ========================================================PELAKSANAAN=========================
                worksheet.write(row, 0, "", normal_border_style)
                worksheet.write_merge(row, row, 1, 2, "", normal_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", normal_border_style)
                worksheet.write(row, 8, "", normal_border_style)
                row += 1

                worksheet.write(row, 0, "", bold_border_style)
                worksheet.write(row, 1, "II.", bold_border_style)
                worksheet.write(row, 2, "TAHAP PELAKSANAAN", bold_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", bold_border_style)
                worksheet.write(row, 8, paper_adv.subtotal2, bold_just_money_border_style)
                row += 1
                # ========detail1
                jml_detail1 = 0
                ur_item = 0
                header_1 = ""
                header_2 = ""
                ur_abj2 = chr(ord('a'))
                for hitung_ttl in paper_adv.advance_expense_line_ids2:
                    jml_detail1 += hitung_ttl.unit_amount * hitung_ttl.quantity

                for paper_adv_adv2 in paper_adv.advance_expense_line_ids2:
                    if header_1 != paper_adv_adv2.detail1.name:
                        worksheet.write(row, 0, paper_adv_adv2.detail1.account_id.code or '', bold_border_style)
                        worksheet.write(row, 1, ur_abj2 + ".", bold_border_style)
                        worksheet.write(row, 2, paper_adv_adv2.detail1.name or '', bold_left_border_style)
                        for x in range(3, 9):
                            worksheet.write(row, x, "", bold_border_style)
                        # worksheet.write(row, 8, jml_detail1, bold_just_money_border_style) # Angka total Header 1 belum benar
                        header_1 = paper_adv_adv2.detail1.name
                        ur_abj2 = chr(ord(ur_abj2) + 1)
                        row += 1

                    # ========header2
                    if header_2 != paper_adv_adv2.detail2.name:
                        worksheet.write(row, 0, '', bold_border_style)
                        worksheet.write(row, 1, '', bold_border_style)
                        worksheet.write(row, 2, paper_adv_adv2.detail2.name or '', bold_left_border_style)
                        for x in range(3, 9):
                            worksheet.write(row, x, '', bold_border_style)
                        # worksheet.write(row, 8, jml_detail1, bold_just_money_border_style) # Angka total Header 1 belum benar
                        header_2 = paper_adv_adv2.detail2.name
                        row += 1

                    # ===============================detail komponen===================
                    ur_item += 1
                    worksheet.write(row, 0, "", normal_left_border_style)
                    worksheet.write(row, 1, str(ur_item) + ".", normal_border_style)
                    worksheet.write(row, 2, paper_adv_adv2.detail3.name, normal_left_border_style)
                    for x in range(3, 5):
                        worksheet.write(row, x, "", normal_left_border_style)
                    # worksheet.write(row, 5, tools.ustr(int(paper_adv_adv2.quantity)) + paper_adv_adv2.product_uom_id.name,
                                    # normal_left_border_style)
                    worksheet.write(row, 5, paper_adv_adv2.uraian or '', normal_border_style)
                    worksheet.write(row, 6, paper_adv_adv2.quantity, normal_border_style)
                    worksheet.write(row, 7, paper_adv_adv2.unit_amount, normal_just_money_border_style)
                    worksheet.write(row, 8, paper_adv_adv2.unit_amount * paper_adv_adv2.quantity, normal_just_money_border_style)
                    row += 1


                # ========================================================AKHIR=========================
                worksheet.write(row, 0, "", normal_border_style)
                worksheet.write_merge(row, row, 1, 2, "", normal_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", normal_border_style)
                worksheet.write(row, 8, "", normal_border_style)
                row += 1

                worksheet.write(row, 0, "", bold_border_style)
                worksheet.write(row, 1, "III.", bold_border_style)
                worksheet.write(row, 2, "TAHAP AKHIR", bold_border_style)
                for x in range(3, 8):
                    worksheet.write(row, x, "", bold_border_style)
                worksheet.write(row, 8, paper_adv.subtotal3, bold_just_money_border_style)
                row += 1
                # ========detail1
                jml_detail1 = 0
                ur_item = 0
                header_1 = ""
                header_2 = ""
                ur_abj3 = chr(ord('a'))
                for hitung_ttl in paper_adv.advance_expense_line_ids3:
                    jml_detail1 += hitung_ttl.unit_amount * hitung_ttl.quantity

                for paper_adv_adv3 in paper_adv.advance_expense_line_ids3:
                    if header_1 != paper_adv_adv3.detail1.name:
                        worksheet.write(row, 0, paper_adv_adv3.detail1.account_id.code or '', bold_border_style)
                        worksheet.write(row, 1, ur_abj3 + ".", bold_border_style)
                        worksheet.write(row, 2, paper_adv_adv3.detail1.name or '', bold_left_border_style)
                        for x in range(3, 8):
                            worksheet.write(row, x, "", bold_border_style)
                        # worksheet.write(row, 8, jml_detail1, bold_just_money_border_style) # Angka total Header 1 belum benar
                        header_1 = paper_adv_adv3.detail1.name
                        ur_abj3 = chr(ord(ur_abj3) + 1)
                        row += 1

                    # ========header2
                    if header_2 != paper_adv_adv3.detail2.name:
                        worksheet.write(row, 0, '', bold_border_style)
                        worksheet.write(row, 1, '', bold_border_style)
                        worksheet.write(row, 2, paper_adv_adv3.detail2.name or '', bold_left_border_style)
                        for x in range(3, 9):
                            worksheet.write(row, x, '', bold_border_style)
                        # worksheet.write(row, 8, jml_detail1, bold_just_money_border_style) # Angka total Header 1 belum benar
                        header_2 = paper_adv_adv3.detail2.name
                        row += 1

                    # ===============================detail komponen===================
                    ur_item += 1
                    worksheet.write(row, 0, "", normal_left_border_style)
                    worksheet.write(row, 1, str(ur_item) + ".", normal_border_style)
                    worksheet.write(row, 2, paper_adv_adv3.detail3.name, normal_left_border_style)
                    for x in range(3, 5):
                        worksheet.write(row, x, "", normal_left_border_style)
                    # worksheet.write(row, 5,
                                    # tools.ustr(int(paper_adv_adv3.quantity)) + paper_adv_adv3.product_uom_id.name,
                                    # normal_left_border_style)
                    worksheet.write(row, 5, paper_adv_adv3.uraian or '', normal_border_style)
                    worksheet.write(row, 6, paper_adv_adv3.quantity, normal_border_style)
                    worksheet.write(row, 7, paper_adv_adv3.unit_amount, normal_just_money_border_style)
                    worksheet.write(row, 8, paper_adv_adv3.unit_amount * paper_adv_adv3.quantity,
                                    normal_just_money_border_style)
                    row += 1









        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        res = base64.b64encode(data)
        excel_export_summay_id = self.env['excel.export.summay'].create({'name': 'Rincian Anggaran Program.xls', 'file': res})
        return {
            'name': _('Download Excel'),
            'res_id': excel_export_summay_id.id,
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'excel.export.summay',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }