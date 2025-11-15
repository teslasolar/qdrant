# Quick Command Overlay (Ctrl+K)

Keyboard-driven command interface with shortcuts.

## HTML Template

```html
<div id="quickcmd">
    <h2>⚡ Quick Command</h2>
    <input
        type="text"
        id="cmd-input"
        placeholder="Type command... (chazon, isa, docs, automation)"
        autofocus>
    <div class="shortcuts">
        <div><span class="key">Ctrl+K</span> - Quick command</div>
        <div><span class="key">Ctrl+1/2/3/4</span> - Switch tabs</div>
        <div><span class="key">Esc</span> - Close overlay</div>
    </div>
</div>
```

## CSS Styles

```css
#quickcmd {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0,0,0,0.95);
    border: 2px solid #00ff88;
    padding: 30px;
    border-radius: 10px;
    display: none;
    z-index: 2000;
    min-width: 500px;
}

#quickcmd.active {
    display: block;
}
```

## JavaScript

```javascript
const quickcmd = document.getElementById('quickcmd');
const cmdInput = document.getElementById('cmd-input');

document.addEventListener('keydown', (e) => {
    // Ctrl+K - Quick command
    if(e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        quickcmd.classList.toggle('active');
        if(quickcmd.classList.contains('active')) {
            cmdInput.focus();
        }
    }

    // Esc - Close overlay
    if(e.key === 'Escape') {
        quickcmd.classList.remove('active');
    }

    // Ctrl+1/2/3/4 - Tab switching
    if(e.ctrlKey && e.key >= '1' && e.key <= '4') {
        e.preventDefault();
        const tabs = ['chazon', 'isaos', 'automation', 'docs'];
        switchTab(tabs[parseInt(e.key) - 1]);
    }
});

cmdInput.addEventListener('keypress', (e) => {
    if(e.key === 'Enter') {
        const cmd = cmdInput.value.toLowerCase().trim();

        if(cmd.includes('chazon') || cmd === 'os') {
            switchTab('chazon');
        } else if(cmd.includes('isa') || cmd.includes('container')) {
            switchTab('isaos');
        } else if(cmd.includes('auto') || cmd.includes('search')) {
            switchTab('automation');
        } else if(cmd.includes('doc') || cmd.includes('help')) {
            switchTab('docs');
        }

        quickcmd.classList.remove('active');
        cmdInput.value = '';
    }
});
```

## Keyboard Shortcuts Config

```yaml
shortcuts:
  quick_command: Ctrl+K
  close_overlay: Esc
  switch_tab_1: Ctrl+1
  switch_tab_2: Ctrl+2
  switch_tab_3: Ctrl+3
  switch_tab_4: Ctrl+4
```

## Tokens
~245 tokens
