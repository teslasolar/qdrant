# Starfield Generator

JavaScript to generate animated stars in the background.

```javascript
function generateStarfield(containerId, starCount = 100) {
    const starsContainer = document.getElementById(containerId);

    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.width = Math.random() * 3 + 'px';
        star.style.height = star.style.width;
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        starsContainer.appendChild(star);
    }
}

// Auto-generate on page load
window.addEventListener('DOMContentLoaded', () => {
    generateStarfield('stars', 100);
});
```

## Config Parameters

```yaml
starCount: 100
minSize: 0px
maxSize: 3px
animationDuration: 3s
```

## Tokens
~140 tokens
