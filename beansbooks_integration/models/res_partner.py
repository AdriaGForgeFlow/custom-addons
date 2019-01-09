# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.addons.queue_job.job import job
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

WHAT = """
        id,
        default_shipping_address_id
        default_billing_address_id
        default_remit_address_id
        default_account_id
        type
        first_name
        last_name
        company_name
        email
        phone_number
        fax_number
        """


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @job
    def execute_query(self, sql_query, sql_params=None, metadata=False):
        if not self.dbsource_id.conn_string:
            raise ValidationError('Missing fields on the database source specified')
        res = self.dbsource_id.execute(sql_query, sql_params, metadata)
        return res

    def get_parameter(self, what, where, condition):
        """Gets an parameter from other table"""
        query = "SELECT %s FROM %s WHERE %s" % (what, where, condition)
        res = self.execute_query(query)
        if res:
            return res[0]
        return

    @job
    def retrieve_entities(self):
        """Retrieve all the issues from the Mantis database"""
        # Database query
        query = "SELECT %s FROM entities;" % WHAT
        res = self.execute_query(query, None, True)

        # Create Partner from the result of the query
        for partner_obj in res['rows']:
            partner = {}
            name = "%s %s " % \
                   (partner_obj['first_name'], partner_obj['last_name'])
            company = partner_obj['company_name']
            if company:
                display_name = "%s, %s" % (company, name)
            else:
                display_name = name
            partner.update({
                'name': name,
                'display_name': display_name,
                'commercial_partner_id': partner_obj['company_name'],
                'email': partner_obj['email'],
                'phone': partner_obj['phone_number'],
            })

            # Check if the issue that has been retrieved already exists or not
            existing_issue = self.mantis_issues_id.search([
                ('name', '=', name),
            ])
            if not existing_issue:
                self.mantis_issues_id.create(partner)
            else:
                existing_issue.write(partner)

        return True

    # Method called by the scheduler
    @api.model
    def retrieve_beansbooks_entities(self):
        try:
            for obj in self:
                description = "Attempt to retrieve entities from beansbooks " \
                              "database"
                obj.with_delay(
                    description=description).retrieve_entities()
        except Exception:
            _logger.exception("Failed updating BeansBooks entities")

        return None
