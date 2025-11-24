# templatetags/hero_tags.py
from django import template
from ..models import HeroMedia

register = template.Library()

@register.simple_tag
def get_hero_media():
    try:
        return HeroMedia.objects.first()
    except HeroMedia.DoesNotExist:
        return None

@register.inclusion_tag('includes/hero_section.html')
def render_hero_section(page_name, hero_media=None):
    """Render hero section for specific page"""
    if not hero_media:
        try:
            hero_media = HeroMedia.objects.first()
        except HeroMedia.DoesNotExist:
            hero_media = None
    
    context = {
        'hero_media': hero_media,
        'page_name': page_name,
    }
    return context