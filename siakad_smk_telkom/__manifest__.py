# -*- coding: utf-8 -*-
{
    'name': "SIAKAD SMK TELKOM MALANG",

    'summary': """
        Aplikasi Sistem Informasi Akademik SMK Telkom Malang berbasis Odoo16""",

    'description': """
        Aplikasi Sistem Informasi Akademik SMK Telkom Malang berbasis Odoo16
    """,

    'author': "SMK Telkom Malang",
    'website': "https://www.smktelkom-mlg.sch.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [

        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu_siakad.xml',
        'views/tahunajaran.xml',
        'views/jurusan.xml',
        'views/kelas.xml',
        'views/kelas_tahunajaran.xml',
        'views/siswa.xml',
        'views/ekstrakurikuler.xml',
        'views/organisasi.xml',
        'views/mapel.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
