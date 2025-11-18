/**
 * Template Loader
 * Loads and renders HMI screens, components, and tags from JSON templates
 */

class TemplateLoader {
  constructor(basePath = '/templates') {
    this.basePath = basePath;
    this.cache = new Map();
    this.indexes = {
      screens: null,
      components: null,
      tags: null
    };
  }

  /**
   * Load and cache template indexes
   */
  async loadIndexes() {
    if (!this.indexes.screens) {
      this.indexes.screens = await this.fetchJSON(`${this.basePath}/screens/index.json`);
    }
    if (!this.indexes.components) {
      this.indexes.components = await this.fetchJSON(`${this.basePath}/components/index.json`);
    }
    if (!this.indexes.tags) {
      this.indexes.tags = await this.fetchJSON(`${this.basePath}/tags/index.json`);
    }
  }

  /**
   * Fetch JSON with caching
   */
  async fetchJSON(url) {
    if (this.cache.has(url)) {
      return this.cache.get(url);
    }

    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${url}: ${response.statusText}`);
    }

    const data = await response.json();
    this.cache.set(url, data);
    return data;
  }

  /**
   * Load screen by UUID
   */
  async loadScreenByUUID(uuid) {
    await this.loadIndexes();

    const screen = this.indexes.screens.screens.find(s => s.uuid === uuid);
    if (!screen) {
      throw new Error(`Screen with UUID ${uuid} not found`);
    }

    return await this.fetchJSON(`${this.basePath}/${screen.path}`);
  }

  /**
   * Load screens by tag
   */
  async loadScreensByTag(tag) {
    await this.loadIndexes();

    const screens = this.indexes.screens.screens.filter(s =>
      s.tags && s.tags.includes(tag)
    );

    return await Promise.all(
      screens.map(s => this.fetchJSON(`${this.basePath}/${s.path}`))
    );
  }

  /**
   * Load screen by name
   */
  async loadScreenByName(name) {
    await this.loadIndexes();

    const screen = this.indexes.screens.screens.find(s =>
      s.name.toLowerCase() === name.toLowerCase()
    );

    if (!screen) {
      throw new Error(`Screen with name "${name}" not found`);
    }

    return await this.fetchJSON(`${this.basePath}/${screen.path}`);
  }

  /**
   * Load component by UUID
   */
  async loadComponentByUUID(uuid) {
    await this.loadIndexes();

    const component = this.indexes.components.components.find(c => c.uuid === uuid);
    if (!component) {
      throw new Error(`Component with UUID ${uuid} not found`);
    }

    return await this.fetchJSON(`${this.basePath}/${component.path}`);
  }

  /**
   * Render screen to container
   */
  async renderScreen(screenData, containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
      throw new Error(`Container ${containerId} not found`);
    }

    // Clear container
    container.innerHTML = '';

    // Apply layout
    this.applyLayout(container, screenData.layout);

    // Render components
    for (const componentData of screenData.components) {
      await this.renderComponent(componentData, container);
    }

    // Execute actions
    this.executeActions(screenData.actions, 'onLoad');

    return container;
  }

  /**
   * Apply layout to container
   */
  applyLayout(container, layout) {
    container.style.display = 'grid';
    container.style.gridTemplateColumns = `repeat(${layout.grid.columns}, 1fr)`;
    container.style.gridTemplateRows = `repeat(${layout.grid.rows}, 1fr)`;
    container.style.gap = `${layout.grid.gap}px`;

    if (layout.theme === 'dark') {
      container.style.background = '#0a0a0a';
      container.style.color = '#00ff88';
    }
  }

  /**
   * Render component
   */
  async renderComponent(componentData, container) {
    const componentTemplate = await this.loadComponentByUUID(componentData.uuid);

    // Create component element
    const element = document.createElement('div');
    element.className = `component component-${componentTemplate.category}`;
    element.style.gridColumn = `${componentData.position.x + 1} / span ${componentData.position.width}`;
    element.style.gridRow = `${componentData.position.y + 1} / span ${componentData.position.height}`;

    // Replace template variables
    let html = componentTemplate.template.html;
    for (const [key, value] of Object.entries(componentData.config)) {
      html = html.replace(new RegExp(`{{${key}}}`, 'g'), value);
    }
    element.innerHTML = html;

    // Apply CSS
    if (componentTemplate.template.css) {
      const style = document.createElement('style');
      style.textContent = componentTemplate.template.css;
      element.appendChild(style);
    }

    // Initialize component JS
    if (componentTemplate.template.js) {
      const initFn = new Function('element', 'config', componentTemplate.template.js);
      const instance = initFn(element, componentData.config);

      // Set up tag bindings
      if (componentData.bindings && componentData.bindings.tags) {
        this.bindTags(element, instance, componentData.bindings.tags, componentTemplate);
      }
    }

    container.appendChild(element);
    return element;
  }

  /**
   * Bind tags to component
   */
  bindTags(element, instance, tagPaths, componentTemplate) {
    // This would integrate with your tag provider system
    // For now, just a placeholder
    tagPaths.forEach(tagPath => {
      console.log(`Binding tag ${tagPath} to component`);

      // Subscribe to tag updates
      // tagProvider.subscribe(tagPath, (value) => {
      //   if (instance && instance.updateGauge) {
      //     instance.updateGauge(value);
      //   }
      // });
    });
  }

  /**
   * Execute actions
   */
  executeActions(actions, trigger) {
    if (!actions) return;

    actions
      .filter(action => action.trigger === trigger)
      .forEach(action => {
        console.log(`Executing action: ${action.action}`, action.params);

        switch (action.action) {
          case 'subscribeToTags':
            // Implement tag subscription
            break;
          case 'navigate':
            // Implement navigation
            break;
          case 'writeTag':
            // Implement tag writing
            break;
          default:
            console.warn(`Unknown action: ${action.action}`);
        }
      });
  }

  /**
   * Search templates
   */
  async searchTemplates(query, type = 'screen') {
    await this.loadIndexes();

    const index = type === 'screen' ? this.indexes.screens.screens :
                  type === 'component' ? this.indexes.components.components :
                  this.indexes.tags.tags;

    const lowerQuery = query.toLowerCase();

    return index.filter(item =>
      item.name.toLowerCase().includes(lowerQuery) ||
      item.description.toLowerCase().includes(lowerQuery) ||
      (item.tags && item.tags.some(tag => tag.toLowerCase().includes(lowerQuery)))
    );
  }
}

// Global instance
window.templateLoader = new TemplateLoader('/templates');

// Helper functions
async function loadScreen(uuid, containerId = 'hmi-container') {
  const screenData = await window.templateLoader.loadScreenByUUID(uuid);
  return await window.templateLoader.renderScreen(screenData, containerId);
}

async function loadScreenByTag(tag, containerId = 'hmi-container') {
  const screens = await window.templateLoader.loadScreensByTag(tag);
  if (screens.length > 0) {
    return await window.templateLoader.renderScreen(screens[0], containerId);
  }
  throw new Error(`No screens found with tag "${tag}"`);
}

async function loadScreenByName(name, containerId = 'hmi-container') {
  const screenData = await window.templateLoader.loadScreenByName(name);
  return await window.templateLoader.renderScreen(screenData, containerId);
}
