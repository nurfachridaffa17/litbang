from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import time
from Tkconstants import LEFT
from datetime import date
from time import gmtime, strftime

class surat_internal(models.Model):
    _name           = 'surat_internal'
    _description    = 'Model TNDE Surat Internal'
    _inherit        = ['mail.thread', 'ir.needaction_mixin'] #
    _order          = 'id desc'
    
    @api.model
    def _get_log_employee_id(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        return int(employee.id)
    
    def _compute_log_employee_id(self):
        employee = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        
        self.employee_id = employee.id
       
    employee_id     = fields.Many2one('hr.employee',string="Yang Login", store=True, default=_get_log_employee_id, compute="_compute_log_employee_id")
    name            = fields.Char(string="Perihal", required=True)
    jenis_surat     = fields.Many2one(comodel_name='tnde.m_pengaturan_master_surat', string="Jenis Surat", required=True)
    kode_sekunder   = fields.Many2one(comodel_name='kode_sekunder', string="Kode Klasifikasi", required=False)
    tgl_surat       = fields.Date(string="Tgl Surat", required=True)  
    no_surat        = fields.Char(string="Nomor Surat" )
    bidbag          = fields.Many2one(comodel_name='bidbag', string="Bidang /Bagian", required=True)
    no_urut         = fields.Integer(string="Nomor Urut Surat" )
    penandatangan   = fields.Many2one('hr.employee', string="Penandatangan" )
    konseptor       = fields.Many2one('hr.employee', string="Konseptor", required=True)
    tujuan_surat    = fields.Many2many('hr.employee', string="Tujuan Surat", required=True)
    keterangan      = fields.Text("Lembar Surat", default="")
    scan_surat      = fields.Binary(string="Upload Surat")
    lampiran        = fields.Char("lampiran")
    keterangan      = fields.Text("Keterangan")
    history_surat_internal_ids      = fields.One2many(comodel_name='history_surat_internal', string="Versioning", inverse_name='id_surat_internal', ondelete='cascade')
    baca_surat_internal_ids         = fields.One2many(comodel_name='baca_surat_internal', string="ID", inverse_name='surat_internal_id', ondelete='cascade')
    tindakan        = fields.Selection([('Biasa', 'Biasa'),('Cepat', 'Cepat')], string='Respon', default='Biasa')
    date_due        = fields.Datetime(string="Limit Respon", required=False)  
    state           = fields.Selection([('Buat Surat', 'Buat Surat'),('Draft', 'Draft'),('ACC Konseptor', 'ACC Konseptor'),('Selesai', 'Selesai')], string='State', default='Buat Surat')
    
    @api.one
    def confirm(self, vals):
        self.env.cr.execute("""
                            SELECT
                                * 
                            FROM
                                surat_internal s 
                            WHERE
                                id = %s
                            """,(self.id,))

        namee = self.env.cr.dictfetchone()

        file = namee['scan_surat']

        self.state='ACC Konseptor'

        date_now = datetime.now() + timedelta()

        self.env.cr.execute(""" INSERT INTO history_surat_internal (name,lampiran,scan_surat,id_surat_internal,create_date) VALUES ('Confirm',%s,%s,'%s',%s)""", (self.lampiran,file, self.id,date_now))    
        # self.env.cr.commit()

        for row in self:
            mail = row.konseptor
            for role in mail:
                template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'template_mail_internal')
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
                self.state = 'Draft'

                self.env.cr.execute(""" UPDATE baca_surat_internal SET status_baca = 'Y' WHERE surat_internal_id = %s""", (self.id,))
                self.env.cr.execute(""" INSERT INTO baca_surat_internal (surat_internal_id,id_user,status_baca) VALUES ('%s','%s','N')""", (self.id, role.id))    
                self.env.cr.commit()



    @api.one
    def acc_konseptor(self):
        self.state='ACC Konseptor'

        self.env.cr.execute("""
                            SELECT
                                * 
                            FROM
                                surat_internal s 
                            WHERE
                                id = %s
                            """,(self.id,))

        namee = self.env.cr.dictfetchone()

        file = namee['scan_surat']

        self.state='ACC Konseptor'

        date_now = datetime.now() + timedelta()

        self.env.cr.execute(""" INSERT INTO history_surat_internal (name,lampiran,scan_surat,id_surat_internal,create_date) VALUES ('ACC Konseptor',%s,%s,'%s',%s)""", (self.lampiran,file, self.id,date_now))    
        # self.env.cr.commit()
        # self.env.cr.commit()

        for row in self:
            mail = row.tujuan_surat
            for role in mail:
                template_obj = self.env['ir.model.data'].sudo().get_object('tnde', 'template_mail_tujuan_internal')
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

                self.env.cr.execute(""" UPDATE baca_surat_internal SET status_baca = 'Y' WHERE surat_internal_id = %s""", (self.id,))
                self.env.cr.execute(""" INSERT INTO baca_surat_internal (surat_internal_id,id_user,status_baca) VALUES ('%s','%s','N')""", (self.id, role.id))    
                self.env.cr.commit()
     
    @api.multi
    def write(self, vals):
         
        if self.state == 'Selesai':
            raise exceptions.ValidationError('Surat Tidak dapat Diubah, Karena Status Surat sudah selesai') 
         
        return models.Model.write(self, vals)
     
     
#    @api.onchange('jenis_surat')
 #   def _onchange_keterangan(self):
  #      # Contoh set auto-changing field
   #     surat_template = self.env['tnde.m_pengaturan_master_surat'].search([('id','=',self.jenis_surat.id)])
    #    print "onnnnchangeeee"
     #   str_surat_template = surat_template.template
