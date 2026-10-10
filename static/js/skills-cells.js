(function() {
  var GIST_BASE = "https://gist.githubusercontent.com/SiFTW/b46bc084c972c7c87e3bc5c7849c7920/raw";

  var NODES = [
    { id: "simon", cores: 72, apiVer: 3, url: "" },
    { id: "jlp",   cores: 104, apiVer: 3, url: "" },
    { id: "priti", cores: 12,  apiVer: 3, url: "" },
    { id: "nas",   cores: 4,   apiVer: 4, url: "" }
  ];

  var COLOR_STOPS = [
    { p: 0.00, r: 140, g: 155, b: 180 },
    { p: 0.20, r: 2,   g: 132, b: 199 },
    { p: 0.50, r: 16,  g: 185, b: 129 },
    { p: 0.75, r: 245, g: 158, b: 11  },
    { p: 1.00, r: 236, g: 72,  b: 153 }
  ];

  function getContinuousColor(pct) {
    var t = Math.max(0, Math.min(100, pct)) * 0.01;
    var lower = COLOR_STOPS[0];
    var upper = COLOR_STOPS[COLOR_STOPS.length - 1];

    for (var i = 0; i < COLOR_STOPS.length - 1; i++) {
      if (t >= COLOR_STOPS[i].p && t <= COLOR_STOPS[i + 1].p) {
        lower = COLOR_STOPS[i];
        upper = COLOR_STOPS[i + 1];
        break;
      }
    }

    var range = upper.p - lower.p;
    var factor = range === 0 ? 0 : (t - lower.p) / range;
    var r = Math.round(lower.r + (upper.r - lower.r) * factor);
    var g = Math.round(lower.g + (upper.g - lower.g) * factor);
    var b = Math.round(lower.b + (upper.b - lower.b) * factor);
    return "rgb(" + r + ", " + g + ", " + b + ")";
  }

  function init() {
    var canvas = document.getElementById("home-skills-cell-canvas");
    var badge = document.getElementById("skills-badge-container");
    if (!canvas) return;

    var parentSection = canvas.closest("section");
    if (!parentSection) {
      parentSection = canvas.parentElement;
      while (parentSection && parentSection.tagName !== "SECTION" && !parentSection.classList.contains("wg-featurette")) {
        parentSection = parentSection.parentElement;
      }
    }
    if (!parentSection) parentSection = canvas.parentElement;

    parentSection.classList.add("skills-widget-parent");

    if (canvas.parentElement !== parentSection) {
      parentSection.insertBefore(canvas, parentSection.firstChild);
    }
    if (badge && badge.parentElement !== parentSection) {
      parentSection.appendChild(badge);
    }

    var ctx = canvas.getContext("2d");

    function getDims() {
      return {
        w: parentSection.offsetWidth || window.innerWidth || 1200,
        h: parentSection.offsetHeight || 500
      };
    }

    var dims = getDims();
    canvas.width = dims.w;
    canvas.height = dims.h;

    // --- PARALLAX TRACKING ---
    var scrollOffset = 0;
    function updateScrollPosition() {
      var rect = parentSection.getBoundingClientRect();
      var winH = window.innerHeight || 800;
      // Normalized offset: -1 (top of screen) to +1 (bottom of screen)
      var progress = (rect.top - winH * 0.5) / winH;
      // Noticeable 140px vertical translation travel
      scrollOffset = progress * 140;
    }
    window.addEventListener("scroll", updateScrollPosition, { passive: true });
    updateScrollPosition();

    var clusterCorePool = {};
    for (var n = 0; n < NODES.length; n++) {
      clusterCorePool[NODES[n].id] = new Array(NODES[n].cores);
      for (var k = 0; k < NODES[n].cores; k++) {
        clusterCorePool[NODES[n].id][k] = 0;
      }
    }

    var cellIndex = 0;
    var cells = [];
    for (var ni = 0; ni < NODES.length; ni++) {
      var node = NODES[ni];
      for (var c = 0; c < node.cores; c++) {
        var angle = Math.random() * Math.PI * 2;
        // Depth layer: 0.35 (distant/slow) to 1.0 (foreground/fast)
        var depth = 0.35 + Math.random() * 0.65;
        cells.push({
          id: cellIndex++,
          nodeId: node.id,
          coreIdx: c,
          depth: depth,
          fluidVx: 0,
          fluidVy: 0,
          x: Math.random() * dims.w,
          y: Math.random() * dims.h,
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
    }

    var temporaryDaughters = [];

    function resizeCanvas() {
      var prevW = canvas.width || dims.w;
      var prevH = canvas.height || dims.h;
      var cur = getDims();

      canvas.width = cur.w;
      canvas.height = cur.h;

      if (cells.length > 0 && (cur.w > prevW || cur.h > prevH)) {
        for (var i = 0; i < cells.length; i++) {
          if (cur.w > prevW && cells[i].x < prevW) {
            cells[i].x = (cells[i].x / prevW) * cur.w;
          }
          if (cur.h > prevH && Math.random() > 0.4) {
            cells[i].y = Math.random() * cur.h;
          }
        }
      }
      updateScrollPosition();
    }
    window.addEventListener("resize", resizeCanvas);
    setTimeout(resizeCanvas, 150);

    function spawnIndependentDaughter(x, y, angle, load, depth) {
      var speed = 0.08 + Math.random() * 0.05;
      temporaryDaughters.push({
        id: "daughter-" + Date.now() + "-" + Math.random(),
        x: x,
        y: y,
        depth: depth || 0.7,
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
      var candidates = [];
      for (var i = 0; i < cells.length; i++) {
        if (cells[i].mitosisState === 'none' && cells[i].deathState === 'none') {
          candidates.push(cells[i]);
        }
      }
      if (candidates.length === 0) return;

      var active = [];
      for (var j = 0; j < candidates.length; j++) {
        if (candidates[j].currentLoad > 25) active.push(candidates[j]);
      }
      var chosen = (active.length > 0)
        ? active[Math.floor(Math.random() * active.length)]
        : candidates[Math.floor(Math.random() * candidates.length)];

      chosen.mitosisState = 'growing';
      chosen.mitosisProgress = 0;
      chosen.splitAngle = Math.random() * Math.PI * 2;
    }
    setInterval(triggerMitosisEvent, 9000);

    // --- ACCURATE POINTER COORDINATES ---
    var fluidMouse = {
      x: -9999,
      y: -9999,
      prevX: -9999,
      prevY: -9999,
      vx: 0,
      vy: 0,
      active: false,
      radius: 90
    };

    function updatePointerPosition(clientX, clientY) {
      var rect = parentSection.getBoundingClientRect();
      var currX = clientX - rect.left;
      var currY = clientY - rect.top;

      if (fluidMouse.prevX !== -9999) {
        fluidMouse.vx = (currX - fluidMouse.prevX) * 0.4;
        fluidMouse.vy = (currY - fluidMouse.prevY) * 0.4;
      }

      fluidMouse.prevX = currX;
      fluidMouse.prevY = currY;
      fluidMouse.x = currX;
      fluidMouse.y = currY;
      fluidMouse.active = true;
    }

    parentSection.addEventListener("mousemove", function(e) {
      updatePointerPosition(e.clientX, e.clientY);
    });

    parentSection.addEventListener("mouseleave", function() {
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

      for (var i = 0; i < cells.length; i++) {
        var c = cells[i];
        var targetLoad = (clusterCorePool[c.nodeId] && clusterCorePool[c.nodeId][c.coreIdx] !== undefined)
          ? clusterCorePool[c.nodeId][c.coreIdx]
          : 0;

        if (c.currentLoad > 40 && targetLoad < 8 && c.deathState === 'none' && c.mitosisState === 'none') {
          c.deathState = 'swelling';
          c.deathProgress = 0;
        }

        c.currentLoad += (targetLoad - c.currentLoad) * 0.010;
        var loadNorm = c.currentLoad * 0.01;
        var speedMult = 0.10 + (loadNorm * 0.28);

        // Fluid displacement with depth factor
        if (fluidMouse.active) {
          // Render Y includes the parallax shift
          var renderY = c.y + (scrollOffset * c.depth);
          var dx = c.x - fluidMouse.x;
          var dy = renderY - fluidMouse.y;
          var dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < fluidMouse.radius && dist > 1) {
            var force = Math.pow(1 - dist / fluidMouse.radius, 2) * 0.35 * c.depth;
            var normalX = dx / dist;
            var normalY = dy / dist;
            c.fluidVx += (normalX * force * 0.55) + (fluidMouse.vx * force * 0.18);
            c.fluidVy += (normalY * force * 0.55) + (fluidMouse.vy * force * 0.18);
          }
        }

        c.fluidVx = (c.fluidVx || 0) * 0.84;
        c.fluidVy = (c.fluidVy || 0) * 0.84;

        c.x += (c.vx * speedMult) + c.fluidVx;
        c.y += (c.vy * speedMult) + c.fluidVy;

        // Wrap coordinates seamlessly
        if (c.x < -30) c.x = canvas.width + 30;
        if (c.x > canvas.width + 30) c.x = -30;
        if (c.y < -100) c.y = canvas.height + 100;
        if (c.y > canvas.height + 100) c.y = -100;

        // Render point with parallax depth displacement
        var drawY = c.y + (scrollOffset * c.depth);
        var color = getContinuousColor(c.currentLoad);
        var baseRadius = (1.8 + (loadNorm * 2.6)) * (0.7 + c.depth * 0.4);

        ctx.save();
        if (c.currentLoad > 75) {
          ctx.shadowColor = color;
          ctx.shadowBlur = (c.currentLoad - 75) * 0.25;
        }

        if (c.deathState !== 'none') {
          c.deathProgress += 0.035;
          if (c.deathState === 'swelling') {
            var swellScale = 1.0 + (c.deathProgress * 0.7);
            ctx.beginPath();
            ctx.arc(c.x, drawY, baseRadius * swellScale, 0, Math.PI * 2);
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
            ctx.arc(c.x, drawY, c.popRadius, 0, Math.PI * 2);
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
          ctx.arc(c.x, drawY, baseRadius * (1.0 + c.mitosisProgress), 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();

          if (c.mitosisProgress >= 1.0) {
            c.mitosisState = 'splitting';
            c.mitosisProgress = 0;
          }
        } else if (c.mitosisState === 'splitting') {
          c.mitosisProgress += 0.014;
          var daughterRadius = baseRadius;
          var separation = c.mitosisProgress * (daughterRadius * 2.8);
          var splitDx = Math.cos(c.splitAngle) * separation;
          var splitDy = Math.sin(c.splitAngle) * separation;

          ctx.beginPath();
          ctx.arc(c.x - (splitDx * 0.5), drawY - (splitDy * 0.5), daughterRadius, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();

          ctx.beginPath();
          ctx.arc(c.x + (splitDx * 0.5), drawY + (splitDy * 0.5), daughterRadius, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();

          if (c.mitosisProgress >= 1.0) {
            c.mitosisState = 'none';
            c.mitosisProgress = 0;
            c.x -= splitDx * 0.5;
            c.y -= splitDy * 0.5;
            c.vx = -Math.cos(c.splitAngle) * 0.08;
            c.vy = -Math.sin(c.splitAngle) * 0.08;
            spawnIndependentDaughter(c.x + splitDx, c.y + splitDy, c.splitAngle, c.currentLoad, c.depth);
          }
        } else {
          ctx.beginPath();
          ctx.arc(c.x, drawY, Math.max(1.2, baseRadius), 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();
        }

        ctx.restore();
      }

      for (var dIdx = temporaryDaughters.length - 1; dIdx >= 0; dIdx--) {
        var d = temporaryDaughters[dIdx];
        var dDrawY = d.y + (scrollOffset * d.depth);

        if (fluidMouse.active) {
          var ddx = d.x - fluidMouse.x;
          var ddy = dDrawY - fluidMouse.y;
          var ddist = Math.sqrt(ddx * ddx + ddy * ddy);

          if (ddist < fluidMouse.radius && ddist > 1) {
            var dforce = Math.pow(1 - ddist / fluidMouse.radius, 2) * 0.35 * d.depth;
            d.fluidVx = (d.fluidVx || 0) + ((ddx / ddist) * dforce * 0.55) + (fluidMouse.vx * 0.18);
            d.fluidVy = (d.fluidVy || 0) + ((ddy / ddist) * dforce * 0.55) + (fluidMouse.vy * 0.18);
          }
        }

        d.fluidVx = (d.fluidVx || 0) * 0.84;
        d.fluidVy = (d.fluidVy || 0) * 0.84;

        d.x += d.vx + d.fluidVx;
        d.y += d.vy + d.fluidVy;

        if (d.x < -30) d.x = canvas.width + 30;
        if (d.x > canvas.width + 30) d.x = -30;
        if (d.y < -100) d.y = canvas.height + 100;
        if (d.y > canvas.height + 100) d.y = -100;

        var dColor = getContinuousColor(d.currentLoad);
        var dBaseRadius = (1.8 + (d.currentLoad * 0.01 * 2.6)) * (0.7 + d.depth * 0.4);

        ctx.save();
        if (d.currentLoad > 75) {
          ctx.shadowColor = dColor;
          ctx.shadowBlur = (d.currentLoad - 75) * 0.25;
        }

        if (d.deathState === 'none') {
          d.timeRemaining--;
          if (d.timeRemaining <= 0) {
            d.deathState = 'swelling';
            d.deathProgress = 0;
          }
          ctx.beginPath();
          ctx.arc(d.x, dDrawY, Math.max(1.2, dBaseRadius), 0, Math.PI * 2);
          ctx.fillStyle = dColor;
          ctx.fill();
        } else if (d.deathState === 'swelling') {
          d.deathProgress += 0.035;
          var dSwellRadius = dBaseRadius * (1.0 + d.deathProgress * 0.7);
          ctx.beginPath();
          ctx.arc(d.x, dDrawY, dSwellRadius, 0, Math.PI * 2);
          ctx.fillStyle = dColor;
          ctx.fill();

          if (d.deathProgress >= 1.0) {
            d.deathState = 'popping';
            d.popRadius = dSwellRadius;
            d.popAlpha = 0.85;
          }
        } else if (d.deathState === 'popping') {
          d.popRadius += 0.8;
          d.popAlpha -= 0.06;
          ctx.beginPath();
          ctx.arc(d.x, dDrawY, d.popRadius, 0, Math.PI * 2);
          ctx.strokeStyle = dColor;
          ctx.lineWidth = 1.2;
          ctx.globalAlpha = Math.max(0, d.popAlpha);
          ctx.stroke();

          if (d.popAlpha <= 0) {
            temporaryDaughters.splice(dIdx, 1);
          }
        }

        ctx.restore();
      }

      fluidMouse.vx *= 0.85;
      fluidMouse.vy *= 0.85;
      requestAnimationFrame(animateCells);
    }
    requestAnimationFrame(animateCells);

    function fetchNodeTelemetry(node) {
      if (!node.url) return;
      fetch(node.url + "/api/" + node.apiVer + "/percpu")
        .then(function(res) {
          if (!res.ok) return null;
          return res.json();
        })
        .then(function(cpus) {
          if (Array.isArray(cpus)) {
            for (var i = 0; i < cpus.length; i++) {
              var core = cpus[i];
              var loadVal = (typeof core.total === 'number') ? core.total : (100 - (core.idle !== undefined ? core.idle : 100));
              if (clusterCorePool[node.id] && clusterCorePool[node.id][i] !== undefined) {
                clusterCorePool[node.id][i] = loadVal;
              }
            }
          }
        })
        .catch(function() {});
    }

    function initSkillsCanvas() {
      fetch(GIST_BASE + "/endpoints.json?t=" + Date.now())
        .then(function(res) {
          if (!res.ok) return null;
          return res.json();
        })
        .then(function(endpoints) {
          if (endpoints) {
            for (var i = 0; i < NODES.length; i++) {
              var n = NODES[i];
              if (endpoints[n.id]) n.url = endpoints[n.id].replace(/\/+$/, "");
            }
          }
        })
        .catch(function() {});

      var refresh = function() {
        for (var i = 0; i < NODES.length; i++) {
          fetchNodeTelemetry(NODES[i]);
        }
      };
      refresh();
      setInterval(refresh, 3000);
    }

    initSkillsCanvas();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
