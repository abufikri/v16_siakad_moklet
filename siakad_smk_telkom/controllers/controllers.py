# -*- coding: utf-8 -*-
# from odoo import http


# class SiakadSmkTelkom(http.Controller):
#     @http.route('/siakad_smk_telkom/siakad_smk_telkom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/siakad_smk_telkom/siakad_smk_telkom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('siakad_smk_telkom.listing', {
#             'root': '/siakad_smk_telkom/siakad_smk_telkom',
#             'objects': http.request.env['siakad_smk_telkom.siakad_smk_telkom'].search([]),
#         })

#     @http.route('/siakad_smk_telkom/siakad_smk_telkom/objects/<model("siakad_smk_telkom.siakad_smk_telkom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('siakad_smk_telkom.object', {
#             'object': obj
#         })
