from django import template
from ..models import MenuItem
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.inclusion_tag('tree_menu/menu_render.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    path = getattr(request, 'path', '') if request else ''

    items = list(MenuItem.objects.filter(menu_name=menu_name).order_by('order', 'id'))

    by_id = {
        item.id: {
            'obj': item,
            'children': [],
            'expanded': False,
            'active': False,
            'parent_id': item.parent_id,
            'url': None,
        }
        for item in items
    }

    for node in by_id.values():
        item = node['obj']
        url = None
        if item.named_url:
            try:
                url = reverse(item.named_url)
            except NoReverseMatch:
                url = None
        if not url and item.explicit_url:
            url = item.explicit_url
        node['url'] = url

    roots = []
    for node in by_id.values():
        pid = node['parent_id']
        if pid and pid in by_id:
            by_id[pid]['children'].append(node)
        else:
            roots.append(node)

    active_id = None
    for nid, node in by_id.items():
        if node['url'] and node['url'] == path:
            active_id = nid
            break
    if active_id is None:
        for nid, node in by_id.items():
            if node['url'] and path.startswith(node['url'].rstrip('/')) and len(node['url']) > 1:
                active_id = nid
                break

    if active_id:
        by_id[active_id]['active'] = True
        by_id[active_id]['expanded'] = True

        cur = by_id[active_id]
        visited = set()
        while cur.get('parent_id'):
            pid = cur['parent_id']
            if not pid or pid not in by_id or pid in visited:
                break
            visited.add(pid)
            parent = by_id[pid]
            parent['expanded'] = True
            cur = parent

        for child in by_id[active_id]['children']:
            child['expanded'] = True

    return {
        'menu_name': menu_name,
        'roots': roots,
        'request': request,
    }
