#!/usr/bin/env python3
"""
Generate hmi.html, plc.html, and scada.html files for all subdirectories in os/
"""
import os
from pathlib import Path

# Base directory
OS_DIR = Path("/home/user/qdrant/os")

# Template for HMI file
def generate_hmi_html(area_name, area_path_from_os):
    """Generate HMI HTML content for a specific area"""
    # Convert path to title (e.g., "tag-providers" -> "Tag Providers")
    title = area_name.replace("-", " ").replace("_", " ").title()

    # Calculate relative path to os root
    depth = len(Path(area_path_from_os).parts)
    root_path = "../" * depth

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} HMI - Chazon Control Panel</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Courier New', monospace;
    background: #0a0a0a;
    color: #00ff88;
    height: 100vh;
    overflow: hidden;
  }}

  #hmi-container {{
    display: grid;
    grid-template-rows: 60px 1fr 50px;
    height: 100vh;
  }}

  #hmi-header {{
    background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
    border-bottom: 3px solid #00ff88;
    display: flex;
    align-items: center;
    padding: 0 20px;
    justify-content: space-between;
  }}

  #hmi-header h1 {{
    font-size: 1.5em;
    color: #00ff88;
  }}

  #hmi-main {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    padding: 20px;
    overflow-y: auto;
  }}

  .control-btn {{
    background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
    border: 2px solid #00ff88;
    border-radius: 12px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    min-height: 150px;
  }}

  .control-btn:hover {{
    border-color: #00ccff;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    transform: translateY(-2px);
  }}

  .control-icon {{
    font-size: 3em;
    margin-bottom: 10px;
  }}

  .control-label {{
    color: #00ff88;
    font-weight: bold;
    font-size: 1.1em;
    margin-bottom: 8px;
  }}

  .control-status {{
    color: #888;
    font-size: 0.9em;
  }}

  .indicator {{
    position: absolute;
    top: 10px;
    right: 10px;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 10px #00ff88;
  }}

  #hmi-footer {{
    background: #1a1a2e;
    border-top: 2px solid #00ff88;
    display: flex;
    align-items: center;
    padding: 0 20px;
    justify-content: space-between;
  }}

  .btn {{
    padding: 8px 16px;
    background: #00ff88;
    color: #000;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-weight: bold;
  }}

  .btn:hover {{ background: #00cc66; }}
  .btn.secondary {{ background: #333; color: #00ff88; }}
</style>
</head>
<body>

<div id="hmi-container">
  <div id="hmi-header">
    <h1>🎛️ {title} - HMI Control Panel</h1>
    <div style="color: #00ccff; font-size: 1.2em;" id="system-time">00:00:00</div>
  </div>

  <div id="hmi-main">
    <div class="control-btn" onclick="window.location.href='index.html'">
      <div class="indicator"></div>
      <div class="control-icon">📄</div>
      <div class="control-label">Main View</div>
      <div class="control-status">Index Page</div>
    </div>

    <div class="control-btn" onclick="window.location.href='scada.html'">
      <div class="indicator"></div>
      <div class="control-icon">📈</div>
      <div class="control-label">SCADA View</div>
      <div class="control-status">Real-time Data</div>
    </div>

    <div class="control-btn" onclick="window.location.href='plc.html'">
      <div class="indicator"></div>
      <div class="control-icon">⚙️</div>
      <div class="control-label">PLC Logic</div>
      <div class="control-status">Control Logic</div>
    </div>
  </div>

  <div id="hmi-footer">
    <div>
      <button class="btn secondary" onclick="window.location.href='{root_path}index.html'">🏠 OS Home</button>
      <button class="btn secondary" onclick="window.history.back()">← Back</button>
    </div>
    <div>
      <button class="btn" onclick="location.reload()">🔄 Refresh</button>
    </div>
  </div>
</div>

<script>
function updateTime() {{
  document.getElementById('system-time').textContent = new Date().toLocaleTimeString();
}}
setInterval(updateTime, 1000);
updateTime();
</script>

</body>
</html>
'''

# Template for PLC file
def generate_plc_html(area_name, area_path_from_os):
    """Generate PLC HTML content for a specific area"""
    title = area_name.replace("-", " ").replace("_", " ").title()
    depth = len(Path(area_path_from_os).parts)
    root_path = "../" * depth

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} PLC - Chazon Control Logic</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Courier New', monospace;
    background: #0a0a0a;
    color: #00ff88;
    padding: 20px;
  }}
  .container {{ max-width: 1400px; margin: 0 auto; }}
  header {{
    background: #1a1a2e;
    border: 2px solid #00ff88;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
  }}
  h1 {{ color: #00ff88; margin-bottom: 10px; }}
  .breadcrumb {{
    color: #888;
    font-size: 14px;
  }}
  .breadcrumb a {{ color: #00ccff; text-decoration: none; }}

  .plc-card {{
    background: #1a1a2e;
    border: 1px solid #333;
    border-left: 3px solid #00ff88;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
  }}

  .plc-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
  }}

  .plc-name {{
    color: #00ff88;
    font-weight: bold;
    font-size: 16px;
  }}

  .plc-status {{
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: bold;
    background: #00ff88;
    color: #000;
  }}

  .code-block {{
    background: #000;
    padding: 10px;
    border-radius: 4px;
    font-size: 11px;
    overflow-x: auto;
    margin-top: 10px;
    color: #00ccff;
  }}

  .btn {{
    padding: 6px 12px;
    background: #00ff88;
    color: #000;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-size: 11px;
    font-weight: bold;
    margin-right: 8px;
  }}

  .btn:hover {{ background: #00cc66; }}
  .btn.secondary {{ background: #333; color: #00ff88; }}
</style>
</head>
<body>

<div class="container">
  <header>
    <h1>⚙️ {title} - PLC Control Logic</h1>
    <div class="breadcrumb">
      <a href="{root_path}index.html">OS Home</a> /
      <a href="index.html">{title}</a> /
      PLC
    </div>
  </header>

  <div class="plc-card">
    <div class="plc-header">
      <div class="plc-name">{title} Controller</div>
      <div class="plc-status">RUNNING</div>
    </div>
    <div style="color: #888; font-size: 12px; margin-bottom: 10px;">
      Scan Time: 100ms | Status: OK
    </div>
    <div class="code-block">
// {title} Control Logic
if (systemReady) {{
  processData();
  updateState();
  logMetrics();
}}
    </div>
    <div style="margin-top: 10px;">
      <button class="btn" onclick="window.location.href='index.html'">View Main</button>
      <button class="btn secondary" onclick="window.location.href='hmi.html'">HMI Panel</button>
      <button class="btn secondary" onclick="window.location.href='scada.html'">SCADA View</button>
    </div>
  </div>

  <div class="plc-card">
    <div class="plc-header">
      <div class="plc-name">System Log</div>
    </div>
    <div class="code-block" style="height: 150px; overflow-y: auto;" id="log">
      <div style="color: #00ff88;">[00:00:00] PLC initialized</div>
      <div style="color: #00ccff;">[00:00:01] Scanning tags...</div>
      <div style="color: #00ff88;">[00:00:02] System online</div>
    </div>
  </div>
</div>

<script>
function log(message, type = 'info') {{
  const time = new Date().toLocaleTimeString();
  const entry = document.createElement('div');
  entry.style.color = type === 'error' ? '#ff0044' : '#00ccff';
  entry.textContent = `[${{time}}] ${{message}}`;
  document.getElementById('log').appendChild(entry);
  document.getElementById('log').scrollTop = document.getElementById('log').scrollHeight;
}}

setInterval(() => {{
  if (Math.random() > 0.9) {{
    log('Scan cycle complete');
  }}
}}, 5000);
</script>

</body>
</html>
'''

# Template for SCADA file
def generate_scada_html(area_name, area_path_from_os):
    """Generate SCADA HTML content for a specific area"""
    title = area_name.replace("-", " ").replace("_", " ").title()
    depth = len(Path(area_path_from_os).parts)
    root_path = "../" * depth

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} SCADA - Chazon Monitoring</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Courier New', monospace;
    background: #0a0a0a;
    color: #00ff88;
    overflow: hidden;
    height: 100vh;
  }}

  #scada-container {{
    display: grid;
    grid-template-rows: 60px 1fr 40px;
    height: 100vh;
  }}

  #scada-header {{
    background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
    border-bottom: 3px solid #00ff88;
    display: flex;
    align-items: center;
    padding: 0 20px;
    justify-content: space-between;
  }}

  #scada-header h1 {{
    font-size: 1.5em;
    color: #00ff88;
  }}

  #scada-main {{
    display: grid;
    grid-template-columns: 250px 1fr 300px;
    overflow: hidden;
  }}

  #sidebar {{
    background: #1a1a2e;
    border-right: 2px solid #00ff88;
    overflow-y: auto;
    padding: 15px;
  }}

  #content {{
    background: #000;
    position: relative;
    overflow: auto;
    padding: 20px;
  }}

  #data-panel {{
    background: #1a1a2e;
    border-left: 2px solid #00ff88;
    overflow-y: auto;
    padding: 15px;
  }}

  .data-section {{
    margin-bottom: 20px;
  }}

  .data-section h3 {{
    color: #00ccff;
    border-bottom: 1px solid #00ff88;
    padding-bottom: 5px;
    margin-bottom: 10px;
    font-size: 14px;
  }}

  .data-item {{
    display: flex;
    justify-content: space-between;
    padding: 5px 0;
    border-bottom: 1px solid #222;
    font-size: 12px;
  }}

  .data-label {{ color: #888; }}
  .data-value {{ color: #00ff88; font-weight: bold; }}

  #status-bar {{
    background: #1a1a2e;
    border-top: 2px solid #00ff88;
    display: flex;
    align-items: center;
    padding: 0 20px;
    justify-content: space-between;
    font-size: 12px;
  }}

  .indicator {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    background: #00ff88;
    box-shadow: 0 0 8px #00ff88;
  }}

  .btn {{
    padding: 6px 12px;
    background: #00ff88;
    color: #000;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-family: inherit;
    font-size: 11px;
    font-weight: bold;
  }}

  .btn:hover {{ background: #00cc66; }}
  .btn.secondary {{ background: #333; color: #00ff88; }}
</style>
</head>
<body>

<div id="scada-container">
  <div id="scada-header">
    <h1>📈 {title} - SCADA Monitor</h1>
    <div style="color: #00ccff; font-size: 1.2em;" id="system-time">00:00:00</div>
  </div>

  <div id="scada-main">
    <div id="sidebar">
      <h3 style="color: #00ccff; margin-bottom: 15px;">Navigation</h3>
      <button class="btn" style="width: 100%; margin-bottom: 10px;" onclick="window.location.href='index.html'">📄 Main View</button>
      <button class="btn secondary" style="width: 100%; margin-bottom: 10px;" onclick="window.location.href='hmi.html'">🎛️ HMI Panel</button>
      <button class="btn secondary" style="width: 100%; margin-bottom: 10px;" onclick="window.location.href='plc.html'">⚙️ PLC Logic</button>
      <button class="btn secondary" style="width: 100%; margin-top: 20px;" onclick="window.location.href='{root_path}index.html'">🏠 OS Home</button>
    </div>

    <div id="content">
      <h2 style="color: #00ccff; margin-bottom: 20px;">{title} Overview</h2>
      <div style="background: #1a1a2e; border: 2px solid #00ff88; border-radius: 8px; padding: 20px;">
        <p style="color: #888; margin-bottom: 15px;">Real-time monitoring and control for {title}</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
          <div style="background: #000; padding: 15px; border-radius: 4px;">
            <div style="color: #888; font-size: 12px;">Status</div>
            <div style="color: #00ff88; font-size: 24px; font-weight: bold;">ONLINE</div>
          </div>
          <div style="background: #000; padding: 15px; border-radius: 4px;">
            <div style="color: #888; font-size: 12px;">Scan Rate</div>
            <div style="color: #00ff88; font-size: 24px; font-weight: bold;">100ms</div>
          </div>
          <div style="background: #000; padding: 15px; border-radius: 4px;">
            <div style="color: #888; font-size: 12px;">Uptime</div>
            <div style="color: #00ff88; font-size: 24px; font-weight: bold;" id="uptime">0m</div>
          </div>
        </div>
      </div>
    </div>

    <div id="data-panel">
      <div class="data-section">
        <h3>System Metrics</h3>
        <div class="data-item">
          <span class="data-label">CPU:</span>
          <span class="data-value" id="cpu">0%</span>
        </div>
        <div class="data-item">
          <span class="data-label">Memory:</span>
          <span class="data-value" id="memory">0 MB</span>
        </div>
        <div class="data-item">
          <span class="data-label">Status:</span>
          <span class="data-value">RUNNING</span>
        </div>
      </div>

      <div class="data-section">
        <h3>Alarms</h3>
        <div style="color: #888; font-size: 11px;">No active alarms</div>
      </div>
    </div>
  </div>

  <div id="status-bar">
    <div>
      <span><span class="indicator"></span>System: ONLINE</span>
    </div>
    <div>
      <span id="connection">Connection: STABLE</span>
    </div>
  </div>
</div>

<script>
let startTime = Date.now();

function updateTime() {{
  document.getElementById('system-time').textContent = new Date().toLocaleTimeString();
  const uptime = Math.floor((Date.now() - startTime) / 60000);
  document.getElementById('uptime').textContent = uptime + 'm';
}}

function updateMetrics() {{
  document.getElementById('cpu').textContent = (Math.random() * 30 + 10).toFixed(1) + '%';
  document.getElementById('memory').textContent = (Math.random() * 500 + 1000).toFixed(0) + ' MB';
}}

setInterval(updateTime, 1000);
setInterval(updateMetrics, 1000);
updateTime();
updateMetrics();
</script>

</body>
</html>
'''

def main():
    """Main function to generate all missing interface files"""
    created_files = []

    # Walk through all directories in os/
    for root, dirs, files in os.walk(OS_DIR):
        root_path = Path(root)

        # Get area name from directory
        area_name = root_path.name

        # Get relative path from os/ directory
        try:
            area_path_from_os = root_path.relative_to(OS_DIR)
        except ValueError:
            continue

        # Check which files are missing
        has_hmi = (root_path / "hmi.html").exists()
        has_plc = (root_path / "plc.html").exists()
        has_scada = (root_path / "scada.html").exists()

        # Create missing files
        if not has_hmi:
            hmi_path = root_path / "hmi.html"
            hmi_path.write_text(generate_hmi_html(area_name, str(area_path_from_os)))
            created_files.append(str(hmi_path))
            print(f"Created: {hmi_path}")

        if not has_plc:
            plc_path = root_path / "plc.html"
            plc_path.write_text(generate_plc_html(area_name, str(area_path_from_os)))
            created_files.append(str(plc_path))
            print(f"Created: {plc_path}")

        if not has_scada:
            scada_path = root_path / "scada.html"
            scada_path.write_text(generate_scada_html(area_name, str(area_path_from_os)))
            created_files.append(str(scada_path))
            print(f"Created: {scada_path}")

    print(f"\n✅ Total files created: {len(created_files)}")
    return created_files

if __name__ == "__main__":
    main()
