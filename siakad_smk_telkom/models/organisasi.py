from odoo import models, fields, api

class MokletOrganisasi(models.Model):
    _name = 'moklet.organisasi'
    _description = 'Moklet Organisasi'

    name = fields.Char(string='Organisasi', required=True)
    pembina_id = fields.Many2one(comodel_name='hr.employee', string='Pembina')
    keterangan = fields.Text(string='Keterangan')
    siswa_ids = fields.Many2many(comodel_name='moklet.siswa', string='Siswa')
    

    
