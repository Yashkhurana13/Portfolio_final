/**
 * blog_detail.js
 * Handles interactivity for the 3-column editorial blog post view.
 */

document.addEventListener('DOMContentLoaded', () => {
    initReadingProgress();
    initTableOfContents();
    initCodeBlocks();
    initCopyLinkButton();
});

/**
 * 1. Reading Progress Bar
 */
function initReadingProgress() {
    const progressBar = document.getElementById('readingProgressBar');
    const postBody = document.getElementById('post-body');
    
    if (!progressBar || !postBody) return;

    window.addEventListener('scroll', () => {
        const postTop = postBody.offsetTop;
        const postHeight = postBody.clientHeight;
        const windowHeight = window.innerHeight;
        const scrollY = window.scrollY;

        if (scrollY < postTop - windowHeight / 2) {
            progressBar.style.width = '0%';
            return;
        }

        const scrollDistance = scrollY - postTop + (windowHeight / 2);
        let progress = (scrollDistance / postHeight) * 100;
        
        progress = Math.max(0, Math.min(100, progress));
        progressBar.style.width = `${progress}%`;
    });
}

/**
 * 2. Table of Contents & ScrollSpy
 */
function initTableOfContents() {
    const postBody = document.getElementById('post-body');
    const tocContainer = document.getElementById('tocContainer');
    const tocList = document.getElementById('tocList');
    
    if (!postBody || !tocContainer || !tocList) return;

    // Find all h2 and h3 elements
    const headings = postBody.querySelectorAll('h2, h3');
    if (headings.length === 0) return;

    // Show the TOC container
    tocContainer.style.display = 'block';

    const tocLinks = [];

    // Generate TOC
    headings.forEach((heading, index) => {
        // Ensure heading has an ID
        if (!heading.id) {
            heading.id = heading.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
        }
        // Fallback if ID is empty
        if (!heading.id) {
            heading.id = `heading-${index}`;
        }

        const li = document.createElement('li');
        // Add left padding for h3 to show hierarchy
        if (heading.tagName.toLowerCase() === 'h3') {
            li.style.paddingLeft = '1rem';
        }

        const a = document.createElement('a');
        a.href = `#${heading.id}`;
        a.textContent = heading.textContent;
        a.className = 'toc-link';
        
        li.appendChild(a);
        tocList.appendChild(li);
        tocLinks.push({ link: a, section: heading });

        // Smooth scroll on click
        a.addEventListener('click', (e) => {
            e.preventDefault();
            const yOffset = -140; // Offset for sticky navbar
            const y = heading.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: 'smooth' });
        });
    });

    // ScrollSpy logic using Intersection Observer
    const observerOptions = {
        root: null,
        rootMargin: '-140px 0px -60% 0px',
        threshold: 0
    };

    let activeLink = null;

    const observer = new IntersectionObserver((entries) => {
        // Find the first intersecting heading
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                
                // Remove active class from all
                tocLinks.forEach(item => item.link.classList.remove('active'));
                
                // Add active class to current
                const current = tocLinks.find(item => item.section.id === id);
                if (current) {
                    current.link.classList.add('active');
                    activeLink = current.link;
                }
            }
        });
    }, observerOptions);

    headings.forEach(h => observer.observe(h));
}

/**
 * 3. Code Blocks (Mac window controls + Copy)
 */
function initCodeBlocks() {
    const preElements = document.querySelectorAll('.article-body pre');
    
    preElements.forEach(pre => {
        // 1. Inject Mac Window Controls
        const header = document.createElement('div');
        header.className = 'code-window-header';
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'code-window-dot';
            header.appendChild(dot);
        }
        pre.insertBefore(header, pre.firstChild);

        // 2. Inject Copy Button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'code-copy-btn';
        copyBtn.textContent = 'Copy';
        copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
        pre.appendChild(copyBtn);

        copyBtn.addEventListener('click', async () => {
            const code = pre.querySelector('code');
            if (!code) return;

            try {
                await navigator.clipboard.writeText(code.innerText || code.textContent);
                copyBtn.textContent = 'Copied!';
                copyBtn.classList.add('copied');
                
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                    copyBtn.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
                copyBtn.textContent = 'Failed';
                setTimeout(() => {
                    copyBtn.textContent = 'Copy';
                }, 2000);
            }
        });
    });
}

/**
 * 4. Share Buttons (Auto-Copy to Clipboard)
 */
function initCopyLinkButton() {
    const shareBtns = document.querySelectorAll('.share-btn');
    if (!shareBtns.length) return;

    shareBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            // Let the default action (opening new tab) proceed, but also copy link
            const url = window.location.href;
            const titleElement = document.querySelector('.article-title');
            const blogTitle = titleElement ? titleElement.innerText.trim() : document.title;
            const copyText = `Check out the Blog ${blogTitle} on ${url}`;
            
            try {
                await navigator.clipboard.writeText(copyText);
                
                // Visual feedback
                const originalColor = btn.style.color;
                btn.style.color = '#4CAF50'; // green feedback
                
                setTimeout(() => {
                    btn.style.color = originalColor;
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text', err);
            }
        });
    });
}
