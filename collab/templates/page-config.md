# Page Configuration Parameters

Configuration parameters for different pages.

## Index Page

```yaml
page:
  title: "🌌 AutomationGPT + Chazon OS | lablab.ai Qdrant Challenge"
  heading: "🌌 AutomationGPT Project"
  subtitle: "lablab.ai Qdrant Challenge | ISA Standards + AI"

projects:
  - name: "Chazon OS"
    icon: "🌌"
    url: "chazon.html"
    badge: "NEW! φ-Balanced"
    hebrew: "חזון - Vision"
    description: "Revolutionary pseudo-OS that runs entirely in your browser."
    features:
      - "All files < 250 tokens"
      - "Markdown → JavaScript compiler"
      - "CI/CD agents (ISA-95 L0-L4)"
      - "Terminal + Desktop UI"
      - "No backend required"
      - "φ = 1.618 design"

  - name: "ISA-OS"
    icon: "🏭"
    url: "isa-os.html"
    badge: "NEW! Container Runtime"
    description: "Browser-Based ISA Kernel"
    features:
      - "ISA-95 L0-L4 kernel"
      - "Docker → ISA mapping"
      - "Live layer visualization"
      - "Terminal interface"
      - "Load from GitHub URLs"
      - "100% client-side"

  - name: "AutomationGPT"
    icon: "🔍"
    url: "automationgpt.html"
    badge: "Classic"
    description: "Multimodal Search Engine"
    features:
      - "6 Qdrant collections"
      - "Hybrid search (RRF)"
      - "Claude AI RAG pipeline"
      - "21 CFR Part 11 mapping"
      - "EU Annex 11 compliance"
      - "CPU-optimized (no GPU)"

footer:
  tagline: "🏭 ISA Standards | 📜 Regulatory Compliance | 💻 Open Source | 🚀 Production Ready"
  credit: "Built with ❤️ for the automation community"
  links:
    - text: "GitHub"
      url: "https://github.com/teslasolar/qdrant"
    - text: "Submission"
      url: "docs/LABLAB_SUBMISSION.md"
    - text: "Chazon Docs"
      url: "chazon/README.md"
```

## Dashboard Config

```yaml
dashboard:
  title: "🌌 Chazon Unified Dashboard | All Tools"
  logo: "🌌 CHAZON"

tabs:
  - id: "chazon"
    label: "Chazon OS"
    url: "chazon.html"
    mode: "Chazon OS Terminal"

  - id: "isaos"
    label: "ISA-OS Container"
    url: "isa-os.html"
    mode: "ISA-OS Container Runtime"

  - id: "automation"
    label: "AutomationGPT"
    url: "automationgpt.html"
    mode: "AutomationGPT Search"

  - id: "docs"
    label: "Documentation"
    url: "docs/index.html"
    mode: "Documentation Hub"

shortcuts:
  quick_command: "Ctrl+K"
  close_overlay: "Esc"
  tab_shortcuts: ["Ctrl+1", "Ctrl+2", "Ctrl+3", "Ctrl+4"]
```

## Tokens
~245 tokens
