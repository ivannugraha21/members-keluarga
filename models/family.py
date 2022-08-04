# -*- coding: utf-8 -*-
from odoo import api, fields, models


class FamilyL(models.Model):
    _name = "family.family"
    _description = "Family List"

    ### Declare
    name = fields.Many2one('res.partner', string="Keluarga")
    #status = fields.Char(string="Coba dulu")
    list_keluarga_ids = fields.One2many('family.list.line', 'list_keluarga_id', string="List Keluarga")
    #
    alamat = fields.Char(string="Masukan Alamat")
    kelurahan = fields.Char(string="Masukan Kelurahan")
    kecamatan = fields.Char(string="Masukan Kecamatan")
    nohp = fields.Char(string="Masukan Nomor HP")
    sektor = fields.Char(string="Masukan Sektor")
    status_rumah = fields.Selection([
        ("milik_sendiri", "Milik Sendiri"),
        ("sewa_kontrak", "Sewa / Kontrak")
        ], default="milik_sendiri")
    
    count = fields.Char(string="Jumlah Keluarga", compute='_count_family')

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


class ListFamily(models.Model):
    _name = 'family.list.line'
    _description = "List member dari satu keluarga"

    member_id = fields.Many2one("res.partner", string="Nama")
    gender = fields.Selection(related="member_id.gender", string="L/P", readonly=False)
    relation = fields.Selection([
        ('suami', 'Suami'),
        ('isteri', 'Isteri'),
        ('anak', 'Anak'),
        ('tanggungan', 'Tanggungan')
        ])
    date_of_birth = fields.Date(related="member_id.date_of_birth", string="Lahir", readonly=False)
    baptis = fields.Date(related="member_id.baptis", string="Baptis", readonly=False)
    sidi = fields.Date(related="member_id.sidi", string="Sidi", readonly=False)
    married = fields.Date(related="member_id.married", string="Menikah", readonly=False)
    job = fields.Char(related="member_id.function", string="Pekerjaan", readonly=True)

    list_keluarga_id = fields.Many2one('family.family', 'List Keluarga')