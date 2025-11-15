# Method Group Template

Template for breaking down large classes into method groups.

## Concept

Instead of one massive class file, split into method groups:
- `classname-core.md` - Constructor and core methods
- `classname-normalize.md` - Normalization methods
- `classname-stats.md` - Statistical calculations
- `classname-features.md` - Feature extraction
- `classname-utils.md` - Utility methods

Each file < 250 tokens.

## Template Structure

```markdown
# {ClassName} - {GroupName} Methods

Part of {ClassName} class - {group_description}

\`\`\`python
class {ClassName}:
    # ... (constructor in core file)

    {methods}
\`\`\`
```

## Assembly Pattern

```javascript
async function assembleClass(className, groups) {
    const parts = [];

    // Load constructor from core
    const core = await fetch(`./modules/${className}-core.md`);
    parts.push(await extractCode(core));

    // Load method groups
    for (const group of groups) {
        const mod = await fetch(`./modules/${className}-${group}.md`);
        parts.push(await extractCode(mod));
    }

    // Combine into full class
    return parts.join('\n\n');
}
```

## Token Savings

- Original class: 600+ tokens
- Split into 5 modules: ~120 tokens each
- Can load only what you need
- Better caching and reusability

## Tokens
~35 tokens (template only)
