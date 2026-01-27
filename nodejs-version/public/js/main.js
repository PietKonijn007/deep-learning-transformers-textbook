// Deep Learning and Transformers Textbook - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy button to code blocks
    document.querySelectorAll('pre code').forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = 'Copy';
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent).then(() => {
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            });
        });
        block.parentElement.style.position = 'relative';
        block.parentElement.appendChild(button);
    });

    // Add equation numbering
    let equationNumber = 1;
    document.querySelectorAll('.equation').forEach(eq => {
        if (!eq.querySelector('.equation-number')) {
            const number = document.createElement('span');
            number.className = 'equation-number';
            number.textContent = `(${equationNumber})`;
            eq.appendChild(number);
            equationNumber++;
        }
    });

    // Highlight current section in navigation
    const sections = document.querySelectorAll('h2, h3');
    const navLinks = document.querySelectorAll('nav a');

    function highlightNavigation() {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= sectionTop - 100) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', highlightNavigation);

    // Add dark mode toggle (optional)
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });

        // Load dark mode preference
        if (localStorage.getItem('darkMode') === 'true') {
            document.body.classList.add('dark-mode');
        }
    }

    // Add table of contents generator
    function generateTOC() {
        const toc = document.getElementById('table-of-contents');
        if (!toc) return;

        const headings = document.querySelectorAll('h2, h3');
        const tocList = document.createElement('ul');

        headings.forEach((heading, index) => {
            if (!heading.id) {
                heading.id = `section-${index}`;
            }

            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = `#${heading.id}`;
            a.textContent = heading.textContent;
            
            if (heading.tagName === 'H3') {
                li.style.marginLeft = '1.5em';
            }

            li.appendChild(a);
            tocList.appendChild(li);
        });

        toc.appendChild(tocList);
    }

    generateTOC();

    // MathJax configuration
    window.MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\(', '\\)']],
            displayMath: [['$$', '$$'], ['\\[', '\\]']],
            processEscapes: true,
            processEnvironments: true,
            tags: 'ams',
            macros: {
                R: '{\\mathbb{R}}',
                N: '{\\mathbb{N}}',
                Z: '{\\mathbb{Z}}',
                C: '{\\mathbb{C}}',
                vx: '{\\mathbf{x}}',
                vy: '{\\mathbf{y}}',
                vz: '{\\mathbf{z}}',
                vh: '{\\mathbf{h}}',
                vw: '{\\mathbf{w}}',
                vb: '{\\mathbf{b}}',
                vq: '{\\mathbf{q}}',
                vk: '{\\mathbf{k}}',
                vv: '{\\mathbf{v}}',
                mA: '{\\mathbf{A}}',
                mB: '{\\mathbf{B}}',
                mC: '{\\mathbf{C}}',
                mW: '{\\mathbf{W}}',
                mX: '{\\mathbf{X}}',
                mY: '{\\mathbf{Y}}',
                mQ: '{\\mathbf{Q}}',
                mK: '{\\mathbf{K}}',
                mV: '{\\mathbf{V}}',
                mH: '{\\mathbf{H}}',
                mI: '{\\mathbf{I}}',
                mU: '{\\mathbf{U}}',
                mM: '{\\mathbf{M}}',
                transpose: '{^\\top}',
                norm: ['\\left\\|#1\\right\\|', 1],
                abs: ['\\left|#1\\right|', 1]
            }
        },
        svg: {
            fontCache: 'global'
        },
        options: {
            skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
        }
    };

    console.log('Deep Learning Textbook HTML initialized');
});
