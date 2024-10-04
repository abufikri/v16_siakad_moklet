from odoo import models, fields, api


class MokletSiswa(models.Model):
    _name = 'moklet.siswa'
    _description = 'Tabel Siswa SMK Telkom'

    name = fields.Char(string='Nama Siswa', required=True)
    nis = fields.Char(string='NIS', required=True)
    tmp_lahir = fields.Char(string='Tempat Lahir')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', selection=[('l', 'Laki-laki'), ('p', 'Perempuan'),], required=True)
    alamat = fields.Text(string='Alamat Lengkap')
    no_hp = fields.Char(string='No HP')
    
    
    
    
    
    
    
