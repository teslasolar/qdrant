# Markdown File Modularization Guide

Complete guide to breaking down large markdown files into < 250 token modules.

## Problem: Large Files

```markdown
# MyProgram.md (800 tokens)
- Header (40 tokens)
- Full class with 15 methods (650 tokens)
- Features list (50 tokens)
- Usage examples (60 tokens)
```

**Issues:**
- Exceeds 250 token limit
- Hard to reuse individual methods
- Poor caching
- Difficult to maintain

## Solution: Modular Architecture

### Step 1: Identify Logical Groups

Break class into method groups:
- **Core** - Constructor, init, basic setup
- **Stats** - Statistical calculations
- **Normalize** - Normalization methods
- **Features** - Feature extraction
- **Utils** - Utility/helper methods

### Step 2: Create Module Files

```
modules/
├── myprogram-core.md (45 tokens)
├── myprogram-stats.md (180 tokens)
├── myprogram-normalize.md (240 tokens)
├── myprogram-features.md (220 tokens)
├── myprogram-utils.md (150 tokens)
└── myprogram-usage.md (60 tokens)
```

### Step 3: Use Templates for Headers

Instead of repeating header structure, use templates:

```markdown
<!-- OLD WAY (repeated in every file): -->
# Program Name - Jython 2.7
**Purpose**: Does stuff
**Runtime**: Jython 2.7
**Company**: Company Name

<!-- NEW WAY (use template): -->
{{jython-header:
  title: "Program Name",
  purpose: "Does stuff"
}}
```

### Step 4: Assembly Pattern

```javascript
// Load modules dynamically
const modules = [
    'myprogram-core',
    'myprogram-stats',
    'myprogram-normalize'
];

const code = await ModuleLoader.loadAll(modules);
// All methods now available
```

## Token Savings Calculation

### Before Modularization:
```
myprogram.md: 800 tokens (OVER LIMIT)
- Can't use efficiently
- Single point of failure
- Hard to update
```

### After Modularization:
```
myprogram-core.md: 45 tokens ✅
myprogram-stats.md: 180 tokens ✅
myprogram-normalize.md: 240 tokens ✅
myprogram-features.md: 220 tokens ✅
myprogram-utils.md: 150 tokens ✅
myprogram-usage.md: 60 tokens ✅

Total: 895 tokens across 6 files
Average per file: 149 tokens ✅
All under 250 token limit ✅
```

**Benefits:**
- ✅ All files under 250 tokens
- ✅ Load only what you need
- ✅ Better caching
- ✅ Easier to maintain
- ✅ Reusable components

## Common Patterns

### Pattern 1: Class Method Groups

```python
# Original (600 tokens)
class BigClass:
    def __init__(self): pass
    def method1(self): pass
    # ... 15 more methods

# Modular (6 files × 100 tokens)
# bigclass-core.md
class BigClass:
    def __init__(self): pass

# bigclass-group1.md
class BigClass:
    def method1(self): pass
    def method2(self): pass

# bigclass-group2.md
class BigClass:
    def method3(self): pass
    def method4(self): pass
```

### Pattern 2: Configuration Data

```yaml
# Instead of embedding in code
# Create separate config modules

# myprogram-config.md
features:
  - "Feature 1"
  - "Feature 2"
  - "Feature 3"

operations:
  - "Operation 1"
  - "Operation 2"
```

### Pattern 3: Examples Separation

```markdown
# myprogram.md - Just the code (200 tokens)
# myprogram-examples.md - Usage examples (80 tokens)
# myprogram-readme.md - Documentation (120 tokens)
```

## Template Variables Strategy

### Instead of Repeating Text:

```markdown
<!-- BAD: Repeated 10 times across files -->
**Purpose**: Data processing
**Runtime**: Jython 2.7
**Company**: Konomi Systems

<!-- GOOD: Use template -->
{{header: "data-processor", type: "jython"}}
```

### Template Expansion:

```javascript
const templates = {
    jython_header: {
        runtime: "Jython 2.7",
        company: "Konomi Systems"
    }
};

function expandTemplate(template, vars) {
    return Object.assign({}, templates[template.type], vars);
}
```

## Best Practices

1. **One Responsibility Per Module**
   - Each file should have a single, clear purpose
   - Example: `normalize.md` only for normalization

2. **Use Descriptive Names**
   - `dataprocessor-normalize.md` not `dp-n.md`
   - Makes assembly clear

3. **Keep Dependencies Explicit**
   - List required modules in header
   - Example: "Requires: dataprocessor-stats.md"

4. **Document Token Counts**
   - Add `## Tokens: ~180` to each file
   - Track against 250 limit

5. **Test Independently**
   - Each module should be testable alone
   - Use mocks for dependencies

## Assembly Strategies

### Strategy 1: Lazy Loading
```javascript
// Load only when needed
async function getFeatures(data) {
    if (!window.DataProcessorFeatures) {
        await ModuleLoader.load('dataprocessor-features');
    }
    return DataProcessorFeatures.extractFeatures(data);
}
```

### Strategy 2: Bundle Loading
```javascript
// Load related modules together
const dataProcessingBundle = [
    'dataprocessor-core',
    'dataprocessor-stats',
    'dataprocessor-normalize'
];

await ModuleLoader.loadAll(dataProcessingBundle);
```

### Strategy 3: On-Demand Assembly
```javascript
// Assemble full class only when needed
async function assembleDataProcessor() {
    const modules = [
        'dataprocessor-core',
        'dataprocessor-stats',
        'dataprocessor-normalize',
        'dataprocessor-features',
        'dataprocessor-utils'
    ];

    return await ModuleLoader.loadAll(modules);
}
```

## Migration Checklist

- [ ] Identify large files (> 250 tokens)
- [ ] Group methods by functionality
- [ ] Create module files
- [ ] Extract headers to templates
- [ ] Test each module independently
- [ ] Update loader to use new modules
- [ ] Document dependencies
- [ ] Verify token counts
- [ ] Test assembly pattern
- [ ] Update documentation

## Token Counting

```bash
# Count tokens in a file (rough estimate)
# 1 token ≈ 4 characters for code
# 1 token ≈ 0.75 words for English

wc -w file.md  # Word count
# Divide by 0.75 for token estimate
```

## Example: DataProcessor Breakdown

**Original File:**
- Single file: ~800 tokens ❌

**Modular Files:**
- `dataprocessor-core.md`: 45 tokens ✅
- `dataprocessor-stats.md`: 180 tokens ✅
- `dataprocessor-normalize.md`: 240 tokens ✅
- `dataprocessor-outliers.md`: 190 tokens ✅
- `dataprocessor-smooth.md`: 120 tokens ✅
- `dataprocessor-features.md`: 220 tokens ✅
- `dataprocessor-utils.md`: 150 tokens ✅

**Total: 1,145 tokens across 7 files (avg 163 tokens/file)** ✅

**Savings:** Can now load only what you need instead of all 800 tokens!

## Tokens
~245 tokens
