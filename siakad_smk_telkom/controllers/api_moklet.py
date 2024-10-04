from odoo import http
from odoo.http import request
from odoo.http import Response
import json
import requests

class ApiMoklet(http.Controller):
    # Get Siswa
    @http.route('/get_siswa', auth='user', type='json', methods=['GET'])
    def get_siswa(self, **rec):
        pos_siswa = rec.get('pos_siswa', False)
        pos_limit = rec.get('pos_limit', False)
        pos_offset = rec.get('pos_offset', False)

        #pasar_rec = request.env['simpasar.pasar'].search([('id', 'in', pos_pasar)], limit=None if not pos_limit else pos_limit, offset=0 if not pos_offset else pos_offset, order='id asc')
        if pos_siswa:
            siswa = request.env['moklet.siswa'].search([('id', 'in', pos_siswa)], limit=None if not pos_limit else pos_limit, offset=0 if not pos_offset else pos_offset, order='id asc')
        else:
            siswa = request.env['moklet.siswa'].search([], limit=None if not pos_limit else pos_limit, offset=0 if not pos_offset else pos_offset, order='id asc')
        list_siswa = []
        for data in siswa:
            list_siswa.append({
                'id': data['id'],
                'name': data['name'],
                'nis': data['nis'],
                'tmp_lahir': data['tmp_lahir'],
                'tgl_lahir': data['tgl_lahir'],
                'alamat': data['alamat'],
                'no_hp': data['no_hp'],
            })
            data = {
                'status': 200,
                'message': 'Success',
                'data': list_siswa
            }
        return data
    
    # Create Siswa
    @http.route('/create_siswa', auth='user', type='json', methods=['POST'])
    def create_siswa(self, **rec):
        name = rec.get('name', False)
        nis = rec.get('nis', False)
        tmp_lahir = rec.get('tmp_lahir', False)
        tgl_lahir = rec.get('tgl_lahir', False)
        jenis_kelamin = rec.get('jenis_kelamin', False)
        alamat = rec.get('alamat', False)
        no_hp = rec.get('no_hp', False)

        siswa = request.env['moklet.siswa'].create({
            'name': name,
            'nis': nis,
            'tmp_lahir': tmp_lahir,
            'tgl_lahir': tgl_lahir,
            'jenis_kelamin': jenis_kelamin,
            'alamat': alamat,
            'no_hp': no_hp,
        })
        data = {
            'status': 200,
            'message': 'Success',
            'data': {
                'id': siswa.id,
                'name': siswa.name,
                'nis': siswa.nis,
                'tmp_lahir': siswa.tmp_lahir,
                'tgl_lahir': siswa.tgl_lahir,
                'alamat': siswa.alamat,
                'no_hp': siswa.no_hp,
            }
        }
        return data