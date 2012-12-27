# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import pooler
from report.render import render

class external_pdf(render):
    def __init__(self, pdf):
        render.__init__(self)
        self.pdf = pdf
        self.output_type='pdf'
    
    def _render(self):
        return self.pdf

def compute_burndown(cr, uid, story_ids, sprint_date_start, sprint_date_stop, total_points):
    latest = False
    pool = pooler.get_pool(cr.dbname)
    sprint_pool = pool.get('project.scrum.sprint')
    story_pool = pool.get('project.scrum.product.backlog')
    
    if len(story_ids):
        story_ids = story_pool.search(cr, uid, [('id', 'in', story_ids)], order='create_date')
        stories = story_pool.read(cr, uid, story_ids, ['complexity', 'date_open', 'sprint_id'])
        sprint = sprint_pool.read(cr, uid, stories[0]['sprint_id'][0])
        done_story_ids = story_pool.search(cr, uid, [('id', 'in', story_ids),('state', '=', 'done')], order='date_done asc')
        done_stories = story_pool.read(cr, uid, done_story_ids, ['complexity', 'date_done'])
        
    else:
        stories = []
        done_stories = []
    
    current_date = sprint_date_start
    total = 0
    done = 0
    result = []
    
    # scan the date from sprint start date to sprint state stop
    while datetime.strptime(current_date, '%Y-%m-%d') <= datetime.strptime(sprint_date_stop, '%Y-%m-%d'):
        
        #scan the stories with date_open <= current_date increment
        while len(stories) and stories[0]['date_open'] and datetime.strptime(stories[0]['date_open'][:10], '%Y-%m-%d')<=datetime.strptime(current_date, '%Y-%m-%d'):
            latest = stories.pop(0)
            total += float(latest.get('complexity', 0.0))
        
        i = 0
        while i < len(done_stories):
            if done_stories[i] and done_stories[i]['date_done'] == current_date:
                date_done = done_stories[i].get('date_done', False)
                done += float(done_stories[i].get('complexity', 0.0))
            else:
                date_done = current_date
                done += 0.0
            i+=1
        
        result.append( (int(time.mktime(time.strptime(current_date,'%Y-%m-%d'))), total_points - done) )
        current_date = (datetime.strptime(current_date, '%Y-%m-%d') + relativedelta(days=1)).strftime('%Y-%m-%d')
        
        if not len(stories) and not len(done_stories):
            break
        
    result.append( (int(time.mktime(time.strptime(date_done,'%Y-%m-%d'))), 0) )
    return result


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

