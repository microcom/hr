# -*- coding:utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Savoir-faire Linux. All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import api, fields, models


class HrEmployeeBenefit(models.Model):
    _inherit = 'hr.employee.benefit'

    @api.multi
    def compute_amounts(self, payslip, context=None):
        benefits = self.browse(context=context)

        other_benefit_ids = [
            b.id for b in benefits if b.amount_type != 'per_hour'
        ]

        super(HrEmployeeBenefit, self).compute_amounts(
            other_benefit_ids, payslip)

        benefits_per_hour = [
            b for b in benefits if b.amount_type == 'per_hour'
        ]

        # Case where the benefit is per_hour
        for benefit in benefits_per_hour:

            # Case where the benefit is related to a single job
            if benefit.job_id:
                worked_days = [
                    wd for wd in payslip.worked_days_line_ids
                    if wd.activity_id.job_id == benefit.job_id
                ]

            # Case where the benefit is related to a contract
            # In that case, the benefit applies for all jobs
            elif benefit.contract_id:
                worked_days = [
                    wd for wd in payslip.worked_days_line_ids
                    if wd.activity_id.type == 'job'
                ]

            else:
                worked_days = []

            for wd in worked_days:
                benefit.rate_id.compute_amounts_per_hour(wd)

    job_id = fields.Many2one(
            'hr.job',
            'Job',
            ondelete='cascade',
            select=True
        )
