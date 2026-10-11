+++
widget = "featurette4"
headless = true
weight = 10
active = true

title = "Our Core Pillars"
subtitle = "An iterative cycle connecting mathematics, computation, and wet lab to clinic"

[[feature]]
  icon = "square-root-alt"
  icon_pack = "fas"
  name = "Mathematics"
  description = "Mechanistic ODE modeling of cell signaling dynamics and regulatory networks."

[[feature]]
  icon = "microchip"
  icon_pack = "fas"
  name = "Computing"
  description = "High-performance digital twins simulating heterogeneous tumor drug responses."

[[feature]]
  icon = "dna"
  icon_pack = "fas"
  name = "Experiments"
  description = "Flow cytometry, co-culture assays, and microscopy validating model predictions."

[[feature]]
  icon = "hospital-user"
  icon_pack = "fas"
  name = "Medicine"
  description = "Translational stratification strategies to overcome drug resistance in lymphoma."
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
