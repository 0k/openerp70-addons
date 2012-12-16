# -*- coding: utf-8 -*-
{
    'name' : "Project Scrum Management",
    'version' : "0.6",
    'author' : "Cogitae",
    'category' : "Cogitae Project Scrum",
    'summary': 'Projects, Scrum',
    'description' : """
Scrum Module for OpenERP 7.0 (developped by Cogitae)

This application respects the scrum org protocol (scrum.org) and has been developed and is maintened by ITIL Certified Members.

    * Linked to project native module

Manage
    * Releases
    * Sprints
        * date_start and date_stop
        * standup meetings for each user of team (TODO)
        * sprint review
        * sprint retrospective
    * Product Backlog
    * Product Owner and Scrum Master on each sprint
    * display Burndown Chart

TODO
    * Dev Team management
    * Others artefacts
    * Rights "Cogitae Scrum / Product Owner", "Cogitae Scrum / Scrum Master" and "Cogitae Scrum / Developer"
    * Complexity points

Thanks to report questions to david.drapeau@cogitae.net
    """,
    
    'website': 'http://www.cogitae.net/openerp/cogitae-addons/ddrapeau_project_scrum/',
    'images' : [],
    'depends' : ["base", "project"],
    'data': [
        "security/ddrapeau_project_scrum_security.xml",
        "security/ir.model.access.csv",
        "project_scrum_report.xml",
        "wizard/project_scrum_backlog_create_task_view.xml",
        "wizard/project_scrum_email_view.xml",
        "view/project_scrum_menu.xml",
        "view/project_scrum_role_view.xml",
        "view/project_scrum_view.xml",
    ],
    'css': [
        'static/src/css/ddrapeau_project_scrum.css',
    ],
    'demo': [],
    'test': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    #'certificate': '',
}
