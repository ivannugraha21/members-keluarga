# -*- coding: utf-8 -*-
# from odoo import http


# class MdFamily(http.Controller):
#     @http.route('/md_family/md_family', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/md_family/md_family/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('md_family.listing', {
#             'root': '/md_family/md_family',
#             'objects': http.request.env['md_family.md_family'].search([]),
#         })

#     @http.route('/md_family/md_family/objects/<model("md_family.md_family"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('md_family.object', {
#             'object': obj
#         })
