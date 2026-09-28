---
title: ""
layout: "single"
url: "/status/kiosk/"
summary: "Widescreen telemetry HUD for Mitchell Lab cluster compute."
---

<style>
  :root {
    --bg-base: #03060a;
    --card-bg: rgba(8, 14, 24, 0.85);
    --card-border: rgba(56, 189, 248, 0.2);
    --accent-cyan: #38bdf8;
    --accent-emerald: #10b981;
    --accent-purple: #c084fc;
    --accent-amber: #f59e0b;
    --accent-rose: #f43f5e;
    --accent-tumor: #ec4899;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --mono-font: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
  }

  html, body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none;
    -webkit-user-select: none;
    overflow-x: hidden !important;
  }

  /* RESET HUGO / WOWCHEMY PARENT WRAPPERS & REMOVE PAGE TITLE */
  .page-header, .navbar, .page-footer, .site-footer, footer, header, .docs-sidebar, .docs-toc,
  .article-header, .page-title, h1.article-title, .article-metadata {
    display: none !important;
  }
  .page-body, .universal-wrapper, .article-container, .docs-article-container, .container-fluid, .container, main, article {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: visible !important;
  }

  .hud-wrapper {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 100vh !important;
    box-sizing: border-box !important;
    padding: 12px 16px !important;
    display: flex !important;
    flex-direction: column !important;
    background-image: 
      radial-gradient(circle at 50% 0%, rgba(236, 72, 153, 0.08), transparent 60%),
      radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.05), transparent 50%),
      linear-gradient(to right, rgba(255,255,255,0.012) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.012) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 28px 28px, 28px 28px;
  }

  /* TOP COMMAND BANNER (WITH SUBTLE CELL BACKDROP) */
  .cluster-hud-header {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 12px;
    background: rgba(10, 16, 28, 0.78);
    border: 1px solid rgba(236, 72, 153, 0.28);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 14px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
    box-sizing: border-box;
    width: 100%;
    overflow: hidden;
  }

  #header-cell-canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
    opacity: 0.75;
  }

  .hud-top-bar {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 10px;
    gap: 14px;
    flex-wrap: wrap;
  }

  .hud-title-group {
    min-width: 0;
    flex: 1 1 auto;
  }

  .hud-title-group h1 {
    margin: 0;
    font-size: clamp(0.95rem, 2.5vw, 1.25rem);
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    line-height: 1.2;
    color: #ffffff !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.9);
  }

  .hud-subtitle {
    font-size: clamp(0.62rem, 1.8vw, 0.72rem);
    color: var(--accent-tumor);
    font-family: var(--mono-font);
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 3px;
    flex-wrap: wrap;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
  }

  .hud-activity-badge {
    background: rgba(0, 0, 0, 0.55);
    border: 1px solid rgba(236, 72, 153, 0.3);
    border-radius: 8px;
    padding: 4px 10px;
    font-family: var(--mono-font);
    font-size: 0.68rem;
    color: var(--accent-cyan);
    white-space: nowrap;
    backdrop-filter: blur(8px);
  }

  /* FLUID AGGREGATE STATS ROW */
  .hud-metrics-row {
    position: relative;
    z-index: 1;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    width: 100%;
    box-sizing: border-box;
  }

  .heatmap-legend {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.58rem;
    font-family: var(--mono-font);
    color: var(--text-muted);
    text-transform: none;
    letter-spacing: normal;
  }

  .legend-bar {
    width: 64px;
    height: 6px;
    border-radius: 3px;
    overflow: hidden;
    background: linear-gradient(to right, 
      rgb(40, 50, 70) 0%, 
      rgb(2, 132, 199) 20%, 
      rgb(16, 185, 129) 50%, 
      rgb(245, 158, 11) 75%, 
      rgb(236, 72, 153) 100%);
    background-repeat: no-repeat;
    background-size: 100% 100%;
    display: inline-block;
    vertical-align: middle;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.12);
  }

  @media (max-width: 900px) {
    .hud-metrics-row {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 480px) {
    .hud-metrics-row {
      grid-template-columns: 1fr;
    }
  }

  .hud-stat-box {
    background: rgba(4, 8, 16, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 8px;
    padding: 6px 10px;
    text-align: left;
    min-width: 0;
    overflow: hidden;
    backdrop-filter: blur(10px);
  }

  .hud-stat-box .val {
    font-size: clamp(0.90rem, 1.8vw, 1.15rem);
    font-weight: 800;
    color: var(--accent-cyan);
    font-family: var(--mono-font);
    line-height: 1.15;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .hud-stat-box .lbl {
    font-size: clamp(0.58rem, 1.2vw, 0.65rem);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-top: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* FLUID 4-COLUMN CARD GRID */
  .nodes-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    flex: 1;
    align-items: stretch;
    width: 100%;
    box-sizing: border-box;
  }

  @media (max-width: 1150px) {
    .nodes-grid { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 600px) {
    .nodes-grid { grid-template-columns: 1fr; }
  }

  .node-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 12px 14px;
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
  }

  .node-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-tumor), transparent);
    opacity: 0.6;
  }

  .node-card-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
    gap: 6px;
  }

  .node-name {
    font-size: 0.95rem;
    font-weight: 800;
    font-family: var(--mono-font);
    display: flex;
    align-items: center;
    gap: 6px;
    letter-spacing: 0.04em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--text-muted);
    flex-shrink: 0;
  }
  .status-dot.online {
    background: var(--accent-emerald);
    box-shadow: 0 0 8px var(--accent-emerald);
  }

  .node-submeta {
    font-size: 0.68rem;
    font-family: var(--mono-font);
    color: var(--text-secondary);
    white-space: nowrap;
    flex-shrink: 0;
  }

  .node-biometa {
    font-size: 0.62rem;
    font-family: var(--mono-font);
    color: var(--accent-cyan);
    margin-bottom: 6px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* JUPYTERHUB STATUS ROW */
  .service-status-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 5px;
    padding: 3px 8px;
    margin-bottom: 7px;
    font-family: var(--mono-font);
    font-size: 0.64rem;
  }

  .service-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-weight: 700;
    font-size: 0.60rem;
    letter-spacing: 0.04em;
  }

  .service-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--text-muted);
  }

  .service-dot.active {
    background: var(--accent-emerald);
    box-shadow: 0 0 6px var(--accent-emerald);
  }

  .service-dot.inactive {
    background: #64748b;
  }

  .net-hud-bar {
    background: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    padding: 4px 8px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    font-family: var(--mono-font);
    font-size: 0.65rem;
    white-space: nowrap;
    overflow: hidden;
  }

  .metric-block { margin-bottom: 6px; }

  .metric-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.68rem;
    margin-bottom: 3px;
    font-family: var(--mono-font);
    white-space: nowrap;
  }

  .track-bar {
    width: 100%;
    height: 5px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 2px;
    overflow: hidden;
  }

  .fill-bar {
    height: 100%;
    width: 0%;
    border-radius: 2px;
    transition: width 0.5s ease;
  }

  .fill-cpu  { background: linear-gradient(90deg, #ec4899, #f43f5e); }
  .fill-ram  { background: linear-gradient(90deg, #a855f7, #6366f1); }
  .fill-disk { background: linear-gradient(90deg, #10b981, #06b6d4); }

  .heatmap-wrap {
    margin-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    padding-top: 6px;
  }

  .section-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 4px;
    font-family: var(--mono-font);
    white-space: nowrap;
  }

  .core-grid {
    display: grid;
    gap: 2px;
    background: rgba(0, 0, 0, 0.3);
    padding: 3px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }

  .core-cell {
    aspect-ratio: 1;
    border-radius: 1px;
    background: rgb(40, 50, 70);
    border: 1px solid rgba(255, 255, 255, 0.04);
    transition: background-color 0.35s ease, box-shadow 0.35s ease;
  }

  .process-box {
    margin-top: 8px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    padding-top: 6px;
  }

  .process-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--mono-font);
    font-size: 0.65rem;
    table-layout: fixed;
  }

  .process-table th {
    text-align: left;
    color: var(--text-muted);
    font-weight: 500;
    padding-bottom: 2px;
    font-size: 0.58rem;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }

  .process-table td {
    padding: 2.5px 0;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .cpu-pill {
    background: rgba(236, 72, 153, 0.15);
    color: var(--accent-tumor);
    padding: 1px 3px;
    border-radius: 3px;
    font-weight: 700;
    font-size: 0.62rem;
  }

  /* NAS CLEAN BACKUP HUD BAR */
  .cloudsync-hud {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.28);
    border-radius: 8px;
    padding: 6px 10px;
    margin-top: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--mono-font);
  }

  .kiosk-btn {
    position: fixed;
    bottom: 12px;
    right: 12px;
    background: rgba(10, 16, 28, 0.85);
    color: var(--text-secondary);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.7rem;
    backdrop-filter: blur(8px);
    cursor: pointer;
    z-index: 100;
  }
</style>

<div class="hud-wrapper">
<div class="cluster-hud-header" id="hud-header-container">
<canvas id="header-cell-canvas"></canvas>
<div class="hud-top-bar">
<div class="hud-title-group">
<h1>OVERALL SIMULATION STATUS</h1>
<div class="hud-subtitle">
<span>SYSTEMS ONCOLOGY SERVERS</span> • <span id="hud-last-update">CONNECTING...</span>
</div>
</div>
<div class="hud-activity-badge" id="mitotic-index">Active Load: 0%</div>
</div>
<div class="hud-metrics-row">
<div class="hud-stat-box">
<div class="val" id="total-cores">192 Cores</div>
<div class="lbl">Compute Cores</div>
</div>
<div class="hud-stat-box">
<div class="val" id="total-ram-active">0 / 324 GB</div>
<div class="lbl">Cluster RAM</div>
</div>
<div class="hud-stat-box">
<div class="val" id="cluster-total-net">-- / --</div>
<div class="lbl">Network Traffic (Rx/Tx)</div>
</div>
<div class="hud-stat-box">
<div class="val" id="nas-sync-top">ONLINE</div>
<div class="lbl">Cloud Sync</div>
</div>
</div>
</div>
<div class="nodes-grid" id="kiosk-nodes-container"></div>
</div>

<button class="kiosk-btn" onclick="toggleFullScreen()">⛶ Fullscreen</button>

<script>
  const GIST_BASE = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw";

  const NODES = [
    { id: "simon", name: "HP-Z4", role: "Systems Oncology Compute", bioRole: "72 Cores • 62GB RAM",  hasJupyter: true,  cores: 72, columns: 12, apiVer: 3, url: "" },
    { id: "jlp",   name: "JLP",   role: "Systems Oncology Compute", bioRole: "104 Cores • 188GB RAM", hasJupyter: true,  cores: 104, columns: 13, apiVer: 3, url: "" },
    { id: "priti", name: "PRITI", role: "Systems Oncology Compute", bioRole: "12 Cores • 64GB RAM",  hasJupyter: true,  cores: 12, columns: 6,  apiVer: 3, url: "" },
    { id: "nas",   name: "NAS",   role: "Storage Node",            bioRole: "4 Cores • 23TB RAID",    hasJupyter: false, cores: 4, columns: 4,  apiVer: 4, url: "" }
  ];

  const clusterState = {
      mem: { simon: 0, jlp: 0, priti: 0, nas: 0 },
      netRx: { simon: 0, jlp: 0, priti: 0, nas: 0 },
      netTx: { simon: 0, jlp: 0, priti: 0, nas: 0 },
      cpu: { simon: 0, jlp: 0, priti: 0, nas: 0 },
      cpuAvg: 0,
      cpuMax: 0
    };

  // --- CONTINUOUS COLOR INTERPOLATION ---
  const COLOR_STOPS = [
    { p: 0.00, r: 40,  g: 50,  b: 70  }, // 0%: Idle Slate
    { p: 0.20, r: 2,   g: 132, b: 199 }, // 20%: Cyan/Blue
    { p: 0.50, r: 16,  g: 185, b: 129 }, // 50%: Emerald
    { p: 0.75, r: 245, g: 158, b: 11  }, // 75%: Amber
    { p: 1.00, r: 236, g: 72,  b: 153 }  // 100%: Mitotic Peak Pink
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

  function toggleFullScreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(()=>{});
    } else {
      document.exitFullscreen().catch(()=>{});
    }
  }

  function formatBytesSec(bytes) {
    if (!bytes || bytes <= 0) return "0 B/s";
    const k = 1024;
    const sizes = ['B/s', 'KB/s', 'MB/s', 'GB/s'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  }

 // --- AMBIENT HEADER CELL SIMULATION CANVAS (1:1 CORE MAPPED) ---
  const headerContainer = document.getElementById("hud-header-container");
  const canvas = document.getElementById("header-cell-canvas");
  const ctx = canvas.getContext("2d");

  function resizeCanvas() {
    canvas.width = headerContainer.clientWidth;
    canvas.height = headerContainer.clientHeight;
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  // Cluster core registry: exactly 192 cores
  const clusterCorePool = {};
  NODES.forEach(n => {
    clusterCorePool[n.id] = new Array(n.cores).fill(0);
  });

 // Spawn exactly 1 cell for every core in the cluster (192 total)
  let cellIndex = 0;
  const cells = [];
  NODES.forEach(n => {
    for (let c = 0; c < n.cores; c++) {
      cells.push({
        id: cellIndex++,
        nodeId: n.id,
        coreIdx: c,
        x: Math.random() * (canvas.width || 800),
        y: Math.random() * (canvas.height || 120),
        // Gentle baseline velocity
        baseVx: (Math.random() - 0.5) * 0.18,
        baseVy: (Math.random() - 0.5) * 0.18,
        currentLoad: 0
      });
    }
  });

  function animateHeaderCells() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    cells.forEach(c => {
      // 1. Fetch real-time core load reported by Glances
      const targetLoad = (clusterCorePool[c.nodeId] && clusterCorePool[c.nodeId][c.coreIdx] !== undefined)
        ? clusterCorePool[c.nodeId][c.coreIdx]
        : 0;

      // 2. Smoothly ease toward real-time core load (no instant jumps)
      c.currentLoad += (targetLoad - c.currentLoad) * 0.08;

      // 3. Calm speed curve:
      // Idle: 0.2x speed | Peak (100%): 0.85x speed (subtle, non-distracting drift)
      const loadNorm = c.currentLoad / 100;
      const speedMult = 0.20 + (loadNorm * 0.65);

      c.x += c.baseVx * speedMult;
      c.y += c.baseVy * speedMult;

      // Wrap-around bounds smoothly
      if (c.x < -15) c.x = canvas.width + 15;
      if (c.x > canvas.width + 15) c.x = -15;
      if (c.y < -15) c.y = canvas.height + 15;
      if (c.y > canvas.height + 15) c.y = -15;

      // 4. Exact continuous color matching with core heatmaps
      const color = getContinuousColor(c.currentLoad);

      // 5. Purely telemetry-driven size (NO artificial sine pulse)
      // Idle (0%): 2.2px -> Peak (100%): 5.2px
      const radius = 2.2 + (loadNorm * 3.0);

      // Soft ambient glow only for heavy/saturated compute
      const glow = c.currentLoad > 75 ? (c.currentLoad - 75) * 0.25 : 0;

      ctx.beginPath();
      ctx.arc(c.x, c.y, radius, 0, Math.PI * 2);
      ctx.fillStyle = color;
      if (glow > 0) {
        ctx.shadowColor = color;
        ctx.shadowBlur = glow;
      } else {
        ctx.shadowBlur = 0;
      }
      ctx.fill();
    });

    requestAnimationFrame(animateHeaderCells);
  }
  requestAnimationFrame(animateHeaderCells);

  // --- TASK CLASSIFIER ---
  function classifyBioTask(cmdName, cmdLine = "") {
    const full = (cmdName + " " + cmdLine).toLowerCase();
    
    if (full.includes("julia")) {
      return { tag: "ODE Solving", icon: "🧬" };
    }
    
    if (full.includes("python") || full.includes("python3") ||
        full.includes("rscript") || full.includes("r.bin") ||
        full.includes("nextflow") || full.includes("snakemake") ||
        full.includes("bwa") || full.includes("samtools") ||
        full.includes("bedtools") || full.includes("bowtie")) {
      return { tag: "Data Processing", icon: "📊" };
    }
    
    if (full.includes("cloudsync") || full.includes("rsync") || full.includes("syno")) {
      return { tag: "Cloud Sync", icon: "💾" };
    }

    return { tag: "General Computing", icon: "⚙️" };
  }

  function renderKioskCards() {
    const container = document.getElementById("kiosk-nodes-container");
    container.innerHTML = "";

    NODES.forEach(n => {
      const isNas = n.id === "nas";
      const card = document.createElement("div");
      card.className = "node-card";
      card.id = `card-${n.id}`;

      const syncSnippet = isNas ? `
        <div class="cloudsync-hud" id="nas-sync-banner">
          <div style="font-size:0.64rem; font-weight:700; color:#10b981;" id="nas-sync-state-txt">BACKUP: SUCCESSFUL</div>
          <div id="nas-sync-time" style="font-size:0.65rem; color:#94a3b8; text-align:right; white-space:nowrap;">Last: --</div>
        </div>
      ` : "";

      const jupyterSnippet = n.hasJupyter ? `
        <div class="service-status-bar">
          <span style="color:var(--text-muted);">JupyterHub</span>
          <span class="service-pill" id="jup-pill-${n.id}" style="color:#64748b;">
            <span class="service-dot inactive" id="jup-dot-${n.id}"></span>
            <span id="jup-txt-${n.id}">CHECKING</span>
          </span>
        </div>
      ` : "";

      card.innerHTML = `
        <div>
          <div class="node-card-head">
            <div class="node-name">
              <span class="status-dot" id="dot-${n.id}"></span>
              ${n.name}
            </div>
            <span class="node-submeta" id="uptime-${n.id}">--</span>
          </div>

          <div class="node-biometa">${n.bioRole}</div>

          ${jupyterSnippet}

          <div class="net-hud-bar">
            <span>↓ Rx: <b id="net-rx-${n.id}" style="color:var(--accent-emerald);">0 B/s</b></span>
            <span>↑ Tx: <b id="net-tx-${n.id}" style="color:var(--accent-cyan);">0 B/s</b></span>
          </div>

          <div class="metric-block">
            <div class="metric-row">
              <span>CPU LOAD</span>
              <span id="cpu-txt-${n.id}">--%</span>
            </div>
            <div class="track-bar">
              <div class="fill-bar fill-cpu" id="cpu-bar-${n.id}"></div>
            </div>
          </div>

          <div class="metric-block">
            <div class="metric-row">
              <span>RAM USAGE</span>
              <span id="ram-txt-${n.id}">-- GB</span>
            </div>
            <div class="track-bar">
              <div class="fill-bar fill-ram" id="ram-bar-${n.id}"></div>
            </div>
          </div>

          <div class="metric-block">
            <div class="metric-row">
              <span>STORAGE</span>
              <span id="disk-txt-${n.id}">--</span>
            </div>
            <div class="track-bar">
              <div class="fill-bar fill-disk" id="disk-bar-${n.id}"></div>
            </div>
          </div>

          ${syncSnippet}

          <div class="heatmap-wrap">
            <div class="section-label">
              <span>Cores (${n.cores})</span>
              <div class="heatmap-legend">
                <span>0%</span>
                <span class="legend-bar"></span>
                <span>100%</span>
              </div>
            </div>
            <div class="core-grid" id="grid-${n.id}" style="grid-template-columns: repeat(${n.columns}, 1fr);">
              ${Array.from({ length: n.cores }).map((_, i) => `<div class="core-cell" id="core-${n.id}-${i}"></div>`).join('')}
            </div>
          </div>
        </div>

        <div class="process-box">
          <div class="section-label">Top Tasks</div>
          <table class="process-table">
            <thead>
              <tr>
                <th style="width: 25%;">PID</th>
                <th style="width: 50%;">TASK</th>
                <th style="width: 25%; text-align:right;">CPU</th>
              </tr>
            </thead>
            <tbody id="proc-tbody-${n.id}">
              <tr><td colspan="3" style="color:var(--text-muted);">Polling processes...</td></tr>
            </tbody>
          </table>
        </div>
      `;

      container.appendChild(card);
    });
  }

 function updateClusterAggregates() {
    const totalUsed = Object.values(clusterState.mem).reduce((a, b) => a + b, 0);
    const ramEl = document.getElementById("total-ram-active");
    if (ramEl) ramEl.innerText = `${totalUsed.toFixed(0)} / 324 GB`;

    const sumRx = Object.values(clusterState.netRx).reduce((a, b) => a + b, 0);
    const sumTx = Object.values(clusterState.netTx).reduce((a, b) => a + b, 0);
    const netEl = document.getElementById("cluster-total-net");
    if (netEl) netEl.innerText = `↓${formatBytesSec(sumRx)} ↑${formatBytesSec(sumTx)}`;

    let weightedCpuSum = 0;
    let totalCores = 0;
    let maxLoad = 0;

    NODES.forEach(n => {
      const load = clusterState.cpu[n.id] || 0;
      weightedCpuSum += (load * n.cores);
      totalCores += n.cores;
      if (load > maxLoad) maxLoad = load;
    });

    clusterState.cpuAvg = totalCores > 0 ? (weightedCpuSum / totalCores) : 0;
    clusterState.cpuMax = maxLoad;

    const mitEl = document.getElementById("mitotic-index");
    if (mitEl) {
      const roundedCpu = Math.round(clusterState.cpuAvg);
      mitEl.innerText = `Active Load: ${roundedCpu}%`;
    }
  }

  async function fetchTelemetry(node) {
    if (!node.url) return;
    const base = `${node.url}/api/${node.apiVer}`;

    try {
      const [cpu, mem, fs, upt, cpus, procs, load, net] = await Promise.all([
        fetch(`${base}/quicklook`).then(r => r.json()).catch(() => ({})),
        fetch(`${base}/mem`).then(r => r.json()).catch(() => ({})),
        fetch(`${base}/fs`).then(r => r.json()).catch(() => []),
        fetch(`${base}/uptime`).then(r => r.json()).catch(() => "ONLINE"),
        fetch(`${base}/percpu`).then(r => r.json()).catch(() => []),
        fetch(`${base}/processlist`).then(r => r.json()).catch(() => []),
        fetch(`${base}/load`).then(r => r.json()).catch(() => ({})),
        fetch(`${base}/network`).then(r => r.json()).catch(() => [])
      ]);

      const dotEl = document.getElementById(`dot-${node.id}`);
      if (dotEl) dotEl.className = "status-dot online";
      
      const uptEl = document.getElementById(`uptime-${node.id}`);
      if (uptEl) uptEl.innerText = upt || "ONLINE";

      // JupyterHub Detection
      if (node.hasJupyter && Array.isArray(procs)) {
        const jupDot = document.getElementById(`jup-dot-${node.id}`);
        const jupTxt = document.getElementById(`jup-txt-${node.id}`);
        const jupPill = document.getElementById(`jup-pill-${node.id}`);
        
        const isJupyterRunning = procs.some(p => {
          const combined = ((p.name || '') + ' ' + (p.cmdline || '')).toLowerCase();
          return combined.includes('jupyterhub') || combined.includes('jupyter-lab') || combined.includes('jupyter-server');
        });

        if (jupDot && jupTxt && jupPill) {
          if (isJupyterRunning) {
            jupDot.className = "service-dot active";
            jupTxt.innerText = "ACTIVE";
            jupPill.style.color = "#10b981";
          } else {
            jupDot.className = "service-dot inactive";
            jupTxt.innerText = "INACTIVE";
            jupPill.style.color = "#64748b";
          }
        }
      }

      // Top Processes Table
      const tbody = document.getElementById(`proc-tbody-${node.id}`);
      if (tbody && Array.isArray(procs) && procs.length > 0) {
        const sorted = [...procs]
          .sort((a, b) => (b.cpu_percent || 0) - (a.cpu_percent || 0))
          .slice(0, 4);

        tbody.innerHTML = sorted.map(p => {
          const cpuUsage = (p.cpu_percent || 0).toFixed(1);
          const rawCmd = (p.name || "task").replace(/^.*\//, '');
          const bioInfo = classifyBioTask(rawCmd, p.cmdline || "");
          return `
            <tr>
              <td style="color:var(--text-muted); font-size:0.60rem;">${p.pid}</td>
              <td style="color:#e2e8f0; font-weight:600;" title="${rawCmd}">
                <span style="color:var(--accent-tumor); font-size:0.58rem; display:block; text-transform:uppercase;">${bioInfo.icon} ${bioInfo.tag}</span>
                ${rawCmd}
              </td>
              <td style="text-align:right;">
                <span class="cpu-pill">${cpuUsage}%</span>
              </td>
            </tr>
          `;
        }).join('');
      }

      // Network Traffic
      if (Array.isArray(net) && net.length > 0) {
        let totalRx = 0, totalTx = 0;
        net.forEach(iface => {
          if (iface.interface_name && !iface.interface_name.startsWith('lo') && !iface.interface_name.startsWith('docker')) {
            totalRx += (iface.rx || 0);
            totalTx += (iface.tx || 0);
          }
        });
        clusterState.netRx[node.id] = totalRx;
        clusterState.netTx[node.id] = totalTx;
        const rxEl = document.getElementById(`net-rx-${node.id}`);
        const txEl = document.getElementById(`net-tx-${node.id}`);
        if (rxEl) rxEl.innerText = formatBytesSec(totalRx);
        if (txEl) txEl.innerText = formatBytesSec(totalTx);
      }

      // CPU Load Tracking
      const cpuVal = Math.round(cpu.cpu ?? 0);
      clusterState.cpu[node.id] = cpuVal;
      const cpuTxt = document.getElementById(`cpu-txt-${node.id}`);
      const cpuBar = document.getElementById(`cpu-bar-${node.id}`);
      if (cpuTxt) cpuTxt.innerText = `${cpuVal}%`;
      if (cpuBar) cpuBar.style.width = `${cpuVal}%`;

      // RAM
      if (mem && mem.used && mem.total) {
        const usedGbNum = mem.used / (1024 ** 3);
        const totalGbNum = mem.total / (1024 ** 3);
        clusterState.mem[node.id] = usedGbNum;
        const ramTxt = document.getElementById(`ram-txt-${node.id}`);
        const ramBar = document.getElementById(`ram-bar-${node.id}`);
        if (ramTxt) ramTxt.innerText = `${usedGbNum.toFixed(1)} / ${totalGbNum.toFixed(1)} GB`;
        if (ramBar) ramBar.style.width = `${Math.round((mem.used/mem.total)*100)}%`;
      }

      // Load average
      if (load && load.min15 !== undefined) {
        const loadAvgEl = document.getElementById(`load-avg-${node.id}`);
        if (loadAvgEl) loadAvgEl.innerText = `15m: ${Number(load.min15).toFixed(1)}`;
      }

      // Storage
      if (Array.isArray(fs) && fs.length > 0) {
        const root = fs.find(d => d.mnt_point === "/" || d.mnt_point === "/volume1") || fs[0];
        if (root) {
          const dUsed = (root.used / (1024 ** 4) >= 1) ? `${(root.used / (1024 ** 4)).toFixed(1)} TB` : `${Math.round(root.used / (1024 ** 3))} GB`;
          const dTotal = (root.size / (1024 ** 4) >= 1) ? `${(root.size / (1024 ** 4)).toFixed(1)} TB` : `${Math.round(root.size / (1024 ** 3))} GB`;
          const diskTxt = document.getElementById(`disk-txt-${node.id}`);
          const diskBar = document.getElementById(`disk-bar-${node.id}`);
          if (diskTxt) diskTxt.innerText = `${dUsed} / ${dTotal}`;
          if (diskBar) diskBar.style.width = `${root.percent}%`;
        }
      }

  // Continuous Core Heatmap Rendering & Cell Pool Synchronization
      if (Array.isArray(cpus) && cpus.length > 0) {
        cpus.forEach((core, i) => {
          const loadVal = (typeof core.total === 'number') ? core.total : (100 - (core.idle ?? 100));

          // Pipe directly to the header simulation
          if (clusterCorePool[node.id] && clusterCorePool[node.id][i] !== undefined) {
            clusterCorePool[node.id][i] = loadVal;
          }

          const el = document.getElementById(`core-${node.id}-${i}`);
          if (el) {
            const color = getContinuousColor(loadVal);
            el.style.backgroundColor = color;
            el.style.boxShadow = loadVal > 65 ? `0 0 6px ${color}` : "none";
          }
        });
      }

      updateClusterAggregates();
    } catch (e) {
      console.warn(`Telemetry error on node ${node.id}:`, e);
      const dotEl = document.getElementById(`dot-${node.id}`);
      if (dotEl) dotEl.className = "status-dot";
      if (node.hasJupyter) {
        const jupDot = document.getElementById(`jup-dot-${node.id}`);
        const jupTxt = document.getElementById(`jup-txt-${node.id}`);
        if (jupDot) jupDot.className = "service-dot inactive";
        if (jupTxt) jupTxt.innerText = "OFFLINE";
      }
    }
  }

  async function updateCloudSync() {
    try {
      const res = await fetch(`${GIST_BASE}/cloudsync.json?t=${Date.now()}`);
      if (!res.ok) return;
      const sync = await res.json();

      const banner = document.getElementById("nas-sync-banner");
      const stateTxt = document.getElementById("nas-sync-state-txt");
      const timeEl = document.getElementById("nas-sync-time");
      const topSync = document.getElementById("nas-sync-top");

      if (sync.state === "success") {
        if (banner) banner.style.borderColor = "rgba(16, 185, 129, 0.4)";
        if (topSync) { 
          topSync.innerText = "SUCCESS"; 
          topSync.style.color = "#10b981"; 
        }
        if (stateTxt) {
          stateTxt.innerText = "BACKUP: SUCCESSFUL";
          stateTxt.style.color = "#10b981";
        }
        if (timeEl) timeEl.innerText = `Last: ${sync.last_synced || 'Recently'}`;
      } else {
        if (banner) banner.style.borderColor = "rgba(244, 63, 94, 0.4)";
        if (topSync) { 
          topSync.innerText = "FAILED"; 
          topSync.style.color = "#f43f5e"; 
        }
        if (stateTxt) {
          stateTxt.innerText = "BACKUP: FAILED";
          stateTxt.style.color = "#f43f5e";
        }
        if (timeEl) timeEl.innerText = `Errors: ${sync.recent_errors || 1}`;
      }
    } catch(e) {}
  }

  async function initKiosk() {
    renderKioskCards();

    try {
      const res = await fetch(`${GIST_BASE}/endpoints.json?t=${Date.now()}`);
      const endpoints = await res.json();
      NODES.forEach(n => {
        if (endpoints[n.id]) n.url = endpoints[n.id].replace(/\/+$/, "");
      });
    } catch(e) {}

    const refreshAll = () => {
      NODES.forEach(fetchTelemetry);
      const now = new Date();
      document.getElementById("hud-last-update").innerText = `CONNECTED // ${now.toLocaleTimeString()}`;
    };

    refreshAll();
    updateCloudSync();

    setInterval(refreshAll, 2500);
    setInterval(updateCloudSync, 20000);
  }

  window.addEventListener("DOMContentLoaded", initKiosk);
</script>
