# -*- coding: utf-8 -*-

from django.template import Library
register = Library()


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


@register.inclusion_tag('bootstrap/sortable_th.html', takes_context=True)
def sortable_th(context, column_name, o, get_name, get_value, colspan=1, rowspan=1, *args, **kwargs):
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
