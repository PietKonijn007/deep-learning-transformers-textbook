// Application State
const state = {
    chapters: [],
    currentChapterIndex: -1,
    searchTerm: ''
};

// DOM Elements
const elements = {
    sidebar: document.getElementById('sidebar'),
    sidebarToggle: document.getElementById('sidebar-toggle'),
    mobileMenuBtn: document.getElementById('mobile-menu-btn'),
    chapterList: document.getElementById('chapter-list'),
    chapterContent: document.getElementById('chapter-content'),
    searchInput: document.getElementById('search'),
    prevBtn: document.getElementById('prev-chapter'),
    nextBtn: document.getElementById('next-chapter'),
    themeToggle: document.getElementById('theme-toggle'),
    loadingBar: document.getElementById('loading-bar'),
    tocToggle: document.getElementById('toc-toggle'),
    chapterToc: document.getElementById('chapter-toc'),
    tocClose: document.getElementById('toc-close'),
    tocContent: document.getElementById('toc-content')
};

// Show/hide loading bar
function showLoading() {
    elements.loadingBar.style.width = '70%';
    elements.loadingBar.classList.add('active');
}

function hideLoading() {
    elements.loadingBar.style.width = '100%';
    setTimeout(() => {
        elements.loadingBar.classList.remove('active');
        elements.loadingBar.style.width = '0';
    }, 300);
}

// Initialize App
async function init() {
    await loadChapters();
    setupEventListeners();
    initTheme();
    loadChapterFromURL();
}

// Initialize theme
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

// Toggle theme
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

// Update theme icon
function updateThemeIcon(theme) {
    elements.themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Toggle TOC
function toggleToc() {
    elements.chapterToc.classList.toggle('hidden');
}

// Generate chapter TOC
function generateChapterToc() {
    const headings = elements.chapterContent.querySelectorAll('h2, h3');
    
    if (headings.length === 0) {
        elements.tocContent.innerHTML = '<p style="color: #666;">No sections found</p>';
        return;
    }
    
    let tocHtml = '';
    headings.forEach((heading, index) => {
        const id = `heading-${index}`;
        heading.id = id;
        
        const level = heading.tagName.toLowerCase();
        const text = heading.textContent;
        
        tocHtml += `<a href="#${id}" class="toc-${level}" data-id="${id}">${text}</a>`;
    });
    
    elements.tocContent.innerHTML = tocHtml;
    
    // Add click handlers
    elements.tocContent.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.dataset.id;
            const target = document.getElementById(targetId);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                elements.chapterToc.classList.add('hidden');
            }
        });
    });
}

// Load chapters from API
async function loadChapters() {
    try {
        console.log('=== LOADING CHAPTERS ===');
        console.log('Chapter list element:', elements.chapterList);
        
        // Static chapter list - no API needed
        state.chapters = [
            { id: 'preface', title: 'Preface', part: 'Front Matter' },
            { id: 'chapter01_linear_algebra', title: 'Chapter 1: Linear Algebra Essentials', part: 'Part I: Foundations for Leaders' },
            { id: 'chapter02_calculus_optimization', title: 'Chapter 2: Calculus and Optimization', part: 'Part I: Foundations for Leaders' },
            { id: 'chapter03_attention_fundamentals', title: 'Chapter 3: Attention Fundamentals', part: 'Part I: Foundations for Leaders' },
            { id: 'bridge_I_to_II', title: 'Bridge: From Foundations to Architecture', part: 'Part I: Foundations for Leaders' },
            { id: 'chapter04_training_transformers', title: 'Chapter 4: Training Transformers', part: 'Part II: Architecture & Infrastructure' },
            { id: 'chapter05_production_deployment', title: 'Chapter 5: Production Deployment', part: 'Part II: Architecture & Infrastructure' },
            { id: 'chapter06_advanced_techniques', title: 'Chapter 6: Advanced Techniques', part: 'Part II: Architecture & Infrastructure' },
            { id: 'bridge_II_to_III', title: 'Bridge: From Architecture to Production', part: 'Part II: Architecture & Infrastructure' },
            { id: 'chapter07_hardware_infrastructure', title: 'Chapter 7: Hardware Infrastructure', part: 'Part III: Production Layer' },
            { id: 'chapter08_data_pipeline', title: 'Chapter 8: Data Pipeline', part: 'Part III: Production Layer' },
            { id: 'chapter09_operationalization', title: 'Chapter 9: Operationalization', part: 'Part III: Production Layer' },
            { id: 'bridge_III_to_IV', title: 'Bridge: From Production to Applications', part: 'Part III: Production Layer' },
            { id: 'chapter10_enterprise_nlp', title: 'Chapter 10: Enterprise NLP', part: 'Part IV: Industry Applications' },
            { id: 'chapter11_code_tools', title: 'Chapter 11: Code and Development Tools', part: 'Part IV: Industry Applications' },
            { id: 'chapter12_healthcare', title: 'Chapter 12: Healthcare Applications', part: 'Part IV: Industry Applications' },
            { id: 'chapter13_legal', title: 'Chapter 13: Legal and Compliance', part: 'Part IV: Industry Applications' },
            { id: 'chapter14_finance', title: 'Chapter 14: Financial Applications', part: 'Part IV: Industry Applications' },
            { id: 'chapter15_autonomous_systems', title: 'Chapter 15: Autonomous Systems', part: 'Part IV: Industry Applications' },
            { id: 'chapter16_synthesis', title: 'Chapter 16: Strategic Synthesis', part: 'Part V: Strategic Synthesis' },
            { id: 'chapter17_frontiers', title: 'Chapter 17: Future Frontiers', part: 'Part V: Strategic Synthesis' }
        ];
        console.log('Chapters loaded:', state.chapters.length);
        console.log('Calling renderChapterList...');
        renderChapterList();
        console.log('renderChapterList completed');
    } catch (error) {
        console.error('Failed to load chapters:', error);
        elements.chapterList.innerHTML = '<div class="loading">Failed to load chapters</div>';
    }
}

