# Eternius / CassWorld — Complete Project Briefing
**Date:** 2026-03-09
**Author:** Paul Cassidy
**Purpose:** Full context handoff for AI assistant continuity

---

## What This Project Is

CassWorld is a 2D educational board game built in Python. It uses a custom mythology-based framework called the **Eternius Animus System**. Players select an Animus (cognitive archetype), navigate a grid, collect XP, encounter shadow traits, and receive guidance from AI mentors. The system is designed around personal growth, ethical reflection, and strengths-based learning.

---

## Files Built (All Working)

### Core Data Files

| File | What It Contains |
|---|---|
| `Animus_catalogue.json` | 14 player Animus entries with class, mentor, strengths, shadow risks, XP bonuses, pillar alignment |
| `Animus_framework.json` | Celestial Triad (Lilith, Odin, Hekete) + 12 Pillars with virtue/sin duality and lumen/umbra forms |

### Python Modules

| File | What It Does |
|---|---|
| `animus.py` | **Single access layer** — bridges player catalogue (JSON) and Eternius registry. CRUD for catalogue + registry lookup functions |
| `animus_registry.py` | 14 pillars × 3 forms (Omega/Ultima/Eternium) = 42 forms with 126 abilities. Helper functions for lookup |
| `shadow_traits.py` | 14 pillars × 18 traits each = 252 total traits. Light/shadow × core/developed/ascended tiers. Data-first, no gameplay logic |
| `framework.py` | Reads `Animus_framework.json`. Functions for Celestial Triad lookup, pillar lookup by virtue/sin, lumen/umbra forms |
| `mentor.py` | 4 mentors (KONG, ODIN, Hekete, Lilith). Each has: profile, guidance per tier, form unlock responses, shadow encounter prompts, communication style |
| `main.py` | Game loop — loads catalogue, player selects Animus, 5×5 grid with W/A/S/D movement, XP collection with Animus bonuses, shadow trait encounters |
| `test_animus.py` | 35+ unit tests for catalogue (structure, CRUD, XP calc, mentors, strengths, shadow risks) |
| `test_framework.py` | 22 unit tests for Celestial Triad + 12 Pillars (structure, forms, virtue/sin lookup) |

### Documentation

| File | What It Contains |
|---|---|
| `MASTER_DOC.md` | Full master document — mission, vision, ethos, 14 pillars, governance, gameplay, community |
| `Master_Doc_Beta.md` | Expanded beta doc — technical architecture, The Worx, methodology, scaling |
| `README.md` | Project overview and getting started guide |
| `PROJECT_STATUS.md` | Project status file for AI assistant context |

### Empty (Not Yet Built)

| File | Intended Purpose |
|---|---|
| `utils.py` | Shared helpers — grid display, input validation, formatting |
| `module1.py` | First playable mission module |

---

## System Architecture

---

## 📦 Animus Catalogue Structure (`Animus_catalogue.json`)

Each player Animus entry has these fields:

| Field | Type | Example |
|---|---|---|
| `title` | string | "Strategic Thinker" |
| `class` | string | "Strategist" |
| `mentor` | string | "ODIN" / "KONG" / "Hekete" |
| `description` | string | Full description of the Animus |
| `category` | string | "strategic" / "creative" / "empathetic" etc. |
| `pillar_alignment` | list | ["Vision", "Innovation"] |
| `strengths` | list | ["analysis", "strategy", "research"] |
| `xp_bonus` | object | {"type": "multiplier", "value": 1.1, "condition": "planning"} |
| `xp_bonus_tasks` | list | ["coding", "research", "engineering"] |
| `shadow_trait_interaction` | string | "default" / "bypass_once" / "reduce_half" / "detect_nearby" |
| `shadow_risk` | list | ["overthinking", "impulsivity"] |
| `mentor_note` | string | Mentor AI guidance text |
| `special_ability` | string | (optional) "double_move_once", "reveal_hidden_xp" etc. |

---

## ⦿ Animus Framework Structure (`Animus_framework.json`)

### Celestial Triad (3 entities)

| Entity | Tier | Domain | Forms |
|---|---|---|---|
| Lilith | Prime Origin | Balance of Void and Creation | Prime / Lumen / Umbra |
| Odin | Celestial Mentor | Wisdom and Strategy | Prime / Lumen / Umbra |
| Hekete | Celestial Mentor | Guidance and Transformation | Prime / Lumen / Umbra |

### 12 Pillars (virtue/sin duality)

| Pillar | Virtue | Sin | Lumen Form | Umbra Form |
|---|---|---|---|---|
| Janus | Wisdom | Deception | Gatekeeper of Light | Watcher of False Paths |
| Jormungandr | Balance | Consumption | World Serpent of Order | Devourer of Realms |
| Anubis | Justice | Judgment | Guardian of Souls | Harbinger of Death |
| Apep | Chaos Control | Annihilation | Breaker of False Order | Serpent of the Abyss |
| Raven | Knowledge | Manipulation | Messenger of Wisdom | Whisperer of Secrets |
| Ravana | Power | Domination | King of Ten Minds | Tyrant of Flames |
| Vali | Strength | Vengeance | Champion of Honor | Avenger of Blood |
| Vritra | Storm Control | Destruction | Dragon of the Tempest | Devourer of Skies |
| Iris | Hope | Illusion | Bearer of Light | Mistress of Mirage |
| Irlis | Rebellion | Corruption | Breaker of Chains | Lord of the Void |
| Sigyn | Loyalty | Sacrifice | Protector of the Fallen | Bearer of Eternal Grief |
| Set | Survival | Betrayal | Storm Bringer | Lord of Chaos |

