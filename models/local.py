#Kelurahan > Kecamatan > Sektor
# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Localization(models.Model):
    _name = "local.localization"
    _description = "Data lokasi"

    kelurahan = fields.Char(string="Kelurahan")
    kecamatan = fields.Char(string="Kecamatan")
    sektor = fields.Char(string="Sektor")

