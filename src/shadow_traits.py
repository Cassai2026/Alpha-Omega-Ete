# -----------------------------
# Eternius Animus — Shadow Traits Data Module
# 14 Pillars × 18 traits each = 252 traits total
#
# Structure per pillar:
#   light:
#     core:      [3 traits]
#     developed: [3 traits]
#     ascended:  [3 traits]
#   shadow:
#     core:      [3 traits]
#     developed: [3 traits]
#     ascended:  [3 traits]
# -----------------------------

PILLAR_TRAITS = {

    # ===== 1. JANUS — Wisdom / Deception =====
    "Janus": {
        "virtue": "Wisdom",
        "sin": "Deception",
        "light": {
            "core": [
                {"name": "decisiveness",       "description": "The clarity to choose a path without hesitation."},
                {"name": "honesty",            "description": "An unwavering commitment to truth in all dealings."},
                {"name": "true_guidance",      "description": "The ability to lead others toward the right door."},
            ],
            "developed": [
                {"name": "strategic_foresight", "description": "Seeing consequences many moves ahead."},
                {"name": "diplomatic_truth",    "description": "Delivering hard truths with grace and precision."},
                {"name": "pathfinding",         "description": "Navigating complex choices to find the optimal route."},
            ],
            "ascended": [
                {"name": "gatekeeper_mastery",   "description": "Absolute command over which doors open and close."},
                {"name": "timeline_navigation",  "description": "Perceiving branching futures and selecting the wisest path."},
                {"name": "destiny_alignment",    "description": "Harmonising personal will with the flow of fate."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "indecision",     "description": "Paralysis when faced with two equally weighted choices."},
                {"name": "deception",      "description": "Instinct to mislead others for personal advantage."},
                {"name": "false_paths",    "description": "Unconsciously guiding others toward dead ends."},
            ],
            "developed": [
                {"name": "manipulation",     "description": "Weaponising trust to control outcomes."},
                {"name": "misdirection",     "description": "Creating elaborate diversions to conceal true intent."},
                {"name": "power_brokering",  "description": "Trading secrets and influence for personal gain."},
            ],
            "ascended": [
                {"name": "false_prophet",       "description": "Commanding blind faith through fabricated visions."},
                {"name": "reality_distortion",  "description": "Bending perception so others cannot distinguish truth from lies."},
                {"name": "fate_corruption",     "description": "Twisting the threads of destiny to serve a selfish agenda."},
            ],
        },
    },

    # ===== 2. JORMUNGANDR — Balance / Consumption =====
    "Jormungandr": {
        "virtue": "Balance",
        "sin": "Consumption",
        "light": {
            "core": [
                {"name": "equilibrium",       "description": "Maintaining inner and outer balance under pressure."},
                {"name": "cyclical_wisdom",   "description": "Understanding that all things rise and fall in cycles."},
                {"name": "boundary_sense",    "description": "Knowing where limits should be drawn and held."},
            ],
            "developed": [
                {"name": "harmonic_restoration", "description": "Restoring balance to disrupted systems and relationships."},
                {"name": "coil_of_patience",     "description": "Enduring great tension without breaking composure."},
                {"name": "tidal_awareness",      "description": "Reading the ebb and flow of power and emotion."},
            ],
            "ascended": [
                {"name": "world_serpent_unity",  "description": "Binding all forces into a single harmonious whole."},
                {"name": "ouroboros_mastery",     "description": "Commanding the cycle of destruction and renewal."},
                {"name": "cosmic_equilibrium",   "description": "Balancing creation and entropy on a universal scale."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "excess",            "description": "Taking more than what is needed or deserved."},
                {"name": "hoarding",          "description": "Clinging to resources, energy, or control out of fear."},
                {"name": "stagnation",        "description": "Refusing to release what must end."},
            ],
            "developed": [
                {"name": "devouring_hunger",  "description": "An insatiable need to absorb everything in reach."},
                {"name": "constriction",      "description": "Squeezing the life from relationships and systems."},
                {"name": "tidal_domination",  "description": "Using cycles of chaos to keep others off-balance."},
            ],
            "ascended": [
                {"name": "world_eater",       "description": "Consuming entire systems to fuel personal growth."},
                {"name": "entropy_lord",      "description": "Accelerating decay and collapse for selfish rebirth."},
                {"name": "ouroboros_curse",   "description": "Trapping others in endless destructive loops."},
            ],
        },
    },

    # ===== 3. ANUBIS — Justice / Judgment =====
    "Anubis": {
        "virtue": "Justice",
        "sin": "Judgment",
        "light": {
            "core": [
                {"name": "fairness",           "description": "Weighing all sides before rendering a decision."},
                {"name": "moral_clarity",      "description": "Seeing right from wrong without hesitation."},
                {"name": "soul_reading",       "description": "Perceiving the true nature of a person's intentions."},
            ],
            "developed": [
                {"name": "impartial_verdict",  "description": "Delivering justice free from personal bias."},
                {"name": "karmic_insight",     "description": "Understanding the long-term consequences of actions."},
                {"name": "guardian_vigilance",  "description": "Watching over the vulnerable with tireless dedication."},
            ],
            "ascended": [
                {"name": "scales_of_maat",     "description": "Perfect cosmic justice — truth weighed against the feather."},
                {"name": "death_passage_guide", "description": "Guiding souls through their darkest transitions with grace."},
                {"name": "eternal_arbiter",    "description": "Final authority over moral reckoning across lifetimes."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "harsh_judgment",     "description": "Condemning others without mercy or context."},
                {"name": "self_righteousness", "description": "Believing your moral view is the only valid one."},
                {"name": "cold_detachment",    "description": "Withholding compassion in the name of fairness."},
            ],
            "developed": [
                {"name": "executioner_zeal",   "description": "Taking pleasure in punishing those deemed unworthy."},
                {"name": "moral_tyranny",      "description": "Imposing rigid ethical codes on everyone around you."},
                {"name": "soul_condemnation",  "description": "Writing off others as irredeemable."},
            ],
            "ascended": [
                {"name": "death_bringer",      "description": "Becoming the instrument of final, merciless judgment."},
                {"name": "scales_of_ruin",     "description": "Corrupting justice into a weapon of personal vengeance."},
                {"name": "eternal_prosecutor", "description": "Pursuing punishment across lifetimes without forgiveness."},
            ],
        },
    },

    # ===== 4. APEP — Chaos Control / Annihilation =====
    "Apep": {
        "virtue": "Chaos Control",
        "sin": "Annihilation",
        "light": {
            "core": [
                {"name": "adaptive_instinct",  "description": "Thriving in disorder and unpredictability."},
                {"name": "disruption_sense",   "description": "Detecting when systems need to be broken and rebuilt."},
                {"name": "creative_entropy",   "description": "Finding new possibilities inside collapse."},
            ],
            "developed": [
                {"name": "controlled_demolition", "description": "Breaking down failing structures with surgical precision."},
                {"name": "chaos_navigation",      "description": "Moving through disorder with purpose and clarity."},
                {"name": "rebirth_catalyst",      "description": "Triggering transformation by dismantling the old."},
            ],
            "ascended": [
                {"name": "primordial_command",    "description": "Directing raw chaos as a force for creation."},
                {"name": "void_architect",        "description": "Building new order from the ashes of the old."},
                {"name": "serpent_of_renewal",    "description": "Embodying the eternal cycle of destruction and rebirth."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "reckless_destruction", "description": "Breaking things without thought for consequences."},
                {"name": "instability",          "description": "Spreading chaos wherever you go without control."},
                {"name": "nihilism",             "description": "Believing nothing matters and nothing is worth saving."},
            ],
            "developed": [
                {"name": "annihilation_drive",   "description": "An urge to erase rather than repair."},
                {"name": "entropy_addiction",     "description": "Feeding on collapse and crisis for stimulation."},
                {"name": "scorched_earth",       "description": "Destroying everything rather than letting others benefit."},
            ],
            "ascended": [
                {"name": "abyss_herald",         "description": "Summoning total annihilation as an act of will."},
                {"name": "void_devourer",        "description": "Erasing existence itself to fill an inner emptiness."},
                {"name": "serpent_of_the_end",   "description": "Becoming the embodiment of irreversible extinction."},
            ],
        },
    },

    # ===== 5. RAVEN — Knowledge / Manipulation =====
    "Raven": {
        "virtue": "Knowledge",
        "sin": "Manipulation",
        "light": {
            "core": [
                {"name": "curiosity",          "description": "An insatiable drive to learn and understand."},
                {"name": "message_bearing",    "description": "Carrying truth between worlds and people."},
                {"name": "sharp_perception",   "description": "Noticing what others overlook."},
            ],
            "developed": [
                {"name": "lore_mastery",       "description": "Deep knowledge of history, myth, and hidden truths."},
                {"name": "code_breaking",      "description": "Deciphering patterns and encrypted information."},
                {"name": "truth_weaving",      "description": "Connecting scattered facts into a coherent picture."},
            ],
            "ascended": [
                {"name": "omniscient_sight",   "description": "Seeing all knowledge as a single interconnected web."},
                {"name": "wisdom_keeper",      "description": "Safeguarding sacred knowledge for future generations."},
                {"name": "raven_oracle",       "description": "Channelling universal knowledge to illuminate the unknown."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "gossip",             "description": "Spreading information carelessly to stir conflict."},
                {"name": "prying",             "description": "Invading others' privacy in pursuit of secrets."},
                {"name": "half_truths",        "description": "Sharing just enough to mislead."},
            ],
            "developed": [
                {"name": "intelligence_warfare", "description": "Using knowledge as a weapon against allies and enemies."},
                {"name": "puppet_mastery",       "description": "Pulling strings from the shadows using information leverage."},
                {"name": "secret_hoarding",      "description": "Withholding critical knowledge for personal power."},
            ],
            "ascended": [
                {"name": "mind_spider",        "description": "Weaving invisible webs of influence across entire networks."},
                {"name": "truth_eraser",       "description": "Rewriting history and memory to control narratives."},
                {"name": "raven_tyrant",       "description": "Ruling through total information dominance."},
            ],
        },
    },

    # ===== 6. RAVANA — Power / Domination =====
    "Ravana": {
        "virtue": "Power",
        "sin": "Domination",
        "light": {
            "core": [
                {"name": "inner_authority",    "description": "Commanding respect through self-mastery."},
                {"name": "fierce_devotion",    "description": "Channelling intense focus into worthy causes."},
                {"name": "ten_fold_focus",     "description": "Managing multiple challenges simultaneously."},
            ],
            "developed": [
                {"name": "sovereign_will",     "description": "Bending circumstances through disciplined intent."},
                {"name": "warrior_scholarship", "description": "Combining intellectual and physical mastery."},
                {"name": "empire_building",    "description": "Creating lasting structures that empower others."},
            ],
            "ascended": [
                {"name": "dharma_king",        "description": "Wielding absolute power in service of righteousness."},
                {"name": "ten_crowned_sage",   "description": "Mastery of all ten domains of knowledge and action."},
                {"name": "cosmic_sovereign",   "description": "Ruling with wisdom that transcends personal desire."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "arrogance",          "description": "Believing yourself above all others."},
                {"name": "control_hunger",     "description": "Needing to dominate every situation and person."},
                {"name": "pride_blindness",    "description": "Refusing to see your own flaws or failures."},
            ],
            "developed": [
                {"name": "subjugation",        "description": "Forcing others into servitude to feed your ambition."},
                {"name": "fear_lordship",      "description": "Maintaining power through intimidation and dread."},
                {"name": "legacy_obsession",   "description": "Sacrificing everything to build a monument to yourself."},
            ],
            "ascended": [
                {"name": "tyrant_eternal",     "description": "Ruling through absolute terror with no possibility of dissent."},
                {"name": "soul_enslaver",      "description": "Binding the wills of others permanently to your own."},
                {"name": "ravana_unchained",   "description": "Power without limit, conscience, or restraint."},
            ],
        },
    },

    # ===== 7. VALI — Strength / Vengeance =====
    "Vali": {
        "virtue": "Strength",
        "sin": "Vengeance",
        "light": {
            "core": [
                {"name": "courage",            "description": "Standing firm in the face of danger and doubt."},
                {"name": "endurance",          "description": "Persevering through hardship without breaking."},
                {"name": "protective_instinct", "description": "Using strength to shield those who cannot defend themselves."},
            ],
            "developed": [
                {"name": "righteous_fury",     "description": "Channelling anger into just and purposeful action."},
                {"name": "iron_discipline",    "description": "Forging unbreakable self-control through trial."},
                {"name": "honour_bound",       "description": "Holding to a code of conduct even at personal cost."},
            ],
            "ascended": [
                {"name": "champion_eternal",   "description": "Becoming an unbreakable symbol of justice and strength."},
                {"name": "titan_heart",        "description": "Strength that inspires entire generations."},
                {"name": "valkyrie_resolve",   "description": "Choosing who is worthy of being lifted from the battlefield."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "blind_rage",         "description": "Lashing out without thought or aim."},
                {"name": "grudge_holding",     "description": "Carrying old wounds as fuel for future violence."},
                {"name": "brute_force",        "description": "Solving every problem with aggression."},
            ],
            "developed": [
                {"name": "vengeance_oath",     "description": "Swearing to repay every slight tenfold."},
                {"name": "blood_debt",         "description": "Believing every wrong demands a physical price."},
                {"name": "war_addiction",       "description": "Needing conflict to feel alive and purposeful."},
            ],
            "ascended": [
                {"name": "berserker_void",     "description": "Entering a state of destruction beyond reason or recall."},
                {"name": "god_slayer_wrath",   "description": "Strength so great it threatens the foundations of order."},
                {"name": "eternal_avenger",    "description": "Pursuing retribution across lifetimes without end."},
            ],
        },
    },

    # ===== 8. VRITRA — Storm Control / Destruction =====
    "Vritra": {
        "virtue": "Storm Control",
        "sin": "Destruction",
        "light": {
            "core": [
                {"name": "tempest_calm",       "description": "Finding stillness inside the storm."},
                {"name": "pressure_mastery",   "description": "Performing at your best under extreme conditions."},
                {"name": "elemental_awareness", "description": "Sensing shifts in energy and atmosphere."},
            ],
            "developed": [
                {"name": "storm_channelling",  "description": "Directing volatile forces into constructive outcomes."},
                {"name": "thunder_discipline",  "description": "Harnessing explosive power with controlled release."},
                {"name": "lightning_insight",   "description": "Sudden flashes of clarity in moments of chaos."},
            ],
            "ascended": [
                {"name": "tempest_sovereign",  "description": "Absolute command over the forces of storm and change."},
                {"name": "sky_dragon_ascent",  "description": "Rising above all turbulence to see with perfect clarity."},
                {"name": "cosmic_storm_weaver", "description": "Reshaping reality through controlled elemental fury."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "volatility",         "description": "Erupting without warning and leaving damage behind."},
                {"name": "emotional_storms",   "description": "Unleashing inner chaos on those around you."},
                {"name": "collateral_damage",  "description": "Hurting bystanders through uncontrolled force."},
            ],
            "developed": [
                {"name": "siege_mentality",    "description": "Hoarding resources and blocking all flow of life."},
                {"name": "drought_bringer",    "description": "Withholding nourishment and support as punishment."},
                {"name": "destructive_surge",  "description": "Overwhelming others with wave after wave of force."},
            ],
            "ascended": [
                {"name": "sky_devourer",       "description": "Consuming the heavens and leaving only darkness."},
                {"name": "apocalypse_dragon",  "description": "Embodying total elemental annihilation."},
                {"name": "vritra_unchained",   "description": "Destruction without limit, purpose, or remorse."},
            ],
        },
    },

    # ===== 9. IRIS — Hope / Illusion =====
    "Iris": {
        "virtue": "Hope",
        "sin": "Illusion",
        "light": {
            "core": [
                {"name": "optimism",           "description": "Seeing possibility even in the darkest moments."},
                {"name": "bridge_building",    "description": "Connecting divided people and ideas."},
                {"name": "radiant_presence",   "description": "Uplifting others simply by being near."},
            ],
            "developed": [
                {"name": "vision_casting",     "description": "Painting a future others can believe in and work toward."},
                {"name": "spectral_empathy",   "description": "Sensing the full emotional spectrum in others."},
                {"name": "rainbow_diplomacy",  "description": "Finding harmony between opposing forces."},
            ],
            "ascended": [
                {"name": "hope_eternal",       "description": "Becoming an inexhaustible source of light for all."},
                {"name": "divine_messenger",   "description": "Carrying sacred truths between realms and realities."},
                {"name": "prismatic_ascension", "description": "Transforming all colours of experience into wisdom."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "false_hope",         "description": "Promising what can never be delivered."},
                {"name": "denial",             "description": "Refusing to see reality as it truly is."},
                {"name": "surface_beauty",     "description": "Hiding pain behind a bright and polished exterior."},
            ],
            "developed": [
                {"name": "mirage_crafting",    "description": "Building elaborate illusions to deceive and distract."},
                {"name": "emotional_manipulation", "description": "Using hope and despair as tools to control others."},
                {"name": "spectral_deception", "description": "Making the false appear real and the real appear false."},
            ],
            "ascended": [
                {"name": "grand_illusionist",  "description": "Rewriting what others perceive as truth and reality."},
                {"name": "phantom_queen",      "description": "Ruling a kingdom built entirely on beautiful lies."},
                {"name": "iris_shattered",     "description": "Shattering all hope so only your illusions remain."},
            ],
        },
    },

    # ===== 10. IBLIS — Rebellion / Corruption =====
    "Iblis": {
        "virtue": "Rebellion",
        "sin": "Corruption",
        "light": {
            "core": [
                {"name": "defiance",           "description": "Refusing to submit to unjust authority."},
                {"name": "free_will",          "description": "Championing the right to choose your own path."},
                {"name": "system_questioning", "description": "Challenging rules and structures that harm the many."},
            ],
            "developed": [
                {"name": "revolutionary_fire",  "description": "Igniting movements that dismantle oppressive systems."},
                {"name": "chain_breaking",      "description": "Liberating others from invisible bonds and false obligations."},
                {"name": "sacred_dissent",      "description": "Speaking truth to power with conviction and purpose."},
            ],
            "ascended": [
                {"name": "liberator_supreme",  "description": "Freeing entire peoples from systemic oppression."},
                {"name": "flame_of_autonomy",  "description": "Embodying the eternal right to self-determination."},
                {"name": "iblis_redeemed",     "description": "Rebellion transformed into the highest form of service."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "spite",              "description": "Opposing authority purely out of bitterness."},
                {"name": "temptation",         "description": "Luring others toward destructive choices."},
                {"name": "moral_erosion",      "description": "Slowly dissolving ethical boundaries in yourself and others."},
            ],
            "developed": [
                {"name": "corruption_seed",    "description": "Planting doubt and decay inside strong foundations."},
                {"name": "whisper_of_ruin",    "description": "Poisoning minds with subtle, persistent influence."},
                {"name": "false_liberation",   "description": "Promising freedom while delivering a different prison."},
            ],
            "ascended": [
                {"name": "arch_corruptor",     "description": "Turning the virtuous against their own principles."},
                {"name": "void_sovereign",     "description": "Ruling through the total absence of meaning and order."},
                {"name": "iblis_unchained",    "description": "Corruption so deep it becomes indistinguishable from truth."},
            ],
        },
    },

    # ===== 11. SIGYN — Loyalty / Sacrifice =====
    "Sigyn": {
        "virtue": "Loyalty",
        "sin": "Sacrifice",
        "light": {
            "core": [
                {"name": "steadfastness",      "description": "Standing by your people through every trial."},
                {"name": "unconditional_care",  "description": "Supporting others without expectation of return."},
                {"name": "quiet_strength",     "description": "Enduring silently so others may carry on."},
            ],
            "developed": [
                {"name": "unbreakable_bond",   "description": "Forging connections that survive betrayal and time."},
                {"name": "compassion_shield",  "description": "Protecting others from harm through selfless devotion."},
                {"name": "grief_alchemy",      "description": "Transforming sorrow into wisdom and renewed purpose."},
            ],
            "ascended": [
                {"name": "eternal_guardian",    "description": "A protector whose loyalty transcends death itself."},
                {"name": "sigyn_ascended",     "description": "Loyalty so pure it becomes a cosmic force for good."},
                {"name": "love_immortal",      "description": "A bond that cannot be broken by any power."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "self_neglect",       "description": "Giving everything to others while destroying yourself."},
                {"name": "blind_loyalty",      "description": "Following someone unworthy because you cannot let go."},
                {"name": "suffering_addiction", "description": "Believing that pain is proof of devotion."},
            ],
            "developed": [
                {"name": "martyr_complex",     "description": "Making your suffering a spectacle to earn love."},
                {"name": "guilt_binding",      "description": "Keeping others close through shared guilt and obligation."},
                {"name": "emotional_hostage",  "description": "Trapping others with your sacrifices so they cannot leave."},
            ],
            "ascended": [
                {"name": "eternal_mourner",    "description": "Grief so deep it paralyses all growth and change."},
                {"name": "sigyn_shattered",    "description": "Loyalty twisted into a prison for yourself and others."},
                {"name": "sacrifice_abyss",    "description": "Giving so much that nothing of the self remains."},
            ],
        },
    },

    # ===== 12. SET — Survival / Betrayal =====
    "Set": {
        "virtue": "Survival",
        "sin": "Betrayal",
        "light": {
            "core": [
                {"name": "resourcefulness",    "description": "Making the most of whatever is at hand."},
                {"name": "desert_endurance",   "description": "Thriving where others would perish."},
                {"name": "primal_instinct",    "description": "Trusting the body and gut when logic fails."},
            ],
            "developed": [
                {"name": "storm_riding",       "description": "Using adversity as fuel rather than obstacle."},
                {"name": "territory_mastery",  "description": "Commanding your environment with adaptive intelligence."},
                {"name": "predator_focus",     "description": "Locking onto a goal with total single-minded pursuit."},
            ],
            "ascended": [
                {"name": "unkillable_will",    "description": "A survival instinct so powerful nothing can extinguish it."},
                {"name": "set_reborn",         "description": "Rising from total defeat stronger than before."},
                {"name": "sovereign_of_storms", "description": "Mastering the harshest forces of nature and fate."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "treachery",          "description": "Betraying trust to gain advantage."},
                {"name": "paranoia",           "description": "Seeing threats everywhere, trusting no one."},
                {"name": "selfish_survival",   "description": "Saving yourself at the expense of everyone else."},
            ],
            "developed": [
                {"name": "kin_slayer",         "description": "Destroying those closest to you for power or safety."},
                {"name": "throne_usurper",     "description": "Seizing what belongs to others through betrayal."},
                {"name": "scorpion_nature",    "description": "Stinging those who carry you because it is in your nature."},
            ],
            "ascended": [
                {"name": "lord_of_betrayal",   "description": "Betrayal elevated to an art form and a way of life."},
                {"name": "chaos_sovereign",    "description": "Ruling through unpredictability and broken trust."},
                {"name": "set_unchained",      "description": "Survival at any cost — no bond, oath, or life is sacred."},
            ],
        },
    },

    # ===== 13. HORUS — Vision / Ego =====
    "Horus": {
        "virtue": "Vision",
        "sin": "Ego",
        "light": {
            "core": [
                {"name": "clarity_of_sight",    "description": "Perceiving the truth of a situation without bias or distortion."},
                {"name": "purposeful_vision",   "description": "Setting a clear goal and holding it through adversity."},
                {"name": "sky_awareness",       "description": "Seeing the full landscape of a situation from above."},
            ],
            "developed": [
                {"name": "divine_perception",   "description": "Reading the deeper intention behind words and actions."},
                {"name": "dual_crown_wisdom",   "description": "Holding both the higher and earthly view in balance simultaneously."},
                {"name": "falcon_focus",        "description": "Locking onto what matters with total precision."},
            ],
            "ascended": [
                {"name": "all_seeing_sovereignty", "description": "Commanding entire systems through perfect visionary clarity."},
                {"name": "falcon_ascent",       "description": "Rising above all conflict to see with unclouded eyes."},
                {"name": "horus_reborn",        "description": "Vision so complete it heals and unifies what was divided."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "ego_blindness",       "description": "Believing your view is the only correct one."},
                {"name": "self_obsession",      "description": "Centering every situation around your own needs and glory."},
                {"name": "tunnel_vision",       "description": "Fixating so hard on one goal that all else is destroyed."},
            ],
            "developed": [
                {"name": "narcissistic_fury",   "description": "Lashing out when others fail to validate your greatness."},
                {"name": "wounded_eye",         "description": "Using past wounds as justification for present cruelty."},
                {"name": "vengeance_sight",     "description": "Seeing every setback as a personal attack requiring retaliation."},
            ],
            "ascended": [
                {"name": "ego_eclipse",         "description": "Your need for supremacy blotting out all other light."},
                {"name": "tyrant_vision",       "description": "Ruling through the imposition of your personal worldview on all others."},
                {"name": "horus_corrupted",     "description": "Divine sight turned inward, consuming its host with pride."},
            ],
        },
    },

    # ===== 14. MORRIGAN — Fate / Despair =====
    "Morrigan": {
        "virtue": "Fate",
        "sin": "Despair",
        "light": {
            "core": [
                {"name": "fate_acceptance",     "description": "Embracing what cannot be changed without losing yourself."},
                {"name": "prophetic_sight",     "description": "Reading the currents of what is coming before it arrives."},
                {"name": "death_unafraid",      "description": "Facing endings with courage rather than avoidance."},
            ],
            "developed": [
                {"name": "sovereignty_of_self", "description": "Claiming complete ownership of your path and destiny."},
                {"name": "battle_clarity",      "description": "Finding sharp focus in the midst of chaos and loss."},
                {"name": "crow_wisdom",         "description": "Understanding that transformation lives inside every ending."},
            ],
            "ascended": [
                {"name": "fate_weaver",         "description": "Shaping the threads of destiny with conscious intent."},
                {"name": "rebirth_herald",      "description": "Announcing the end of one age and the beginning of another."},
                {"name": "morrigan_ascended",   "description": "Fate fully integrated — death and life held as one truth."},
            ],
        },
        "shadow": {
            "core": [
                {"name": "doom_fixation",       "description": "Obsessing over worst-case outcomes until they feel inevitable."},
                {"name": "despair_paralysis",   "description": "Unable to act because defeat already feels certain."},
                {"name": "prophecy_obsession",  "description": "Treating feared futures as fixed truths that cannot be changed."},
            ],
            "developed": [
                {"name": "grief_spiral",        "description": "Drowning in loss so completely that nothing can pull you out."},
                {"name": "fate_denial",         "description": "Refusing to accept necessary endings until they become catastrophic."},
                {"name": "crow_curse",          "description": "Spreading hopelessness to others like a contagion."},
            ],
            "ascended": [
                {"name": "despair_sovereign",   "description": "Ruling through the weaponisation of inevitability and dread."},
                {"name": "morrigan_unchained",  "description": "Despair so absolute that possibility itself ceases to exist."},
                {"name": "fate_destroyer",      "description": "Tearing apart the threads of destiny out of grief or spite."},
            ],
        },
    },
}


