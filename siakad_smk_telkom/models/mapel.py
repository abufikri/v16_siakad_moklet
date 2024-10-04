from odoo import models, fields, api

class MokletMapel(models.Model):
    _name = 'moklet.mapel'
    _description = 'Moklet Mapel'

    name = fields.Char(string='Nama Mata Pelajaran', required=True)
    jenis = fields.Selection(string='Jenis', selection=[('umum', 'Umum'), ('kejuruan', 'Kejuruan'),])
    guru_id = fields.Many2one(comodel_name='hr.employee', string='Guru Pengajar')
    keterangan = fields.Text(string='Keterangan')
    
    
    
    
