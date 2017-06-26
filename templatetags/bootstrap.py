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
