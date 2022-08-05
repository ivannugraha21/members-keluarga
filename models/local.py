#Kelurahan > Kecamatan > Sektor
# -*- coding: utf-8 -*-
from odoo import api, fields, models

class LocalizationKecamatan(models.Model):
	_name = "local.kecamatan"
	_description = "Data Kecamatan"

	name = fields.Char(string="Kecamatan", required=True)

class LocalizationKelurahan(models.Model):
	_name = "local.kelurahan"
	_description = "Data Kelurahan"

	name = fields.Char(string="Kelurahan", required=True)
	kecamatan = fields.Many2one('local.kecamatan', string="Kecamatan", required=True)


class LocalizationSektor(models.Model):
	_name = "local.sektor"
	_description = "Data Sektor"

	name = fields.Char(string="Sektor", required=True)
	kecamatan = fields.Many2one('local.kecamatan', string="Kecamatan", required=True)
	kelurahan = fields.Many2one('local.kelurahan', string="Kelurahan", required=True)

	@api.onchange('kecamatan')
	def filter_kelurahan(self):
		self.kelurahan = False
		for rec in self:
			return {'domain': {'kelurahan': [('kecamatan', '=', rec.kecamatan.name)]}}
