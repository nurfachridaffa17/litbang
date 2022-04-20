from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import time
from Tkconstants import LEFT
from datetime import date
from time import gmtime, strftime

class surat_masuk_fix(models.Model):
    _name           = 'surat_masuk_fix'  # nama model  
    _description    = 'Model TNDE Surat Masuk' 
    
    _inherit        = ['mail.thread', 'ir.needaction_mixin'] #untuk Notif Jumlah Surat Yang belum Dibaca
        
    # _order          = 'tindakan, tindakan desc' #Menampilkan List Data DESC / ASC
    
    name            = fields.Char(string="Nomor Surat", required=False)
    kategori_id     = fields.Many2one(comodel_name='tnde.kategori',required=True,string= 'Kategori Surat')
    jenis_surat     = fields.Many2one(comodel_name='tnde.m_pengaturan_master_surat', string="Jenis Surat", required=True)
    disposisi_ids   = fields.One2many(comodel_name='surat.masuk.disposisi', string="Disposisi", inverse_name='surat_masuk_fix_id', ondelete='cascade')
    no_agenda       = fields.Char(string="Nomor Agenda")  
    no_surat        = fields.Integer(string="Nomor Surat")
    asal_surat      = fields.Many2one(comodel_name='asal_surat', string="Asal Surat", required=True)
    tgl_surat       = fields.Date(string="Tgl Surat", required=True)
    tgl_diterima    = fields.Date(string="Tgl Terima Surat", required=True)  
    date_due        = fields.Datetime(string="Limit Respon", required=False)  
    perihal         = fields.Char(string="Perihal", required=True)
    sifat_surat     = fields.Selection([('Biasa', 'Biasa'),('Rahasia', 'Rahasia'),('Kompidensil', 'Kompidensil')], string='Sifat Surat', default='Biasa')
    tujuan_surat    = fields.Many2many('hr.employee', string="Tujuan Surat", required=True)
    scan_surat      = fields.Binary(string="Scan Surat", required=True)
    lampiran        = fields.Char("lampiran")
    keterangan      = fields.Text("Keterangan")
    tindakan        = fields.Selection([('Biasa', 'Biasa'),('Cepat', 'Cepat')], string='Respon', default='Biasa')
    state           = fields.Selection([('Proses', 'Proses'),('Confirm', 'Confirm'),('Selesai', 'Selesai')], string='State', default='Proses')

    def confirm(self, vals):
        bln_romawi  = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        get_thn_now = str(datetime.now().strftime("%Y"))
        get_bln_now = int(datetime.now().strftime("%m"))   
        self.env.cr.execute("""
                            SELECT
                                MAX(s.no_surat) AS no_max 
                            FROM
                                surat_masuk_fix s 
                            WHERE
                                date_part ( 'year', s.create_date ) = date_part ( 'year', CURRENT_DATE )
                            AND kategori_id = %s
                            """,(self.kategori_id.id,))
        get_no_max  = self.env.cr.dictfetchall()
        print get_no_max
        next_no_max = 1
        for data in get_no_max :
            if data['no_max'] :
                next_no_max = int(data['no_max']) + 1
                print 'Uda Ada'
            else :
                print 'Belum Ada'
        kategori = self.kategori_id.name
        print "ada kok ini buktinya",self.kategori_id.name
        
        if kategori:            
            str_no_agenda       = kategori + "/" +str(next_no_max) + "/" + bln_romawi[get_bln_now - 1] + "/" + get_thn_now  
            print "hahahahhahah",str_no_agenda        
            self.no_agenda   = str(str_no_agenda)
            self.no_surat    = str(next_no_max)
            self.state='Confirm'
        else :
            self.state='Confirm'
        
        for row in self:
            mail = row.tujuan_surat
            for role in mail:
                template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'template_mail_surat_masuk')
                body = template_obj.body_html
                body=body.replace('<---aa--->',str(row.id))
                body=body.replace('--tindakan--',str(row.tindakan))
                body=body.replace('--limit--',str(row.date_due))
                if template_obj:
                    mail_values = {
                        'subject': template_obj.subject,
                        'body_html': body,
                        'email_to':''.join(map(lambda x: x, role.work_email)),
                        # 'email_cc':';'.join(map(lambda x: x, email_cc)),
                        'email_from': template_obj.email_from,
                    }
                create_and_send_email = self.env['mail.mail'].create(mail_values).send() 

    # ---- end


    def baca_surat(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        user_id = employee.id
        self.env.cr.execute("""
                            UPDATE surat_masuk_disposisi
                            SET state='Dibaca' 
                            WHERE tujuan_id = %s 
                            AND surat_masuk_fix_id = %s
                            """,(user_id,self.id))
#         action = self.env.ref('tnde.surat_masuk_fix') 
#         print self.id
        return{
            'type'      : 'ir.actions.act_window',
            'name'      : '',
            'view_type' : 'form',
            'view_mode' : 'form',
#             'domain'    : [('id', 'in', [self.id])],
            'res_model' : 'surat_masuk_fix',
#             'context'   : {'default_surat_masuk_fix_id':self.id },
            'res_id'    : self.id,
#             'view_id'   : self.id,
            'target'    : 'current'
            }


    def disposisi_surat(self):
        action = self.env.ref('tnde.view_surat_masuk_fix_popup')
        # manggil form, action, tree
        return{
            'type'      : 'ir.actions.act_window',
            'name'      : 'Form Disposisi',
            'view_type' : 'form',
            'view_mode' : 'form',
            'domain'    : '',
            'res_model' : 'surat.masuk.disposisi',
            'context'   : {'default_surat_masuk_fix_id':self.id, 'default_surat_masuk_fix_id':self.id },
            'view_id'   : action.id,
            'target'    : 'new'
            }

    def view_disposisi(self):
        action = self.env.ref('tnde.list_disposisi_sm') 
        print self.id
        return{
            'type'      : 'ir.actions.act_window',
            'name'      : 'List Disposisi',
            'view_type' : 'form',
            'view_mode' : 'tree',
            'domain'    : [('surat_masuk_fix_id', 'in', [self.id])],
            'res_model' : 'surat.masuk.disposisi',
#             'context'   : {'default_surat_masuk_fix_id':self.id },
            'view_id'   : action.id,
            'target'    : 'current'
            } 

#    Klik Tombol selsesai
    def selesai(self):
        self.state='Selesai'


    #    Notifikasi Jumlah Pesan / SELECT DATA UTK Menampilkan jumlah data pada notif
    @api.model
    def _needaction_domain_get(self):
        count = 0
        ids = list()
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        user_id = employee.id
        print  user_id
# #         query select stage jika depart user terdaftar
        record_login = self.env['surat.masuk.disposisi'].search([('tujuan_id', '=', user_id)])
#         print  daftar_stage
#          
        for data in record_login :
            ids.append(data.surat_masuk_fix_id.id)
        print " ========================== OKKEEEE ===========================", ids
     
         
        return ['&',('disposisi_ids.state', '=', 'Belum Dibaca'),('disposisi_ids.surat_masuk_fix_id','in',ids),('disposisi_ids.tujuan_id','=',user_id)]
        # return ['&',('disposisi_ids.state', '=', 'Belum Dibaca'),('disposisi_ids.id','in',ids)]
        # return [('disposisi_ids.state', '=', 'Belum Dibaca')]

    @api.one
    def _get_template_lembar_disposisi_blank(self):
        kosong     = ' '
        ditujukan     	= 'Sespus, Kabid  Opsnal, Kabid Gasbin, Kabid Rikwastu, Kabag Labtekpol, Analis, Kasubbag Sumda, Kasubbag Kerma, Kasubbag Ren,  Kasubbag Dokinfo, Kataud, Kaurkeu / Spri'
        surat_ld        = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat','=','LD')])
        str_surat_ld    = surat_ld.template 
        str_surat_ld    = str_surat_ld.replace("{tgl_action}",str(datetime.now().strftime("%d"))+'-'+str(datetime.now().strftime("%m"))+'-'+str(datetime.now().strftime("%Y")))
        str_surat_ld    = str_surat_ld.replace("{asal_surat}",str(self.asal_surat.name))
        str_surat_ld    = str_surat_ld.replace("{no_surat}",str(self.name))
        str_surat_ld    = str_surat_ld.replace("{tgl_surat}",str(self.tgl_surat))
        str_surat_ld    = str_surat_ld.replace("{perihal}",str(self.perihal))
        str_surat_ld    = str_surat_ld.replace("{ditujukan_ke}",str(ditujukan))
        str_surat_ld    = str_surat_ld.replace("{catatan_disposisi}",str(kosong))
        str_surat_ld    = str_surat_ld.replace("{sifat_surat}",str(self.sifat_surat).upper())
        str_surat_ld    = str_surat_ld.replace("{no_agenda}",str(self.no_agenda))
        str_surat_ld    = str_surat_ld.replace("{tgl_terima}",str(self.tgl_diterima))
        str_surat_ld    = str_surat_ld.replace("{jam_action}",str(datetime.now().strftime("%H:%M:%S")))
        self.prev_lembar_disposisi_blank = str_surat_ld

    prev_lembar_disposisi_blank = fields.Html(string='Lembar Disposisi Blank', 
                                        store=False,
#                                         translate=True,
                                        sanitize=True,
                                        strip_style=False, 
                                        compute = "_get_template_lembar_disposisi_blank") # option: translate=True

class PopupDisposisi_SM(models.Model):
    _name           = 'surat.masuk.disposisi'
    _description    = 'Disposisi Surat Masuk'
    
    surat_masuk_fix_id       = fields.Many2one(comodel_name='surat_masuk_fix',  string="Parent Id", ondelete='set null', index=True)
    #---ambil data user employee login
    @api.model
    def _get_log_employee_id(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        return int(employee.id)
    
    def _compute_log_employee_id(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        
        self.employee_id    = employee.id
        
    employee_id         = fields.Integer(string="Yang Login", store=False, default=_get_log_employee_id, compute="_compute_log_employee_id")
    #--- end
    
    surat_masuk_fix_id  = fields.Many2one(comodel_name='surat_masuk_fix', string='ID Surat')
    tujuan_id           = fields.Many2one(comodel_name='hr.employee', string='Tujuan Disposisi')
    disposisi           = fields.Many2one(comodel_name='pengaturan_disposisi', string='Disposisi')
    catatan_disposisi   = fields.Text("Catatan Disposisi")
    state               = fields.Selection([('Baca', 'Baca'),('Belum Dibaca', 'Belum Dibaca')], string='State', default='Belum Dibaca')               
    
    
    
    @api.one
    def _get_template_lembar_disposisi(self):
        surat_ld        = self.env['tnde.m_pengaturan_master_surat'].search([('kode_surat','=','LD')]) 
       	tujukan_ke = 'Yth, '+ str(self.disposisi.name)
        str_surat_ld    = surat_ld.template 
        str_surat_ld    = str_surat_ld.replace("{ditujukan_ke}",str(self.tujuan_id.name))
        str_surat_ld    = str_surat_ld.replace("{tgl_action}",str(datetime.now().strftime("%d"))+'-'+str(datetime.now().strftime("%m"))+'-'+str(datetime.now().strftime("%Y")))
        str_surat_ld    = str_surat_ld.replace("{asal_surat}",str(self.surat_masuk_fix_id.asal_surat.name))
        str_surat_ld    = str_surat_ld.replace("{catatan_disposisi}",str(self.catatan_disposisi))
        str_surat_ld    = str_surat_ld.replace("{no_surat}",str(self.surat_masuk_fix_id.name))
        str_surat_ld    = str_surat_ld.replace("{ditujukan_ke}",str(tujukan_ke))
        str_surat_ld    = str_surat_ld.replace("{tgl_surat}",str(self.surat_masuk_fix_id.tgl_surat))
        str_surat_ld    = str_surat_ld.replace("{perihal}",str(self.surat_masuk_fix_id.perihal))
        str_surat_ld    = str_surat_ld.replace("{sifat_surat}",str(self.surat_masuk_fix_id.sifat_surat).upper())
        str_surat_ld    = str_surat_ld.replace("{no_agenda}",str(self.surat_masuk_fix_id.no_agenda))
        str_surat_ld    = str_surat_ld.replace("{tgl_terima}",str(self.surat_masuk_fix_id.tgl_diterima))
#         str_surat_ld    = str_surat_ld.replace("{jam_action}",str(time.asctime(time.localtime(time.tm_hour()))))
        str_surat_ld    = str_surat_ld.replace("{jam_action}",str(datetime.now().strftime("%H:%M:%S")))
#         str_surat_pi = str_surat_pi.replace("{anggota_tim}",temp_tim)
        self.prev_lembar_disposisi = str_surat_ld

    prev_lembar_disposisi = fields.Html(string='Lembar Disposisi', 
                                        store=False,
#                                         translate=True,
                                        sanitize=True,
                                        strip_style=False, 
                                        compute = "_get_template_lembar_disposisi") # option: translate=True
    
    @api.multi
    def kirim_surat_disposisi(self):
        print 'ID Surat', self.surat_masuk_fix_id.id
        print 'ID Tujuan', self.tujuan_id.id
        print 'CATATAN', self.catatan_disposisi
#         lhp = self.env['surat.masuk.disposisi'].create({
#                 'surat_masuk_fix_id'    : self.surat_masuk_fix_id.id,
#                 'tujuan_id'         : self.tujuan_id.id,
#                 'disposisi'         : self.disposisi.id,
#                 'catatan_disposisi' : self.catatan_disposisi,
#             })
        self.env.cr.commit()
        get_partner_tujuan = self.env['surat_masuk_fix'].search([('id', '=', self.surat_masuk_fix_id.id)])
        print "ID Tujuan Disposisi", self.tujuan_id.work_email   
        print "saveeeeeee"

        template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'template_mail_disposisi')
        body = template_obj.body_html
        body=body.replace('<---aa--->',str(self.id))
        if template_obj:
            mail_values = {
                'subject': template_obj.subject,
                'body_html': body,
                'email_to':''.join(map(lambda x: x, self.tujuan_id.work_email)),
                # 'email_cc':';'.join(map(lambda x: x, email_cc)),
                'email_from': template_obj.email_from,
            }
        create_and_send_email = self.env['mail.mail'].create(mail_values).send()
        
        self.env.cr.execute(""" INSERT INTO hr_employee_surat_masuk_fix_rel (surat_masuk_fix_id,hr_employee_id) VALUES ('%s','%s')""", (self.surat_masuk_fix_id.id, self.tujuan_id.id))    
        self.env.cr.commit()
        
        

        raise exceptions.ValidationError('Surat Berhasil Terkirim')




class surat_keluar(models.Model):
    _name           = 'surat_keluar'
    _inherit        = ['mail.thread', 'ir.needaction_mixin'] #untuk Notif Jumlah Surat Yang belum Dibaca
    _description    = 'Model TNDE Surat Keluar'
    _order          = 'id desc'
    
    jenis_surat     = fields.Many2one(comodel_name='tnde.m_pengaturan_master_surat', string="Jenis Surat", required=True)
    name            = fields.Char(string="Perihal", required=True)
    kd_klasifikasi  = fields.Many2one(comodel_name='kode_tersier', string="Pilih Kode", required=False)
    tgl_surat       = fields.Date(string="Tgl Surat", required=True)  
    no_surat        = fields.Char(string="Nomor Surat" )
    no_urut         = fields.Char(string="Nomor Urut Surat" )
    kepada          = fields.Char(string="Kepada" )
    konseptor       = fields.Many2many('hr.employee', string="Konseptor / Pemeriksa", required=True)
    penandatangan   = fields.Many2one('hr.employee', string="Penandatangan" )
    keterangan      = fields.Text("Lembar Surat", default="")
    lampiran_srt_msk= fields.Many2many(comodel_name='surat_masuk_fix', string="Lampiran Surat Masuk")
    scan_surat      = fields.Binary(string="Upload Surat")
    lampiran        = fields.Char("lampiran")
    keterangan      = fields.Text("Keterangan")
    tindakan        = fields.Selection([('Biasa', 'Biasa'),('Cepat', 'Cepat')], string='Tindakan /Respon', default='Biasa')
    history_surat_keluar_ids   = fields.One2many(comodel_name='history_surat_keluar', string="Disposisi", inverse_name='id_surat_keluar', ondelete='cascade')
    state           = fields.Selection([('Buat Surat', 'Buat Surat'),('Draft', 'Draft'),('ACC Konseptor', 'ACC Konseptor'),('ACC TAUD', 'ACC TAUD'),('ACC Sespus', 'ACC Sespus'),('ACC KAPUSLITBANG', 'ACC KAPUSLITBANG'),('Selesai', 'Selesai')], string='State', default='Buat Surat')
    baca_ids        = fields.One2many(comodel_name='baca_surat_keluar', string="Baca", inverse_name='surat_keluar_id', ondelete='cascade')
    
    def confirm(self):
        for row in self:
            mail = row.konseptor
            for role in mail:
                template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'email_approve_konseptor')
                body = template_obj.body_html
                body=body.replace('<---aa--->',str(row.id))
                if template_obj:
                    mail_values = {
                        'subject': template_obj.subject,
                        'body_html': body,
                        'email_to':''.join(map(lambda x: x, role.work_email)),
                        # 'email_cc':';'.join(map(lambda x: x, email_cc)),
                        'email_from': template_obj.email_from,
                    }
                create_and_send_email = self.env['mail.mail'].create(mail_values).send() 
                row.state='Draft'
            
                self.env.cr.execute(""" INSERT INTO baca_surat_keluar (surat_keluar_id,id_user,status_baca) VALUES ('%s','%s','N')""", (self.id, self.konseptor.id))    
                self.env.cr.commit()

    @api.one
    def acc_konseptor(self):
        self.env.cr.execute("""
                            SELECT
                                * 
                            FROM
                                surat_keluar s 
                            WHERE
                                id = %s
                            """,(self.id,))

        namee = self.env.cr.dictfetchone()

        file = namee['scan_surat']

        self.state='ACC Konseptor'

        date_now = datetime.now() + timedelta()
        print '======================================================================', date_now

        self.env.cr.execute(""" INSERT INTO history_surat_keluar (name,lampiran,scan_surat,id_surat_keluar,create_date) VALUES ('ACC Konseptor',%s,%s,'%s',%s)""", (self.lampiran,file, self.id, date_now))    
        # self.env.cr.commit()

        taud = self.env['hr.employee'].search([('job_id.name', '=', 'KATAUD')],limit = 1)
        
       

        for send in taud:
            template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'email_approve_acc_taud')
            body = template_obj.body_html
            body=body.replace('<---aa--->',str(self.id))
            if template_obj:
                mail_values = {
                    'subject': template_obj.subject,
                    'body_html': body,
                    'email_to':''.join(map(lambda x: x, send.work_email)),
                    # 'email_cc':';'.join(map(lambda x: x, email_cc)),
                    'email_from': template_obj.email_from,
                }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send() 
            self.env.cr.execute(""" UPDATE baca_surat_keluar SET status_baca = 'Y' WHERE surat_keluar_id = %s""", (self.id,))
            self.env.cr.execute(""" INSERT INTO baca_surat_keluar (surat_keluar_id,id_user,status_baca) VALUES ('%s','%s','N')""", (self.id, send.id))    
            self.env.cr.commit()



    @api.one
    def acc_taud(self):
        self.state='ACC TAUD'
        
        self.env.cr.execute("""
                            SELECT
                                * 
                            FROM
                                surat_keluar s 
                            WHERE
                                id = %s
                            """,(self.id,))

        namee = self.env.cr.dictfetchone()

        file = namee['scan_surat']

        date_now = datetime.now() + timedelta()

        self.env.cr.execute(""" INSERT INTO history_surat_keluar (name,lampiran,scan_surat,id_surat_keluar,create_date) VALUES ('ACC TAUD',%s,%s,'%s',%s)""", (self.lampiran,file, self.id, date_now))    

        taud = self.env['hr.employee'].search([('job_id.name', '=', 'SES')],limit = 1)
       
        for send in taud:
            template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'email_approve_acc_sespus')
            body = template_obj.body_html
            body=body.replace('<---aa--->',str(self.id))
            if template_obj:
                mail_values = {
                    'subject': template_obj.subject,
                    'body_html': body,
                    'email_to':''.join(map(lambda x: x, send.work_email)),
                    # 'email_cc':';'.join(map(lambda x: x, email_cc)),
                    'email_from': template_obj.email_from,
                }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send()
            self.env.cr.execute(""" UPDATE baca_surat_keluar SET status_baca = 'Y' WHERE surat_keluar_id = %s""", (self.id,))
            self.env.cr.execute(""" INSERT INTO baca_surat_keluar (surat_keluar_id,id_user,status_baca) VALUES ('%s','%s','N')""", (self.id, send.id))    
            self.env.cr.commit()

    @api.one
    def acc_sespus(self):
        self.env.cr.execute("""
                            SELECT
                                * 
                            FROM
                                surat_keluar s 
                            WHERE
                                id = %s
                            """,(self.id,))

        namee = self.env.cr.dictfetchone()

        file = namee['scan_surat']

        date_now = datetime.now() + timedelta()

        print '======================================================================', date_now
        self.env.cr.execute(""" INSERT INTO history_surat_keluar (name,lampiran,scan_surat,id_surat_keluar,create_date) VALUES ('ACC Sespus',%s,%s,'%s',%s)""", (self.lampiran,file, self.id, date_now))    
        # self.env.cr.commit()

        self.state='ACC Sespus'
        
        taud = self.env['hr.employee'].search([('job_id.name', '=', 'KAPUS LITBANG POLRI')],limit = 1)
       
        for send in taud:
            template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'email_approve_acc_kapus')
            body = template_obj.body_html
            body=body.replace('<---aa--->',str(self.id))
            if template_obj:
                mail_values = {
                    'subject': template_obj.subject,
                    'body_html': body,
                    'email_to':''.join(map(lambda x: x, send.work_email)),
                    # 'email_cc':';'.join(map(lambda x: x, email_cc)),
                    'email_from': template_obj.email_from,
                }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send() 
            self.env.cr.execute(""" UPDATE baca_surat_keluar SET status_baca = 'Y' WHERE surat_keluar_id = %s""", (self.id,))
            self.env.cr.execute(""" INSERT INTO baca_surat_keluar (surat_keluar_id,id_user,status_baca) VALUES ('%s','%s','N')""", (self.id, taud.id))    
            self.env.cr.commit()

    @api.one
    def acc_kapuslitbang(self):
        
        self.state='ACC KAPUSLITBANG'
        self.env.cr.execute("""
                            SELECT
                                * 
                            FROM
                                surat_keluar s 
                            WHERE
                                id = %s
                            """,(self.id,))

        namee = self.env.cr.dictfetchone()

        file = namee['scan_surat']

        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        
        self.employee_id    = employee.id

        date_now = datetime.now() + timedelta()
        print '======================================================================', date_now
        self.env.cr.execute(""" UPDATE baca_surat_keluar SET status_baca = 'Y' WHERE surat_keluar_id = %s""", (self.id,))
        self.env.cr.execute(""" INSERT INTO history_surat_keluar (name,lampiran,scan_surat,id_surat_keluar,create_date) VALUES ('ACC KAPUSLITBANG',%s,%s,'%s',%s)""", (self.lampiran,file, self.id, date_now))    
        self.env.cr.commit()
        

    @api.multi
    def write(self, values):


        if self.state == 'Selesai':
            raise exceptions.ValidationError('Surat Tidak dapat Diubah, Karena Status Surat sudah selesai') 
        else :
            data_sk = self.env['surat_keluar'].search([('id', '=', self.id)])
            status_old = data_sk.state

            status_baru =  values.get("state")
            print '====================== Status Baru ===========', values.get("state")
            print '====================== Status Baru ===========', status_baru
            print '====================== Status Lama ================', status_old


            if not status_baru :
                print 'Tidak perlu insert History'
                self.env.cr.execute("""
                                SELECT
                                    * 
                                FROM
                                    surat_keluar s 
                                WHERE
                                    id = %s
                                """,(self.id,))

                namee = self.env.cr.dictfetchone()

                file = namee['scan_surat']

                employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
                
                self.employee_id    = employee.id

                date_now = datetime.now() + timedelta()

                self.env.cr.execute(""" INSERT INTO history_surat_keluar (name,lampiran,scan_surat,id_surat_keluar,create_date) VALUES ('Revisi Surat',%s,%s,'%s',%s)""", (self.lampiran,file, self.id, date_now))    
       
                
        return models.Model.write(self, values)
    
    
    # @api.onchange('jenis_surat')
    # def _onchange_keterangan(self):
    #     # Contoh set auto-changing field
    #     surat_template = self.env['tnde.m_pengaturan_master_surat'].search([('id','=',self.jenis_surat.id)])
    #     print "onnnnchangeeee"
    #     str_surat_template = surat_template.template
    #     self.keterangan = str_surat_template
    
   
    @api.one
    def get_number(self):
        self.prev_suratkeluar =""
        
    #buat report
    prev_suratkeluar = fields.Html(string='Surat Keluar', 
                                        store=False,
#                                         translate=True,
                                        sanitize=True,
                                        strip_style=False, 
                                        compute = "get_number") # option: translate=True  
        
        
    @api.multi
    def create_number(self):
        bln_romawi  = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
        get_thn_now = str(datetime.now().strftime("%Y"))
        get_bln_now = int(datetime.now().strftime("%m"))
        
        print self.jenis_surat.id
        surat_id        = self.env['tnde.m_pengaturan_master_surat'].search([('id','=',self.jenis_surat.id)])
        
        print surat_id.format_nomor
        str_no_suratkeluar = surat_id.format_nomor
        str_suratkeluar    = self.keterangan 
