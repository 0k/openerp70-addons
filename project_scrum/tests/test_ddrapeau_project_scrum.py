# -*- coding: utf-8 -*-
import xmlrpclib
import csv

username = 'admin'
pwd = 'admin'
pwd_a = 'a'
dbname = 'dev70_04'

class fontColors(object):
    OKGREEN = '\033[92m' # green
    USERSTORY = '\033[94m' # blue
    WARNING = '\033[93m' # red
    FAIL = '\033[91m' # red
    ENDC = '\033[0m' # nocolor

sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/common')
uid = sock_common.login(dbname, username, pwd)
sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object', allow_none=True)

def delete_lines(model, condition):
    ids_to_delete = sock.execute(dbname, uid, pwd, model, 'search', condition)
    print "ids to delete : ", ids_to_delete
    sock.execute(dbname, uid, pwd, model, 'unlink', ids_to_delete)
    return True

def update_devteam_for_res_users():
    ids_to_update = sock.execute(dbname, uid, pwd, 'res.users', 'search', [])
    sock.execute(dbname, uid, pwd, 'res.users', 'write', ids_to_update, {'scrum_devteam_id': None})

def get_country_id(name):
    country_id = sock.execute(dbname, uid, pwd, 'res.country', 'search', [('name', '=', name)])
    if len(country_id) > 0:
        return country_id[0]
    else:
        return None

# USER
def admin_create_user(fields):
    return sock.execute(dbname, uid, pwd, 'res.users', 'create', fields)

def test_admin_create_user(vals):
    user_id = admin_create_user(vals)
    if user_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create user with fields ", vals
        return user_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create user with fields ", vals
        return False

def check_uid(user_id=None):
    password = ''
    if not user_id:
        user_id = uid
        password = pwd
    else:
        if user_id == uid:
            password = pwd
        else:
            password = pwd_a
    return {'uid': user_id, 'pwd':password}

# PARTNER
def create_partner(fields, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'res.partner', 'create', fields)

def test_create_partner(vals, user_id=None):
    if not user_id:
        user_id = uid
    partner_id = create_partner(vals, user_id)
    if partner_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create partner with fields ", vals
        return partner_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create partner with fields ", vals
        return False

# PRODUCT
def create_product_product(fields):
    return sock.execute(dbname, uid, pwd, 'product.product', 'create', fields)

def test_product(fields):
    product_id = create_product_product(fields)
    if product_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create product with fields ", fields
        return product_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create product with fields ", fields
        return False

