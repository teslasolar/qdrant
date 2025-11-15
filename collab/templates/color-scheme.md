# Color Scheme Configuration

Theme colors used across all pages.

## Primary Colors

```yaml
colors:
  background: "#0a0a0a"
  background_gradient: "linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%)"
  primary: "#00ff88"
  secondary: "#00ccff"
  accent: "#ffd700"
  text: "#00ff88"
  text_secondary: "#cccccc"
  text_dim: "#888888"
  border: "#00ff88"
  border_dim: "#333333"
```

## CSS Variables

```css
:root {
    --color-bg: #0a0a0a;
    --color-bg-gradient: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
    --color-primary: #00ff88;
    --color-secondary: #00ccff;
    --color-accent: #ffd700;
    --color-text: #00ff88;
    --color-text-secondary: #cccccc;
    --color-text-dim: #888888;
    --color-border: #00ff88;
    --color-border-dim: #333333;
}

body {
    background: var(--color-bg-gradient);
    color: var(--color-text);
}

h1 {
    color: var(--color-primary);
    text-shadow: 0 0 20px var(--color-primary);
}

a {
    color: var(--color-secondary);
}

.badge {
    background: var(--color-primary);
    color: var(--color-bg);
}

.phi {
    color: var(--color-accent);
}
```

## Tokens
~180 tokens
