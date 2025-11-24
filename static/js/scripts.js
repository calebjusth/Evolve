document.addEventListener('DOMContentLoaded', function() {
    const loaderOverlay = document.getElementById('loaderOverlay');
    const loaderProgress = document.getElementById('loaderProgress');
    const loaderCounter = document.getElementById('loaderCounter');

    if (!loaderOverlay) return;

    let progress = 0;
    const duration = 1500; // total time in ms (1.5 seconds)
    const interval = 30;   // update every 30ms
    const increment = 100 / (duration / interval);

    // Simulate progress bar smoothly
    const progressTimer = setInterval(() => {
        progress += increment;
        if (progress > 100) progress = 100;
        if (loaderProgress) loaderProgress.style.width = progress + '%';
        if (loaderCounter) loaderCounter.textContent = Math.floor(progress) + '%';
    }, interval);

    // Hide loader after 3 seconds
    setTimeout(() => {
        clearInterval(progressTimer);
        loaderOverlay.classList.add('hidden');
        setTimeout(() => loaderOverlay.remove(), 800);
    }, duration);
});


// Video loading handler
document.addEventListener('DOMContentLoaded', function() {
    const video = document.querySelector('.parallax-video');
    
    if (video) {
        video.addEventListener('loadeddata', function() {
            console.log('Video loaded successfully');
        });
        
        video.addEventListener('error', function() {
            console.log('Video failed to load, using fallback');
        });
    }
});

// Enhanced parallax with scroll event for better performance
document.addEventListener('DOMContentLoaded', function() {
    const hero = document.querySelector('.hero');
    const video = document.querySelector('.parallax-video');
    
    if (!video) return;
    
    // Enable smooth scrolling behavior
    function handleParallax() {
        const scrolled = window.pageYOffset;
        const heroHeight = hero.offsetHeight;
        const heroTop = hero.getBoundingClientRect().top + window.pageYOffset;
        
        // Only apply parallax when hero section is in view
        if (scrolled < heroTop + heroHeight) {
            const rate = scrolled * 0.5;
            video.style.transform = `translateZ(-1px) scale(2) translateY(${rate}px)`;
        }
    }
    
    // Use requestAnimationFrame for smoother performance
    let ticking = false;
    function updateParallax() {
        handleParallax();
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    }
    
    // Listen to scroll events
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // Initial call
    handleParallax();
});




  (function() {
    const track = document.querySelector('.carousel-track');
    const cards = document.querySelectorAll('.testimonial-card');
    const prevBtn = document.querySelector('.nav-arrow-left');
    const nextBtn = document.querySelector('.nav-arrow-right');
    const progressBar = document.querySelector('.progress-bar');
    
    let currentIndex = 0;
    let cardsPerView = 3;
    let autoScrollInterval;
    let progressInterval;
    let progressValue = 0;
    const autoScrollDuration = 5000; // 5 seconds
    const progressStep = 100 / (autoScrollDuration / 50); // Update every 50ms

    // Calculate cards per view based on screen size
    function updateCardsPerView() {
      const width = window.innerWidth;
      if (width <= 768) {
        cardsPerView = 1;
      } else if (width <= 1024) {
        cardsPerView = 2;
      } else {
        cardsPerView = 3;
      }
    }

    // Update carousel position
    function updateCarousel(smooth = true) {
      const cardWidth = cards[0].offsetWidth;
      const gap = 24;
      const offset = currentIndex * (cardWidth + gap);
      
      if (!smooth) {
        track.style.transition = 'none';
      } else {
        track.style.transition = 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      }
      
      track.style.transform = `translateX(-${offset}px)`;
      
      // Force reflow if transition was disabled
      if (!smooth) {
        track.offsetHeight;
        track.style.transition = 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
      }
    }

    // Navigate to next set of cards
    function goToNext() {
      const maxIndex = cards.length - cardsPerView;
      
      if (currentIndex >= maxIndex) {
        // Loop back to start
        currentIndex = 0;
      } else {
        currentIndex++;
      }
      
      updateCarousel();
      resetProgress();
    }

    // Navigate to previous set of cards
    function goToPrev() {
      if (currentIndex <= 0) {
        currentIndex = cards.length - cardsPerView;
      } else {
        currentIndex--;
      }
      
      updateCarousel();
      resetProgress();
    }

    // Update progress bar
    function updateProgress() {
      progressValue += progressStep;
      
      if (progressValue >= 100) {
        progressValue = 100;
        progressBar.style.width = progressValue + '%';
        goToNext();
      } else {
        progressBar.style.width = progressValue + '%';
      }
    }

    // Reset progress bar
    function resetProgress() {
      progressValue = 0;
      progressBar.style.width = '0%';
      clearInterval(progressInterval);
      startAutoScroll();
    }

    // Start auto-scroll
    function startAutoScroll() {
      progressInterval = setInterval(updateProgress, 50);
    }

    // Stop auto-scroll
    function stopAutoScroll() {
      clearInterval(progressInterval);
    }

    // Event listeners
    nextBtn.addEventListener('click', () => {
      goToNext();
    });

    prevBtn.addEventListener('click', () => {
      goToPrev();
    });

    // Pause on hover
    track.addEventListener('mouseenter', stopAutoScroll);
    track.addEventListener('mouseleave', () => {
      resetProgress();
    });

    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        updateCardsPerView();
        currentIndex = Math.min(currentIndex, cards.length - cardsPerView);
        updateCarousel(false);
      }, 250);
    });

    // Initialize
    updateCardsPerView();
    updateCarousel(false);
    startAutoScroll();
  })();




  // Wait for DOM to be fully loaded