# PROJECT
def create_project(fields, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.project', 'create', fields)

def test_create_project(vals, user_id=None):
    if not user_id:
        user_id=uid
    project_id = create_project(vals, user_id)
    if project_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create project with vals ", vals
        return project_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create project with vals ", vals
        return False

# ADD DEVELOPER TO PROJECT
def add_developer_to_project(fields, project_id, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.project', 'write', project_id, fields)

def test_add_developer_to_project(vals, project_id, user_id=None):
    if not user_id:
        user_id=uid
    return_value = add_developer_to_project(vals, project_id, user_id)
    if project_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "add developer in project with vals ", vals
        return project_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "add developer in project with vals ", vals
        return False


# RELEASE
def create_release(fields, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.scrum.release', 'create', fields)

def test_create_release(vals, user_id=None):
    if not user_id:
        user_id=uid
    release_id = create_release(vals, user_id)
    if release_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create release with vals ", vals
        return release_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create release with vals ", vals
        return False

# ROLE
def create_role(fields, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.scrum.role', 'create', fields)
    
def test_create_role(vals, user_id=None):
    if not user_id:
        user_id=uid
    role_id = create_role(vals, user_id)
    if role_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create role with vals ", vals
        return role_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create role with vals ", vals
        return False

# PERSONA ADDING TO ROLE
def test_persona_adding_to_role(role_id, vals):
    req_bool_value = sock.execute(dbname, uid, pwd, 'project.scrum.role', 'write', role_id, vals)
    if req_bool_value:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "add persona for role with vals ", vals
        return True
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "add persona for role with vals ", vals
        return False

# PRODUCT BACKLOG
def create_user_story(fields, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.scrum.product.backlog', 'create', fields)
    
def test_create_user_story(vals, user_id=None):
    if not user_id:
        user_id=uid
    user_story_id = create_user_story(vals, user_id)
    if user_story_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create user story with vals ", vals
        return user_story_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create user story with vals ", vals
        return False

# SPRINT
def create_sprint(fields, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.scrum.sprint', 'create', fields)
    
def test_create_sprint(vals, user_id=None):
    if not user_id:
        user_id=uid
    sprint_id = create_sprint(vals, user_id)
    if sprint_id:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "create sprint with vals ", vals
        return sprint_id
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "create sprint with vals ", vals
        return False


# FILL SPRINT WITH STORIES
def affect_sprint_to_user_story(vals, story_id, user_id=None):
    user = check_uid(user_id)
    return sock.execute(dbname, user['uid'], user['pwd'], 'project.scrum.product.backlog', 'write', story_id, vals)
    
def test_affect_sprint_to_user_story(vals, story_id, user_id=None):
    if not user_id:
        user_id=uid
    return_value = affect_sprint_to_user_story(vals, story_id, user_id)
    if return_value:
        print fontColors.OKGREEN + "OK "+ fontColors.ENDC + "affect sprint to user story"
        return True
    else:
        print fontColors.FAIL + "FAILED "+ fontColors.ENDC + "affect sprint to user story"
        return False


print "delete daily meetings..."
delete_lines('project.scrum.meeting', [])

print "delete tasks..."
delete_lines('project.task', [])

print "delete product backlog..."
delete_lines('project.scrum.product.backlog', [])

print "delete sandbox..."
delete_lines('project.scrum.sandbox', [])

print "delete roles..."
delete_lines('project.scrum.role', [])

print "delete sprints..."
delete_lines('project.scrum.sprint', [])

print "delete releases..."
delete_lines('project.scrum.release', [])

print "delete tasks of projects..."
delete_lines('project.task', [])

print "delete projects..."
delete_lines('project.project', [])

print "delete products..."
delete_lines('product.product', [])

#NOTE Delete mail alias before res partner
print "delete mail alias..."
delete_lines('mail.alias', [('id', '>', 2)])

#NOTE Do not delete res_users because deleted by mail.alias will DELETE ON CASCADE
#print "delete users..."
#delete_lines('res.users', [('id', '>', 2)])

print "delete partners..."
delete_lines('res.partner', [('id', '>', 3)])
#NOTE res.partner.address does not exist in OpenERP v7.0
#delete_lines('res.partner.address', [('id', '>', 2)])


#NOTE Delete note stages for users created during tests (if module notes installed)
#print "delete note stages..."
#delete_lines('note.stage', [('user_id', '>', 2)])



print "=========================="
print "===== TESTS STARTING ====="
print "=========================="

print fontColors.USERSTORY + """
[Administrator] create a Scrum Master
for permit him manage projects and SCRUM
""" + fontColors.ENDC
#Group Partner Manager
group_cc_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Contact Creation')])

#Group Scrum Master
group_sm_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Scrum Master')])

#Group Project Manager
group_category_project_id = sock.execute(dbname, uid, pwd, 'ir.module.category', 'search', [('name', '=', 'Project')])
group_pm_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Manager'), ('category_id', '=', group_category_project_id)])

#Group Employee
group_category_hr_id = sock.execute(dbname, uid, pwd, 'ir.module.category', 'search', [('name', '=', 'Human Resources')])
group_hr_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Employee'), ('category_id', '=', group_category_hr_id)])

#Group Portal
group_portal_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Portal')])
print "group_portal_id = ", group_portal_id
# create user
scrum_master_vals = {
    'name': "David SCRUMMASTERONE",
    'login': "ddrapeau",
    'password': pwd_a,
    'lang': "fr_FR",
    'tz': 'Europe/Paris',
    'phone': '+336 455 942 76',
    'groups_id': [(6, 0, [group_sm_id[0], group_pm_id[0], group_hr_id[0], group_cc_id[0], group_portal_id[0]])]
}
sm01_id = test_admin_create_user(scrum_master_vals)
sm01_uid = sock_common.login(dbname, 'sm01', pwd_a)

print fontColors.USERSTORY + """
[Administrator] create a Product Owner
for permit Scrum Master affect him to a project
""" + fontColors.ENDC
group_po_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Product Owner')])

product_owner_vals = {
    'name': "Steven OWNERONE",
    'login': "po01",
    'password': pwd_a,
    'lang': "fr_FR",
    'tz': 'Europe/Paris',
    'groups_id': [(6, 0, [group_po_id[0], group_portal_id[0]])]
}
po01_id = test_admin_create_user(product_owner_vals)
po01_uid = sock_common.login(dbname, 'po01', pwd_a)

product_owner_vals = {
    'name': "Doobie OWNERTWO",
    'login': "po02",
    'password': pwd_a,
    'lang': "fr_FR",
    'tz': 'Europe/Paris',
    'groups_id': [(6, 0, [group_po_id[0], group_portal_id[0]])]
}
po02_id = test_admin_create_user(product_owner_vals)
po02_uid = sock_common.login(dbname, 'po02', pwd_a)


print fontColors.USERSTORY + """
[Administrator] create a developer
for permit Scrum Master affect him to a development team of a project
""" + fontColors.ENDC
group_dev_id = sock.execute(dbname, uid, pwd, 'res.groups', 'search', [('name', '=', 'Developer')])
developer_vals = {
    'name': "Maurice DEVONE",
    'login': "dev01",
    'password': pwd_a,
    'lang': "fr_FR",
    'tz': 'Europe/Paris',
    'groups_id': [(6, 0, [group_dev_id[0], group_portal_id[0]])]
}
dev01_id = test_admin_create_user(developer_vals)
dev01_uid = sock_common.login(dbname, 'dev01', pwd_a)

developer_vals = {
    'name': "Michel DEVTWO",
    'login': "dev02",
    'password': pwd_a,
    'lang': "fr_FR",
    'tz': 'Europe/Paris',
    'groups_id': [(6, 0, group_dev_id)]
}
dev02_id = test_admin_create_user(developer_vals)
dev02_uid = sock_common.login(dbname, 'dev02', pwd_a)

# variables
project_date_start  = '2013-01-05'
release01_date_start = project_date_start
release01_date_stop = '2013-02-26'

print fontColors.USERSTORY + """
[Scrum Master] create a Scrum project
for affect it a Product Owner
""" + fontColors.ENDC
project_vals = {
    'name': "Scrum Module for OE7.0",
    'is_scrum': True,
    'product_owner_id': po01_id,
    'goal' : "Manage project with Scrum in OpenERP 7.0",
    'date_start': project_date_start,
}
project01_id = test_create_project(project_vals, sm01_uid)


print fontColors.USERSTORY + """
[Scrum Master] add developers to project
define a development team for Scrum Project
""" + fontColors.ENDC
vals = {
    'members': [(6, 0, [dev01_id, dev02_id])]
}
print "vals = ", vals
test_add_developer_to_project(vals, project01_id, sm01_uid)


print fontColors.USERSTORY + """
[Scrum Master] create a release
for planification of sprints and delivery date of new version
""" + fontColors.ENDC
release_vals = {
    'name':"Release 001",
    'project_id':project01_id,
    'date_start': release01_date_start,
    'date_stop': release01_date_stop,
}
release01_id = test_create_release(release_vals, sm01_uid)

print fontColors.USERSTORY + """
[Scrum Master] create a Sprint
permit to development team to fill it with user stories
""" + fontColors.ENDC
vals = {
    'name': "required features",
    'date_start': '2012-12-24',
    'date_stop': '2012-12-31',
    'release_id': release01_id,
    'product_owner_id': po01_id,
    'scrum_master_id': sm01_id,
    'goal':"Required features to manage projects with Scrum"
}
sprint01_id = test_create_sprint(vals)

print fontColors.USERSTORY + """
[Product Owner]	create a role
use it in user stories writing
""" + fontColors.ENDC
role01_id = test_create_role({'name':"Scrum Master", 'code': "SM", 'project_id': project01_id}, po01_uid)
role02_id = test_create_role({'name':"Product Owner", 'code': "PO", 'project_id': project01_id}, po01_uid)
role03_id = test_create_role({'name':"Developer", 'code': "DEV", 'project_id': project01_id}, po01_uid)

print "add persona name and description to roles..."
persona_vals = {
    'persona_name': "David",
    'persona_description': """
Manage Scrum.
    """,
}
test_persona_adding_to_role(role01_id, persona_vals)

print fontColors.USERSTORY + """
[Product Owner]	add a user story in product backlog
permit to development team to realize it
""" + fontColors.ENDC
user_story_vals = {
    'role_id': role01_id,
    'name': "create a new sale order",
    'for_then': "mailing to customer",
    'project_id': project01_id,
    'release_id': release01_id,
    'acceptance_testing': """Go to sales menu and clic on button 'Create'"""
}
story01_id = test_create_user_story(user_story_vals, po01_uid)

print fontColors.USERSTORY + """
[Scrum Master] fill sprint with user stories
planificate the sprint
""" + fontColors.ENDC
test_affect_sprint_to_user_story({'sprint_id': sprint01_id}, story01_id, sm01_id)
