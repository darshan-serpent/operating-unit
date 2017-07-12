# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tools.translate import _
from odoo import api, models
from odoo.exceptions import UserError


class HrPayslip(models.Model):

    _inherit = 'hr.payslip'

    @api.multi
    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if 'move_id' in vals and vals.get('move_id', False):
            for slip in self:
                if slip.contract_id and slip.contract_id.operating_unit_id:
                    slip.move_id.write({'operating_unit_id':
                                        slip.contract_id.operating_unit_id.id})
                    if slip.move_id.line_ids:
                        slip.move_id.line_ids.\
                            write({'operating_unit_id':
                                   slip.contract_id.operating_unit_id.id})
        return res

    @api.multi
    def action_payslip_done(self):
        OU = None
        for slip in self:
            # Check that all slips are related to contracts
            # that belong to the same OU.
            if OU:
                if slip.contract_id.operating_unit_id.id != OU:
                    raise UserError(_('Configuration error! '
                                      'The Contracts must refer the same '
                                      'Operating Unit.'))
            OU = slip.contract_id.operating_unit_id.id
        return super(HrPayslip, self).action_payslip_done()
