# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResPasangan(models.Model):
    _name = "res.pasangan"
    _description = "Data pasangan yang sudah menikah"

    name  = fields.Char()
    nama_suami = fields.Many2one('res.partner', string="Suami", required=True)
    nama_istri = fields.Many2one('res.partner', string="Istri", required=True)
    # Make double filed, one field hidden
    married = fields.Date(related='nama_suami.married', string="Menikah", readonly=False)
    married_con = fields.Date(related='nama_istri.married', string="Menikah", readonly=False)

    alamat = fields.Char(string="Alamat")
    sektor = fields.Many2one('local.sektor', string="Sektor")

    # Buat hidden field untuk update data status_menikah di contact
    status_menikah1 = fields.Selection(related='nama_suami.status_menikah', readonly=False)
    status_menikah2 = fields.Selection(related='nama_istri.status_menikah', readonly=False)
    #
    pasangan1 = fields.Many2one(related='nama_suami.pasangan', readonly=False)
    pasangan2 = fields.Many2one(related='nama_istri.pasangan', readonly=False)
    #pasangan1 = fields.Char(related='nama_suami.pasangan', readonly=False)
    # Set related field gender 
    gender_suami = fields.Selection(related='nama_suami.gender', readonly=False)
    gender_istri = fields.Selection(related='nama_istri.gender', readonly=False)

    @api.onchange('nama_suami', 'nama_istri')
    def update_name(self):
        NS = ' '
        NI = ' '

        # if (self.nama_suami.name != False):
            

        # if (self.nama_istri != False):

        
        # varObj = self.env['res.pasangan']
        # varObj.write({
        #     'status_menikah1': 'menikah',
        #     'status_menikah2': 'menikah',
        #     })

        # # Reset Data
        # self.status_menikah1 = False
        # self.status_menikah2 = False
        # self.pasangan1 = False
        # self.pasangan2 = False
        # self.gender_suami = False
        # self.gender_istri = False
        # # Update Data
        # for rec in self:
        #     rec.status_menikah1 = 'menikah'
        #     rec.status_menikah2 = 'menikah'

        #     rec.name = str(NS) + ' & ' + str(NI)

        #     rec.pasangan1 = rec.nama_istri
        #     rec.pasangan2 = rec.nama_suami

        #     rec.gender_suami = 'lakilaki'
        #     rec.gender_istri = 'perempuan'



        self.status_menikah1 = False
        self.status_menikah2 = False
        self.pasangan1 = False
        self.pasangan2 = False
        self.gender_suami = False
        self.gender_istri = False



        if self.nama_suami and self.nama_istri:
            NI = self.nama_istri.name
            NS = self.nama_suami.name

            self.name = str(NS) + ' & ' + str(NI)

            self.status_menikah1 = 'menikah'

            self.status_menikah2 = 'menikah'

            #
            self.pasangan1 = self.nama_istri
            self.pasangan2 = self.nama_suami
            #
            self.gender_suami = 'lakilaki'
            self.gender_istri = 'perempuan'
            #
            self.married_con = self.married





    @api.onchange('married')
    def update_married_i(self):
        self.married_con = self.married
