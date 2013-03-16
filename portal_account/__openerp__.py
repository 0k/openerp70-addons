# -*- coding: utf-8 -*-
{
    'name': "Portal Account",
    'version': "0.1",
    'category': 'Tools',
    'complexity': 'easy',
    'author': "EL2DE SARL <david.drapeau@el2de.com>",
    'website': "http://www.el2de.com",
    'description': """
    
    """,
    
    'depends': ['account','portal'],
    'data': [
        'security/portal_account_security.xml',
        'security/ir.model.access.csv',
        'view/portal_account_view.xml',
    ],
    
    'installable': True,
    'auto_install': False,
    'web': True,
}