#         print str_suratkeluar
        
        self.env.cr.execute("""
                            SELECT
                                MAX(s.no_urut) AS no_max 
                            FROM
                                surat_keluar s 
                            WHERE
                                date_part ( 'year', s.create_date ) = date_part ( 'year', CURRENT_DATE )
                            AND jenis_surat = %s
                            """,(self.jenis_surat.id,))

        get_no_max  = self.env.cr.dictfetchall()
        print get_no_max
        next_no_max = 1
        for data in get_no_max :
            if data['no_max'] :
                next_no_max = int(data['no_max']) + 1
                print 'Uda Ada'
            else :
                print 'Belum Ada'

    # ---- end
        kode_tersier          = self.kd_klasifikasi.name
        print '+++++++++++++++++++++++++++++++', kode_tersier


        str_no_suratkeluar    = str_no_suratkeluar.replace("{no_urut_surat}", str(next_no_max))
        str_no_suratkeluar    = str_no_suratkeluar.replace("{kd_klasifikasi}",kode_tersier)
        str_no_suratkeluar    = str_no_suratkeluar.replace("{thn}", str(datetime.now().strftime("%Y")))
        str_no_suratkeluar    = str_no_suratkeluar.replace("{bln}", bln_romawi[get_bln_now - 1])
        print '+++++++++++++++++++++++++++++++', str_no_suratkeluar
        str_suratkeluar = str_suratkeluar.replace("{nomor_surat}", str(str_no_suratkeluar))
        # str_suratkeluar = str_suratkeluar.replace("{tgl_today}", str(datetime.now().strftime("%d %B %Y")))
       
        self.env.cr.execute(""" UPDATE surat_keluar SET no_urut = %s, keterangan = %s, state = 'Selesai', no_surat = %s  WHERE id = %s""", (str(next_no_max), str_suratkeluar, str(str_no_suratkeluar), self.id ))
        self.env.cr.commit()
       
