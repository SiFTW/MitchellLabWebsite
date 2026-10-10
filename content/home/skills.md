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

# Uncomment to use emoji icons.
# [[feature]]
#  icon = ":smile:"
#  icon_pack = "emoji"
#  name = "Emojiness"
#  description = "100%"  

# Uncomment to use custom SVG icons.
# Place custom SVG icon in `assets/images/icon-pack/`, creating folders if necessary.
# Reference the SVG icon name (without `.svg` extension) in the `icon` field.
# [[feature]]
#  icon = "your-custom-icon-name"
#  icon_pack = "custom"
#  name = "Surfing"
#  description = "90%"

+++

<style>
  /* Isolate section positioning for the background canvas layer */
  #skills, 
  section[id*="skills"],
  section[id*="what-we-do"],
  .wg-featurette,
  .wg-featurette4 {
    position: relative !important;
    overflow: hidden !important;
  }

  /* Full-bleed background canvas behind Wowchemy icons and text */
  #home-skills-cell-canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    opacity: 0.65;
  }

  /* Ensure Wowchemy container elements sit cleanly on top */
  #skills .container,
  section[id*="skills"] .container,
  section[id*="what-we-do"] .container,
  .wg-featurette .container,
  .wg-featurette4 .container {
    position: relative !important;
    z-index: 1 !important;
  }

  /* Subtle link pill pointing to telemetry */
  .skills-cluster-badge-wrap {
    position: relative;
    z-index: 2;
    text-align: center;
    margin-top: 28px;
    margin-bottom: 6px;
  }

  .skills-cluster-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 5px 14px;
    font-size: 0.74rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    color: #64748b !important;
    background: rgba(255, 255, 255, 0.75);
    border: 1px solid rgba(226, 232, 240, 0.85);
    border-radius: 9999px;
    backdrop-filter: blur(8px);
    text-decoration: none !important;
    transition: all 0.25s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
  }

  /* Dark mode compatibility */
  .dark .skills-cluster-badge {
    color: #94a3b8 !important;
    background: rgba(15, 23, 42, 0.65);
    border-color: rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .skills-cluster-badge:hover {
    color: #0284c7 !important;
    border-color: rgba(56, 189, 248, 0.45);
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
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

<div class="skills-cluster-badge-wrap">
  <a href="/status/" class="skills-cluster-badge">
    <span class="skills-live-dot"></span>
    This animation reflects the live status of our cluster ↗
  </a>
</div>

<script>
(function() {
  const GIST_BASE = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw";

  const NODES = [
    { id: "simon", cores: 72, apiVer: 3, url: "" },
    { id: "jlp",   cores: 104, apiVer: 3, url: "" },
    { id: "priti", cores: 12,  apiVer: 3, url: "" },
    { id: "nas",   cores: 4,   apiVer: 4, url: "" }
  ];

  const COLOR_STOPS = [
    { p: 0.00, r: 140, g: 155, b: 180 }, // Slate backdrop
    { p: 0.20, r: 2,   g: 132, b: 199 }, // Cyan
    { p: 0.50, r: 16,  g: 185, b: 129 }, // Emerald
    { p: 0.75, r: 245, g: 158, b: 11  }, // Amber
    { p: 1.00, r: 236, g: 72,  b: 153 }  // Pink
  ];

  function getContinuousColor(pct) {
    const t = Math.max(0, Math.min(100, pct)) / 100;
    let lower = COLOR_STOPS[0];
    let upper = COLOR_STOPS[COLOR_STOPS.length - 1];

    for (let i = 0; i < COLOR_STOPS.length - 1; i++) {
      if (t >= COLOR_STOPS[i].p && t <= COLOR_STOPS[i + 1].p) {
        lower = COLOR_STOPS[i];
        upper = COLOR_STOPS[i + 1];
        break;
      }
    }

    const range = upper.p - lower.p;
    const factor = range === 0 ? 0 : (t - lower.p) / range;
    const r = Math.round(lower.r + (upper.r - lower.r) * factor);
    const g = Math.round(lower.g + (upper.g - lower.g) * factor);
    const b = Math.round(lower.b + (upper.b - lower.b) * factor);
    return `rgb(${r}, ${g}, ${b})`;
  }

  const canvas = document.getElementById("home-skills-cell-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const parentSection = canvas.closest("section") || canvas.parentElement;

  let initialWidth = parentSection.clientWidth || window.innerWidth || 1200;
  let initialHeight = parentSection.clientHeight || 450;
  canvas.width = initialWidth;
  canvas.height = initialHeight;

  const clusterCorePool = {};
  NODES.forEach(n => {
    clusterCorePool[n.id] = new Array(n.cores).fill(0);
  });

  let cellIndex = 0;
  const cells = [];
  NODES.forEach(n => {
    for (let c = 0; c < n.cores; c++) {
      const angle = Math.random() * Math.PI * 2;
      cells.push({
        id: cellIndex++,
        nodeId: n.id,
        coreIdx: c,
        fluidVx: 0,
        fluidVy: 0,
        x: Math.random() * initialWidth,
        y: Math.random() * initialHeight,
        vx: Math.cos(angle) * (0.04 + Math.random() * 0.05),
        vy: Math.sin(angle) * (0.04 + Math.random() * 0.05),
        currentLoad: 0,
        mitosisState: 'none',
        mitosisProgress: 0,
        splitAngle: 0,
        deathState: 'none',
        deathProgress: 0,
        popRadius: 0,
        popAlpha: 1
      });
    }
  });

  const temporaryDaughters = [];

  function resizeCanvas() {
    const prevWidth = canvas.width || initialWidth;
    const prevHeight = canvas.height || initialHeight;
    const newWidth = parentSection.clientWidth || window.innerWidth;
    const newHeight = parentSection.clientHeight || 450;

    canvas.width = newWidth;
    canvas.height = newHeight;

    if (cells.length > 0 && (newWidth > prevWidth || newHeight > prevHeight)) {
      cells.forEach(c => {
        if (newWidth > prevWidth && c.x < prevWidth) {
          c.x = (c.x / prevWidth) * newWidth;
        }
        if (newHeight > prevHeight && Math.random() > 0.4) {
          c.y = Math.random() * newHeight;
        }
      });
    }
  }
  window.addEventListener("resize", resizeCanvas);
  setTimeout(resizeCanvas, 150);

  function spawnIndependentDaughter(x, y, angle, load) {
    const speed = 0.08 + Math.random() * 0.05;
    temporaryDaughters.push({
      id: `daughter-${Date.now()}-${Math.random()}`,
      x: x,
      y: y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      fluidVx: 0,
      fluidVy: 0,
      currentLoad: load,
      deathState: 'none',
      deathProgress: 0,
      popRadius: 0,
      popAlpha: 1,
      timeRemaining: 600
    });
  }

  function triggerMitosisEvent() {
    const candidates = cells.filter(c => c.mitosisState === 'none' && c.deathState === 'none');
    if (candidates.length === 0) return;

    const active = candidates.filter(c => c.currentLoad > 25);
    const chosen = (active.length > 0)
      ? active[Math.floor(Math.random() * active.length)]
      : candidates[Math.floor(Math.random() * candidates.length)];

    chosen.mitosisState = 'growing';
    chosen.mitosisProgress = 0;
    chosen.splitAngle = Math.random() * Math.PI * 2;
  }
  setInterval(triggerMitosisEvent, 9000);

  const fluidMouse = {
    x: -9999,
    y: -9999,
    prevX: -9999,
    prevY: -9999,
    vx: 0,
    vy: 0,
    active: false,
    radius: 65
  };

  function updatePointerPosition(clientX, clientY) {
    const rect = parentSection.getBoundingClientRect();
    const currX = clientX - rect.left;
    const currY = clientY - rect.top;

    if (fluidMouse.prevX !== -9999) {
      fluidMouse.vx = (currX - fluidMouse.prevX) * 0.35;
      fluidMouse.vy = (currY - fluidMouse.prevY) * 0.35;
    }

    fluidMouse.prevX = currX;
    fluidMouse.prevY = currY;
    fluidMouse.x = currX;
    fluidMouse.y = currY;
    fluidMouse.active = true;
  }

  parentSection.addEventListener("mousemove", (e) => {
    updatePointerPosition(e.clientX, e.clientY);
  });

  parentSection.addEventListener("mouseleave", () => {
    fluidMouse.active = false;
    fluidMouse.x = -9999;
    fluidMouse.y = -9999;
    fluidMouse.prevX = -9999;
    fluidMouse.prevY = -9999;
    fluidMouse.vx = 0;
    fluidMouse.vy = 0;
  });

  function animateCells() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    cells.forEach(c => {
      const targetLoad = (clusterCorePool[c.nodeId] && clusterCorePool[c.nodeId][c.coreIdx] !== undefined)
        ? clusterCorePool[c.nodeId][c.coreIdx]
        : 0;

      if (c.currentLoad > 40 && targetLoad < 8 && c.deathState === 'none' && c.mitosisState === 'none') {
        c.deathState = 'swelling';
        c.deathProgress = 0;
      }

      c.currentLoad += (targetLoad - c.currentLoad) * 0.010;
      const loadNorm = c.currentLoad / 100;
      const speedMult = 0.10 + (loadNorm * 0.28);

      if (fluidMouse.active) {
        const dx = c.x - fluidMouse.x;
        const dy = c.y - fluidMouse.y;
        const dist = Math.hypot(dx, dy);

        if (dist < fluidMouse.radius && dist > 1) {
          const force = Math.pow(1 - dist / fluidMouse.radius, 2) * 0.22;
          const normalX = dx / dist;
          const normalY = dy / dist;
          c.fluidVx += (normalX * force * 0.45) + (fluidMouse.vx * force * 0.12);
          c.fluidVy += (normalY * force * 0.45) + (fluidMouse.vy * force * 0.12);
        }
      }

      c.fluidVx = (c.fluidVx || 0) * 0.82;
      c.fluidVy = (c.fluidVy || 0) * 0.82;

      c.x += (c.vx * speedMult) + c.fluidVx;
      c.y += (c.vy * speedMult) + c.fluidVy;

      if (c.x < -20) c.x = canvas.width + 20;
      if (c.x > canvas.width + 20) c.x = -20;
      if (c.y < -20) c.y = canvas.height + 20;
      if (c.y > canvas.height + 20) c.y = -20;

      const color = getContinuousColor(c.currentLoad);
      const baseRadius = 2.0 + (loadNorm * 2.6);

      ctx.save();
      if (c.currentLoad > 75) {
        ctx.shadowColor = color;
        ctx.shadowBlur = (c.currentLoad - 75) * 0.25;
      }

      if (c.deathState !== 'none') {
        c.deathProgress += 0.035;
        if (c.deathState === 'swelling') {
          const swellScale = 1.0 + (c.deathProgress * 0.7);
          ctx.beginPath();
          ctx.arc(c.x, c.y, baseRadius * swellScale, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();

          if (c.deathProgress >= 1.0) {
            c.deathState = 'popping';
            c.popRadius = baseRadius * swellScale;
            c.popAlpha = 0.85;
          }
        } else if (c.deathState === 'popping') {
          c.popRadius += 0.8;
          c.popAlpha -= 0.06;
          ctx.beginPath();
          ctx.arc(c.x, c.y, c.popRadius, 0, Math.PI * 2);
          ctx.strokeStyle = color;
          ctx.lineWidth = 1.2;
          ctx.globalAlpha = Math.max(0, c.popAlpha);
          ctx.stroke();

          if (c.popAlpha <= 0) {
            c.deathState = 'none';
            c.deathProgress = 0;
            c.currentLoad = Math.min(c.currentLoad, 10);
          }
        }
      } else if (c.mitosisState === 'growing') {
        c.mitosisProgress += 0.009;
        ctx.beginPath();
        ctx.arc(c.x, c.y, baseRadius * (1.0 + c.mitosisProgress), 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();

        if (c.mitosisProgress >= 1.0) {
          c.mitosisState = 'splitting';
          c.mitosisProgress = 0;
        }
      } else if (c.mitosisState === 'splitting') {
        c.mitosisProgress += 0.014;
        const daughterRadius = baseRadius;
        const separation = c.mitosisProgress * (daughterRadius * 2.8);
        const dx = Math.cos(c.splitAngle) * separation;
        const dy = Math.sin(c.splitAngle) * separation;

        ctx.beginPath();
        ctx.arc(c.x - (dx * 0.5), c.y - (dy * 0.5), daughterRadius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(c.x + (dx * 0.5), c.y + (dy * 0.5), daughterRadius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();

        if (c.mitosisProgress >= 1.0) {
          c.mitosisState = 'none';
          c.mitosisProgress = 0;
          c.x -= dx * 0.5;
          c.y -= dy * 0.5;
          c.vx = -Math.cos(c.splitAngle) * 0.08;
          c.vy = -Math.sin(c.splitAngle) * 0.08;
          spawnIndependentDaughter(c.x + dx, c.y + dy, c.splitAngle, c.currentLoad);
        }
      } else {
        ctx.beginPath();
        ctx.arc(c.x, c.y, Math.max(1.2, baseRadius), 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
      }

      ctx.restore();
    });

    for (let i = temporaryDaughters.length - 1; i >= 0; i--) {
      const d = temporaryDaughters[i];

      if (fluidMouse.active) {
        const dx = d.x - fluidMouse.x;
        const dy = d.y - fluidMouse.y;
        const dist = Math.hypot(dx, dy);

        if (dist < fluidMouse.radius && dist > 1) {
          const force = Math.pow(1 - dist / fluidMouse.radius, 2) * 0.22;
          d.fluidVx = (d.fluidVx || 0) + ((dx / dist) * force * 0.45) + (fluidMouse.vx * force * 0.12);
          d.fluidVy = (d.fluidVy || 0) + ((dy / dist) * force * 0.45) + (fluidMouse.vy * force * 0.12);
        }
      }

      d.fluidVx = (d.fluidVx || 0) * 0.82;
      d.fluidVy = (d.fluidVy || 0) * 0.82;

      d.x += d.vx + d.fluidVx;
      d.y += d.vy + d.fluidVy;

      if (d.x < -20) d.x = canvas.width + 20;
      if (d.x > canvas.width + 20) d.x = -20;
      if (d.y < -20) d.y = canvas.height + 20;
      if (d.y > canvas.height + 20) d.y = -20;

      const color = getContinuousColor(d.currentLoad);
      const baseRadius = 2.0 + (d.currentLoad / 100 * 2.6);

      ctx.save();
      if (d.currentLoad > 75) {
        ctx.shadowColor = color;
        ctx.shadowBlur = (d.currentLoad - 75) * 0.25;
      }

      if (d.deathState === 'none') {
        d.timeRemaining--;
        if (d.timeRemaining <= 0) {
          d.deathState = 'swelling';
          d.deathProgress = 0;
        }
        ctx.beginPath();
        ctx.arc(d.x, d.y, Math.max(1.2, baseRadius), 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
      } else if (d.deathState === 'swelling') {
        d.deathProgress += 0.035;
        const swellRadius = baseRadius * (1.0 + d.deathProgress * 0.7);
        ctx.beginPath();
        ctx.arc(d.x, d.y, swellRadius, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();

        if (d.deathProgress >= 1.0) {
          d.deathState = 'popping';
          d.popRadius = swellRadius;
          d.popAlpha = 0.85;
        }
      } else if (d.deathState === 'popping') {
        d.popRadius += 0.8;
        d.popAlpha -= 0.06;
