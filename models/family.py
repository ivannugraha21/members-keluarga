# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FamilyL(models.Model):
    _name = "family.family"
    _description = "Family List"
    #
    name = fields.Many2one('res.partner', string="Kepala Keluarga", required=True)
    list_keluarga_ids = fields.One2many('family.list.line', 'list_keluarga_id', string="List Keluarga")
    alamat = fields.Char(string="Alamat")
    kecamatan = fields.Many2one('local.kecamatan', string="Kecamatan")
    kelurahan = fields.Many2one('local.kelurahan', string="Kelurahan")
    nohp = fields.Char(string="Nomor HP")
    sektor = fields.Many2one('local.sektor', string="Sektor")
    status_rumah = fields.Selection([
        ("milik_sendiri", "Milik Sendiri"),
        ("sewa_kontrak", "Sewa / Kontrak")
        ], default="milik_sendiri")
    count = fields.Char(string="Jumlah Anggota Keluarga", compute='_count_family')
    #
    @api.onchange('kecamatan')
    def filter_kelurahan(self):
        self.kelurahan = False
        for rec in self:
            return {'domain': {'kelurahan': [('kecamatan', '=', rec.kecamatan.name)]}}

    #
    def _count_family(self):
        bundle = self.list_keluarga_ids
        vsum = 0
        for each in bundle:
            vsum += 1
        self.count = vsum

    #
    @api.onchange('name')
    def update_line(self):
        if (self.name):
            #
            self.nohp = self.name.phone
            self.list_keluarga_ids = [(5, 0, 0)]
            vals = {
                'member_id': self.name,
                'gender': self.name.gender,
                'relation': 'suami',
                'date_of_birth': self.name.date_of_birth,
                'baptis': self.name.baptis,
                'sidi': self.name.sidi,
                'married': self.name.married,
                'job': self.name.function
            }
            self.list_keluarga_ids = [(0, 0, vals)]
        else:
            self.list_keluarga_ids = [(5, 0, 0)]

    #
    @api.model
    def create(self, vals):
        # Create data baru berdasarkan input
        rec = super(FamilyL, self).create(vals)
        # Update data Alamat dan Sektor di res.partner
        for reclist in rec.list_keluarga_ids:
            print(reclist.member_id)
            # Ambil id res.partner
            id_res = reclist.member_id.id
            # Update data res.partner
            id_data = rec.env['res.partner'].search([('id', '=', id_res)], limit=1)
            id_data.write({
                'street': rec.alamat,
                'sektor': rec.sektor
                })   
        return rec

    #
    def write(self, vals):
        res = super(FamilyL, self).write(vals)
        id_val = self.id
        id_update = self.env['family.family'].search([('id', '=', id_val)], limit=1)

        for rec in id_update.list_keluarga_ids:
            id_partner = rec.member_id.id
            partner_update = self.env['res.partner'].search([('id', '=', id_partner)], limit=1)
            partner_update.write({
                'street': self.alamat,
                'sektor': self.sektor
                })
        return res


class ListFamily(models.Model):
    _name = 'family.list.line'
    _description = "List member dari satu keluarga"
    #
    member_id = fields.Many2one("res.partner", string="Nama", required=True)
    gender = fields.Selection(related="member_id.gender", string="L/P", readonly=False)
    relation = fields.Selection([
        ('suami', 'Suami'),
        ('istri', 'Istri'),
        ('anak', 'Anak'),
        ('tanggungan', 'Tanggungan')
        ])
    date_of_birth = fields.Date(related="member_id.date_of_birth", string="Lahir", readonly=False)
    baptis = fields.Date(related="member_id.baptis", string="Baptis", readonly=False)
    sidi = fields.Date(related="member_id.sidi", string="Sidi", readonly=False)
    married = fields.Date(related="member_id.married", string="Menikah", readonly=False)
    job = fields.Char(related="member_id.function", string="Pekerjaan", readonly=True)
    list_keluarga_id = fields.Many2one('family.family', 'List Keluarga')
    #
    @api.onchange('relation')
    def filter_kelurahan(self):
        if (self.relation == 'suami'):
            self.gender = 'lakilaki'
        
        if (self.relation == 'istri'):
            self.gender = 'perempuan'
            
