// Parallax Car Animation
const parallaxCar = document.getElementById('parallaxCar');
const parallaxSection = document.querySelector('.parallax-section');
const statsSection = document.querySelector('.stats-section');

let parallaxActive = true;

function updateParallax() {
    if (!parallaxActive || !parallaxCar) return;
    
    const scrollPosition = window.pageYOffset;
    const parallaxStart = parallaxSection.offsetTop - window.innerHeight;
    const parallaxEnd = statsSection.offsetTop - window.innerHeight;
    
    // Check if we've scrolled past the stats section (third section)
    if (scrollPosition > parallaxEnd) {
        parallaxActive = false;
        parallaxCar.style.transform = 'translateX(0)';
        return;
    }
    
    // Only apply parallax effect when in the first two sections
    if (scrollPosition > parallaxStart && scrollPosition < parallaxEnd) {
        const progress = (scrollPosition - parallaxStart) / (parallaxEnd - parallaxStart);
        const moveAmount = progress * 100; // Move from 0 to 100 pixels
        parallaxCar.style.transform = `translateX(${moveAmount}px)`;
    }
}

// Throttle function for better performance
function throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

if (parallaxCar) {
    window.addEventListener('scroll', throttle(updateParallax, 10));
}

// Reset parallax when scrolling back up
window.addEventListener('scroll', () => {
    if (!parallaxCar) return;
    
    const scrollPosition = window.pageYOffset;
    const parallaxStart = parallaxSection.offsetTop - window.innerHeight;
    
    if (scrollPosition < parallaxStart) {
        parallaxActive = true;
    }
});

// Animated Counter for Stats
const statNumbers = document.querySelectorAll('.stat-number');
let statsAnimated = false;

function animateStats() {
    const statsSection = document.querySelector('.stats-section');
    if (!statsSection || statsAnimated) return;
    
    const statsSectionTop = statsSection.offsetTop;
    const statsSectionHeight = statsSection.offsetHeight;
    const scrollPosition = window.pageYOffset + window.innerHeight;
    
    if (scrollPosition > statsSectionTop + statsSectionHeight / 3 && !statsAnimated) {
        statsAnimated = true;
        
        statNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            const duration = 2000; // 2 seconds
            const increment = target / (duration / 16); // 60fps
            let current = 0;
            
            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    stat.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    stat.textContent = target;
                }
            };
            
            updateCounter();
        });
    }
}

if (statNumbers.length > 0) {
    window.addEventListener('scroll', animateStats);
}

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all vehicle cards
document.querySelectorAll('.vehicle-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Observe about features
document.querySelectorAll('.about-feature').forEach((feature, index) => {
    feature.style.opacity = '0';
    feature.style.transform = 'translateX(-30px)';
    feature.style.transition = `opacity 0.6s ease ${index * 0.2}s, transform 0.6s ease ${index * 0.2}s`;
    observer.observe(feature);
});

// Add hover effect to buttons
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
    });
    
    btn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Initialize animations on page load
window.addEventListener('load', () => {
    // Trigger initial parallax calculation
    if (parallaxCar) {
        updateParallax();
    }
    
    // Check if stats section is already in view
    if (statNumbers.length > 0) {
        animateStats();
    }
});

// Enhanced navbar scroll functionality
window.addEventListener('scroll', () => {
    const header = document.getElementById('header');
    if (header) {
        const scrolled = window.scrollY > 100;
        if (scrolled) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }
});