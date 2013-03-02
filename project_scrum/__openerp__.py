# -*- coding: utf-8 -*-
{
    'name': "Project Scrum Management",
    'version': "1.3",
    'author': "David DRAPEAU",
    'category': "Project Scrum Management",
    'summary': 'Projects, Scrum',
    'description': """
Scrum Module for OpenERP 7.0 (developped by David DRAPEAU <david.drapeau@el2de.com.com>)

This application respects the scrum.org protocol and has been developed and is maintened by ITIL Certified Member (in course of certification).
    * Linked to OpenERP native module 'project'

Manage
    * Project roles
        * Scrum Master
        * Product Owner
        * Development Team (inherits from project module)
    * Releases
    * Sprints
        * date_start and date_stop
        * standup meetings for each user of team (TODO)
        * sprint review
        * sprint retrospective
        * planned velocity (you write velocity desired and displayed on Sprint Velocity Chart)
        * effective velocity (it is computed by all users stories affected to the sprint)
        * effective velocity done (it is computed by all users stories done and displayed on Sprint Velocity Chart)
    * Product Backlog (users stories)
        * new kanban view
        * date_open and date_done
        * story complexity points
        * text area for describe tests acceptance
    * Display charts
        * Burdown Chart (based on story points)
        * Sprints Velocity (for each Scrum project)
    * Sandbox
        * a developer of development team can add a user story to sandbox 
        * the product owner can valid it (transfer into product backlog) or delete it


Thanks to report questions to david.drapeau@el2de.com
    """,
    
    'website': 'https://github.com/ddrapeau/openerp70-addons',
    'images': [],
    'depends': [
        'base',
        'mail',
        'project',
    ],
    'data': [
        "project_scrum_report.xml",
        "view/project_view.xml",
        
        "security/project_scrum_security.xml",
        "security/ir.model.access.csv",
        
        
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
        'static/src/css/project_scrum.css',
    ],
    'demo': [],
    'test': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'web': True,
    #'certificate': '',
}
