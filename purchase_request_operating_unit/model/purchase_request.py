# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models, api, _


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=lambda self:
        self.env['res.users'].
        operating_unit_default_get(self._uid),
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and \
                    rec.company_id != rec.operating_unit_id.company_id:
                raise Warning(_('The Company in the Purchase Request and in '
                                'the Operating Unit must be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_warehouse_operating_unit(self):
        for rec in self:
            picking_type = rec.picking_type_id
            if picking_type:
                if picking_type.warehouse_id and\
                        picking_type.warehouse_id.operating_unit_id\
                        and rec.operating_unit_id and\
                        picking_type.warehouse_id.operating_unit_id !=\
                        rec.operating_unit_id:
                    raise Warning(_('Configuration error!\nThe\
                    Purchase Request and the Warehouse of picking type\
                    must belong to the same Operating Unit.'))


class PurchaseRequestLine(models.Model):
    _inherit = 'purchase.request.line'

    operating_unit_id = fields.Many2one(
        'operating.unit',
        related='request_id.operating_unit_id',
        string='Operating Unit', readonly=True,
        store=True,
    )
