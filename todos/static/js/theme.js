const themes = {
    dark: {
        name: 'Dark',
        icon: 'bi-moon-fill',
        metaColor: '#0d1117'
    },
    light: {
        name: 'Light',
        icon: 'bi-sun-fill',
        metaColor: '#f6f8fa'
    },
    nord: {
        name: 'Nord',
        icon: 'bi-snow',
        metaColor: '#2e3440'
    },
    solarized: {
        name: 'Solarized',
        icon: 'bi-brightness-high',
        metaColor: '#002b36'
    },
    forest: {
        name: 'Forest',
        icon: 'bi-tree',
        metaColor: '#2d3a2d'
    }
};

document.addEventListener('DOMContentLoaded', () => {
    const theme = localStorage.getItem('theme') || 'dark';
    applyTheme(theme);
    setupThemeSelector();
});

function setupThemeSelector() {
    const themeSelector = document.getElementById('theme-selector');
    if (!themeSelector) return;

    Object.keys(themes).forEach(themeKey => {
        const option = document.createElement('a');
        option.classList.add('dropdown-item', 'd-flex', 'align-items-center', 'gap-2');
        option.href = '#';
        option.innerHTML = `
            <i class="bi ${themes[themeKey].icon}"></i>
            ${themes[themeKey].name}
        `;
        option.onclick = (e) => {
            e.preventDefault();
            applyTheme(themeKey);
            localStorage.setItem('theme', themeKey);
        };
        themeSelector.appendChild(option);
    });
}

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update theme icon in navbar
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        // Remove all possible theme icons
        Object.values(themes).forEach(t => {
            themeIcon.classList.remove(t.icon);
        });
        themeIcon.classList.add(themes[theme].icon);
    }

    // Update meta theme color for mobile browsers
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
        metaThemeColor.setAttribute('content', themes[theme].metaColor);
    }

    // Add animation class
    document.body.classList.add('theme-transition');
    setTimeout(() => {
        document.body.classList.remove('theme-transition');
    }, 300);
}

// Add smooth transitions for theme changes
document.addEventListener('DOMContentLoaded', () => {
    const style = document.createElement('style');
    style.textContent = `
        * {
            transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
        }
    `;
    document.head.appendChild(style);
});