#         raise exceptions.ValidationError('Nomor Surat Berhasil Digenerate / Buat')   
        
        return{
            'type'      : 'ir.actions.act_window',
            'name'      : 'Surat Keluar',
            'view_type' : 'form',
            'view_mode' : 'tree,kanban,form,graph',
            'domain'    : [],
            'res_model' : 'surat_keluar',
#             'context'   : {'default_surat_masuk_fix_id':self.id },
#             'view_id'   : action.id,
            'target'    : 'current'
            } 
        
        
        
    @api.one
    def _get_template_surat_keluar(self):
        str_surat_ld            = self.keterangan 
        # str_surat_ld            = str_surat_ld.replace("{tgl_today}", str(datetime.now().strftime("%d %B %Y")))
        self.prev_surat_keluar  = str_surat_ld

    prev_surat_keluar = fields.Html(string='Surat Keluar', 
                                        store=False,
#                                         translate=True,
                                        sanitize=True,
                                        strip_style=False, 
                                        compute = "_get_template_surat_keluar")


    # Notifikasi Jumlah Pesan / SELECT DATA UTK Menampilkan jumlah data pada notif
#     @api.model
#     def _needaction_domain_get(self):
#         count = 0
#         ids = list()
#         employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
#         user_id = employee.id
#         print  '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ DI USER : ',user_id
# # #         query select stage jika depart user terdaftar
#         record_login = self.env['baca_surat_keluar'].search([('id_user', '=', user_id)])
# #         print  daftar_stage
# #          
#         for data in record_login :
#             ids.append(data.surat_keluar_id.id)
#         print " ========================== OKKEEEE ===========================", ids
     
         
#         return ['&',('baca_ids.status_baca', '=', 'N'),('baca_ids.surat_keluar_id','in',ids),('baca_ids.id_user','=',user_id)]
#         # return ['&',('disposisi_ids.state', '=', 'Belum Dibaca'),('disposisi_ids.id','in',ids)]
#         # return [('disposisi_ids.state', '=', 'Belum Dibaca')]
       
   
class pengaturan_disposisi(models.Model):
    _name = 'pengaturan_disposisi'  # nama model  
    _description = 'Model pengaturan_disposisi'
    name = fields.Char(string="Nama Disposisi", required=True)  
    ket = fields.Text("Keterangan")   
    
    
