# Index Page Cards Styles

CSS for project cards with hover effects and badges.

```css
.projects {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 30px;
    margin-top: 40px;
}

.card {
    background: rgba(0, 0, 0, 0.7);
    border: 2px solid #00ff88;
    border-radius: 15px;
    padding: 30px;
    transition: all 0.3s;
    cursor: pointer;
    text-decoration: none;
    color: inherit;
    display: block;
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 10px 40px rgba(0, 255, 136, 0.3);
    border-color: #00ffff;
}

.card h2 {
    font-size: 2em;
    margin-bottom: 15px;
    color: #00ff88;
}

.badge {
    display: inline-block;
    background: #00ff88;
    color: #000;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8em;
    margin-top: 15px;
    font-weight: bold;
}

.badge.new {
    background: linear-gradient(45deg, #ff00ff, #00ffff);
    animation: rainbow 3s linear infinite;
}

@keyframes rainbow {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}
```

## Tokens
~210 tokens
