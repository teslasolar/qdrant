# Jython Program Header Template

Template for Jython 2.7 program file headers.

## Template Variables

```yaml
title: "Program Title"
purpose: "What this program does"
runtime: "Jython 2.7"
company: "Konomi Systems"
dependencies: "Java packages used"
```

## Template Output

```markdown
# {title} - Jython 2.7

**Purpose**: {purpose}
**Runtime**: {runtime}
**Company**: {company}
**Dependencies**: {dependencies}

## Description

{description}
```

## Usage

```javascript
function renderJythonHeader(vars) {
    return `# ${vars.title} - Jython 2.7

**Purpose**: ${vars.purpose}
**Runtime**: ${vars.runtime}
**Company**: ${vars.company}
**Dependencies**: ${vars.dependencies}

## Description

${vars.description}`;
}
```

## Tokens
~45 tokens (without description)