// Render chapter list in sidebar
function renderChapterList() {
    const groupedChapters = groupChaptersByPart(state.chapters);
    
    console.log('=== RENDER DEBUG ===');
    console.log('Total chapters:', state.chapters.length);
    console.log('Grouped chapters:', Object.keys(groupedChapters));
    Object.entries(groupedChapters).forEach(([part, chapters]) => {
        console.log(`${part}: ${chapters.length} chapters`);
    });
    
    let html = '';
    for (const [part, chapters] of Object.entries(groupedChapters)) {
        html += `
            <div class="chapter-group">
                <div class="part-title">${part}</div>
                ${chapters.map((chapter, index) => `
                    <div class="chapter-item" data-id="${chapter.id}" data-index="${state.chapters.indexOf(chapter)}">
                        ${chapter.title}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    elements.chapterList.innerHTML = html;
    console.log('HTML length:', html.length);
    console.log('Chapter items rendered:', elements.chapterList.querySelectorAll('.chapter-item').length);
}

// Group chapters by part
function groupChaptersByPart(chapters) {
    const grouped = {};
    chapters.forEach(chapter => {
        if (!grouped[chapter.part]) {
            grouped[chapter.part] = [];
        }
        grouped[chapter.part].push(chapter);
    });
    
    console.log('Grouping result:');
    Object.entries(grouped).forEach(([part, chaps]) => {
        console.log(`  ${part}: ${chaps.map(c => c.id).join(', ')}`);
    });
    
    return grouped;
}

// Setup event listeners
function setupEventListeners() {
    // Chapter selection
    elements.chapterList.addEventListener('click', (e) => {
        const chapterItem = e.target.closest('.chapter-item');
        if (chapterItem) {
            const chapterId = chapterItem.dataset.id;
            const index = parseInt(chapterItem.dataset.index);
            loadChapter(chapterId, index);
            
            // Close sidebar on mobile
            if (window.innerWidth <= 768) {
                elements.sidebar.classList.remove('open');
            }
        }
    });

    // Search functionality
    elements.searchInput.addEventListener('input', (e) => {
        state.searchTerm = e.target.value.toLowerCase();
        filterChapters();
    });

    // Navigation buttons
    elements.prevBtn.addEventListener('click', () => navigateChapter(-1));
    elements.nextBtn.addEventListener('click', () => navigateChapter(1));

    // Sidebar toggle for mobile
    if (elements.sidebarToggle) {
        elements.sidebarToggle.addEventListener('click', () => {
            elements.sidebar.classList.toggle('open');
        });
    }
    
    // Mobile menu button
    if (elements.mobileMenuBtn) {
        elements.mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            elements.sidebar.classList.toggle('open');
            console.log('Mobile menu clicked, sidebar open:', elements.sidebar.classList.contains('open'));
        });
    } else {
        console.error('Mobile menu button not found!');
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            elements.sidebar.classList.contains('open') &&
            !elements.sidebar.contains(e.target) &&
            !elements.sidebarToggle.contains(e.target) &&
            !elements.mobileMenuBtn.contains(e.target)) {
            elements.sidebar.classList.remove('open');
        }
    });

    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);

    // TOC toggle
    elements.tocToggle.addEventListener('click', toggleToc);
    elements.tocClose.addEventListener('click', () => {
        elements.chapterToc.classList.add('hidden');
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft' && !elements.prevBtn.disabled) {
            navigateChapter(-1);
        } else if (e.key === 'ArrowRight' && !elements.nextBtn.disabled) {
            navigateChapter(1);
        }
    });

    // Handle browser back/forward
    window.addEventListener('popstate', () => {
        loadChapterFromURL();
    });
}

