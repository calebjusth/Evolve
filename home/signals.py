from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from blog.models import BlogPost
from .models import PortfolioItem, Testimonial, Client

@receiver([post_save, post_delete], sender=PortfolioItem)
def clear_portfolio_cache(sender, **kwargs):
    """Clear portfolio cache when projects change"""
    print("Clearing portfolio cache...")  # For debugging
    cache.delete_many([
        'featured_portfolio_items',
        'portfolio_construction',
        'portfolio_industrial', 
        'portfolio_transportation',
        'portfolio_import_export',
        'construction_featured_project',
        'construction_projects',
    ])

@receiver([post_save, post_delete], sender=Testimonial)
def clear_testimonials_cache(sender, **kwargs):
    """Clear testimonials cache when testimonials change"""
    print("Clearing testimonials cache...")
    cache.delete('testimonials_section')

@receiver([post_save, post_delete], sender=Client)
def clear_clients_cache(sender, **kwargs):
    """Clear clients cache when clients change"""
    print("Clearing clients cache...")
    cache.delete_many(['clients_section', 'construction_clients'])

@receiver([post_save, post_delete], sender=BlogPost)
def clear_blog_cache(sender, **kwargs):
    """Clear blog cache when posts change"""
    print("Clearing blog cache...")
    cache.delete('latest_posts_section')