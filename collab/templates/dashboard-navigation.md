# Dashboard Navigation Template

Top navigation bar with tab switching functionality.

## HTML Structure

```html
<div id="topnav">
    <div class="logo">🌌 CHAZON</div>
    <div class="nav-tabs">
        <button class="tab active" onclick="switchTab('chazon')">Chazon OS</button>
        <button class="tab" onclick="switchTab('isaos')">ISA-OS Container</button>
        <button class="tab" onclick="switchTab('automation')">AutomationGPT</button>
        <button class="tab" onclick="switchTab('docs')">Documentation</button>
    </div>
    <div class="status">
        <span id="current-mode">Chazon OS Terminal</span>
    </div>
</div>
```

## CSS Styles

```css
#topnav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 60px;
    background: rgba(0,0,0,0.95);
    border-bottom: 2px solid #00ff88;
    display: flex;
    align-items: center;
    padding: 0 20px;
    z-index: 1000;
    gap: 20px;
}

.tab {
    background: transparent;
    border: 2px solid #333;
    color: #0f0;
    padding: 8px 20px;
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 5px 5px 0 0;
}

.tab.active {
    border-color: #00ff88;
    background: rgba(0,255,136,0.2);
}
```

## JavaScript Logic

```javascript
function switchTab(name) {
    document.querySelectorAll('.content').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));

    const panelMap = {
        'chazon': 'chazon-panel',
        'isaos': 'isaos-panel',
        'automation': 'automation-panel',
        'docs': 'docs-panel'
    };

    const modeMap = {
        'chazon': 'Chazon OS Terminal',
        'isaos': 'ISA-OS Container Runtime',
        'automation': 'AutomationGPT Search',
        'docs': 'Documentation Hub'
    };

    document.getElementById(panelMap[name]).classList.add('active');
    document.getElementById('current-mode').textContent = modeMap[name];
    event.target.classList.add('active');
}
```

## Tokens
~220 tokens
