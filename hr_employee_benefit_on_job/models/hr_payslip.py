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

from openerp import api, models
from itertools import chain


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def _search_benefits(self, payslip):

        benefits = super(HrPayslip, self)._search_benefits(payslip)

        return benefits + list(chain(*[
            job.benefit_line_ids for job in [
                contract_job.job_id for contract_job in
                payslip.contract_id.contract_job_ids
            ]
        ]))
