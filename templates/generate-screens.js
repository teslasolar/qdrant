#!/usr/bin/env node

/**
 * HMI Screen Generator
 * Generates static HTML files from JSON templates
 *
 * Usage:
 *   node generate-screens.js [options]
 *
 * Options:
 *   --all              Generate all screens
 *   --uuid <uuid>      Generate specific screen by UUID
 *   --tag <tag>        Generate all screens with tag
 *   --output <dir>     Output directory (default: ./generated)
 */

const fs = require('fs').promises;
const path = require('path');

class ScreenGenerator {
  constructor(options = {}) {
    this.templatesDir = options.templatesDir || path.join(__dirname);
    this.outputDir = options.outputDir || path.join(__dirname, 'generated');
    this.screens = null;
    this.components = null;
    this.tags = null;
  }

  /**
   * Load template indexes
   */
  async loadIndexes() {
    const screensIndex = await this.loadJSON(path.join(this.templatesDir, 'screens/index.json'));
    const componentsIndex = await this.loadJSON(path.join(this.templatesDir, 'components/index.json'));
    const tagsIndex = await this.loadJSON(path.join(this.templatesDir, 'tags/index.json'));

    this.screens = screensIndex.screens;
    this.components = componentsIndex.components;
    this.tags = tagsIndex.tags;
  }

  /**
   * Load JSON file
   */
  async loadJSON(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      return JSON.parse(content);
    } catch (error) {
      console.error(`Error loading ${filePath}:`, error.message);
      throw error;
    }
  }

  /**
   * Generate all screens
   */
  async generateAll() {
    await this.loadIndexes();
    console.log(`Generating ${this.screens.length} screens...`);

    for (const screenMeta of this.screens) {
      await this.generateScreen(screenMeta.uuid);
    }

    console.log(`✓ All screens generated to ${this.outputDir}`);
  }

  /**
   * Generate screen by UUID
   */
  async generateScreen(uuid) {
    await this.loadIndexes();

    const screenMeta = this.screens.find(s => s.uuid === uuid);
    if (!screenMeta) {
      throw new Error(`Screen not found: ${uuid}`);
    }

    console.log(`Generating screen: ${screenMeta.name} (${uuid})`);

    // Load screen template
    const screenPath = path.join(this.templatesDir, screenMeta.path);
    const screenTemplate = await this.loadJSON(screenPath);

    // Generate HTML
    const html = await this.generateHTML(screenTemplate, screenMeta);

    // Write to file
    const outputPath = path.join(
      this.outputDir,
      screenMeta.category,
      `${this.sanitizeFilename(screenMeta.name)}.html`
    );

    await this.ensureDir(path.dirname(outputPath));
    await fs.writeFile(outputPath, html, 'utf8');

    console.log(`  ✓ Generated: ${outputPath}`);
    return outputPath;
  }

  /**
   * Generate screens by tag
   */
  async generateByTag(tag) {
    await this.loadIndexes();

    const matchingScreens = this.screens.filter(s =>
      s.tags && s.tags.includes(tag)
    );

    if (matchingScreens.length === 0) {
      console.log(`No screens found with tag: ${tag}`);
      return [];
    }

    console.log(`Generating ${matchingScreens.length} screens with tag: ${tag}`);

    const results = [];
    for (const screenMeta of matchingScreens) {
      const outputPath = await this.generateScreen(screenMeta.uuid);
      results.push(outputPath);
    }

    return results;
  }

  /**
   * Generate HTML from template
   */
  async generateHTML(screenTemplate, screenMeta) {
    const { metadata, layout, components, actions } = screenTemplate;

    // Build component HTML
    let componentsHTML = '';
    let componentScripts = '';
    let componentStyles = '';

    for (const comp of components) {
      const componentTemplate = await this.loadComponentTemplate(comp.uuid);
      const componentHTML = await this.renderComponent(comp, componentTemplate);
      componentsHTML += componentHTML.html;
      componentStyles += componentHTML.css;
      componentScripts += componentHTML.js;
    }

    // Generate full HTML document
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${metadata.name}</title>
<meta name="description" content="${metadata.description}">
<meta name="generator" content="HMI Screen Generator v1.0.0">
<meta name="template-uuid" content="${screenTemplate.uuid}">

<style>
/* Base Styles */
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Courier New', monospace;
  background: ${layout.theme === 'dark' ? '#0a0a0a' : '#ffffff'};
  color: ${layout.theme === 'dark' ? '#00ff88' : '#000000'};
  height: 100vh;
  overflow: hidden;
}

/* Screen Container */
#screen-container {
  display: grid;
  grid-template-columns: repeat(${layout.grid.columns}, 1fr);
  grid-template-rows: repeat(${layout.grid.rows}, 1fr);
  gap: ${layout.grid.gap}px;
  height: 100vh;
  padding: 20px;
}

