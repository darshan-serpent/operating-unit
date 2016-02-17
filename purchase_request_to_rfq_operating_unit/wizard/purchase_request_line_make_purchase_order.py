# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Eficent (<http://www.eficent.com/>)
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
from openerp.exceptions import except_orm


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        readonly=True,
    )

    @api.model
    def default_get(self, fields):
        res = super(PurchaseRequestLineMakePurchaseOrder, self).\
            default_get(fields)
        request_line_obj = self.env['purchase.request.line']
        request_line_ids = self._context.get('active_ids', [])
        operating_unit_id = False
        for line in request_line_obj.browse(request_line_ids):
            line_operating_unit_id = line.request_id.operating_unit_id \
                and line.request_id.operating_unit_id.id or False
            if operating_unit_id is not False \
                    and line_operating_unit_id != operating_unit_id:
                raise except_orm(
                    _('Could not process !'),
                    _('You have to select lines '
                      'from the same operating unit.'))
            else:
                operating_unit_id = line_operating_unit_id
        res['operating_unit_id'] = operating_unit_id

        return res

    @api.model
    def _prepare_purchase_order(self, warehouse_id, company_id):
        data = super(PurchaseRequestLineMakePurchaseOrder, self).\
            _prepare_purchase_order(warehouse_id, company_id)
        data['requesting_operating_unit_id'] = \
            self.operating_unit_id.id
        data['operating_unit_id'] = \
            self.operating_unit_id.id
        return data
