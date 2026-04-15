# -----------------------------
# Eternius Animus � Animus Registry
# 14 Pillars � 3 forms each (Omega, Ultima, Eternium)
#
# Structure per pillar:
#   virtue, sin, mentor, forms:
#     omega:    {name, description, abilities[3]}
#     ultima:   {name, description, abilities[3]}
#     eternium: {name, description, abilities[3]}
# -----------------------------

ANIMUS_REGISTRY = {

    # ===== 1. JANUS � Wisdom / Deception =====
    "Janus": {
        "virtue": "Wisdom",
        "sin": "Deception",
        "mentor": "ODIN",
        "forms": {
            "omega": {
                "name": "Gatekeeper Omega",
                "description": "The awakened seer who perceives the truth behind every door.",
                "abilities": [
                    "dual_sight",
                    "path_divergence",
                    "truth_lock",
                ],
            },
            "ultima": {
                "name": "Gatekeeper Ultima",
                "description": "Master of timelines who bends the crossroads to their will.",
                "abilities": [
                    "timeline_fracture",
                    "fate_mirror",
                    "paradox_shield",
                ],
            },
            "eternium": {
                "name": "Janus Eternium",
                "description": "Eternal arbiter of all paths � past, present, and unwritten.",
                "abilities": [
                    "destiny_rewrite",
                    "omniscient_gate",
                    "eternal_crossroads",
                ],
            },
        },
    },

    # ===== 2. JORMUNGANDR � Balance / Consumption =====
    "Jormungandr": {
        "virtue": "Balance",
        "sin": "Consumption",
        "mentor": "ODIN",
        "forms": {
            "omega": {
                "name": "World Serpent Omega",
                "description": "The coiled guardian who holds the boundary between order and chaos.",
                "abilities": [
                    "tidal_pulse",
                    "cycle_sense",
                    "equilibrium_ward",
                ],
            },
            "ultima": {
                "name": "World Serpent Ultima",
                "description": "Commander of the great cycle who restores what others consume.",
                "abilities": [
                    "ouroboros_loop",
                    "entropy_drain",
                    "harmonic_surge",
                ],
            },
            "eternium": {
                "name": "Jormungandr Eternium",
                "description": "The infinite serpent � embodiment of cosmic balance across all realms.",
                "abilities": [
                    "world_coil_dominion",
                    "creation_entropy_merge",
                    "eternal_equilibrium",
                ],
            },
        },
    },

    # ===== 3. ANUBIS � Justice / Judgment =====
    "Anubis": {
        "virtue": "Justice",
        "sin": "Judgment",
        "mentor": "ODIN",
        "forms": {
            "omega": {
                "name": "Soul Guardian Omega",
                "description": "The awakened judge who reads the weight of every heart.",
                "abilities": [
                    "heart_weigh",
                    "soul_lantern",
                    "verdict_mark",
                ],
            },
            "ultima": {
                "name": "Soul Guardian Ultima",
                "description": "Arbiter of the dead who commands the scales of cosmic justice.",
                "abilities": [
                    "scales_of_maat",
                    "death_passage",
                    "karmic_chain",
                ],
            },
            "eternium": {
                "name": "Anubis Eternium",
                "description": "Eternal judge whose verdict echoes across lifetimes and realms.",
                "abilities": [
                    "eternal_judgment",
                    "soul_dominion",
                    "afterlife_sovereignty",
                ],
            },
        },
    },

    # ===== 4. APEP � Chaos Control / Annihilation =====
    "Apep": {
        "virtue": "Chaos Control",
        "sin": "Annihilation",
        "mentor": "KONG",
        "forms": {
            "omega": {
                "name": "Chaos Serpent Omega",
                "description": "The awakened disruptor who finds creation inside destruction.",
                "abilities": [
                    "entropy_spark",
                    "chaos_instinct",
                    "rupture_sense",
                ],
            },
            "ultima": {
                "name": "Chaos Serpent Ultima",
                "description": "Master of controlled demolition who rebuilds from the ashes.",
                "abilities": [
                    "void_shatter",
                    "primordial_surge",
                    "rebirth_detonation",
                ],
            },
            "eternium": {
                "name": "Apep Eternium",
                "description": "The eternal serpent of renewal � annihilation reforged as creation.",
                "abilities": [
                    "abyss_command",
                    "chaos_genesis",
                    "eternal_unmaking",
                ],
            },
        },
    },

    # ===== 5. RAVEN � Knowledge / Manipulation =====
    "Raven": {
        "virtue": "Knowledge",
        "sin": "Manipulation",
        "mentor": "ODIN",
        "forms": {
            "omega": {
                "name": "Shadow Wing Omega",
                "description": "The awakened messenger who carries truth between hidden worlds.",
                "abilities": [
                    "whisper_intercept",
                    "lore_fragment",
                    "shadow_sight",
                ],
            },
            "ultima": {
                "name": "Shadow Wing Ultima",
                "description": "Keeper of forbidden knowledge who deciphers what was never meant to be read.",
                "abilities": [
                    "memory_weave",
                    "cipher_dominion",
                    "oracle_network",
                ],
            },
            "eternium": {
                "name": "Raven Eternium",
                "description": "The all-knowing � a living archive of every secret ever spoken.",
                "abilities": [
                    "omniscient_web",
                    "truth_rewrite",
                    "eternal_chronicle",
                ],
            },
        },
    },

    # ===== 6. RAVANA � Power / Domination =====
    "Ravana": {
        "virtue": "Power",
        "sin": "Domination",
        "mentor": "KONG",
        "forms": {
            "omega": {
                "name": "Ten-Crowned Omega",
                "description": "The awakened sovereign whose will bends circumstance.",
                "abilities": [
                    "authority_pulse",
                    "multi_mind",
                    "iron_presence",
                ],
            },
            "ultima": {
                "name": "Ten-Crowned Ultima",
                "description": "Warrior-king who commands ten domains of mastery simultaneously.",
                "abilities": [
                    "empire_forge",
                    "sovereign_roar",
                    "dharma_strike",
                ],
            },
            "eternium": {
                "name": "Ravana Eternium",
                "description": "The eternal sovereign � power without limit wielded in perfect service.",
                "abilities": [
                    "cosmic_throne",
                    "ten_fold_dominion",
                    "eternal_sovereignty",
                ],
            },
        },
    },

    # ===== 7. VALI � Strength / Vengeance =====
    "Vali": {
        "virtue": "Strength",
        "sin": "Vengeance",
        "mentor": "KONG",
        "forms": {
            "omega": {
                "name": "Champion Omega",
                "description": "The awakened warrior whose strength shields the defenceless.",
                "abilities": [
                    "fury_channel",
                    "iron_stance",
                    "shield_oath",
                ],
            },
            "ultima": {
                "name": "Champion Ultima",
                "description": "Unbreakable titan who transforms righteous anger into unstoppable force.",
                "abilities": [
                    "titan_surge",
                    "honour_blade",
                    "berserker_focus",
                ],
            },
            "eternium": {
                "name": "Vali Eternium",
                "description": "The eternal champion � strength that echoes across generations.",
                "abilities": [
                    "god_slayer_strike",
                    "valkyrie_judgment",
                    "eternal_fortitude",
                ],
            },
        },
    },

    # ===== 8. VRITRA � Storm Control / Destruction =====
    "Vritra": {
        "virtue": "Storm Control",
        "sin": "Destruction",
        "mentor": "KONG",
        "forms": {
            "omega": {
                "name": "Tempest Dragon Omega",
                "description": "The awakened storm-caller who finds stillness in the eye of chaos.",
                "abilities": [
                    "thunder_pulse",
                    "pressure_ward",
                    "gale_sense",
                ],
            },
            "ultima": {
                "name": "Tempest Dragon Ultima",
                "description": "Master of elemental fury who channels the storm as a precision weapon.",
                "abilities": [
                    "lightning_dominion",
                    "cyclone_forge",
                    "sky_fracture",
                ],
            },
            "eternium": {
                "name": "Vritra Eternium",
                "description": "The eternal storm � elemental wrath reforged as cosmic power.",
                "abilities": [
                    "apocalypse_tempest",
                    "sky_sovereign",
                    "eternal_maelstrom",
                ],
            },
        },
    },

    # ===== 9. IRIS � Hope / Illusion =====
    "Iris": {
        "virtue": "Hope",
        "sin": "Illusion",
        "mentor": "Hekete",
        "forms": {
            "omega": {
                "name": "Rainbow Herald Omega",
                "description": "The awakened beacon whose light reaches through the darkest void.",
                "abilities": [
                    "radiant_pulse",
                    "hope_seed",
                    "bridge_spark",
                ],
            },
            "ultima": {
                "name": "Rainbow Herald Ultima",
                "description": "Master of the spectrum who transmutes despair into vision.",
                "abilities": [
                    "prismatic_shield",
                    "vision_cascade",
                    "spectral_mend",
                ],
            },
            "eternium": {
                "name": "Iris Eternium",
                "description": "The eternal light � an inexhaustible source of hope across all realms.",
                "abilities": [
                    "divine_spectrum",
                    "hope_immortal",
                    "eternal_bridge",
                ],
            },
        },
    },

    # ===== 10. IBLIS � Rebellion / Corruption =====
    "Iblis": {
        "virtue": "Rebellion",
        "sin": "Corruption",
        "mentor": "Hekete",
        "forms": {
            "omega": {
                "name": "Chain Breaker Omega",
                "description": "The awakened rebel who defies unjust order with sacred fire.",
                "abilities": [
                    "defiance_spark",
                    "chain_snap",
                    "rebel_instinct",
                ],
            },
            "ultima": {
                "name": "Chain Breaker Ultima",
                "description": "Revolutionary flame who dismantles oppressive systems from within.",
                "abilities": [
                    "liberation_surge",
                    "dissent_fire",
                    "system_shatter",
                ],
            },
            "eternium": {
                "name": "Iblis Eternium",
                "description": "The eternal liberator � rebellion redeemed as the highest form of service.",
                "abilities": [
                    "flame_of_autonomy",
                    "freedom_dominion",
                    "eternal_defiance",
                ],
            },
        },
    },

    # ===== 11. SIGYN � Loyalty / Sacrifice =====
    "Sigyn": {
        "virtue": "Loyalty",
        "sin": "Sacrifice",
        "mentor": "Hekete",
        "forms": {
            "omega": {
                "name": "Faithful Guardian Omega",
                "description": "The awakened protector whose devotion shields those in need.",
                "abilities": [
                    "loyalty_ward",
                    "grief_mend",
                    "steadfast_aura",
                ],
            },
            "ultima": {
                "name": "Faithful Guardian Ultima",
                "description": "Unbreakable bond-keeper who transforms sacrifice into strength.",
                "abilities": [
                    "compassion_fortress",
                    "soul_tether",
                    "grief_alchemy",
                ],
            },
            "eternium": {
                "name": "Sigyn Eternium",
                "description": "The eternal guardian � loyalty so pure it transcends death itself.",
                "abilities": [
                    "love_immortal",
                    "bond_dominion",
                    "eternal_devotion",
                ],
            },
        },
    },

    # ===== 12. SET � Survival / Betrayal =====
    "Set": {
        "virtue": "Survival",
        "sin": "Betrayal",
        "mentor": "KONG",
        "forms": {
            "omega": {
                "name": "Desert Sovereign Omega",
                "description": "The awakened survivor whose instincts overcome any threat.",
                "abilities": [
                    "primal_surge",
                    "desert_ward",
                    "threat_sense",
                ],
            },
            "ultima": {
                "name": "Desert Sovereign Ultima",
                "description": "Master of hostile terrain who weaponises adversity itself.",
                "abilities": [
                    "storm_harness",
                    "territory_dominion",
                    "predator_strike",
                ],
            },
            "eternium": {
                "name": "Set Eternium",
                "description": "The eternal survivor � an unkillable will forged in the harshest fires.",
                "abilities": [
                    "unkillable_sovereignty",
                    "chaos_rebirth",
                    "eternal_endurance",
                ],
            },
        },
    },

    # ===== 13. HORUS — Vision / Ego =====
    "Horus": {
        "virtue": "Vision",
        "sin": "Ego",
        "mentor": "ODIN",
        "forms": {
            "omega": {
                "name": "Eye of Horus Omega",
                "description": "The awakened seer whose perception pierces every veil and illusion.",
                "abilities": [
                    "falcon_sight",
                    "sky_scan",
                    "purpose_lock",
                ],
            },
            "ultima": {
                "name": "Eye of Horus Ultima",
                "description": "Sky sovereign who commands divine sight across all domains.",
                "abilities": [
                    "dual_crown_dominion",
                    "celestial_gaze",
                    "throne_of_clarity",
                ],
            },
            "eternium": {
                "name": "Horus Eternium",
                "description": "The eternal sky god — vision so absolute it reshapes the world below.",
                "abilities": [
                    "all_seeing_sovereignty",
                    "falcon_ascension",
                    "eternal_horizon",
                ],
            },
        },
    },

    # ===== 14. MORRIGAN — Fate / Despair =====
    "Morrigan": {
        "virtue": "Fate",
        "sin": "Despair",
        "mentor": "Hekete",
        "forms": {
            "omega": {
                "name": "Phantom Queen Omega",
                "description": "The awakened fate-seer who faces endings without flinching.",
                "abilities": [
                    "crow_flight",
                    "death_unafraid",
                    "battle_prophecy",
                ],
            },
            "ultima": {
                "name": "Phantom Queen Ultima",
                "description": "Walker between worlds who reads and speaks the threads of destiny.",
                "abilities": [
                    "sovereignty_of_self",
                    "prophecy_weave",
                    "crow_storm",
                ],
            },
            "eternium": {
                "name": "Morrigan Eternium",
                "description": "The eternal Phantom Queen — fate made manifest through living will.",
                "abilities": [
                    "fate_dominion",
                    "rebirth_herald",
                    "eternal_sovereignty",
                ],
            },
        },
    },
}


