"""
Provides an array of dates for iteration over

A bit like pagination for date ranges

"""

import datetime
from collections import deque

from django import template
from django.template.loader import get_template

register = template.Library()


@register.tag
def date_slider(parser, token):
    try:
        tag_name, current_date = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires two arguments")
    
    return DateSliderNode(current_date)

default_options = {
    'show_current_year': False,    
    'show_current_month': False,
    'show_current_day': True,
    
    'show_past_years': 0,
    'show_past_months': 0,
    'show_past_days': 5,
    
    'show_future_years': 0,
    'show_future_months': 0,
    'show_future_days': 2
}


"""
Wrapper objects for context

"""
class Date(object):
    def __init__(self, date):
        self.date = date
    
    def __getattr__(self, attr_name):
        return self.date.__getattr(attr_name)
    
    def __unicode__(self):
        return unicode(self.date)
    
    def __repr__(self):
        return repr(self.date)
    
    def is_current(self):
        return False
    
    def is_today(self):
        return datetime.date.today() == self.date

class CurrentDate(Date):
    def is_current(self):
        return True

"""
Render

"""
class DateSliderNode(template.Node):
    def __init__(self, current_date, options={}):
        self.current_date = template.Variable(current_date)
        # Compile options dictionary based on defaults
        self.options = dict(default_options.items() + options.items())
    
    def get_dates(self, current_date):
        dates = deque([CurrentDate(current_date)])
        
        for i in range(1, self.options['show_past_days']+1):
            dates.appendleft(Date(current_date - datetime.timedelta(days=i)))
        
        for i in range(1, self.options['show_future_days']+1):
            dates.append(Date(current_date + datetime.timedelta(days=i)))
        
        return list(dates)
    
    def render(self, context):
        try:
            dates = self.get_dates(self.current_date.resolve(context))
            
            context.update({'dates': dates})
            
            return get_template("date_slider/slider.html").render(context)
        except template.VariableDoesNotExist:
            return ''