---
title: "Mitchell Lab Telemetry HUD"
layout: "single"
url: "/status/kiosk/"
summary: "Widescreen wall telemetry HUD for Mitchell Lab cluster compute."
---



<style>
  :root {
    --bg-base: #04070d;
    --card-bg: rgba(10, 16, 28, 0.82);
    --card-border: rgba(56, 189, 248, 0.18);
    --accent-cyan: #38bdf8;
    --accent-emerald: #10b981;
    --accent-purple: #c084fc;
    --accent-amber: #fbbf24;
    --accent-rose: #f43f5e;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --mono-font: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
  }

  

/* ========================================================
     WOWCHEMY / ACADEMIC FULLSCREEN BREAKOUT
     ======================================================== */
  /* 1. Unlock the body and main viewport */
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100vw !important;
    max-width: 100vw !important;
    background-color: #04070d !important;
    overflow-x: hidden !important;
  }

  /* 2. Strip Wowchemy navigation bar and footer */
  .page-header, 
  .navbar, 
  .page-footer, 
  .site-footer, 
  footer, 
  header,
  .docs-sidebar, 
  .docs-toc {
    display: none !important;
  }

  /* 3. Strip padding, margins, and width clamps from EVERY Wowchemy parent */
  .page-body,
  .universal-wrapper,
  .article-container,
  .docs-article-container,
  .container-fluid,
  .container,
  main,
  article {
    max-width: 100vw !important;
    width: 100vw !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: visible !important;
  }

  /* 4. Let the dashboard fill the entire screen edge-to-edge */
  .hud-wrapper {
    width: 100vw !important;
    max-width: 100vw !important;
    min-height: 100vh !important;
    box-sizing: border-box !important;
    padding: 16px 20px !important;
    display: flex !important;
    flex-direction: column !important;
  }

  /* Optional: Hide site header/navbar and footer on kiosk mode so it's a true dashboard */
  header, footer, nav, .header, .footer, .nav {
    display: none !important;
  }

  /* TOP AGGREGATE OPERATIONS BANNER */
  .cluster-hud-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(13, 20, 36, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.28);
    border-radius: 12px;
    padding: 12px 22px;
    margin-bottom: 16px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    flex-wrap: nowrap;
    gap: 16px;
  }

  .hud-title-group {
    flex-shrink: 0;
    white-space: nowrap;
  }

  .hud-title-group h1 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 900;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 10px;
    white-space: nowrap;
  }

  .hud-status-line {
    margin: 3px 0 0 0;
    font-size: 0.72rem;
    color: var(--text-secondary);
    font-family: var(--mono-font);
    white-space: nowrap;
  }

  .hud-metrics-row {
    display: flex;
    gap: 24px;
    flex-shrink: 0;
    align-items: center;
  }

  .hud-stat-box {
    text-align: right;
    white-space: nowrap;
  }

  .hud-stat-box .val {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--accent-cyan);
    font-family: var(--mono-font);
    line-height: 1.1;
    white-space: nowrap;
  }

  .hud-stat-box .lbl {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-top: 2px;
    white-space: nowrap;
  }

  /* TRUE WIDESCREEN 4-COLUMN GRID */
  .nodes-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    flex: 1;
    align-items: stretch;
  }

  @media (max-width: 1023px) {
    .nodes-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  @media (max-width: 640px) {
    .nodes-grid {
      grid-template-columns: 1fr;
    }
  }

  .node-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 14px;
    backdrop-filter: blur(14px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.45);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .node-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    opacity: 0.5;
  }

  .node-card-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }

  .node-name {
    font-size: 1rem;
    font-weight: 800;
    font-family: var(--mono-font);
    display: flex;
    align-items: center;
    gap: 7px;
    letter-spacing: 0.04em;
    white-space: nowrap;
  }

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--text-muted);
    flex-shrink: 0;
  }
  .status-dot.online {
    background: var(--accent-emerald);
    box-shadow: 0 0 8px var(--accent-emerald);
  }

  .node-submeta {
    font-size: 0.7rem;
    font-family: var(--mono-font);
    color: var(--text-secondary);
    white-space: nowrap;
  }

  /* METRICS & PROGRESS */
  .metric-block {
    margin-bottom: 8px;
  }

  .metric-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
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

  .fill-cpu  { background: linear-gradient(90deg, #38bdf8, #818cf8); }
  .fill-ram  { background: linear-gradient(90deg, #c084fc, #f43f5e); }
  .fill-disk { background: linear-gradient(90deg, #10b981, #06b6d4); }

  /* CORE HEATMAP MATRIX */
  .heatmap-wrap {
    margin-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    padding-top: 8px;
  }

  .section-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    margin-bottom: 5px;
    font-family: var(--mono-font);
    white-space: nowrap;
  }

  .core-grid {
    display: grid;
    gap: 2px;
    background: rgba(0, 0, 0, 0.25);
    padding: 4px;
    border-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }

  .core-cell {
    aspect-ratio: 1;
    border-radius: 1px;
    background: rgba(255, 255, 255, 0.04);
    transition: background 0.25s ease, box-shadow 0.25s ease;
  }

  /* TOP PROCESS LIST */
  .process-box {
    margin-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
    padding-top: 8px;
  }

  .process-table {
    width: 100%;
    border-collapse: collapse;
    font-family: var(--mono-font);
    font-size: 0.7rem;
    table-layout: fixed;
  }

  .process-table th {
    text-align: left;
    color: var(--text-muted);
    font-weight: 500;
    padding-bottom: 3px;
    font-size: 0.62rem;
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

  .process-table tr:hover td {
    color: var(--text-primary);
  }

  .cpu-pill {
    background: rgba(56, 189, 248, 0.12);
    color: var(--accent-cyan);
    padding: 1px 3px;
    border-radius: 3px;
    font-weight: 700;
    font-size: 0.65rem;
  }

  .cpu-pill.high {
    background: rgba(244, 63, 94, 0.18);
    color: var(--accent-rose);
  }

  /* CLOUDSYNC SPECIAL BADGE */
  .cloudsync-hud {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.28);
    border-radius: 8px;
    padding: 7px 10px;
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
    background: rgba(15, 23, 42, 0.75);
    color: var(--text-secondary);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.72rem;
    backdrop-filter: blur(8px);
    cursor: pointer;
    z-index: 100;
  }
</style>

<div class="hud-wrapper">
  <!-- Cluster Header Banner -->
  <div class="cluster-hud-header">
    <div class="hud-title-group">
      <h1>
        <span style="color:var(--accent-cyan);">⚡</span> MITCHELL LAB CLUSTER
      </h1>
      <div class="hud-status-line" id="hud-last-update">CONNECTING TO HIGH-THROUGHPUT MESH...</div>
    </div>
    <div class="hud-metrics-row">
      <div class="hud-stat-box">
        <div class="val" id="total-cores">192</div>
        <div class="lbl">Threads / Cores</div>
      </div>
      <div class="hud-stat-box">
        <div class="val" id="total-ram-active">0 / 324 GB</div>
        <div class="lbl">Cluster RAM</div>
      </div>
      <div class="hud-stat-box">
        <div class="val" id="cluster-active-procs">--</div>
        <div class="lbl">Active Procs</div>
      </div>
      <div class="hud-stat-box">
        <div class="val" id="nas-sync-top">ONLINE</div>
        <div class="lbl">Cloud Sync</div>
      </div>
    </div>
  </div>

  <!-- Dynamic Nodes Container (4 Columns) -->
  <div class="nodes-grid" id="kiosk-nodes-container"></div>
</div>

<button class="kiosk-btn" onclick="toggleFullScreen()">⛶ Fullscreen</button>

<script>
  const GIST_BASE = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw";

  const NODES = [
    { id: "simon", name: "SIMON", role: "Gateway", specs: "72C • 62GB", cores: 72, columns: 12, apiVer: 3, url: "" },
    { id: "jlp",   name: "JLP",   role: "Compute", specs: "104C • 188GB", cores: 104, columns: 13, apiVer: 3, url: "" },
    { id: "priti", name: "PRITI", role: "Compute", specs: "12C • 64GB", cores: 12, columns: 6,  apiVer: 3, url: "" },
    { id: "nas",   name: "NAS",   role: "Storage", specs: "4C • 23TB Btrfs", cores: 4, columns: 4,  apiVer: 4, url: "" }
  ];

  const clusterState = {
    mem: { simon: 0, jlp: 0, priti: 0, nas: 0 },
    procs: { simon: 0, jlp: 0, priti: 0, nas: 0 }
  };

  function toggleFullScreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(()=>{});
    } else {
      document.exitFullscreen().catch(()=>{});
    }
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
          <div style="overflow:hidden;">
            <div style="font-size:0.62rem; color:#6ee7b7; letter-spacing:0.06em;">CLOUD SYNC ENGINE</div>
            <div id="nas-sync-file" style="font-size:0.72rem; color:#e2e8f0; font-weight:600; max-width:140px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">Syncing...</div>
          </div>
          <div id="nas-sync-time" style="font-size:0.66rem; color:#94a3b8; text-align:right; white-space:nowrap;">--</div>
        </div>
      ` : "";

      card.innerHTML = `
        <div>
          <div class="node-card-head">
            <div class="node-name">
              <span class="status-dot" id="dot-${n.id}"></span>
              ${n.name} <span style="font-size:0.72rem; color:var(--text-muted); font-weight:400;">(${n.role})</span>
            </div>
            <span class="node-submeta" id="uptime-${n.id}">--</span>
          </div>

          <div class="metric-block">
            <div class="metric-row">
              <span>CPU POOL</span>
              <span id="cpu-txt-${n.id}">--%</span>
            </div>
            <div class="track-bar">
              <div class="fill-bar fill-cpu" id="cpu-bar-${n.id}"></div>
            </div>
          </div>

          <div class="metric-block">
            <div class="metric-row">
              <span>MEMORY</span>
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
              <span>Active Threads (${n.cores} Cores)</span>
              <span id="load-avg-${n.id}">L: --</span>
            </div>
            <div class="core-grid" id="grid-${n.id}" style="grid-template-columns: repeat(${n.columns}, 1fr);">
              ${Array.from({ length: n.cores }).map((_, i) => `<div class="core-cell" id="core-${n.id}-${i}"></div>`).join('')}
            </div>
          </div>
        </div>

        <div class="process-box">
          <div class="section-label">Top Compute Tasks</div>
          <table class="process-table">
            <thead>
              <tr>
                <th style="width: 25%;">PID</th>
                <th style="width: 45%;">COMMAND</th>
                <th style="width: 30%; text-align:right;">%CPU</th>
              </tr>
            </thead>
            <tbody id="proc-tbody-${n.id}">
              <tr><td colspan="3" style="color:var(--text-muted);">Polling process tree...</td></tr>
            </tbody>
          </table>
        </div>
      `;

      container.appendChild(card);
    });
  }

  function getHeatmapColor(load) {
    if (load < 5)   return "rgba(255, 255, 255, 0.04)";
    if (load < 30)  return "#0284c7";
    if (load < 70)  return "#10b981";
    if (load < 90)  return "#f59e0b";
    return "#f43f5e";
  }

  function updateClusterAggregates() {
    const totalUsed = Object.values(clusterState.mem).reduce((a, b) => a + b, 0);
    const ramEl = document.getElementById("total-ram-active");
    if (ramEl) ramEl.innerText = `${totalUsed.toFixed(0)} / 324 GB`;

    const totalProcs = Object.values(clusterState.procs).reduce((a, b) => a + b, 0);
    const procEl = document.getElementById("cluster-active-procs");
    if (procEl) procEl.innerText = totalProcs > 0 ? `${totalProcs} tasks` : "--";
  }

  async function fetchTelemetry(node) {
    if (!node.url) return;
    const base = `${node.url}/api/${node.apiVer}`;

    try {
      const [cpu, mem, fs, upt, cpus, procs, load] = await Promise.all([
        fetch(`${base}/quicklook`).then(r => r.json()).catch(() => ({})),
        fetch(`${base}/mem`).then(r => r.json()).catch(() => ({})),
        fetch(`${base}/fs`).then(r => r.json()).catch(() => []),
        fetch(`${base}/uptime`).then(r => r.json()).catch(() => "ONLINE"),
        fetch(`${base}/percpu`).then(r => r.json()).catch(() => []),
        fetch(`${base}/processlist`).then(r => r.json()).catch(() => []),
        fetch(`${base}/load`).then(r => r.json()).catch(() => ({}))
      ]);

      document.getElementById(`dot-${node.id}`).className = "status-dot online";
      document.getElementById(`uptime-${node.id}`).innerText = upt || "ONLINE";

      // CPU
      const cpuVal = Math.round(cpu.cpu || 0);
      document.getElementById(`cpu-txt-${node.id}`).innerText = `${cpuVal}%`;
      document.getElementById(`cpu-bar-${node.id}`).style.width = `${cpuVal}%`;

      // RAM
      if (mem.used && mem.total) {
        const usedGbNum = mem.used / (1024 ** 3);
        const totalGbNum = mem.total / (1024 ** 3);
        clusterState.mem[node.id] = usedGbNum;
        document.getElementById(`ram-txt-${node.id}`).innerText = `${usedGbNum.toFixed(1)} / ${totalGbNum.toFixed(1)} GB (${Math.round((mem.used/mem.total)*100)}%)`;
        document.getElementById(`ram-bar-${node.id}`).style.width = `${Math.round((mem.used/mem.total)*100)}%`;
      }

      // Load average
      if (load && load.min15 !== undefined) {
        document.getElementById(`load-avg-${node.id}`).innerText = `15m: ${Number(load.min15).toFixed(1)}`;
      }

      // Storage
      if (Array.isArray(fs) && fs.length > 0) {
        const root = fs.find(d => d.mnt_point === "/" || d.mnt_point === "/volume1") || fs[0];
        const dUsed = (root.used / (1024 ** 4) >= 1) ? `${(root.used / (1024 ** 4)).toFixed(1)} TB` : `${Math.round(root.used / (1024 ** 3))} GB`;
        const dTotal = (root.size / (1024 ** 4) >= 1) ? `${(root.size / (1024 ** 4)).toFixed(1)} TB` : `${Math.round(root.size / (1024 ** 3))} GB`;
        document.getElementById(`disk-txt-${node.id}`).innerText = `${dUsed} / ${dTotal}`;
        document.getElementById(`disk-bar-${node.id}`).style.width = `${root.percent}%`;
      }

      // Heatmap Grid
      if (Array.isArray(cpus)) {
        cpus.forEach((core, i) => {
          const el = document.getElementById(`core-${node.id}-${i}`);
          if (el) {
            const loadVal = core.total || 0;
            el.style.background = getHeatmapColor(loadVal);
            el.style.boxShadow = loadVal > 60 ? `0 0 5px ${getHeatmapColor(loadVal)}` : "none";
          }
        });
      }

      // Top Processes (Sorted by CPU, top 4)
      if (Array.isArray(procs) && procs.length > 0) {
        clusterState.procs[node.id] = procs.length;
        const sorted = [...procs]
          .sort((a, b) => (b.cpu_percent || 0) - (a.cpu_percent || 0))
          .slice(0, 4);

        const tbody = document.getElementById(`proc-tbody-${node.id}`);
        if (tbody) {
          tbody.innerHTML = sorted.map(p => {
            const cpuUsage = (p.cpu_percent || 0).toFixed(1);
            const isHigh = p.cpu_percent > 30;
            const cmdName = (p.name || p.cmdline || "task").replace(/^.*\//, '');
            return `
              <tr>
                <td style="color:var(--text-muted);">${p.pid || '--'}</td>
                <td style="color:#e2e8f0; font-weight:600;" title="${cmdName}">${cmdName}</td>
                <td style="text-align:right;">
                  <span class="cpu-pill ${isHigh ? 'high' : ''}">${cpuUsage}%</span>
                </td>
              </tr>
            `;
          }).join('');
        }
      }

      updateClusterAggregates();
    } catch (e) {
      document.getElementById(`dot-${node.id}`).className = "status-dot";
    }
  }

  async function updateCloudSync() {
    try {
      const res = await fetch(`${GIST_BASE}/cloudsync.json?t=${Date.now()}`);
      if (!res.ok) return;
      const sync = await res.json();

      const banner = document.getElementById("nas-sync-banner");
      const fileEl = document.getElementById("nas-sync-file");
      const timeEl = document.getElementById("nas-sync-time");
      const topSync = document.getElementById("nas-sync-top");

      if (sync.state === "success") {
        if (banner) banner.style.borderColor = "rgba(16, 185, 129, 0.4)";
        if (topSync) { topSync.innerText = "ONLINE"; topSync.style.color = "#10b981"; }
        if (fileEl) fileEl.innerText = sync.last_file || "Ready";
        if (timeEl) timeEl.innerText = sync.last_synced;
      } else {
        if (banner) banner.style.borderColor = "rgba(244, 63, 94, 0.4)";
        if (topSync) { topSync.innerText = "ATTN"; topSync.style.color = "#f43f5e"; }
        if (fileEl) fileEl.innerText = `Sync error (${sync.recent_errors || 1})`;
        if (timeEl) timeEl.innerText = "Check Logs";
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
      document.getElementById("hud-last-update").innerText = `MESH RUNNING // REFRESHED: ${now.toLocaleTimeString()}`;
    };

    refreshAll();
    updateCloudSync();

    setInterval(refreshAll, 2500);
    setInterval(updateCloudSync, 20000);
  }

  window.addEventListener("DOMContentLoaded", initKiosk);
</script>