class asal_surat(models.Model):
    _name = 'asal_surat'  # nama model  
    _description = 'Model asal_surat'
    name = fields.Char(string="Nama Lembaga/Kantor", required=True)  
    singkatan = fields.Text("Singkatan") 
    
   
class kode_klasifikasi(models.Model):
    _name               = 'kode_klasifikasi'  # nama model  
    _description        = 'Model Kode Klasifikasi Arsip'

    name                = fields.Char(string="Kode", required=True)  
    nm_klasifikasi      = fields.Char(string="Nama Klasifikasi", required=False)  


class kode_primer(models.Model):
    _name               = 'kode_primer'  # nama model  
    _description        = 'Model Kode Primer'

    name                = fields.Char(string="Nama Kode Primer", required=True)  
    kode_klasifikasi    = fields.Many2one('kode_klasifikasi', string="Kode Klasifikasi", required=True)


class kode_sekunder(models.Model):
    _name               = 'kode_sekunder'  # nama model  
    _description        = 'Model Kode Sekunder'

    name                = fields.Char(string="Nama Kode Sekunder", required=True)  
    kode_klasifikasi    = fields.Many2one('kode_klasifikasi', string="Kode Klasifikasi", required=True)
    kode_primer         = fields.Many2one('kode_primer', string="Kode Primer", required=True)


