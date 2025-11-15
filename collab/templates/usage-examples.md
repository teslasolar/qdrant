# Usage Examples Template

Template for code usage examples section.

## Template Variables

```yaml
examples:
  - title: "Example 1"
    code: "code snippet here"
    description: "What it does"
```

## Template Output

```markdown
## Usage Examples

### {title}

{description}

\`\`\`python
{code}
\`\`\`
```

## JavaScript Renderer

```javascript
function renderUsageExamples(examples, language = 'python') {
    const exampleBlocks = examples.map(ex => `### ${ex.title}

${ex.description}

\`\`\`${language}
${ex.code}
\`\`\``).join('\n\n');

    return `## Usage Examples\n\n${exampleBlocks}`;
}

window.renderUsageExamples = renderUsageExamples;
```

## Tokens
~25 tokens per example + 5 header
