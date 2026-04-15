/**
 * Eternius — 2.5D Isometric Overworld / Underworld
 *
 * 14 Guardian entities (Light pillars) on the Overworld layer.
 * 14 Shadow Lord counterparts (Void pillars) on the Underworld layer.
 * Player movement: WASD.
 * XP Items scattered on the map.
 * Step on a Guardian or Shadow Lord tile to trigger an encounter alert.
 */

(function () {
  "use strict";

  // ── Canvas Setup ──────────────────────────────────────────────────────────
  const canvas = document.getElementById("eternius-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  const TILE_W = 64;
  const TILE_H = 32;
  const GRID_COLS = 20;
  const GRID_ROWS = 20;
  const CANVAS_W = 860;
  const CANVAS_H = 560;

  canvas.width  = CANVAS_W;
  canvas.height = CANVAS_H;

  // ── Isometric projection ──────────────────────────────────────────────────
  /**
   * Convert grid (col, row) to screen (x, y) for the overworld layer.
   * @param {number} col
   * @param {number} row
   * @returns {{x: number, y: number}}
   */
  function isoX(col, row) {
    return (col - row) * (TILE_W / 2) + CANVAS_W / 2;
  }

  function isoY(col, row) {
    return (col + row) * (TILE_H / 2) + 60;
  }

  // ── Pillar Data ───────────────────────────────────────────────────────────
  const PILLARS = [
    { name: "Janus",       guardian: "The Gatekeeper",       shadow: "The Deceiver",        mentor: "ODIN",   color: "#00d4ff", shadowColor: "#6600aa" },
    { name: "Jormungandr", guardian: "The World Serpent",    shadow: "The Consumer",         mentor: "ODIN",   color: "#00ffcc", shadowColor: "#004422" },
    { name: "Anubis",      guardian: "The Soul Judge",       shadow: "The False Arbiter",    mentor: "ODIN",   color: "#f7c948", shadowColor: "#884400" },
    { name: "Apep",        guardian: "Chaos Reborn",         shadow: "The Annihilator",      mentor: "KONG",   color: "#ff6600", shadowColor: "#330000" },
    { name: "Raven",       guardian: "The Lore Keeper",      shadow: "The Manipulator",      mentor: "ODIN",   color: "#9966ff", shadowColor: "#220044" },
    { name: "Ravana",      guardian: "The Sovereign",        shadow: "The Dominator",        mentor: "KONG",   color: "#ff3366", shadowColor: "#550022" },
    { name: "Vali",        guardian: "The Champion",         shadow: "The Avenger",          mentor: "KONG",   color: "#ff9900", shadowColor: "#553300" },
    { name: "Vritra",      guardian: "The Storm Tamer",      shadow: "The Destroyer",        mentor: "KONG",   color: "#33ccff", shadowColor: "#003366" },
    { name: "Iris",        guardian: "The Rainbow Herald",   shadow: "The Illusionist",      mentor: "Hekete", color: "#ff66ff", shadowColor: "#660066" },
    { name: "Iblis",       guardian: "The Chain Breaker",    shadow: "The Corruptor",        mentor: "Hekete", color: "#ff4444", shadowColor: "#440000" },
    { name: "Sigyn",       guardian: "The Faithful",         shadow: "The Martyr",           mentor: "Hekete", color: "#66ffcc", shadowColor: "#004433" },
    { name: "Set",         guardian: "The Desert Sovereign", shadow: "The Betrayer",         mentor: "KONG",   color: "#ffcc33", shadowColor: "#553300" },
    { name: "Pillar13",    guardian: "The Unknown Gate",     shadow: "The Forgotten Shadow", mentor: "TBD",    color: "#aaaaaa", shadowColor: "#333333" },
    { name: "Pillar14",    guardian: "The Final Threshold",  shadow: "The Last Shadow",      mentor: "TBD",    color: "#ffffff", shadowColor: "#222222" },
  ];

  // Fixed grid positions for the 14 guardians (overworld, row 0-13 staggered)
  const GUARDIAN_POSITIONS = PILLARS.map(function (p, i) {
    return {
      col: 3 + (i % 7) * 2,
      row: 2 + Math.floor(i / 7) * 6,
      pillar: p,
      type: "guardian",
    };
  });

  // Shadow Lords occupy shifted positions (underworld layer, offset by 1 col/row)
  const SHADOW_POSITIONS = PILLARS.map(function (p, i) {
    return {
      col: 4 + (i % 7) * 2,
      row: 5 + Math.floor(i / 7) * 6,
      pillar: p,
      type: "shadow",
    };
  });

  // XP items scattered on neutral tiles
  const XP_ITEMS = [];
  (function seedXP() {
    const usedKeys = new Set();
    GUARDIAN_POSITIONS.forEach(function (g) { usedKeys.add(g.col + "," + g.row); });
    SHADOW_POSITIONS.forEach(function (s) { usedKeys.add(s.col + "," + s.row); });
    const candidates = [];
    for (let c = 1; c < GRID_COLS - 1; c++) {
      for (let r = 1; r < GRID_ROWS - 1; r++) {
        if (!usedKeys.has(c + "," + r)) {
          candidates.push({ col: c, row: r });
        }
      }
    }
    // Shuffle and pick 30
    for (let i = candidates.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const tmp = candidates[i];
      candidates[i] = candidates[j];
      candidates[j] = tmp;
    }
    candidates.slice(0, 30).forEach(function (pos) {
      XP_ITEMS.push({ col: pos.col, row: pos.row, collected: false });
    });
  }());

  // ── Player State ──────────────────────────────────────────────────────────
  const player = {
    col: Math.floor(GRID_COLS / 2),
    row: Math.floor(GRID_ROWS / 2),
    xp: 0,
    facing: "right",
  };

  // ── Input ─────────────────────────────────────────────────────────────────
  const keys = {};
  let moveTimer = 0;
  const MOVE_DELAY = 180; // ms between steps

  document.addEventListener("keydown", function (e) {
    keys[e.key.toLowerCase()] = true;
  });
  document.addEventListener("keyup", function (e) {
    keys[e.key.toLowerCase()] = false;
  });

  // Keep focus on canvas when clicked so WASD works
  canvas.setAttribute("tabindex", "0");
  canvas.addEventListener("click", function () { canvas.focus(); });

  // ── Entity Lookup ─────────────────────────────────────────────────────────
  function findEntityAt(col, row) {
    for (let i = 0; i < GUARDIAN_POSITIONS.length; i++) {
      const g = GUARDIAN_POSITIONS[i];
      if (g.col === col && g.row === row) return g;
    }
    for (let i = 0; i < SHADOW_POSITIONS.length; i++) {
      const s = SHADOW_POSITIONS[i];
      if (s.col === col && s.row === row) return s;
    }
    return null;
  }

  function findXPAt(col, row) {
    for (let i = 0; i < XP_ITEMS.length; i++) {
      const x = XP_ITEMS[i];
      if (!x.collected && x.col === col && x.row === row) return x;
    }
    return null;
  }

  // ── Encounter logic ───────────────────────────────────────────────────────
  let lastEncounterKey = null;

  function triggerEncounter(entity) {
    const key = entity.type + "_" + entity.pillar.name;
    if (key === lastEncounterKey) return; // don't re-trigger same tile continuously
    lastEncounterKey = key;

    const p = entity.pillar;
    if (entity.type === "guardian") {
      alert(
        "⚡ You have encountered " + p.name + " — " + p.guardian +
        "\n\nMentor: " + p.mentor +
        "\n\nThe Gate opens. Face your virtue."
      );
    } else {
      alert(
        "☠ You have encountered the Shadow of " + p.name + " — " + p.shadow +
        "\n\nMentor: " + p.mentor +
        "\n\nThe Void hungers. Face your shadow."
      );
    }
  }

  function clearEncounterIfMoved(col, row) {
    if (lastEncounterKey !== null) {
      const entity = findEntityAt(col, row);
      if (!entity) lastEncounterKey = null;
    }
  }

  // ── HUD Update ────────────────────────────────────────────────────────────
  const hudXP    = document.getElementById("hud-xp");
  const hudPos   = document.getElementById("hud-pos");
  const hudStage = document.getElementById("hud-stage");

  function updateHUD() {
    if (hudXP)    hudXP.textContent    = player.xp;
    if (hudPos)   hudPos.textContent   = player.col + ", " + player.row;
    if (hudStage) {
      const e = findEntityAt(player.col, player.row);
      hudStage.textContent = e ? e.pillar.name + " (" + e.type + ")" : "Overworld";
    }
  }

  // ── Draw Helpers ──────────────────────────────────────────────────────────
  function drawIsoTile(col, row, fillStyle, strokeStyle, alpha) {
    const sx = isoX(col, row);
    const sy = isoY(col, row);
    ctx.save();
    ctx.globalAlpha = alpha !== undefined ? alpha : 1;
    ctx.beginPath();
    ctx.moveTo(sx,                sy - TILE_H / 2);
    ctx.lineTo(sx + TILE_W / 2,  sy);
    ctx.lineTo(sx,                sy + TILE_H / 2);
    ctx.lineTo(sx - TILE_W / 2,  sy);
    ctx.closePath();
    ctx.fillStyle   = fillStyle;
    ctx.strokeStyle = strokeStyle || "transparent";
    ctx.lineWidth   = 1;
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }

  function drawGlowCircle(x, y, radius, color, glowColor) {
    ctx.save();
    const grad = ctx.createRadialGradient(x, y, 0, x, y, radius);
    grad.addColorStop(0,   color);
    grad.addColorStop(0.6, glowColor);
    grad.addColorStop(1,   "transparent");
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.restore();
  }

  function drawPseudo3DShape(sx, sy, color, size, aura, time) {
    // Octagon pseudo-3D entity shape with aura pulse
    const pulse = 0.7 + 0.3 * Math.sin(time * 0.004 + aura);
    const r = size * pulse;

    ctx.save();
    // Drop shadow
    ctx.shadowColor = color;
    ctx.shadowBlur  = 18 * pulse;
    // Body
    ctx.beginPath();
    for (let a = 0; a < 8; a++) {
      const angle = (a * Math.PI) / 4 - Math.PI / 8;
      const px = sx + r * Math.cos(angle);
      const py = sy + (r * 0.55) * Math.sin(angle); // flatten for iso look
      if (a === 0) ctx.moveTo(px, py);
      else         ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.fillStyle = color + "cc";
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();
  }

  function drawLabel(x, y, text, color, size) {
    ctx.save();
    ctx.font = (size || 9) + "px 'Segoe UI', monospace";
    ctx.fillStyle = color || "#ffffff";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.shadowColor = color || "#000";
    ctx.shadowBlur = 4;
    ctx.fillText(text, x, y);
    ctx.restore();
  }

  // ── Main Render ───────────────────────────────────────────────────────────
  let lastTime = 0;

  function render(time) {
    ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);

    // ── Sky gradient background ──
    const sky = ctx.createLinearGradient(0, 0, 0, CANVAS_H);
    sky.addColorStop(0,   "#07080f");
    sky.addColorStop(0.5, "#0d1021");
    sky.addColorStop(1,   "#07080f");
    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);

    // ── Stars ──
    ctx.save();
    for (let i = 0; i < 80; i++) {
      const sx = (i * 127 + 11) % CANVAS_W;
      const sy = (i * 89  + 37) % (CANVAS_H * 0.55);
      const alpha = 0.3 + 0.4 * Math.sin(time * 0.001 + i);
      ctx.globalAlpha = alpha;
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(sx, sy, 1, 1);
    }
    ctx.restore();

    // ── Grid tiles ──
    for (let c = 0; c < GRID_COLS; c++) {
      for (let r = 0; r < GRID_ROWS; r++) {
        const even = (c + r) % 2 === 0;
        drawIsoTile(c, r, even ? "#0d1021" : "#080c1a", "rgba(124,92,252,0.07)", 0.9);
      }
    }

    // ── XP Items ──
    XP_ITEMS.forEach(function (item) {
      if (item.collected) return;
      const sx = isoX(item.col, item.row);
      const sy = isoY(item.col, item.row);
      const pulse = 0.7 + 0.3 * Math.sin(time * 0.005 + item.col);
      ctx.save();
      ctx.globalAlpha = 0.85 * pulse;
      ctx.shadowColor = "#f7c948";
      ctx.shadowBlur  = 10;
      ctx.beginPath();
      ctx.arc(sx, sy - 4, 5, 0, Math.PI * 2);
      ctx.fillStyle = "#f7c948";
      ctx.fill();
      ctx.restore();
    });

    // ── Shadow Lords (Underworld layer — drawn first, below guardians) ──
    SHADOW_POSITIONS.forEach(function (s, i) {
      const sx = isoX(s.col, s.row);
      const sy = isoY(s.col, s.row);
      drawIsoTile(s.col, s.row, s.pillar.shadowColor + "44", s.pillar.shadowColor, 0.7);
      drawPseudo3DShape(sx, sy - 8, s.pillar.shadowColor, 14, i * 0.7, time);
      drawLabel(sx, sy - 20, s.pillar.name, s.pillar.shadowColor, 8);
      drawLabel(sx, sy - 11, "⚡ Shadow", "#550055", 7);
    });

    // ── Guardians (Overworld layer) ──
    GUARDIAN_POSITIONS.forEach(function (g, i) {
      const sx = isoX(g.col, g.row);
      const sy = isoY(g.col, g.row);
      drawIsoTile(g.col, g.row, g.pillar.color + "22", g.pillar.color, 0.8);
      // Glow aura
      drawGlowCircle(sx, sy - 6, 18, g.pillar.color + "44", "transparent");
      drawPseudo3DShape(sx, sy - 8, g.pillar.color, 14, i * 0.5, time);
      drawLabel(sx, sy - 21, g.pillar.name, g.pillar.color, 8);
      drawLabel(sx, sy - 12, "★ Guardian", "#aaaaff", 7);
    });

    // ── Player ──
    const px = isoX(player.col, player.row);
    const py = isoY(player.col, player.row);

    // Tile highlight under player
    drawIsoTile(player.col, player.row, "rgba(255,0,204,0.18)", "#ff00cc", 1);

    // Player glow
    drawGlowCircle(px, py - 8, 22, "rgba(255,0,204,0.25)", "transparent");

    // Player body
    const playerPulse = 0.85 + 0.15 * Math.sin(time * 0.006);
    ctx.save();
    ctx.shadowColor = "#ff00cc";
    ctx.shadowBlur  = 20 * playerPulse;
    ctx.beginPath();
    ctx.arc(px, py - 8, 10 * playerPulse, 0, Math.PI * 2);
    ctx.fillStyle = "#ff00cc";
    ctx.fill();
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();

    // Player label
    drawLabel(px, py - 22, "YOU", "#ff00cc", 9);

    // ── HUD overlay ──
    ctx.save();
    ctx.fillStyle   = "rgba(7,8,15,0.7)";
    ctx.strokeStyle = "rgba(124,92,252,0.4)";
    ctx.lineWidth   = 1;
    ctx.beginPath();
    ctx.roundRect(8, 8, 180, 44, 8);
    ctx.fill();
    ctx.stroke();
    ctx.font = "bold 10px monospace";
    ctx.fillStyle = "#7c5cfc";
    ctx.fillText("ETERNIUS — OVERWORLD", 18, 24);
    ctx.fillStyle = "#8e90b4";
    ctx.font = "9px monospace";
    ctx.fillText("XP: " + player.xp + "   POS: " + player.col + "," + player.row, 18, 40);
    ctx.restore();

    requestAnimationFrame(render);
  }

  // ── Game Loop ─────────────────────────────────────────────────────────────
  function gameLoop(time) {
    const dt = time - lastTime;
    lastTime = time;

    // Movement throttle
    moveTimer -= dt;
    if (moveTimer <= 0) {
      let moved = false;
      let nc = player.col;
      let nr = player.row;

      if (keys["w"] || keys["arrowup"])    { nr = Math.max(0, player.row - 1); moved = true; }
      if (keys["s"] || keys["arrowdown"])  { nr = Math.min(GRID_ROWS - 1, player.row + 1); moved = true; }
      if (keys["a"] || keys["arrowleft"])  { nc = Math.max(0, player.col - 1); moved = true; }
      if (keys["d"] || keys["arrowright"]) { nc = Math.min(GRID_COLS - 1, player.col + 1); moved = true; }

      if (moved && (nc !== player.col || nr !== player.row)) {
        player.col = nc;
        player.row = nr;
        moveTimer = MOVE_DELAY;

        // Collect XP
        const xpItem = findXPAt(player.col, player.row);
        if (xpItem) {
          xpItem.collected = true;
          player.xp += 10;
        }

        // Encounter check
        clearEncounterIfMoved(player.col, player.row);
        const entity = findEntityAt(player.col, player.row);
        if (entity) {
          triggerEncounter(entity);
        }

        updateHUD();
      }
    }

    render(time);
    requestAnimationFrame(gameLoop);
  }

  updateHUD();
  requestAnimationFrame(gameLoop);

}());
