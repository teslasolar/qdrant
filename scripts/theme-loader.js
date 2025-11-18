// Theme Loader - Applies Cream & Purple ISA-101 Theme
// Reads from theme.yaml configuration

class ThemeLoader {
  constructor() {
    this.theme = {
      colors: {
        bgPrimary: '#2a1a3a',
        bgSecondary: '#3d2a52',
        bgTertiary: '#1a0f26',
        cream: '#f5f2e8',
        creamDark: '#e8e0c8',
        creamLight: '#faf8f0',
        purpleLight: '#9b7eb8',
        purpleAccent: '#b794f4',
        purpleGlow: '#8b5cf6',
        purpleDark: '#5a3d7a',
        normal: '#90ee90',
        warning: '#ffd700',
        alarm: '#ff6b6b',
        inactive: '#808080',
        active: '#00bfff'
      },
      spacing: {
        dockNorthHeight: '80px',
        dockSouthHeight: '40px',
        dockEastWidth: '280px',
        dockWestWidth: '280px',
        dockGap: '4px'
      }
    };
  }

  // Apply theme to document
  apply() {
    const root = document.documentElement;

    // Colors
    root.style.setProperty('--bg-primary', this.theme.colors.bgPrimary);
    root.style.setProperty('--bg-secondary', this.theme.colors.bgSecondary);
    root.style.setProperty('--bg-tertiary', this.theme.colors.bgTertiary);
    root.style.setProperty('--cream', this.theme.colors.cream);
    root.style.setProperty('--cream-dark', this.theme.colors.creamDark);
    root.style.setProperty('--cream-light', this.theme.colors.creamLight);
    root.style.setProperty('--purple-light', this.theme.colors.purpleLight);
    root.style.setProperty('--purple-accent', this.theme.colors.purpleAccent);
    root.style.setProperty('--purple-glow', this.theme.colors.purpleGlow);
    root.style.setProperty('--purple-dark', this.theme.colors.purpleDark);
    root.style.setProperty('--normal', this.theme.colors.normal);
    root.style.setProperty('--warning', this.theme.colors.warning);
    root.style.setProperty('--alarm', this.theme.colors.alarm);
    root.style.setProperty('--inactive', this.theme.colors.inactive);
    root.style.setProperty('--active', this.theme.colors.active);

    // Spacing
    root.style.setProperty('--dock-north-height', this.theme.spacing.dockNorthHeight);
    root.style.setProperty('--dock-south-height', this.theme.spacing.dockSouthHeight);
    root.style.setProperty('--dock-east-width', this.theme.spacing.dockEastWidth);
    root.style.setProperty('--dock-west-width', this.theme.spacing.dockWestWidth);
    root.style.setProperty('--dock-gap', this.theme.spacing.dockGap);
  }

  // Get color value
  getColor(colorName) {
    return this.theme.colors[colorName] || '#ffffff';
  }
}

// Auto-apply on load
if (typeof document !== 'undefined') {
  const themeLoader = new ThemeLoader();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => themeLoader.apply());
  } else {
    themeLoader.apply();
  }
  window.themeLoader = themeLoader;
}

export default ThemeLoader;
