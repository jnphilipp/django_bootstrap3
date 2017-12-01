# -*- coding: utf-8 -*-
# Copyright (C) 2016-1017 Nathanael Philipp (jnphilipp) <mail@jnphilipp.org>
#
# This file is part of django_bootstrap3.
#
# django_bootstrap3 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django_bootstrap3 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django_bootstrap3. If not, see <http://www.gnu.org/licenses/>.

import types

from copy import copy
from django.template import Library
register = Library()


def _process_field_attributes(field, attr, process):
    # split attribute name and value from 'attr:value' string
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''

    field = copy(field)

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter('append_attr')
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value
    return _process_field_attributes(field, attr, process)


@register.filter(name='add_class')
def add_class(field, css_class):
    return append_attr(field, 'class:' + css_class)


@register.inclusion_tag('bootstrap/css.html')
def bootstrap_css():
    return {}


@register.inclusion_tag('bootstrap/js.html')
def bootstrap_js():
    return {}


@register.inclusion_tag('bootstrap/messages.html', takes_context=True)
def messages(context):
    return {'messages': context['messages']}


@register.inclusion_tag('bootstrap/pagination.html', takes_context=True)
def pagination(context, paginator, page, title=None, *args, **kwargs):
    start_page = max(int(page.number) - 4, 0)
    end_page = min(int(page.number) + 3, paginator.num_pages)
    context['prange'] = paginator.page_range[start_page:end_page]
    context['page'] = page
    context['title'] = title
    context['kwargs'] = kwargs
    return context


@register.inclusion_tag('bootstrap/form/base.html', takes_context=True)
def bootstrap_form(context, form, url='', type='horizontal', **kwargs):
    assert type in ['horizontal', 'inline', 'vertical']
    context['form'] = form
    context['url'] = url
    context['type'] = type
    for k, v in kwargs.items():
        context[k] = v
    return context


@register.inclusion_tag('bootstrap/sortable_th.html', takes_context=True)
def sortable_th(context, column_name, o, get_name, get_value, colspan=1,
                rowspan=1, *args, **kwargs):
    context['column_name'] = column_name
    context['colspan'] = colspan
    context['rowspan'] = rowspan
    context['sort_icon'] = 'up' if o.startswith('-') else 'down'
    context['show_options'] = o.endswith(get_value)

    params = '&'.join(['%s=%s' % (k, v) for k, v in kwargs.items() if v])
    context['link'] = '?%s=%s%s&%s' % (get_name,
                                       '' if o.startswith('-') else '-',
                                       get_value, params)
    context['remove_link'] = '?%s=&%s' % (get_name, params)
    return context