// Filter chapters based on search
function filterChapters() {
    const items = elements.chapterList.querySelectorAll('.chapter-item');
    items.forEach(item => {
        const title = item.textContent.toLowerCase();
        if (title.includes(state.searchTerm)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
}

// Load chapter content
async function loadChapter(chapterId, index) {
    try {
        // Show loading state
        showLoading();
        elements.chapterContent.innerHTML = '<div class="loading">Loading chapter...</div>';
        
        // Fetch chapter content with cache-busting parameter
        const cacheBuster = Date.now();
        const response = await fetch(`/chapters/leadership/${chapterId}.html?v=${cacheBuster}`);
        if (!response.ok) throw new Error('Chapter not found');
        
        const html = await response.text();
        
        // Extract content from HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const mainContent = doc.querySelector('main') || doc.body;
        
        // Fix relative image paths - convert ../diagrams/ to /chapters/diagrams/
        const images = mainContent.querySelectorAll('img[src^="../diagrams/"]');
        images.forEach(img => {
            const oldSrc = img.getAttribute('src');
            const newSrc = oldSrc.replace('../diagrams/', '/chapters/diagrams/');
            img.setAttribute('src', newSrc);
        });
        
        // Update content
        elements.chapterContent.innerHTML = mainContent.innerHTML;
        
        // Update state
        state.currentChapterIndex = index;
        
        // Update URL
        history.pushState({ chapterId, index }, '', `#${chapterId}`);
        
        // Update active chapter in sidebar
        updateActiveChapter(chapterId);
        
        // Update navigation buttons
        updateNavigationButtons();
        
        // Scroll to top
        elements.chapterContent.parentElement.scrollTop = 0;
        
        // Generate chapter TOC
        generateChapterToc();
        
        // Wait a bit for DOM to settle, then render math
        setTimeout(() => {
            if (window.MathJax && window.MathJax.typesetPromise) {
                console.log('Calling MathJax.typesetPromise...');
                window.MathJax.typesetPromise([elements.chapterContent]).then(() => {
                    console.log('MathJax rendering complete');
                    hideLoading();
                }).catch(err => {
                    console.error('MathJax error:', err);
                    hideLoading();
                });
            } else {
                console.warn('MathJax not ready yet, waiting...');
                // If MathJax isn't ready, wait longer and try again
                setTimeout(() => {
                    if (window.MathJax && window.MathJax.typesetPromise) {
                        console.log('MathJax now ready, rendering...');
                        window.MathJax.typesetPromise([elements.chapterContent]).then(() => {
                            console.log('MathJax rendering complete (delayed)');
                            hideLoading();
                        }).catch(err => {
                            console.error('MathJax error (delayed):', err);
                            hideLoading();
                        });
                    } else {
                        console.error('MathJax still not available after waiting');
                        hideLoading();
                    }
                }, 2000);
            }
        }, 100);
        
    } catch (error) {
        console.error('Failed to load chapter:', error);
        elements.chapterContent.innerHTML = '<div class="loading">Failed to load chapter</div>';
        hideLoading();
    }
}

// Update active chapter highlight
function updateActiveChapter(chapterId) {
    const items = elements.chapterList.querySelectorAll('.chapter-item');
    items.forEach(item => {
        if (item.dataset.id === chapterId) {
            item.classList.add('active');
            // Scroll into view if needed
            item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        } else {
            item.classList.remove('active');
        }
    });
}

// Update navigation buttons
function updateNavigationButtons() {
    elements.prevBtn.disabled = state.currentChapterIndex <= 0;
    elements.nextBtn.disabled = state.currentChapterIndex >= state.chapters.length - 1;
}

// Navigate to previous/next chapter
function navigateChapter(direction) {
    const newIndex = state.currentChapterIndex + direction;
    if (newIndex >= 0 && newIndex < state.chapters.length) {
        const chapter = state.chapters[newIndex];
        loadChapter(chapter.id, newIndex);
    }
}

// Load chapter from URL hash
function loadChapterFromURL() {
    const hash = window.location.hash.slice(1);
    if (hash) {
        const index = state.chapters.findIndex(ch => ch.id === hash);
        if (index !== -1) {
            loadChapter(hash, index);
        }
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Expose loadChapter globally for onclick handlers
window.navigateToChapter = function(chapterId) {
    const index = state.chapters.findIndex(ch => ch.id === chapterId);
    if (index !== -1) {
        loadChapter(chapterId, index);
    }
};
