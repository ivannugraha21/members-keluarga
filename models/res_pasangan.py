# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPasangan(models.Model):
    _name = "res.pasangan"
    _description = "Data pasangan yang sudah menikah"

    name  = fields.Char()
    nama_suami = fields.Many2one('res.partner', string="Suami")
    nama_istri = fields.Many2one('res.partner', string="Istri")
    # Make double filed, one field hidden
    married = fields.Date(related='nama_suami.married', string="Menikah", readonly=False)
    married_con = fields.Date(related='nama_istri.married', string="Menikah", readonly=False)

    alamat = fields.Char(string="Alamat")
    sektor = fields.Char(string="Sektor")

    # Buat hidden field untuk update data status_menikah di contact
    status_menikah1 = fields.Selection(related='nama_suami.status_menikah', readonly=False)
    status_menikah2 = fields.Selection(related='nama_istri.status_menikah', readonly=False)
    #
    pasangan1 = fields.Many2one(related='nama_suami.pasangan', readonly=False)
    pasangan2 = fields.Many2one(related='nama_istri.pasangan', readonly=False)

    @api.onchange('nama_suami', 'nama_istri')
    def update_name(self):
        NS = ' '
        NI = ' '

        if (self.nama_suami.name != False):
            NS = self.nama_suami.name

        if (self.nama_istri != False):
            NI = self.nama_istri.name

        self.name = str(NS) + ' & ' + str(NI)
        self.status_menikah1 = 'menikah'
        self.status_menikah2 = 'menikah'
        #
        self.pasangan1 = self.nama_istri
        self.pasangan2 = self.nama_suami
    

    @api.onchange('married')
    def update_married_i(self):
        self.married_con = self.married