class kode_tersier(models.Model):
    _name               = 'kode_tersier'  # nama model  
    _description        = 'Model Kode Tersier'

    name                = fields.Char(string="Kode ", required=True)  
    nm_kode                = fields.Char(string="Nama Kode Tersier", required=False)  
    kode_klasifikasi    = fields.Many2one('kode_klasifikasi', string="Kode Klasifikasi", required=True)
    kode_primer         = fields.Many2one('kode_primer', string="Kode Primer", required=True)
    kode_sekunder       = fields.Many2one('kode_sekunder', string="Kode Sekunder", required=True)


class arsip_surat_masuk_fix(models.Model):
    _name               = 'arsip_surat_masuk_fix'  # nama model  
    _description        = 'Model Arsip Surat Masuk'

    name                = fields.Char(string="Nama Arsip Surat", required=True)  
    no_arsip            = fields.Char(string="No. Arsip", required=False)  
    no_urut             = fields.Char(string="No. Urut", required=False)  
    kode_klasifikasi    = fields.Many2one('kode_klasifikasi', string="Kode Klasifikasi", required=True)
    kode_primer         = fields.Many2one('kode_primer', string="Kode Primer", required=True)
    kode_sekunder       = fields.Many2one('kode_sekunder', string="Kode Sekunder", required=True)
    id_surat_masuk_fix      = fields.Many2one('surat_masuk_fix', string="Pilih Surat Masuk", required=True)