---

## 📦 System Stats

| Component | Count |
|---|---|
| Player Animus entries | 14 |
| Eternius pillars | 14 (12 named + 2 placeholders) |
| Traits per pillar | 18 (9 light + 9 shadow) |
| Total traits | 252 |
| Forms per pillar | 3 (Omega / Ultima / Eternium) |
| Total forms | 42 |
| Abilities per form | 3 |
| Total abilities | 126 |
| Celestial Triad | 3 (Lilith, Odin, Hekete) |
| Mentors | 4 (KONG, ODIN, Hekete, Lilith) |

---

## The 14 Pillars

| Pillar | Virtue | Sin | Mentor |
|---|---|---|---|
| Janus | Wisdom | Deception | ODIN |
| Jormungandr | Balance | Consumption | ODIN |
| Anubis | Justice | Judgment | ODIN |
| Apep | Chaos Control | Annihilation | KONG |
| Raven | Knowledge | Manipulation | ODIN |
| Ravana | Power | Domination | KONG |
| Vali | Strength | Vengeance | KONG |
| Vritra | Storm Control | Destruction | KONG |
| Iris | Hope | Illusion | Hekete |
| Iblis | Rebellion | Corruption | Hekete |
| Sigyn | Loyalty | Sacrifice | Hekete |
| Set | Survival | Betrayal | KONG |
| Pillar13 | TBD | TBD | TBD |
| Pillar14 | TBD | TBD | TBD |

---

## The 4 Mentors

| Mentor | Title | Style | Role |
|---|---|---|---|
| KONG | The Alpha | Direct | Execution, building, physical mastery |
| ODIN | The Allfather | Strategic | Strategy, knowledge, structure |
| Hekete | The Triple Goddess | Reflective | Transformation, intuition, pathways |
| Lilith | The Prime Origin | Absolute | Balance, integration, omega oversight |

Each mentor provides:
- 3 guidance prompts per tier (core / developed / ascended)
- 1 response per form unlock (omega / ultima / eternium)
- 3 shadow encounter prompts

---

## Trait Structure (per pillar)

Each of the 14 pillars has 18 traits:

| Alignment | Tier | Count |
|---|---|---|
| Light | Core | 3 |
| Light | Developed | 3 |
| Light | Ascended | 3 |
| Shadow | Core | 3 |
| Shadow | Developed | 3 |
| Shadow | Ascended | 3 |

Janus is fully authored with named traits. Pillars 2–12 have mythically themed traits. Pillar13 and Pillar14 are placeholders.

---

## Registry Form Structure (per pillar)

Each pillar has 3 progression forms:

| Form | Description |
|---|---|
| Omega | Mastery and balanced control |
| Ultima | Full embodiment of the pillar |
| Eternium | Transcendent state beyond mastery |

Each form has: name, description, and 3 abilities.

---

## Key Functions by File

### `animus.py` — Player Catalogue

- `load_catalogue()` / `save_catalogue(data)`
- `get_animus(name, data)` / `get_all_animus_names(data)`
- `add_animus(name, entry, data)` / `update_animus(name, updates, data)` / `remove_animus(name, data)`
- `calculate_xp(base_xp, name, data)`
- `display_catalogue(data)`

### `animus.py` — Eternius Registry

- `list_animus_pillars()`
- `get_animus_forms(pillar)` / `get_animus_form(pillar, form)` / `get_animus_abilities(pillar, form)`
- `get_animus_mentor(pillar)` / `get_animus_pillars_by_mentor(mentor)`

### `mentor.py`

- `get_mentor_profile(name)` / `get_all_mentor_names()`
- `get_mentor_guidance(name, tier)`
- `get_mentor_form_response(name, form)`
- `get_shadow_encounter_response(name)`
- `get_mentor_style(name)` / `get_mentor_pillars(name)`
- `display_mentors()`

### `shadow_traits.py`

- `get_pillar_traits(pillar)` — all 18 traits
- `get_traits_by_alignment(pillar, alignment)` — light or shadow only
- `get_traits_by_tier(pillar, alignment, tier)` — specific tier
- `get_all_pillar_names()` / `count_total_traits()`

### `animus_registry.py`

- `get_pillar_registry(pillar)` / `get_all_registry_names()`
- `get_form(pillar, form)` / `get_abilities(pillar, form)`
- `get_mentor(pillar)` / `get_pillars_by_mentor(mentor)`

### `framework.py`

- `load_framework()` / `save_framework(data)`
- `get_triad(data)` / `get_triad_member(name, data)` / `get_mentor_forms(name, data)`
- `get_all_pillars(data)` / `get_pillar(name, data)`
- `get_pillar_by_virtue(virtue, data)` / `get_pillar_by_sin(sin, data)`
- `get_form(pillar, type, data)`
- `display_framework(data)`

---

## What Still Needs Building

1. **`utils.py`** — Grid rendering, input validation, shared formatting helpers
2. **`module1.py`** — First playable mission that uses the full trait → form → mentor pipeline
3. **Tests** — Need test files for `animus_registry.py`, `mentor.py`, and `shadow_traits.py`
4. **Pillar13 & Pillar14** — Placeholder pillars need naming and full trait/form authoring
5. **Gameplay integration** — Pillar virtues/sins should influence shadow trait encounters and mentor responses dynamically

---

## Important Notes

- All Python files are in the same project root directory
- `animus.py` is the single access layer — other files should go through it where possible
- The system is data-first — no gameplay logic in data modules
- Mentors read pillar assignments from `animus_registry.py` at runtime
- The project uses Visual Studio 2022 with Python