# -----------------------------
# Helper Functions
# -----------------------------

def get_pillar_traits(pillar_name):
    """
    Return all 18 traits for a given pillar.

    Returns:
        dict with 'light' and 'shadow' keys, or None if pillar not found.
    """
    pillar = PILLAR_TRAITS.get(pillar_name)
    if pillar is None:
        return None
    return {
        "light": pillar["light"],
        "shadow": pillar["shadow"],
    }


def get_traits_by_alignment(pillar_name, alignment):
    """
    Return only light or shadow traits for a given pillar.

    Parameters:
        pillar_name: Name of the pillar (e.g. "Janus")
        alignment:   "light" or "shadow"

    Returns:
        dict with 'core', 'developed', 'ascended' keys, or None.
    """
    pillar = PILLAR_TRAITS.get(pillar_name)
    if pillar is None:
        return None
    if alignment not in ("light", "shadow"):
        return None
    return pillar.get(alignment)


def get_traits_by_tier(pillar_name, alignment, tier):
    """
    Return traits for a specific pillar, alignment, and tier.

    Parameters:
        pillar_name: Name of the pillar (e.g. "Janus")
        alignment:   "light" or "shadow"
        tier:        "core", "developed", or "ascended"

    Returns:
        list of trait dicts, or None.
    """
    traits = get_traits_by_alignment(pillar_name, alignment)
    if traits is None:
        return None
    if tier not in ("core", "developed", "ascended"):
        return None
    return traits.get(tier)


def get_all_pillar_names():
    """Return a list of all pillar names in the trait system."""
    return list(PILLAR_TRAITS.keys())


def count_total_traits():
    """Return the total number of traits across all pillars."""
    total = 0
    for pillar in PILLAR_TRAITS.values():
        for alignment in ("light", "shadow"):
            for tier in ("core", "developed", "ascended"):
                total += len(pillar[alignment][tier])
    return total
