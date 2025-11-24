from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import BlogPost

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ['home', 'construction', 'transport', 'industrial', 'import_and_export', 'portfolio', 'blog', 'job_list']

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return BlogPost.published.all()

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return obj.get_absolute_url()
