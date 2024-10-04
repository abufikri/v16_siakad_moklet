from odoo import models, fields, api

class MokletKelasTahunajaran(models.Model):
    _name = 'moklet.kelas.tahunajaran'
    _description = 'Moklet Kelas Tahunajaran'
    _rec_name = 'kelas_id'

    kelas_id = fields.Many2one(comodel_name='moklet.kelas', string='Kelas', required=True)
    tahunajaran_id = fields.Many2one(comodel_name='moklet.tahun.ajaran', string='Tahun Ajaran')
    # Wali kelas diambil dari tabel hr.employee yang diturunkan dari modul hr
    walikelas_id = fields.Many2one(comodel_name='hr.employee', string='Wali Kelas')
    siswa_ids = fields.Many2many(comodel_name='moklet.siswa', string='Data Siswa')
    jml_siswa = fields.Integer(string='Jumlah Siswa', compute='_compute_jml_siswa')

    @api.depends('siswa_ids')
    def _compute_jml_siswa(self):
        for rec in self:
            rec.jml_siswa = len(rec.siswa_ids)
    
    
    
    
    
    
    
