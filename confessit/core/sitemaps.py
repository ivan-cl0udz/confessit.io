from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Confession


class ConfessionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Confession.objects.filter(is_approved=True)

    def lastmod(self, obj):
        return obj.created_at


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            "home",
            "all_confessions",
            "terms",
        ]

    def location(self, item):
        return reverse(item)
