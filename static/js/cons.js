// Construction Page Specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Cinematic Scroll Animations
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || 0;
                setTimeout(() => {
                    entry.target.classList.add('animate');
                }, delay);
                animateOnScroll.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cinematic text elements
    document.querySelectorAll('.cinematic-text').forEach(element => {
        animateOnScroll.observe(element);
    });

    // Fixed Parallax effect for hero section (no movement)
    let lastScrollY = window.scrollY;
    const hero = document.querySelector('.hero');
    
    function updateParallax() {
        const scrolled = window.scrollY;
        
        // Only apply minimal parallax to prevent overlap issues
        if (hero) {
            const parallaxValue = scrolled * 0.1; // Reduced from 0.5 to 0.1
            hero.style.transform = `translateY(${parallaxValue}px)`;
            
            // Add slight opacity fade when scrolling down
            const opacity = Math.max(0.6, 1 - (scrolled / 1000));
            hero.style.opacity = opacity;
        }
        
        lastScrollY = scrolled;
    }

    // Throttled scroll handler
    let ticking = false;
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateParallax();
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });

    // Add stagger animation to news cards
    const newsCards = document.querySelectorAll('.news-card');
    const newsObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                newsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    newsCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        newsObserver.observe(card);
    });

    // Mobile menu fix - ensure it works with construction page
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const nav = document.getElementById('nav');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');

    if (mobileMenuBtn && nav) {
        // Remove any existing event listeners to prevent conflicts
        mobileMenuBtn.replaceWith(mobileMenuBtn.cloneNode(true));
        const newMobileMenuBtn = document.getElementById('mobileMenuBtn');
        
        newMobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            nav.classList.toggle('active');
            newMobileMenuBtn.classList.toggle('active');
            if (mobileMenuOverlay) {
                mobileMenuOverlay.classList.toggle('active');
            }
            document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
        });
    }

    // Close mobile menu when clicking on nav links
    document.querySelectorAll('.nav a').forEach(link => {
        link.addEventListener('click', () => {
            if (nav.classList.contains('active')) {
                nav.classList.remove('active');
                if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
                if (mobileMenuOverlay) mobileMenuOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Initialize animations on load
    setTimeout(() => {
        document.querySelectorAll('.cinematic-text').forEach(text => {
            const rect = text.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.8) {
                const delay = text.dataset.delay || 0;
                setTimeout(() => {
                    text.classList.add('animate');
                }, delay);
            }
        });
    }, 100);
});