# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Beansbooks Integration',
    'description': """
        Integrates beansbooks into Odoo offering a bi-directional mysql connection.
    """,

    'category': 'Others',
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'base_external_dbsource_mysql',
        'queue_job',
    ],
    'data': [
        'security/mantis_bug_security.xml',
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/mantis_bug_views.xml',
        'views/mantis_issue_views.xml',
        'views/mantis_bug_menuitem.xml',
    ],
    'author': 'Adria Gil Sorribes, Eficent SL,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA',
}
