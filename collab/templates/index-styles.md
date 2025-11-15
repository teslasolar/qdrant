# Index Page Styles Template

CSS styles for the main index page with starfield background and card layout.

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
    color: #00ff88;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}

.stars {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.star {
    position: absolute;
    background: #fff;
    border-radius: 50%;
    animation: twinkle 3s infinite;
}

@keyframes twinkle {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 1; }
}

.container {
    position: relative;
    z-index: 1;
    text-align: center;
    max-width: 1000px;
    padding: 40px;
}

h1 {
    font-size: 3em;
    margin-bottom: 10px;
    text-shadow: 0 0 20px #00ff88;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88; }
    to { text-shadow: 0 0 20px #00ff88, 0 0 40px #00ff88, 0 0 60px #00ff88; }
}
```

## Tokens
~195 tokens
