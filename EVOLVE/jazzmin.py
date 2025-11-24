# main/jazzmin.py

JAZZMIN_SETTINGS = {
    "site_title": "Evolve Admin",
    "site_header": "Evolve Admin",  # This controls the text next to logo
    "site_brand": "Evolve",   # This controls the brand text
    "welcome_sign": "Welcome to Evolve Admin",
    "copyright": "Evolve Business Group",
    "search_model": ["home.Client"],

    # UI Colors
    "theme": "darkly",
    "site_logo": "./images/logo/fav.png",
    "login_logo": None,
    "login_logo_dark": None,
    "site_icon": "./images/logo/fav.png",
    "show_ui_builder": False,

    # Remove "Django Administration" text
    "site_logo_classes": "brand-image",
    
    # Custom Menu
    "topmenu_links": [
        {"name": "Home", "url": "/", "permissions": ["auth.view_user"]},
        {"home": "app"},
    ],

    # Side Menu with enhanced icons
    "icons": {
        # Home app
        "home.Client": "fas fa-handshake",
        "home.BasicWebsiteInfo": "fas fa-folder",
        "home.PortfolioItem": "fas fa-briefcase",
        "home.ImportExportProductCategory": "fa-solid fa-file-import",
        "home.IndustrialPage": "fa-solid fa-industry",
        "home.HeroMedia": "fa-regular fa-square",

        # Blog section
        "blog.BlogCategory": "fa-solid fa-layer-group",
        "blog.BlogPost": "fa-solid fa-blog",
        "blog.BlogComment": "fa-solid fa-comments",
        "blog.BlogTag": "fa-solid fa-tags",


        #job section
        "job.Job": "fa-solid fa-user-doctor",
        
        # Authentication (User & Group)
        "auth.User": "fas fa-user-cog",
        "auth.Group": "fas fa-users",
    },

    # Sidebar
    "hide_homes": [],
    "hide_models": [],
    "order_with_respect_to": ["home.Client", "home.Project", "home.Service"],

    # Custom CSS & JS
    "custom_css": "css/admin_custom.css",
    "custom_js": "js/admin_custom.js",
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly", 
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "actions_sticky_top": True,
    "button_classes": {
        "primary": "btn-primary-custom",
        "secondary": "btn-secondary-custom",
        "info": "btn-info-custom",
        "warning": "btn-warning-custom",
        "danger": "btn-danger-custom",
        "success": "btn-success-custom",
    },
}