/* Component Base Styles */
.component {
  background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
  border: 2px solid #00ff88;
  border-radius: 12px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

${componentStyles}
</style>
</head>
<body>

<!-- Header -->
<div style="position: fixed; top: 0; left: 0; right: 0; height: 60px; background: #1a1a2e; border-bottom: 3px solid #00ff88; display: flex; align-items: center; padding: 0 20px; z-index: 1000;">
  <h1 style="color: #00ff88; font-size: 1.5em;">${metadata.name}</h1>
  <div style="margin-left: auto; color: #00ccff;" id="current-time">00:00:00</div>
</div>

<!-- Screen Container -->
<div id="screen-container" style="margin-top: 60px; height: calc(100vh - 60px);">
  ${componentsHTML}
</div>

<!-- Template Loader -->
<script src="../template-loader.js"></script>

<!-- Screen Scripts -->
<script>
// Update time
function updateTime() {
  const now = new Date();
  document.getElementById('current-time').textContent = now.toLocaleTimeString();
}
setInterval(updateTime, 1000);
updateTime();

// Screen metadata
const screenMetadata = ${JSON.stringify(metadata, null, 2)};

// Component scripts
${componentScripts}

// Execute onLoad actions
${this.generateActionScripts(actions, 'onLoad')}

console.log('Screen loaded:', '${metadata.name}');
console.log('Template UUID:', '${screenTemplate.uuid}');
console.log('Generated:', new Date().toISOString());
</script>

</body>
</html>`;
  }

  /**
   * Load component template
   */
  async loadComponentTemplate(uuid) {
    const componentMeta = this.components.find(c => c.uuid === uuid);
    if (!componentMeta) {
      throw new Error(`Component not found: ${uuid}`);
    }

    const componentPath = path.join(this.templatesDir, componentMeta.path);
    return await this.loadJSON(componentPath);
  }

  /**
   * Render component
   */
  async renderComponent(componentData, componentTemplate) {
    const { position, config } = componentData;
    const { template } = componentTemplate;

    // Replace config placeholders in HTML
    let html = template.html;
    for (const [key, value] of Object.entries(config)) {
      html = html.replace(new RegExp(`{{${key}}}`, 'g'), value);
    }

    // Wrap in positioned div
    const wrappedHTML = `
<div class="component component-${componentTemplate.category}"
     style="grid-column: ${position.x + 1} / span ${position.width};
            grid-row: ${position.y + 1} / span ${position.height};">
  ${html}
</div>
`;

    return {
      html: wrappedHTML,
      css: template.css || '',
      js: template.js || ''
    };
  }

  /**
   * Generate action scripts
   */
  generateActionScripts(actions, trigger) {
    if (!actions) return '';

    const triggerActions = actions.filter(a => a.trigger === trigger);
    if (triggerActions.length === 0) return '';

    let script = `\n// ${trigger} actions\n`;
    for (const action of triggerActions) {
      switch (action.action) {
        case 'subscribeToTags':
          script += `// Subscribe to tags: ${action.params.tags.join(', ')}\n`;
          break;
        case 'navigate':
          script += `// Navigate to: ${action.params.target}\n`;
          break;
        case 'writeTag':
          script += `// Write tag: ${action.params.tagPath} = ${action.params.value}\n`;
          break;
      }
    }

    return script;
  }

  /**
   * Sanitize filename
   */
  sanitizeFilename(name) {
    return name.toLowerCase()
      .replace(/[^a-z0-9]/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
  }

  /**
   * Ensure directory exists
   */
  async ensureDir(dir) {
    try {
      await fs.mkdir(dir, { recursive: true });
    } catch (error) {
      // Ignore if already exists
    }
  }
}

// CLI Usage
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};

  // Parse arguments
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--output' && args[i + 1]) {
      options.outputDir = args[i + 1];
      i++;
    }
  }

  const generator = new ScreenGenerator(options);

  (async () => {
    try {
      if (args.includes('--all')) {
        await generator.generateAll();
      } else if (args.includes('--uuid')) {
        const uuidIndex = args.indexOf('--uuid') + 1;
        const uuid = args[uuidIndex];
        await generator.generateScreen(uuid);
      } else if (args.includes('--tag')) {
        const tagIndex = args.indexOf('--tag') + 1;
        const tag = args[tagIndex];
        await generator.generateByTag(tag);
      } else {
        console.log(`
HMI Screen Generator

Usage:
  node generate-screens.js [options]

Options:
  --all              Generate all screens
  --uuid <uuid>      Generate specific screen by UUID
  --tag <tag>        Generate all screens with tag
  --output <dir>     Output directory (default: ./generated)

Examples:
  node generate-screens.js --all
  node generate-screens.js --uuid 550e8400-e29b-41d4-a716-446655440000
  node generate-screens.js --tag overview
  node generate-screens.js --all --output ./build/screens
        `);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = ScreenGenerator;
