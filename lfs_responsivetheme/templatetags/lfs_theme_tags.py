# django imports
from django.core.cache import cache
from django.template import Library, Node, TemplateSyntaxError
from django.utils.translation import ugettext as _

#from django.form.util import ErrorList as OriginalErrorList
#from django.utils.encoding import force_unicode
#from django.utils.safestring import mark_safe

# portlets imports
import portlets.utils
from portlets.models import Slot
# lfs imports
import lfs.core.utils
from lfs.catalog.models import Category

register = Library()

#class ErrorList(OriginalErrorList):
#    """ """
#    def as_ul(self):
#        if not self: return u''
#        return mark_safe(u'<ul class="errorlist">%s</ul>'
#                % ''.join([u'<li>%s%s</li>' % (k, force_unicode(v))
#                    for k, v in self.items()]))


class SlotsInformationNode(Node):
    """
    """
    def render(self, context):
        request = context.get("request")
        object = context.get("category") or context.get("product") or context.get("page")
        if object is None:
            object = lfs.core.utils.get_default_shop(request)

        slots = cache.get("slots")
        if slots is None:
            slots = Slot.objects.all()
            cache.set("slots", slots)

        for slot in slots:
            cache_key = "has-portlets-%s-%s-%s" % (object.__class__.__name__, object.id, slot.name)
            has_portlets = cache.get(cache_key)
            if has_portlets is None:
                has_portlets = portlets.utils.has_portlets(object, slot)
                cache.set(cache_key, has_portlets)

            context["Slot%s" % slot.name] = has_portlets

        cache_key = "content-class-%s-%s" % (object.__class__.__name__, object.id)
        content_class = cache.get(cache_key)
        if content_class is None:
            content_class = "col-md-12 last"
            if context.get("SlotLeft", None) and context.get("SlotRight", None):
                content_class = "col-md-9 padding-both"
            elif context.get("SlotLeft", None):
                content_class = "col-md-9 padding-left last"
            elif context.get("SlotRight", None):
                content_class = "col-md-9 padding-right"

            cache.set(cache_key, content_class)

        context["content_class"] = content_class
        return ''

def do_slots_information(parser, token):
    """Calculates some context variables based on displayed slots.
    """
    bits = token.contents.split()
    len_bits = len(bits)
    if len_bits != 1:
        raise TemplateSyntaxError(_('%s tag needs no argument') % bits[0])

    return SlotsInformationNode()

register.tag('slots_information', do_slots_information)


@register.inclusion_tag('lfs/mail/mail_html_footer.html', takes_context=True)
def email_html_footer(context):
    request = context.get('request', None)
    shop = lfs.core.utils.get_default_shop(request)
    return {
        "shop": shop
    }


@register.inclusion_tag('lfs/mail/mail_text_footer.html', takes_context=True)
def email_text_footer(context):
    request = context.get('request', None)
    shop = lfs.core.utils.get_default_shop(request)
    return {
        "shop": shop
    }

@register.inclusion_tag('lfs/catalog/top_level_categories.html', takes_context=True)
def menu_top_level_categories(context):
    """Displays the top level categories.
    """
    request = context.get("request")
    obj = context.get("product") or context.get("category")

    categories = []
    top_category = lfs.catalog.utils.get_current_top_category(request, obj)

    for category in Category.objects.filter(parent=None, exclude_from_navigation=False):

        if top_category:
            current = top_category.id == category.id
        else:
            current = False

        categories.append({
            "url": category.get_absolute_url(),
            "name": category.name,
            "current": current,
        })

    return {
        "categories": categories,
    }