class bidbag(models.Model):
    _name               = 'bidbag'  # nama model  
    _description        = 'Model Bidang / Bagian'

    name                = fields.Char(string="Nama Bid/Bag", required=True)  

class history_surat_keluar(models.Model):
    _name                   = 'history_surat_keluar'  # nama model  
    _description            = 'Model History Surat Keluar'

    name                    = fields.Char(string="Aktifitas", required=True) 

    id_surat_keluar         = fields.Many2one(comodel_name='surat_keluar', string='ID Surat')
    scan_surat              = fields.Binary(string="Lampiran Surat")
    lampiran                = fields.Char("lampiran")

class baca_surat_keluar(models.Model):
    _name               = 'baca_surat_keluar'  # nama model  
    _description        = 'Model Baca Surat Keluar'

    name                = fields.Char(comodel_name='kode', string='kode')
    surat_keluar_id     = fields.Many2one(comodel_name='surat_keluar', string='ID Surat')
    id_user             = fields.Many2one(comodel_name='hr.employee', string='Tujuan Disposisi')
    status_baca         = fields.Char(string='Status Baca')
    state               = fields.Selection([('Baca', 'Baca'),('Belum Dibaca', 'Belum Dibaca')], string='State', default='Belum Dibaca')               

class baca_surat_internal(models.Model):
    _name               = 'baca_surat_internal'  # nama model  
    _description        = 'Model Baca Surat Internal'

    name                = fields.Char(comodel_name='kode', string='kode')
    surat_keluar_id     = fields.Many2one(comodel_name='surat_keluar', string='ID Surat')
    id_user             = fields.Many2one(comodel_name='hr.employee', string='Tujuan Disposisi')
    status_baca         = fields.Char(string='Status Baca')
    state               = fields.Selection([('Baca', 'Baca'),('Belum Dibaca', 'Belum Dibaca')], string='State', default='Belum Dibaca')               
