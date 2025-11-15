# Features List Template

Template for feature/capability lists in markdown.

## Template Variables

```yaml
features:
  - name: "Feature Name"
    description: "Feature description"
  - name: "Another Feature"
    description: "Another description"
```

## Template Output

```markdown
## Features

- **{name}** - {description}
- **{name}** - {description}
```

## JavaScript Renderer

```javascript
function renderFeaturesList(features) {
    const items = features.map(f =>
        `- **${f.name}** - ${f.description}`
    ).join('\n');

    return `## Features\n\n${items}`;
}

// Export to window
window.renderFeaturesList = renderFeaturesList;
```

## Tokens
~8 tokens per feature + 3 header = variable
