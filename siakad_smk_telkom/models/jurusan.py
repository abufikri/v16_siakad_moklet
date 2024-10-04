from odoo import models, fields, api

class MokletJurusan(models.Model):
    _name = 'moklet.jurusan'
    _description = 'Moklet Jurusan'

    name = fields.Char(string='Nama Jurusan', required=True)
    deskripsi = fields.Text(string='Keterangan')
    
    
