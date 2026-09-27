---
title: "Mitchell Lab Telemetry HUD"
layout: "single"
url: "/status/kiosk/"
summary: "High-density wall telemetry HUD for Mitchell Lab cluster compute."
---

<style>
  /* KIOSK & SCI-FI TELEMETRY THEME */
  :root {
    --bg-base: #06090e;
    --card-bg: rgba(13, 20, 34, 0.72);
    --card-border: rgba(56, 189, 248, 0.16);
    --card-glow: rgba(56, 189, 248, 0.08);
    --accent-cyan: #38bdf8;
    --accent-green: #10b981;
    --accent-purple: #a855f7;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --mono-font: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
  }

  /* Force Fullscreen Tablet Shell */
  body, html {
    margin: 0;
    padding: 0;
    background-color: var(--bg-base) !important;
    color: var(--text-primary);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    user-select: none;
    -webkit-user-select: none;
    overflow-x: hidden;
  }

  /* Subtly animated cybernetic grid */
  .hud-wrapper {
    min-height: 100vh;
    padding: 24px;
    box-sizing: border-box;
    background-image: 
      radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.08), transparent 60%),
      linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 100% 100%, 32px 32px, 32px 32px;
  }

.cluster-hud-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 16px;
    padding: 16px 24px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    gap: 16px;
  }

  .hud-metrics-row {
    display: flex;
    gap: 20px;
    flex-shrink: 0;
    align-items: center;
  }

  .hud-stat-box {
    text-align: right;
    white-space: nowrap; /* Prevents values and labels from wrapping onto two lines */
  }

  .hud-stat-box .val {
    font-size: 1.25rem;
    font-weight: 800;
    color: var(--accent-cyan);
    font-family: var(--mono-font);
    line-height: 1.2;
    white-space: nowrap;
  }

  .hud-stat-box .lbl {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-secondary);
    white-space: nowrap;
    margin-top: 2px;
  }

  /* Node Cards Grid */
  .nodes-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 20px;
  }

  .node-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(16px);
    transition: transform 0.2s ease, border-color 0.2s ease;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
  }

  .node-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    opacity: 0.4;
  }

  .node-card-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 12px;
  }

  .node-name {
    font-size: 1.2rem;
    font-weight: 700;
    font-family: var(--mono-font);
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #64748b;
    box-shadow: 0 0 8px rgba(100, 116, 139, 0.4);
  }
  .status-dot.online {
    background: var(--accent-green);
    box-shadow: 0 0 10px var(--accent-green);
  }

  .node-uptime {
    font-size: 0.75rem;
    font-family: var(--mono-font);
    color: var(--text-secondary);
  }

  /* Gauges & Progress Bars */
  .metric-block {
    margin-bottom: 12px;
  }

  .metric-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    margin-bottom: 5px;
    font-family: var(--mono-font);
  }

  .track-bar {
    width: 100%;
    height: 6px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 3px;
    overflow: hidden;
  }

  .fill-bar {
    height: 100%;
    width: 0%;
    border-radius: 3px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .fill-cpu { background: linear-gradient(90deg, #38bdf8, #818cf8); }
  .fill-ram { background: linear-gradient(90deg, #a855f7, #ec4899); }
  .fill-disk { background: linear-gradient(90deg, #10b981, #3b82f6); }

  /* Core Heatmap Matrix */
  .heatmap-wrap {
    margin-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 12px;
  }

  .heatmap-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    margin-bottom: 8px;
    font-family: var(--mono-font);
  }

  .core-grid {
    display: grid;
    gap: 3px;
    background: rgba(0, 0, 0, 0.2);
    padding: 6px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.04);
  }

  .core-cell {
    aspect-ratio: 1;
    border-radius: 2px;
    background: rgba(255, 255, 255, 0.05);
    transition: background 0.3s ease, box-shadow 0.3s ease;
  }

  /* Cloud Sync Badge (NAS Special) */
  .cloudsync-hud {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 10px;
    padding: 10px 14px;
    margin-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--mono-font);
  }

  .kiosk-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: rgba(15, 23, 42, 0.7);
    color: var(--text-secondary);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 30px;
    padding: 8px 16px;
    font-size: 0.8rem;
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
        <span style="color:var(--accent-cyan);">⚡</span> Mitchell Lab Cluster
      </h1>
      <p id="hud-last-update">SYSTEM SYNCHRONIZED // STANDBY</p>
    </div>
    <div class="hud-metrics-row">
      <div class="hud-stat-box">
        <div class="val" id="total-cores">192</div>
        <div class="lbl">Total Cores</div>
      </div>
      <div class="hud-stat-box">
        <div class="val" id="total-ram-active">-- / 324 GB</div>
        <div class="lbl">Memory Active</div>
      </div>
      <div class="hud-stat-box">
        <div class="val" id="nas-sync-top">SYNCED</div>
        <div class="lbl">Cloud Sync</div>
      </div>
    </div>
  </div>

  <!-- Dynamic Nodes Container -->
  <div class="nodes-grid" id="kiosk-nodes-container"></div>
</div>

<button class="kiosk-btn" onclick="toggleFullScreen()">⛶ Fullscreen</button>

<script>
  const GIST_BASE = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw";

  // Keep track of latest reported RAM usage per node
  const clusterMem = {
    simon: { used: 0, total: 62 },
    jlp:   { used: 0, total: 188 },
    priti: { used: 0, total: 64 },
    nas:   { used: 0, total: 10 }
  };

  function updateClusterTotalRam() {
    let totalUsed = 0;
    let totalCap = 0;
    let anyReported = false;

    Object.values(clusterMem).forEach(m => {
      if (m.used > 0) anyReported = true;
      totalUsed += m.used;
      totalCap += m.total;
    });

    const el = document.getElementById("total-ram-active");
    if (el) {
      if (anyReported) {
        el.innerText = `${totalUsed.toFixed(0)} / ${totalCap.toFixed(0)} GB`;
      } else {
        el.innerText = `0 / ${totalCap.toFixed(0)} GB`;
      }
    }
  }
  const NODES = [
    { id: "simon", name: "SIMON (Gateway)", specs: "72 Cores • 62GB", cores: 72, columns: 12, apiVer: 3, url: "" },
    { id: "jlp",   name: "JLP (Compute)",    specs: "104 Cores • 188GB", cores: 104, columns: 13, apiVer: 3, url: "" },
    { id: "priti", name: "PRITI (Compute)",  specs: "12 Cores (4GHz)",   cores: 12, columns: 6,  apiVer: 3, url: "" },
    { id: "nas",   name: "SYNOLOGY NAS",     specs: "4 Cores • 23TB RAID", cores: 4, columns: 4,  apiVer: 4, url: "" }
  ];

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
          <div>
            <div style="font-size:0.68rem; color:#6ee7b7; letter-spacing:0.05em;">DROPBOX CLOUD SYNC</div>
            <div id="nas-sync-file" style="font-size:0.75rem; color:#e2e8f0; font-weight:600; max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">Syncing...</div>
          </div>
          <div id="nas-sync-time" style="font-size:0.7rem; color:#94a3b8; text-align:right;">--</div>
        </div>
      ` : "";

      card.innerHTML = `
        <div class="node-card-head">
          <div class="node-name">
            <span class="status-dot" id="dot-${n.id}"></span>
            ${n.name}
          </div>
          <span class="node-uptime" id="uptime-${n.id}">--</span>
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
          <div class="heatmap-title">Active Core Telemetry (${n.cores} Cores)</div>
          <div class="core-grid" id="grid-${n.id}" style="grid-template-columns: repeat(${n.columns}, 1fr);">
            ${Array.from({ length: n.cores }).map((_, i) => `<div class="core-cell" id="core-${n.id}-${i}"></div>`).join('')}
          </div>
        </div>
      `;

      container.appendChild(card);
    });
  }

  function getHeatmapColor(load) {
    if (load < 5)   return "rgba(255, 255, 255, 0.04)";
    if (load < 25)  return "#0284c7"; // Cyan/Blue
    if (load < 60)  return "#10b981"; // Green
    if (load < 85)  return "#f59e0b"; // Amber
    return "#ef4444";                 // High load red
  }

  async function fetchTelemetry(node) {

    if (!node.url) return;
    const base = `${node.url}/api/${node.apiVer}`;

    try {
      const [cpu, mem, fs, upt, cpus] = await Promise.all([
        fetch(`${base}/quicklook`).then(r => r.json()),
        fetch(`${base}/mem`).then(r => r.json()),
        fetch(`${base}/fs`).then(r => r.json()),
        fetch(`${base}/uptime`).then(r => r.json()),
        fetch(`${base}/percpu`).then(r => r.json()).catch(() => [])
      ]);

      document.getElementById(`dot-${node.id}`).className = "status-dot online";
      document.getElementById(`uptime-${node.id}`).innerText = upt || "ONLINE";

      // CPU
      const cpuVal = Math.round(cpu.cpu || 0);
      document.getElementById(`cpu-txt-${node.id}`).innerText = `${cpuVal}%`;
      document.getElementById(`cpu-bar-${node.id}`).style.width = `${cpuVal}%`;


      // RAM
      const usedGbNum = (mem.used / (1024 ** 3));
      const totalGbNum = (mem.total / (1024 ** 3));
      const usedGb = usedGbNum.toFixed(1);
      const totalGb = totalGbNum.toFixed(1);
      const memPct = Math.round((mem.used / mem.total) * 100);
      
      document.getElementById(`ram-txt-${node.id}`).innerText = `${usedGb} / ${totalGb} GB (${memPct}%)`;
      document.getElementById(`ram-bar-${node.id}`).style.width = `${memPct}%`;

      // Update cluster aggregate
      if (clusterMem[node.id]) {
        clusterMem[node.id].used = usedGbNum;
        clusterMem[node.id].total = totalGbNum;
        updateClusterTotalRam();
      }

      // Disk
      if (Array.isArray(fs) && fs.length > 0) {
        const root = fs.find(d => d.mnt_point === "/" || d.mnt_point === "/volume1") || fs[0];
        const dUsed = (root.used / (1024 ** 4) >= 1) ? `${(root.used / (1024 ** 4)).toFixed(1)} TB` : `${Math.round(root.used / (1024 ** 3))} GB`;
        const dTotal = (root.size / (1024 ** 4) >= 1) ? `${(root.size / (1024 ** 4)).toFixed(1)} TB` : `${Math.round(root.size / (1024 ** 3))} GB`;
        document.getElementById(`disk-txt-${node.id}`).innerText = `${dUsed} / ${dTotal}`;
        document.getElementById(`disk-bar-${node.id}`).style.width = `${root.percent}%`;
      }

      // Heatmap Cells
      if (Array.isArray(cpus)) {
        cpus.forEach((core, i) => {
          const el = document.getElementById(`core-${node.id}-${i}`);
          if (el) {
            const load = core.total || 0;
            el.style.background = getHeatmapColor(load);
            el.style.boxShadow = load > 50 ? `0 0 6px ${getHeatmapColor(load)}` : "none";
          }
        });
      }
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
        if (topSync) { topSync.innerText = "SYNCED"; topSync.style.color = "#10b981"; }
        if (fileEl) fileEl.innerText = sync.last_file || "All files updated";
        if (timeEl) timeEl.innerText = sync.last_synced;
      } else {
        if (banner) banner.style.borderColor = "rgba(239, 68, 68, 0.4)";
        if (topSync) { topSync.innerText = "ATTN"; topSync.style.color = "#ef4444"; }
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
      document.getElementById("hud-last-update").innerText = `SYSTEM ACTIVE // ${new Date().toLocaleTimeString()}`;
    };

    refreshAll();
    updateCloudSync();

    setInterval(refreshAll, 2500);       // Fast telemetry refresh for dynamic feel
    setInterval(updateCloudSync, 20000);  // Sync badge update
  }

  window.addEventListener("DOMContentLoaded", initKiosk);
</script>
