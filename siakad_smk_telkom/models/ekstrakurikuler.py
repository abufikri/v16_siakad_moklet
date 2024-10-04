from odoo import models, fields, api

class MokletEkstra(models.Model):
    _name = 'moklet.ekstra'
    _description = 'Moklet Ekstra'

    name = fields.Char(string='Nama Ekstra', required=True)
    keterangan = fields.Text(string='Keterangan')
    pembina_id = fields.Many2one(comodel_name='hr.employee', string='Pembina')
    siswa_ids = fields.Many2many(comodel_name='moklet.siswa', string='Siswa')
    
    
    
    
