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
    padding-bottom: 3.5rem !important;
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

  /* Centered link container with breathing room below skills */
  #skills-badge-container {
    position: relative !important;
    z-index: 2 !important;
    text-align: center !important;
    width: 100% !important;
    margin-top: 3.5rem !important;
    margin-bottom: 0.5rem !important;
  }

  /* Text link styled to mirror the widget's subtitle typography */
  .skills-cluster-link {
    display: inline-block;
    font-family: inherit !important;
    font-size: 0.85rem !important;
    line-height: 1.5;
    color: #64748b !important;
    text-decoration: none !important;
    transition: color 0.2s ease, opacity 0.2s ease;
    opacity: 0.85;
  }

  .dark .skills-cluster-link {
    color: #94a3b8 !important;
  }

  .skills-cluster-link:hover {
    color: #0284c7 !important;
    opacity: 1;
    text-decoration: underline !important;
  }

  .dark .skills-cluster-link:hover {
    color: #38bdf8 !important;
  }
</style>

<canvas id="home-skills-cell-canvas"></canvas>

<div id="skills-badge-container">
  <a href="/status/" class="skills-cluster-link">
    This animation reflects the live status of our computing cluster &rarr;
  </a>
</div>

<script src="/js/skills-cells.js" defer></script>
