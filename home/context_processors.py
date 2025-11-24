from .models import BasicWebsiteInfo

def website_info(request):
    """
    Adds the single BasicWebsiteInfo instance to the context globally.
    """
    info = BasicWebsiteInfo.objects.first()  # Since only one is allowed
    return {
        'website_info': info
    }
