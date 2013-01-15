# -*- coding: utf-8 -*-
{
    'name': "Project Scrum Management",
    'version': "1.1",
    'author': "David DRAPEAU",
    'category': "Project Scrum Management",
    'summary': 'Projects, Scrum',
    'description': """
Scrum Module for OpenERP 7.0 (developped by David DRAPEAU)

This application respects the scrum.org protocol and has been developed and is maintened by ITIL Certified Member (in course of certification).
    * Linked to OpenERP native module 'project'

Manage
    * Releases
    * Sprints
        * date_start and date_stop
        * standup meetings for each user of team (TODO)
        * sprint review
        * sprint retrospective
    * Product Backlog
        * new kanban view
        * date_open and date_done
        * story complexity points
    * display Burndown Chart
        * based on story points (complexity)
    * Sandbox
        * a developer of development team can add a user story to sandbox 
        * the product owner can valid it (transfer into product backlog) or delete it


Thanks to report questions to david.drapeau@gmail.com
    """,
    
    'website': 'https://github.com/ddrapeau/openerp70-addons',
    'images': [],
    'depends': ["base", "project"],
    'data': [
        "view/project_view.xml",
        
        "security/ddrapeau_project_scrum_security.xml",
        "security/ir.model.access.csv",
        
        "project_scrum_report.xml",
        
        "wizard/project_scrum_backlog_create_task_view.xml",
        "wizard/project_scrum_email_view.xml",
        "wizard/user_story_sandbox_to_backlog_view.xml",
        
        "view/project_scrum_menu.xml",
        "view/project_scrum_release_view.xml",
        "view/project_scrum_role_view.xml",
        "view/project_scrum_sandbox_view.xml",
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
