# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([
        ('lakilaki', 'L'),
        ('perempuan', 'P')
        ])
    date_of_birth = fields.Date(string="Masukan Tanggal Lahir")
    baptis = fields.Date(string="Masukan Tanggal Baptis")
    sidi = fields.Date(string="Masukan Tanggal Sidi")
    married = fields.Date(string="Masukan Tanggal Menikah")    
    pasangan = fields.Many2one('res.partner', string="Nama Pasangan")
    sektor = fields.Many2one('local.sektor', string="Sektor")
    ke = fields.Integer(string="Ke")
    status_menikah = fields.Selection([
            ('menikah', 'Menikah'),
            ('belum_menikah', 'Belum Menikah')
        ], string="Status Menikah")

    

    