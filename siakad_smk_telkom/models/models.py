# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class siakad_smk_telkom(models.Model):
#     _name = 'siakad_smk_telkom.siakad_smk_telkom'
#     _description = 'siakad_smk_telkom.siakad_smk_telkom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
