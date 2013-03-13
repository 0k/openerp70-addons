# -*- coding: utf-8 -*-
{
    'name': "Account Accountant Outsourcing",
    'version': "0.1",
    'author': "David DRAPEAU",
    'category': "Accountant Outsourcing",
    'summary': 'Account, Accountant Outsourcing',
    'description': """
This module defines rights for external accountant (enterprise outsourcing).
    """,
    
    'website': 'https://github.com/ddrapeau/openerp70-addons',
    'images': [],
    'depends': [
        'account',
        'account_accountant',
    ],
    'data': [
        "security/account_accountant_outsourcing_security.xml",
        "security/ir.model.access.csv",
    ],
    'css': [],
    'demo': [],
    'test': [],
    'application': False,
    'installable': True,
    'auto_install': False,
    'web': True,
    #'certificate': '',
}