#         str_surat_pi = str_surat_pi.replace("{nip_dalnis}",str(self.dalnis_id.nip))
#         str_surat_pi = str_surat_pi.replace("{anggota_tim}",temp_tim)
      #  self.keterangan = str_surat_template
     
    
    @api.one
    def get_number(self):
        self.prev_suratinternal =""
         
    #buat report
    prev_suratinternal = fields.Html(string='Surat Internal', 
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

        str_no_suratinternal= surat_id.format_nomor
        str_suratinternal    = self.keterangan 
        bidbag               = self.bidbag.id
        nm_bidbag               = self.bidbag.name
#         print str_suratkeluar
        # print 'Bidang ++++++++++++++++++++++++++++++++++++++ :',bidbag
        # print 'Nama Bidang +++++++++++++++++++++++++++++++++ :',nm_bidbag
         
        self.env.cr.execute("""
                            SELECT
                                MAX(si.no_urut) AS no_max 
                            FROM
                                surat_internal si 
                            WHERE
                                date_part ( 'year', si.create_date ) = date_part ( 'year', CURRENT_DATE )
                            AND si.jenis_surat = %s
                            AND si.bidbag = %s
                            """,(self.jenis_surat.id, self.bidbag.id,))
 
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
        satker                  = self.employee_id.department_id.name
        kode_sekunder           = self.kode_sekunder.name
        print "==================  Employee : ",self.employee_id.id   
        print "==================  Sekunder : ",kode_sekunder   
        print "==================  ID Satker: ",bidbag   
        # print "==================  Satker   : ",nm_bidbag   
        print "==================  No. URUT Surat   : ",next_no_max   
        str_no_suratinternal    = str_no_suratinternal.replace("{no_urut_surat}", str(next_no_max))
        str_no_suratinternal    = str_no_suratinternal.replace("{kd_klasifikasi}",str(kode_sekunder))
        str_no_suratinternal    = str_no_suratinternal.replace("{thn}", str(datetime.now().strftime("%Y")))
        str_no_suratinternal    = str_no_suratinternal.replace("{bln}", bln_romawi[get_bln_now - 1])
        str_no_suratinternal    = str_no_suratinternal.replace("{satker}",nm_bidbag)
        print str_no_suratinternal
        str_suratinternal = str_suratinternal.replace("{nomor_surat}", str(str_no_suratinternal))
        str_suratinternal = str_suratinternal.replace("{tgl_today}", str(datetime.now().strftime("%d %B %Y")))


                
        self.env.cr.execute(""" UPDATE surat_internal SET no_urut = %s, keterangan = %s, state = 'Selesai', no_surat = %s  WHERE id = %s""", (str(next_no_max), str_suratinternal, str(str_no_suratinternal), self.id ))
        self.env.cr.commit()
        
          
#         raise exceptions.ValidationError('Nomor Surat Berhasil Digenerate / Buat')   
         
        return{
            'type'      : 'ir.actions.act_window',
            'name'      : 'Surat Internal',
            'view_type' : 'form',
            'view_mode' : 'tree,kanban,form,graph',
            'domain'    : [],
            'res_model' : 'surat_internal',
#             'context'   : {'default_surat_masuk_id':self.id },
#             'view_id'   : action.id,
            'target'    : 'current'
            } 
         
         
         
    @api.one
    def _get_template_surat_internal(self):
        str_surat_ld            = self.keterangan 
        # str_surat_ld            = str_surat_ld.replace("{tgl_today}", str(datetime.now().strftime("%d %B %Y")))
        self.prev_surat_internal  = str_surat_ld
 
    prev_surat_internal = fields.Html(string='Surat Internal', 
                                        store=False,
#                                         translate=True,
                                        sanitize=True,
                                        strip_style=False, 
                                        compute = "_get_template_surat_internal")
        


class history_surat_internal(models.Model):
    _name                   = 'history_surat_internal'  # nama model  
    _description            = 'Model History Surat internal'

    name                    = fields.Char(string="Aktifitas", required=True) 

    id_surat_internal       = fields.Many2one(comodel_name='surat_internal', string='ID Surat')
    scan_surat              = fields.Binary(string="Lampiran Surat")
    lampiran                = fields.Char("lampiran")


class baca_surat_internal(models.Model):
    _name               = 'baca_surat_internal'  # nama model  
    _description        = 'Model Baca Surat Internal'

    name                = fields.Char(comodel_name='kode', string='kode')
    surat_internal_id   = fields.Many2one(comodel_name='surat_internal', string='ID Surat')
    id_user             = fields.Many2one(comodel_name='hr.employee', string='Tujuan Disposisi')
    status_baca         = fields.Char(string='Status Baca')
    state               = fields.Selection([('Baca', 'Baca'),('Belum Dibaca', 'Belum Dibaca')], string='State', default='Belum Dibaca')  

class Followers(models.Model):
    _inherit = 'mail.followers'

    @api.model
    def create(self, vals):
        if 'res_model' in vals and 'res_id' in vals and 'partner_id' in vals:
            dups = self.env['mail.followers'].search([('res_model', '=',vals.get('res_model')),
                                           ('res_id', '=', vals.get('res_id')),
                                           ('partner_id', '=', vals.get('partner_id'))])
            if len(dups):
                for p in dups:
                    p.unlink()
        res = super(Followers, self).create(vals)
        return res