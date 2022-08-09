# -*- coding: utf-8 -*-
from odoo import api, fields, models

# =========================================================================================
# Ini menggunakan fungsi Related
# =========================================================================================
# class ResPasangan(models.Model):
#     _name = "res.pasangan"
#     _description = "Data pasangan yang sudah menikah"

#     name  = fields.Char(string="Nama", compute="get_status_menikah")

#     # Data Field Suami
#     nama_suami = fields.Many2one('res.partner', string="Suami", required=True)
#     nama_istri = fields.Many2one('res.partner', string="Istri", required=True)
#     #
#     status_suami = fields.Selection(related='nama_suami.status_menikah', readonly=False)
#     status_istri = fields.Selection(related='nama_istri.status_menikah', readonly=False)
#     #
#     gender_suami = fields.Selection(related='nama_suami.gender', readonly=False)
#     gender_istri = fields.Selection(related='nama_istri.gender', readonly=False)
#     #
#     pasangan1 = fields.Many2one(related='nama_suami.pasangan', readonly=False)
#     pasangan2 = fields.Many2one(related='nama_istri.pasangan', readonly=False)
#     #
#     married = fields.Date(related='nama_suami.married', string="Menikah", readonly=False)
#     married_con = fields.Date(related='nama_istri.married', string="Menikah", readonly=False)
#     #
#     alamat = fields.Char(string="Alamat")
#     sektor = fields.Many2one('local.sektor', string="Sektor")

#     @api.depends('nama_suami', 'nama_istri')
#     def get_status_menikah(self):
#         for rec in self:
#             if rec.nama_suami and rec.nama_istri:
#                 rec.name = str(rec.nama_suami.name) + ' & ' + str(rec.nama_istri.name)
#                 rec.status_suami = 'menikah'       
#                 rec.status_istri = 'menikah'
#                 #
#                 rec.gender_suami = 'lakilaki'
#                 rec.gender_istri = 'perempuan'
#                 #
#                 rec.pasangan1 = rec.nama_istri
#                 rec.pasangan2 = rec.nama_suami
#                 #
#                 rec.married_con = rec.married  
#             else:
#                 rec.name = 'Null'


#     @api.onchange('married')
#     def update_married_i(self):
#         self.married_con = self.married


# =========================================================================================
# Ini menggunakan fungsi Create dan Write
# =========================================================================================
class ResPasangan(models.Model):
    _name = "res.pasangan"
    _description = "Data pasangan yang sudah menikah"

    name  = fields.Char(string="Nama")

    # Decalre Variable/Field 
    nama_suami = fields.Many2one('res.partner', string="Suami", required=True)
    nama_istri = fields.Many2one('res.partner', string="Istri", required=True)
    married = fields.Date(string="Menikah", required=True)
    alamat = fields.Char(string="Alamat")
    sektor = fields.Many2one('local.sektor', string="Sektor")
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
                'pasangan': rec.nama_istri
                })
            # Update Data Istri
            partner_istri = self.env['res.partner'].search([('id', '=', id_istri)], limit=1)
            partner_istri.write({
                'status_menikah': 'menikah',
                'gender': 'perempuan',
                'married': rec.married,
                'pasangan': rec.nama_suami
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
            'pasangan': self.nama_istri
            })
        # Update Data Istri
        partner_istri = self.env['res.partner'].search([('id', '=', id_istri)], limit=1)
        partner_istri.write({
            'status_menikah': 'menikah',
            'gender': 'perempuan',
            'married': self.married,
            'pasangan': self.nama_suami
            })
        return res
        




