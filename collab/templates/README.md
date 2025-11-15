# HTML Component Templates

This directory contains markdown templates that break down HTML pages into reusable components with code blocks.

## Template Structure

Each template is a markdown file containing:
- **Code blocks** with CSS, HTML, or JavaScript
- **Configuration parameters** in YAML format
- **Token counts** for reference (all < 250 tokens)

## Available Templates

### Styling
- `index-styles.md` - Main page styles with starfield background (~195 tokens)
- `index-cards.md` - Project cards with hover effects (~210 tokens)
- `color-scheme.md` - Color theme configuration (~180 tokens)

### Navigation
- `dashboard-navigation.md` - Top nav bar with tab switching (~220 tokens)
- `quick-command.md` - Ctrl+K command overlay (~245 tokens)

### JavaScript Modules
- `module-loader.md` - Markdown-to-JS module loader (~245 tokens)
- `starfield-generator.md` - Animated stars background (~140 tokens)

### Configuration
- `page-config.md` - Page parameters and content config (~245 tokens)

## Usage

1. **Include in HTML**: Extract code blocks from markdown
2. **Customize parameters**: Edit YAML configs in markdown
3. **Mix and match**: Combine templates to build pages
4. **Stay modular**: Each file < 250 tokens for easy AI processing

## Example

```javascript
// Load a markdown template
const response = await fetch('/collab/templates/module-loader.md');
const markdown = await response.text();

// Extract JavaScript code blocks
const jsCode = extractCodeBlocks(markdown, 'javascript');

// Use it!
eval(jsCode);
```

## Philosophy

All templates follow the Chazon OS philosophy:
- **< 250 tokens per file** for optimal AI context
- **Markdown-first** - code lives in markdown blocks
- **Composable** - mix templates to build features
- **Self-documenting** - code and docs together
