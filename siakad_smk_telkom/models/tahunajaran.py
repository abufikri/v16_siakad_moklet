from odoo import models, fields, api

class MokletTahunAjaran(models.Model):
    _name           = 'moklet.tahun.ajaran'
    _description    = 'Tabel Tahun Ajaran'

    name    = fields.Char(string='Tahun Ajaran', required=True)
    deskripsi = fields.Text(string='Keterangan')
    
    