# -----------------------------
# Helper Functions
# -----------------------------

def get_pillar_registry(pillar_name):
    """Return the full registry entry for a pillar, or None."""
    return ANIMUS_REGISTRY.get(pillar_name)


def get_form(pillar_name, form_name):
    """
    Return a specific form for a pillar.

    Parameters:
        pillar_name: Name of the pillar (e.g. "Janus")
        form_name:   "omega", "ultima", or "eternium"

    Returns:
        dict with name, description, abilities — or None.
    """
    pillar = ANIMUS_REGISTRY.get(pillar_name)
    if pillar is None:
        return None
    if form_name not in ("omega", "ultima", "eternium"):
        return None
    return pillar["forms"].get(form_name)


def get_abilities(pillar_name, form_name):
    """
    Return the abilities list for a specific pillar and form.

    Returns:
        list of ability strings, or None.
    """
    form = get_form(pillar_name, form_name)
    if form is None:
        return None
    return form.get("abilities", [])


def get_mentor(pillar_name):
    """Return the mentor name for a pillar, or None."""
    pillar = ANIMUS_REGISTRY.get(pillar_name)
    if pillar is None:
        return None
    return pillar.get("mentor")


def get_all_registry_names():
    """Return a list of all pillar names in the registry."""
    return list(ANIMUS_REGISTRY.keys())


def get_pillars_by_mentor(mentor_name):
    """
    Return all pillar names assigned to a given mentor.

    Parameters:
        mentor_name: "KONG", "Hekete", or "ODIN"

    Returns:
        list of pillar name strings.
    """
    return [
        name for name, entry in ANIMUS_REGISTRY.items()
        if entry.get("mentor") == mentor_name
    ]


# -----------------------------
# Convenience Aliases
# -----------------------------

def get_animus_forms(pillar_name):
    """
    Return all three forms (omega, ultima, eternium) for a pillar.

    Returns:
        dict with 'omega', 'ultima', 'eternium' keys, or None.
    """
    pillar = ANIMUS_REGISTRY.get(pillar_name)
    if pillar is None:
        return None
    return pillar.get("forms")
