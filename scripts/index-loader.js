// Generic Index Loader with Enhanced Navigation
// Loads structured index data and renders with full navigation hierarchy

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

async function loadIndex() {
  try {
    // Auto-redirect root index to frontend user portal
    const currentPath = window.location.pathname;
    const isRootIndex = currentPath === '/' || currentPath.endsWith('/index.html') || currentPath.endsWith('/qdrant/');

    if (isRootIndex) {
      window.location.href = 'screens/frontend/index.html';
      return;
    }

    // Load index tag data
    const response = await fetch('index/tag.json');
    if (!response.ok) {
      throw new Error('Index data not found');
    }

    const tag = await response.json();

    // Apply color scheme
    document.body.className = `color-${tag.Color_Scheme}`;
    document.title = tag.Title;

    // Build breadcrumb navigation
    let breadcrumbHTML = '';
    if (tag.Breadcrumb_Trail && tag.Breadcrumb_Trail.length > 0) {
      breadcrumbHTML = '<div class="breadcrumb">';
      tag.Breadcrumb_Trail.forEach((crumb, index) => {
        if (index > 0) {
          breadcrumbHTML += '<span class="breadcrumb-separator">›</span>';
        }
        if (index === tag.Breadcrumb_Trail.length - 1) {
          breadcrumbHTML += `<span class="breadcrumb-current">${crumb.icon} ${crumb.title}</span>`;
        } else {
          breadcrumbHTML += `<a href="${crumb.path}">${crumb.icon} ${crumb.title}</a>`;
        }
      });
      breadcrumbHTML += '</div>';
    }

    // Build sidebar navigation
    let sidebarHTML = '';
    if (tag.Child_Directories && tag.Child_Directories.length > 0) {
      sidebarHTML += '<h3>📂 Quick Nav</h3><ul>';
      tag.Child_Directories.forEach(dir => {
        sidebarHTML += `<li><a href="${dir.path}">${dir.icon} ${dir.title}</a></li>`;
      });
      sidebarHTML += '</ul>';
    }

    if (tag.Sibling_Directories && tag.Sibling_Directories.length > 0) {
      sidebarHTML += '<h3 style="margin-top: 20px;">🔗 Related</h3><ul>';
      tag.Sibling_Directories.slice(0, 8).forEach(dir => {
        sidebarHTML += `<li><a href="${dir.path}">${dir.icon} ${dir.title}</a></li>`;
      });
      sidebarHTML += '</ul>';
    }

    if (sidebarHTML) {
      document.getElementById('sidebar').innerHTML = sidebarHTML;
      document.getElementById('sidebar').style.display = 'block';
    }

    // Build main content
    const content = document.getElementById('content');
    content.innerHTML = `
      ${breadcrumbHTML}

      <header>
        <div class="icon">${tag.Icon}</div>
        <h1>${tag.Title}</h1>
        <p class="description">${tag.Description}</p>
        <div>
          <span class="badge">${tag.ISA_Level.replace('_', '-')}</span>
          <span class="badge">UUID: ${tag.UUID.substring(0, 8)}</span>
        </div>
      </header>

      ${tag.Page_Links && tag.Page_Links.length > 0 ? `
      <div class="section">
        <h2>📄 Pages in This Directory</h2>
        <div class="page-list">
          ${tag.Page_Links.map(page => `
            <div class="page-item">
              <a href="${page.path}">
                <span class="page-item-icon">${page.icon}</span>
                <div>
                  <div>${page.name}</div>
                  <div class="page-item-size">${formatSize(page.size)}</div>
                </div>
              </a>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Features && tag.Features.length > 0 ? `
      <div class="section">
        <h2>✨ Features</h2>
        <div class="grid">
          ${tag.Features.map(f => `
            <div class="card">
              <div class="card-icon">${f.icon}</div>
              <h2>${f.title}</h2>
              <p>${f.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Child_Directories && tag.Child_Directories.length > 0 ? `
      <div class="section">
        <h2>📂 Subdirectories</h2>
        <div class="grid">
          ${tag.Child_Directories.map(d => `
            <div class="card">
              ${d.page_count ? `<span class="card-badge">${d.page_count} pages</span>` : ''}
              <div class="card-icon">${d.icon}</div>
              <h2><a href="${d.path}">${d.title}</a></h2>
              <p>${d.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Sibling_Directories && tag.Sibling_Directories.length > 0 ? `
      <div class="section">
        <h2>🔗 Related Directories</h2>
        <div class="grid">
          ${tag.Sibling_Directories.slice(0, 6).map(d => `
            <div class="card">
              <div class="card-icon">${d.icon}</div>
              <h2><a href="${d.path}">${d.title}</a></h2>
              <p>${d.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${(tag.has_plc || tag.has_hmi || tag.has_scada) ? `
      <div class="section">
        <h2>🎛️ Control Interfaces</h2>
        <div style="text-align: center;">
          ${tag.has_scada ? `<a href="${tag.scada_path}" class="btn btn-primary">📊 SCADA</a>` : ''}
          ${tag.has_hmi ? `<a href="${tag.hmi_path}" class="btn btn-primary">🎛️ HMI</a>` : ''}
          ${tag.has_plc ? `<a href="${tag.plc_path}" class="btn btn-primary">⚙️ PLC</a>` : ''}
        </div>
      </div>
      ` : ''}

      ${tag.Related_Files && tag.Related_Files.length > 0 ? `
      <div class="section">
        <h2>📚 Documentation</h2>
        <div class="grid">
          ${tag.Related_Files.map(f => `
            <div class="card">
              <h2><a href="${f.path}">${f.name}</a></h2>
              <p>Type: ${f.type}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Quick_Actions && tag.Quick_Actions.length > 0 ? `
      <div class="section">
        <h2>⚡ Quick Actions</h2>
        <div style="text-align: center;">
          ${tag.Quick_Actions.map(a => `
            <a href="${a.path}" class="btn btn-${a.type}">${a.label}</a>
          `).join('')}
        </div>
      </div>
      ` : ''}

      <footer>
        <p>
          <strong>ISA-95 ${tag.ISA_Level.replace('_', '-')}</strong><br>
          ${tag.Directory_Path}
        </p>
      </footer>
    `;

    // Hide loader, show content
    document.getElementById('loader').style.display = 'none';
    content.style.display = 'block';

  } catch (error) {
    console.error('Error loading index:', error);
    document.getElementById('loader').innerHTML = `
      <div class="card" style="max-width: 500px;">
        <h2 style="color: #ff6666;">⚠️ Error Loading Index</h2>
        <p>${error.message}</p>
        <p style="margin-top: 20px;">
          <a href="../" class="btn btn-secondary">← Go Back</a>
        </p>
      </div>
    `;
  }
}

// Load on page ready
document.addEventListener('DOMContentLoaded', loadIndex);
