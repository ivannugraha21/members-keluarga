# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date

class ResPasangan(models.Model):
    _name = "res.pasangan"
    _description = "Data pasangan yang sudah menikah"
    #
    name  = fields.Char(string="Suami & Istri", compute="update_field")
    nama_suami = fields.Many2one('res.partner', string="Suami", required=True)
    nama_istri = fields.Many2one('res.partner', string="Istri", required=True)
    ke = fields.Char(string="Ke", compute="calculate_date", store=True)
    married = fields.Date(string="Menikah", required=True)
    alamat = fields.Char(string="Alamat")
    sektor = fields.Many2one('local.sektor', string="Sektor")
    #
    @api.depends('nama_suami')
    def update_field(self):
        for rec in self:
            if rec.nama_suami:
                rec.name = str(rec.nama_suami.name) + ' & ' + str(rec.nama_istri.name)
                rec.alamat = rec.nama_suami.street
                rec.sektor = rec.nama_suami.sektor
            else:
                rec.name = "Null"

    @api.depends('married')
    def calculate_date(self):
        for rec in self:
            today = date.today()
            if rec.married:
                # Check Ke
                rec.ke = today.year - rec.married.year - ((today.month, today.day) < (rec.married.month, rec.married.day))
                if int(rec.ke) < 1:
                    rec.ke = False
            else:
                rec.ke = False

    #    
    @api.model
    def create(self, vals):
        # Create data baru berdasarkan input
        rec = super(ResPasangan, self).create(vals)
        # Cek jika data suami dan istri tidak kosong
        if rec.nama_suami and rec.nama_istri:
            # Update Name 
            rec.name = str(rec.nama_suami.name) + ' & ' + str(rec.nama_istri.name)
            # Ambil id suami dan istri
            id_suami = rec.nama_suami.id
            id_istri = rec.nama_istri.id
            # Update Data Suami
            partner_istri = self.env['res.partner'].search([('id', '=', id_suami)], limit=1)
            partner_istri.write({
                'status_menikah': 'menikah',
                'gender': 'lakilaki',
                'married': rec.married,
                'pasangan': rec.nama_istri,
                'ke': rec.ke
                })
            # Update Data Istri
            partner_istri = self.env['res.partner'].search([('id', '=', id_istri)], limit=1)
            partner_istri.write({
                'status_menikah': 'menikah',
                'gender': 'perempuan',
                'married': rec.married,
                'pasangan': rec.nama_suami,
                'ke': rec.ke
                })           
        return rec

    #
    def write(self, vals):
        # Update Sesuai data yang diubah, eg: Cuma ubah nama istri maka values hanya ada data istri saja
        res = super(ResPasangan, self).write(vals)
        # Update Manual Name
        update = {'name': str(self.nama_suami.name) + ' & ' + str(self.nama_istri.name)}
        res = super(ResPasangan, self).write(update)
        # Ambil id dari suami dan istri
        id_suami = self.nama_suami.id
        id_istri = self.nama_istri.id
        # Update Data Suami
        partner_istri = self.env['res.partner'].search([('id', '=', id_suami)], limit=1)
        partner_istri.write({
            'status_menikah': 'menikah',
            'gender': 'lakilaki',
            'married': self.married,
            'pasangan': self.nama_istri,
            #'ke': self.ke          <<< Data Ke disini berebda denga di member
            })
        # Update Data Istri
        partner_istri = self.env['res.partner'].search([('id', '=', id_istri)], limit=1)
        partner_istri.write({
            'status_menikah': 'menikah',    
            'gender': 'perempuan',
            'married': self.married,
            'pasangan': self.nama_suami,
            #'ke': self.ke          <<< Data Ke disini berebda denga di member
            })
        return res
        




