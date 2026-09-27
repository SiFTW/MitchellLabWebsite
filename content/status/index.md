---
title: "Lab Compute Cluster"
summary: "Live monitoring of lab compute workstations."
date: 2026-09-27
type: page
share: false
commentable: false
editable: false
show_breadcrumb: true
---

<div style="display: flex; gap: 10px; margin-bottom: 1.2rem; flex-wrap: wrap;">
  <button id="btn-simon" onclick="switchServer('simon')" class="btn btn-primary">Simon (72 cores @ 2.3GHz)</button>
  <button id="btn-jlp" onclick="switchServer('jlp')" class="btn btn-outline-primary">JLP (104 cores @ 2.1GHz)</button>
  <button id="btn-priti" onclick="switchServer('priti')" class="btn btn-outline-primary">Priti (12 cores @ 4GHz)</button>
</div>

<iframe 
  id="monitor-frame"
  src="PASTE_SIMON_URL_HERE" 
  style="width: 100%; height: 85vh; border: 1px solid #444; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.15);" 
  loading="lazy"
  allowfullscreen>
</iframe>

<script>
const urls = {
  simon: "https://counting-dryer-depot-payments.trycloudflare.com",
  jlp: "https://thereby-william-search-reader.trycloudflare.com",
  priti: "https://info-critics-explanation-ski.trycloudflare.com"
};

function switchServer(name) {
  document.getElementById('monitor-frame').src = urls[name];
  ['simon', 'jlp', 'priti'].forEach(k => {
    const btn = document.getElementById('btn-' + k);
    if (k === name) {
      btn.className = 'btn btn-primary';
    } else {
      btn.className = 'btn btn-outline-primary';
    }
  });
}
</script>
