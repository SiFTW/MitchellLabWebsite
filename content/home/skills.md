+++
# A Skills section created with the Featurette widget.
widget = "featurette4"  # See https://sourcethemes.com/academic/docs/page-builder/
headless = true  # This file represents a page section.
active = true  # Activate this widget? true/false
weight = 5  # Order that this section will appear.

title = "What we do"
subtitle = "Our interdisciplinary approach aims to bring systems biology approaches to the clinic."

# Showcase personal skills or business features.
# 
# Add/remove as many `[[feature]]` blocks below as you like.
# 
# For available icons, see: https://sourcethemes.com/academic/docs/page-builder/#icons

[[feature]]
  icon = "square-root-alt"
  icon_pack = "fas"
  name = "Mathematics"
  description = "to represent cell signaling"
  
[[feature]]
  icon = "laptop-code"
  icon_pack = "fas"
  name = "Computing"
  description = "to simulate disease"  

[[feature]]
  icon = "vial"
  icon_pack = "fas"
  name = "Experiments"
  description = "to test predictions"  
  
[[feature]]
  icon = "prescription-bottle-alt"
  icon_pack = "fas"
  name = "Medicine"
  description = "to improve treatments"

+++

<style>
  .skills-widget-parent {
    position: relative !important;
    overflow: hidden !important;
    padding-bottom: 50px !important;
  }

  #home-skills-cell-canvas {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100% !important;
    z-index: 0 !important;
    pointer-events: none !important;
    opacity: 0.65;
  }

  .skills-widget-parent .container,
  .skills-widget-parent .row,
  .skills-widget-parent .featurette {
    position: relative !important;
    z-index: 1 !important;
  }

  #skills-badge-container {
    position: absolute !important;
    bottom: 14px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    z-index: 2 !important;
    text-align: center;
    width: 100%;
    pointer-events: none;
  }

  .skills-cluster-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 14px;
    font-size: 0.74rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    color: #64748b !important;
    background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(226, 232, 240, 0.9);
    border-radius: 9999px;
    backdrop-filter: blur(8px);
    text-decoration: none !important;
    pointer-events: auto !important;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .dark .skills-cluster-badge {
    color: #94a3b8 !important;
    background: rgba(15, 23, 42, 0.75);
    border-color: rgba(255, 255, 255, 0.12);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
  }

  .skills-cluster-badge:hover {
    color: #0284c7 !important;
    border-color: rgba(56, 189, 248, 0.45);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .dark .skills-cluster-badge:hover {
    color: #38bdf8 !important;
    border-color: rgba(56, 189, 248, 0.45);
  }

  .skills-live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 6px #10b981;
    display: inline-block;
  }
</style>

<canvas id="home-skills-cell-canvas"></canvas>

<div id="skills-badge-container">
  <a href="/status/" class="skills-cluster-badge">
    <span class="skills-live-dot"></span>
    This animation reflects the live status of our cluster ↗
  </a>
</div>

<script src="/js/skills-cells.js" defer></script>
