from odoo import models, fields, api

class MokletKelas(models.Model):
    _name = 'moklet.kelas'
    _description = 'Moklet Kelas'

    name = fields.Char(string='Nama Kelas', required=True)
    deskripsi = fields.Text(string='Keterangan')
    jenjang = fields.Selection(string='Jenjang', selection=[('x', 'X'), ('xi', 'XI'),('xii', 'XII')], required=True)
    jurusan_id = fields.Many2one(comodel_name='moklet.jurusan', string='Jurusan')
    
    
    
    
