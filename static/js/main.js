document.addEventListener("DOMContentLoaded", () => {


    // Mobile Nav Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            const isActive = navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
            hamburger.setAttribute('aria-expanded', isActive);
        });

        // Close menu when link is clicked
        const navItems = document.querySelectorAll('.nav-links a');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
                hamburger.setAttribute('aria-expanded', 'false');
            });
        });
    }

    let isHeroVisible = true;
    const heroSec = document.querySelector('.hero-section');
    if (heroSec) {
        const heroObserver = new IntersectionObserver((entries) => {
            isHeroVisible = entries[0].isIntersecting;
        });
        heroObserver.observe(heroSec);
    }

    // Hero Typewriter
    const heroTextEl = document.getElementById('typewriter-text');
    const typewriterContainer = document.querySelector('.typewriter-container');
    const words = typewriterContainer && typewriterContainer.dataset.words
        ? typewriterContainer.dataset.words.split(',')
        : ["Student", "Web Developer", "Data Analyst"];
    let i = 0;

    if (heroTextEl) {
        function typeWriter() {
            let word = words[i].trim().split('');
            var loopTyping = function () {
                if (word.length > 0) {
                    heroTextEl.textContent += word.shift();
                    setTimeout(loopTyping, 100);
                } else {
                    setTimeout(loopDeleting, 2000);
                }
            };

            function loopDeleting() {
                let currentWord = heroTextEl.textContent;
                if (currentWord.length > 0 && currentWord !== "> ") {
                    currentWord = currentWord.slice(0, -1);
                    heroTextEl.textContent = currentWord;
                    setTimeout(loopDeleting, 50);
                } else {
                    i = (i + 1) % words.length;
                    setTimeout(typeWriter, 500);
                }
            }

            loopTyping();
        }

        heroTextEl.textContent = "> ";
        setTimeout(typeWriter, 1000);
    }


    // About Terminal Typewriter
    const terminalEl = document.getElementById('about-terminal');
    if (terminalEl) {
        const terminalText = terminalEl.dataset.lines ? terminalEl.dataset.lines.replace(/\r/g, '').split('\n') : [
            "> whoami",
            "Software Developer",
            "> status",
            "Building awesome things",
            "> stack",
            "Python | Django | JS | HTML | CSS",
            "> _"
        ];

        let t_idx = 0;
        let c_idx = 0;
        function typeTerminal() {
            if (t_idx === 0 && c_idx === 0) {
                terminalEl.innerHTML = ""; // Flush template whitespace
            }
            if (t_idx < terminalText.length) {
                let line = terminalText[t_idx];
                if (c_idx < line.length) {
                    terminalEl.innerHTML += line.charAt(c_idx);
                    c_idx++;
                    setTimeout(typeTerminal, 40); // Type next character
                } else {
                    terminalEl.innerHTML += "<br>";
                    c_idx = 0;
                    t_idx++;
                    setTimeout(typeTerminal, 600); // Wait before next line
                }
            }
        }
        // Use intersection observer to trigger it when in view
        const terminalObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                setTimeout(typeTerminal, 500);
                terminalObserver.disconnect();
            }
        });
        terminalObserver.observe(terminalEl);
    }

    // Intersection Observer for Animations (Fade in)
    const faders = document.querySelectorAll('.fade-in');
    const appearOptions = {
        threshold: 0.01,
        rootMargin: "0px 0px -50px 0px"
    };

    const appearOnScroll = new IntersectionObserver(function (entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('appear');
            observer.unobserve(entry.target);
        });
    }, appearOptions);

    faders.forEach(fader => {
        appearOnScroll.observe(fader);
    });

    // Make hero section and single blog post elements visible immediately on load
    const immediateFaders = document.querySelectorAll('.hero-section .fade-in, .single-post-view.fade-in');
    immediateFaders.forEach(el => {
        setTimeout(() => {
            el.classList.add('appear');
        }, 300);
    });

    // Count Up Animation for LeetCode
    const counters = document.querySelectorAll('.count-up');
    const countUpObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const endVal = parseInt(target.getAttribute('data-target'));
                if (endVal === 0) return;

                let startVal = 0;
                const duration = 2000;
                const increment = endVal / (duration / 16);

                const updateCounter = () => {
                    startVal += increment;
                    if (startVal < endVal) {
                        target.innerText = Math.ceil(startVal);
                        requestAnimationFrame(updateCounter);
                    } else {
                        target.innerText = endVal;
                    }
                };

                updateCounter();
                observer.unobserve(target);
            }
        });
    });

    counters.forEach(counter => {
        countUpObserver.observe(counter);
    });

    // Scroll to contact section if there are messages (after form submission)
    const messages = document.querySelector('.alert');
    if (messages) {
        const contactSection = document.getElementById('contact');
        if (contactSection) {
            setTimeout(() => {
                contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 300);
        }
    }

    // Education Timeline Progress Line Animation
    const eduTimeline = document.getElementById('education-timeline');
    const timelineLine = document.getElementById('timeline-line');

    if (eduTimeline && timelineLine) {
        function updateTimelineProgress() {
            const rect = eduTimeline.getBoundingClientRect();
            const timelineTop = rect.top;
            const timelineHeight = rect.height;
            const windowHeight = window.innerHeight;

            // Calculate how much of the timeline has been scrolled
            let progress = 0;

            if (timelineTop < windowHeight && timelineTop + timelineHeight > 0) {
                // Calculate progress: 0 when top enters viewport, 1 when bottom is reached
                const scrolled = windowHeight - timelineTop;
                progress = Math.min(Math.max(scrolled / (timelineHeight + windowHeight * 0.2), 0), 1);
            }

            // Update the line height based on progress
            const lineHeight = progress * timelineHeight;
            timelineLine.style.height = `${lineHeight}px`;
        }

        // Update on scroll
        window.addEventListener('scroll', () => {
            requestAnimationFrame(updateTimelineProgress);
        }, { passive: true });

        // Initial call
        updateTimelineProgress();
    }

    // Spline Viewer Fixes
    const splineViewer = document.querySelector('spline-viewer');
    if (splineViewer) {
        // Aggressive DOM patching to remove logo if possible
        const removeLogo = () => {
            const shadowRoot = splineViewer.shadowRoot;
            if (shadowRoot) {
                const logo = shadowRoot.querySelector('#logo');
                if (logo) {
                    logo.style.display = 'none';
                    logo.style.opacity = '0';
                    logo.remove();
                }
            }
        };

        // Try removing periodically as it might re-render
        const logoInterval = setInterval(removeLogo, 100);
        setTimeout(() => clearInterval(logoInterval), 5000); // Stop after 5 seconds

        // Prevent zooming on the spline viewer but allow page scrolling
        splineViewer.addEventListener('wheel', (e) => {
            e.stopPropagation();
        }, { passive: true, capture: true });

        // Prevent pinch zoom on the room but allow other touch actions
        splineViewer.addEventListener('touchmove', (e) => {
            if (e.touches.length > 1) {
                e.stopPropagation();
            }
        }, { passive: true, capture: true });
    }

    // 3D Tilt Interaction for Bitmoji
    const tiltWrapper = document.getElementById('tilt-wrapper');
    const tiltImage = document.getElementById('tilt-image');

    if (tiltWrapper && tiltImage) {
        tiltWrapper.addEventListener('mousemove', (e) => {
            const rect = tiltWrapper.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate tilt amount based on mouse position relative to center
            // Max tilt of 20 degrees
            const tiltX = ((y - centerY) / centerY) * -20;
            const tiltY = ((x - centerX) / centerX) * 20;
            
            // Apply tilt, scale up slightly, and pause the floating animation
            tiltImage.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(1.05)`;
            tiltImage.style.transition = "transform 0.1s ease-out";
            tiltImage.style.animationPlayState = "paused";
        });

        tiltWrapper.addEventListener('mouseleave', () => {
            // Reset transform and resume floating animation
            tiltImage.style.transform = `rotateX(0deg) rotateY(0deg) scale(1)`;
            tiltImage.style.transition = "transform 0.5s ease-out";
            tiltImage.style.animationPlayState = "running";
        });
    }

    // Edit Profile Modal Logic
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const editProfileModal = document.getElementById('edit-profile-modal');
    const editProfileCloseBtn = document.getElementById('edit-profile-close-btn');
    const editProfileCancelBtn = document.getElementById('edit-profile-cancel-btn');
    const editProfileForm = document.getElementById('edit-profile-form');

    if (editProfileBtn && editProfileModal) {
        // Open Modal
        editProfileBtn.addEventListener('click', () => {
            editProfileModal.style.display = 'flex';
            setTimeout(() => {
                editProfileModal.classList.add('active');
            }, 10);
        });

        // Close Modal function
        const closeModal = () => {
            editProfileModal.classList.remove('active');
            setTimeout(() => {
                editProfileModal.style.display = 'none';
            }, 300);
        };

        if (editProfileCloseBtn) editProfileCloseBtn.addEventListener('click', closeModal);
        if (editProfileCancelBtn) editProfileCancelBtn.addEventListener('click', closeModal);

        // Close Modal when clicking outside container
        editProfileModal.addEventListener('click', (e) => {
            if (e.target === editProfileModal) {
                closeModal();
            }
        });

        // Handle AJAX Form Submission
        if (editProfileForm) {
            editProfileForm.addEventListener('submit', (e) => {
                e.preventDefault();

                const formData = new FormData(editProfileForm);
                const saveBtn = document.getElementById('edit-profile-save-btn');
                const originalBtnText = saveBtn ? saveBtn.textContent : 'Save Changes';

                if (saveBtn) {
                    saveBtn.disabled = true;
                    saveBtn.textContent = 'Saving...';
                }

                fetch(editProfileForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Dynamically update contents in real-time
                        
                        // 1. Update Name
                        const nameHeading = document.querySelector('.hero-heading');
                        if (nameHeading) {
                            nameHeading.innerHTML = `Hello, I'm <span class="highlight">${data.name}</span>`;
                        }

                        // 2. Update Typewriter data words
                        const typewriterContainer = document.querySelector('.typewriter-container');
                        if (typewriterContainer) {
                            typewriterContainer.setAttribute('data-words', data.typewriter_words);
                        }

                        // 3. Update Availability Badge Text
                        const availBadge = document.querySelector('.availability-badge');
                        if (availBadge) {
                            const dot = availBadge.querySelector('.dot');
                            availBadge.innerHTML = '';
                            if (dot) availBadge.appendChild(dot);
                            availBadge.appendChild(document.createTextNode(' ' + data.available_badge_text));
                            // Put back the edit button
                            availBadge.appendChild(editProfileBtn);
                        }

                        // 4. Update Card 1
                        const card1 = document.getElementById('hero-card-1');
                        if (card1) {
                            const title = card1.querySelector('.card-title');
                            const text = card1.querySelector('.card-text');
                            if (title) title.textContent = data.card_1_title;
                            if (text) text.textContent = data.card_1_text;
                        }

                        // 5. Update Card 2
                        const card2 = document.getElementById('hero-card-2');
                        if (card2) {
                            const title = card2.querySelector('.card-title');
                            const text = card2.querySelector('.card-text');
                            if (title) title.textContent = data.card_2_title;
                            if (text) text.textContent = data.card_2_text;
                        }

                        // 6. Update Card 3
                        const card3 = document.getElementById('hero-card-3');
                        if (card3) {
                            const title = card3.querySelector('.card-title');
                            const text = card3.querySelector('.card-text');
                            if (title) title.textContent = data.card_3_title;
                            if (text) text.textContent = data.card_3_text;
                        }

                        // Close modal successfully
                        closeModal();

                        // Add a beautiful subtle message or animation
                        showToast("Profile updated successfully!");

                        // Reload after 1 second to fully sync deep script references (like Typewriter logic)
                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    } else {
                        alert("Error saving profile details.");
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert("Error saving profile details.");
                })
                .finally(() => {
                    if (saveBtn) {
                        saveBtn.disabled = false;
                        saveBtn.textContent = originalBtnText;
                    }
                });
            });
        }
    }

    // Helper Toast notification function
    function showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'terminal-toast';
        toast.textContent = `> ${message}`;
        document.body.appendChild(toast);

        // Add sleek styles directly
        toast.style.position = 'fixed';
        toast.style.bottom = '20px';
        toast.style.right = '20px';
        toast.style.background = '#1a1a1a';
        toast.style.color = 'var(--accent)';
        toast.style.padding = '1rem 1.5rem';
        toast.style.borderRadius = '8px';
        toast.style.fontFamily = "'Fira Code', monospace";
        toast.style.border = '2px solid var(--accent)';
        toast.style.zIndex = '10000';
        toast.style.boxShadow = '0 10px 30px rgba(76, 175, 80, 0.2)';
        toast.style.animation = 'slideIn 0.3s ease-out';

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 3000);
    }

    // LinkedIn Share with Auto-Copy
    const linkedinShareBtns = document.querySelectorAll('.js-linkedin-share');
    linkedinShareBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const caption = btn.getAttribute('data-share-caption');
            if (caption && navigator.clipboard) {
                navigator.clipboard.writeText(caption)
                    .then(() => {
                        showToast("Caption copied to clipboard!");
                    })
                    .catch(err => {
                        console.warn("Could not auto-copy caption to clipboard", err);
                    });
            }
            // Default href opens the window because of target="_blank"
        });
    });

    // Interactive 3D Perspective Card Tilt for Certifications
    const certCards = document.querySelectorAll('.cert-card');
    certCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Subtle 3D tilt calculation
            const rotateX = (y - centerY) / 15;
            const rotateY = (centerX - x) / 15;
            
            card.style.transform = `perspective(1000px) translateY(-12px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            card.style.transition = 'transform 0.1s ease-out, background 0.3s, border-color 0.3s, box-shadow 0.3s';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) translateY(0) rotateX(0) rotateY(0)`;
            card.style.transition = 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1), background 0.3s, border-color 0.3s, box-shadow 0.3s';
        });
    });
});
