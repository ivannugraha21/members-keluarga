# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection([
        ('lakilaki', 'L'),
        ('perempuan', 'P')
        ])
    #
    date_of_birth = fields.Date(string="Masukan Tanggal Lahir")
    dob_month = fields.Char(string="Bulan Lahir", compute="_get_month", store=True)
    dob_day = fields.Char(string="Tanggal Lahir", compute="_get_month", store=True)
    #
    baptis = fields.Date(string="Masukan Tanggal Baptis")
    sidi = fields.Date(string="Masukan Tanggal Sidi")
    married = fields.Date(string="Masukan Tanggal Menikah")    
    pasangan = fields.Many2one('res.partner', string="Nama Pasangan")
    sektor = fields.Many2one('local.sektor', string="Sektor")
    ke = fields.Char(string="Ke", default=False)
    status_menikah = fields.Selection([
            ('menikah', 'Menikah'),
            ('belum_menikah', 'Belum Menikah')
        ], string="Status Menikah")

    @api.depends('date_of_birth')
    def _get_month(self):
        if self.date_of_birth:
            self.dob_month = self.date_of_birth.month
            self.dob_day = self.date_of_birth.day

    
    @api.model
    def create(self, vals):
        # Create data baru berdasarkan input
        rec = super(ResPartner, self).create(vals)
        # Update
        today = date.today()   
        id_upd = self.env['res.partner'].search([('id', '=', rec.id)], limit=1)
        if rec.date_of_birth:
            # Filter data jika ulang tahhun ke kurang dari 1 maka data ke False
            ke_val = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            
            if int(ke_val) < 1:
                ke_val = False

            id_upd.write({
                'ke': ke_val
                })
        else:
            id_upd.write({
                'ke': False
                })

        return rec

    def write(self, vals):
        #
        res = super(ResPartner, self).write(vals)
        #
        if self.date_of_birth:
            today = date.today()       
            # Filter data jika ulang tahhun ke kurang dari 1 maka data ke False
            ke_val = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            if int(ke_val) < 1:
                ke_val = False
            update = {'ke': ke_val}
        else:
            update = {'ke': False}

        res = super(ResPartner, self).write(update)

        return res

    def auto_updates_data(self):
        records = self.env['res.partner'].search([('date_of_birth', '!=', False)])
        for rec in records:
            today = date.today()  
            #
            ke_val = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
            #
            if int(ke_val) < 1:
                ke_val = False
            #
            rec.write({
                'ke': ke_val
                })





    