document.addEventListener("DOMContentLoaded", () => {
  const section = document.getElementById("portfolio-section")
  const title = document.getElementById("portfolio-title")
  const caption = document.getElementById("portfolio-caption")
  const cards = document.querySelectorAll(".portfolio-card")
  const ctaBar = document.getElementById("cta-bar")

  let isVisible = false

  // Create Intersection Observer
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !isVisible) {
          isVisible = true
          animateElements()
        }
      })
    },
    { threshold: 0.1 },
  )

  // Observe the section
  if (section) {
    observer.observe(section)
  }

  // Animation function
  function animateElements() {
    // Animate title
    if (title) {
      title.classList.add("animate-fadeInUp")
    }

    // Animate caption with delay
    if (caption) {
      setTimeout(() => {
        caption.classList.add("animate-fadeInUp")
      }, 200)
    }

    // Animate cards with staggered delay
    cards.forEach((card, index) => {
      setTimeout(
        () => {
          card.classList.add("animate-scaleIn")
        },
        400 + index * 150,
      )
    })

    // Animate CTA bar
    if (ctaBar) {
      const totalDelay = 400 + cards.length * 150 + 200
      setTimeout(() => {
        ctaBar.classList.add("animate-slideInUp")
      }, totalDelay)
    }
  }
})



// Fixed Why Choose Us JavaScript
document.addEventListener("DOMContentLoaded", () => {
    const section = document.getElementById("whyChooseUs");
    const introPhase = document.getElementById("introPhase");
    const videoBackground = document.getElementById("videoBackground");
    const valueButtons = document.getElementById("valueButtons");

    if (!section) return;

    let isInView = false;

    // IntersectionObserver to track when section enters/leaves viewport
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    isInView = true;
                    section.classList.add("in-view");
                } else {
                    isInView = false;
                    section.classList.remove("in-view");
                    // Reset everything when section leaves viewport
                    resetSectionState();
                }
            });
        },
        { 
            threshold: 0.1,
            rootMargin: '-50px 0px -50px 0px' // Adjust this to control when the section is considered "in view"
        }
    );

    observer.observe(section);

    function resetSectionState() {
        introPhase.style.opacity = "1";
        videoBackground.style.opacity = "0";
        valueButtons.style.opacity = "0";
        
        const buttons = document.querySelectorAll(".value-button");
        buttons.forEach((button) => {
            button.style.opacity = "0";
            button.style.transform = "scale(0.9)";
        });
    }

    // Enhanced scroll handler
    function handleScroll() {
        if (!isInView) {
            resetSectionState();
            return;
        }

        const rect = section.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const sectionTop = rect.top;
        const sectionBottom = rect.bottom;

        // Calculate how much of the section is visible
        const visibleHeight = Math.min(sectionBottom, windowHeight) - Math.max(sectionTop, 0);
        const progress = Math.max(0, Math.min(1, visibleHeight / windowHeight));

        // Only apply effects when section is significantly in view
        if (sectionTop < windowHeight * 0.8 && sectionBottom > windowHeight * 0.2) {
            const scrollProgress = Math.max(0, Math.min(1, (windowHeight - sectionTop) / (windowHeight * 1.5)));

            // Apply fade transitions
            introPhase.style.opacity = 1 - scrollProgress;
            videoBackground.style.opacity = scrollProgress;
            valueButtons.style.opacity = scrollProgress;

            // Apply parallax to video
            const parallaxOffset = (windowHeight - sectionTop) * 0.3;
            videoBackground.style.transform = `translateY(${parallaxOffset}px)`;

            // Fade in value buttons with staggered delay
            const buttons = document.querySelectorAll(".value-button");
            buttons.forEach((button, index) => {
                const buttonDelay = index * 0.15;
                if (scrollProgress > 0.3 + buttonDelay) {
                    button.style.opacity = "1";
                    button.style.transform = "scale(1)";
                } else if (scrollProgress < 0.2) {
                    button.style.opacity = "0";
                    button.style.transform = "scale(0.9)";
                }
            });
        } else {
            // Section is leaving viewport
            resetSectionState();
        }
    }

    // Throttle scroll events
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(() => {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener("scroll", requestTick, { passive: true });
    
    // Initial call
    handleScroll();
});




