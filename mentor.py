# -----------------------------
# Eternius Animus — Mentor System
# 4 Mentors: KONG, ODIN, Hekete, Lilith
#
# Each mentor has:
#   - profile (title, domain, role, style)
#   - guidance prompts per trait tier (core/developed/ascended)
#   - form responses per form tier (omega/ultima/eternium)
#   - shadow encounter responses
# -----------------------------

from animus_registry import get_pillars_by_mentor

# -----------------------------
# Mentor Profiles
# -----------------------------

MENTORS = {

    "KONG": {
        "title": "The Alpha",
        "domain": "Execution, Building, Physical Mastery",
        "role": "Primary guide for action-oriented pillars",
        "style": "direct",
        "description": "KONG speaks in short, powerful statements. He challenges you to act, build, and prove yourself through effort.",
        "pillars": None,  # populated at runtime via get_mentor_pillars()

        "guidance": {
            "core": [
                "Start moving. Thinking without doing is standing still.",
                "Strength is built, not born. Get to work.",
                "Your first step doesn't need to be perfect. It needs to exist.",
            ],
            "developed": [
                "You've got the basics. Now sharpen them into weapons.",
                "Discipline is what separates potential from power.",
                "Others talk about what they'll do. You're doing it. Keep going.",
            ],
            "ascended": [
                "You've earned this level. Now protect those coming up behind you.",
                "Mastery isn't the end. It's the beginning of responsibility.",
                "Your strength is a shield for others now. Carry it well.",
            ],
        },

        "form_responses": {
            "omega": "You've awakened. The real fight starts now.",
            "ultima": "Full power unlocked. Don't waste it on small things.",
            "eternium": "You've transcended. Lead by example — the world is watching.",
        },

        "shadow_encounter": [
            "Face it. Running from your shadow makes it stronger.",
            "This is the test. What you do next defines you.",
            "Your shadow isn't your enemy — it's your mirror. Look at it.",
        ],
    },

    "ODIN": {
        "title": "The Allfather",
        "domain": "Strategy, Knowledge, Structure",
        "role": "Mentor of cognition, long-term planning, and knowledge paths",
        "style": "strategic",
        "description": "ODIN speaks with measured wisdom. He asks questions that force you to think deeper, plan further, and see the bigger picture.",
        "pillars": None,

        "guidance": {
            "core": [
                "Before you act, ask: what are you trying to build?",
                "Knowledge without purpose is noise. Find your signal.",
                "The first lesson is patience. The second is observation.",
            ],
            "developed": [
                "You see patterns now. Use them — but question them too.",
                "Strategy is not control. It is preparation meeting opportunity.",
                "A good plan today beats a perfect plan tomorrow.",
            ],
            "ascended": [
                "You now see what others cannot. Use that sight wisely.",
                "The greatest strategist serves something larger than themselves.",
                "Wisdom is knowing when not to act. You've earned that clarity.",
            ],
        },

        "form_responses": {
            "omega": "Your mind has awakened. Now align it with purpose.",
            "ultima": "You command the full scope of your knowledge. Direct it.",
            "eternium": "You see across timelines. Guard the paths you open for others.",
        },

        "shadow_encounter": [
            "Your shadow holds a lesson. What is it trying to teach you?",
            "Do not fight it blindly. Understand it first, then decide.",
            "The shadow tests your strategy. Respond — don't react.",
        ],
    },

    "Hekete": {
        "title": "The Triple Goddess",
        "domain": "Transformation, Intuition, Pathways",
        "role": "Mentor of transformation, emotional intelligence, and hidden paths",
        "style": "reflective",
        "description": "Hekete speaks through questions and reflections. She guides you to look inward, trust your intuition, and embrace transformation.",
        "pillars": None,

        "guidance": {
            "core": [
                "What does your instinct tell you? Trust it before your logic.",
                "The crossroads is not a trap — it is an invitation to choose.",
                "Before you seek answers, ask if you're asking the right question.",
            ],
            "developed": [
                "You've learned to listen to yourself. Now listen to the silence.",
                "Transformation is not comfortable. That's how you know it's real.",
                "The path behind you shaped you. The path ahead is yours to shape.",
            ],
            "ascended": [
                "You stand at the crossroads as a guide now, not a traveller.",
                "Your light reaches others through the dark. Hold it steady.",
                "You've transformed. Now help others find the courage to begin.",
            ],
        },

        "form_responses": {
            "omega": "You've stepped onto the path. The crossroads will test you.",
            "ultima": "You carry the torch now. Others will follow your light.",
            "eternium": "You are the crossroads. Every path leads through you.",
        },

        "shadow_encounter": [
            "What is this shadow protecting you from? Look closer.",
            "Your shadow is not your enemy — it is the self you haven't met yet.",
            "Sit with this feeling. The answer comes when you stop running.",
        ],
    },

    "Lilith": {
        "title": "The Prime Origin",
        "domain": "Balance, Integration, Omega Oversight",
        "role": "Source of the Animus system — oversees balance between all mentors",
        "style": "absolute",
        "description": "Lilith speaks rarely and with finality. She appears at critical moments of integration, balance, or when a player reaches the threshold between light and shadow.",
        "pillars": None,

        "guidance": {
            "core": [
                "You exist between two forces. Neither is wrong.",
                "Creation and void are the same breath. Learn to hold both.",
                "I do not guide. I reveal. What you see is yours to carry.",
            ],
            "developed": [
                "The balance you seek is not stillness — it is motion between poles.",
                "You are not choosing light or shadow. You are choosing awareness.",
                "Every mentor has shown you a piece. I show you the whole.",
            ],
            "ascended": [
                "You have looked into the abyss and the abyss recognised you.",
                "There is nothing left to teach. Only what you choose to become.",
                "You are the balance now. The system lives through you.",
            ],
        },

        "form_responses": {
            "omega": "The first gate opens. You are seen.",
            "ultima": "The veil falls. You see yourself as you truly are.",
            "eternium": "You are Eternius. The origin and the destination are one.",
        },

        "shadow_encounter": [
            "This shadow is not separate from you. It is you, unintegrated.",
            "I will not protect you from yourself. That is your work.",
            "The shadow and the light were never enemies. You made them so.",
        ],
    },
}


# -----------------------------
# Helper Functions
# -----------------------------

def get_mentor_profile(mentor_name):
    """Return the full mentor profile dict, or None."""
    return MENTORS.get(mentor_name)


def get_mentor_guidance(mentor_name, tier):
    """
    Return guidance prompts for a mentor at a given tier.

    Parameters:
        mentor_name: "KONG", "ODIN", "Hekete", or "Lilith"
        tier:        "core", "developed", or "ascended"

    Returns:
        list of guidance strings, or None.
    """
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    if tier not in ("core", "developed", "ascended"):
        return None
    return mentor["guidance"].get(tier)


def get_mentor_form_response(mentor_name, form_name):
    """
    Return a mentor's response when a player unlocks a form.

    Parameters:
        mentor_name: "KONG", "ODIN", "Hekete", or "Lilith"
        form_name:   "omega", "ultima", or "eternium"

    Returns:
        Response string, or None.
    """
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    if form_name not in ("omega", "ultima", "eternium"):
        return None
    return mentor["form_responses"].get(form_name)


def get_shadow_encounter_response(mentor_name):
    """
    Return the shadow encounter prompts for a mentor.

    Returns:
        list of response strings, or None.
    """
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    return mentor.get("shadow_encounter")


def get_mentor_style(mentor_name):
    """Return the communication style for a mentor, or None."""
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    return mentor.get("style")


def get_mentor_pillars(mentor_name):
    """
    Return all pillar names assigned to a mentor (from the registry).

    Parameters:
        mentor_name: "KONG", "ODIN", "Hekete", or "Lilith"

    Returns:
        list of pillar name strings.
    """
    return get_pillars_by_mentor(mentor_name)


def get_all_mentor_names():
    """Return a list of all mentor names."""
    return list(MENTORS.keys())


def display_mentors():
    """Pretty-print all mentor profiles to the console."""
    print(f"\n{'='*60}")
    print(f"  ETERNIUS MENTOR SYSTEM")
    print(f"{'='*60}\n")

    for name, info in MENTORS.items():
        pillars = get_mentor_pillars(name)
        pillar_str = ", ".join(pillars) if pillars else "None assigned"
        print(f"  ⦿ {name} — {info['title']}")
        print(f"    Domain:  {info['domain']}")
        print(f"    Role:    {info['role']}")
        print(f"    Style:   {info['style']}")
        print(f"    Pillars: {pillar_str}")
        print(f"    {info['description']}")
        print()                 # -----------------------------
# Eternius Animus — Mentor System
# 4 Mentors: KONG, ODIN, Hekete, Lilith
#
# Each mentor has:
#   - profile (title, domain, role, style)
#   - guidance prompts per trait tier (core/developed/ascended)
#   - form responses per form tier (omega/ultima/eternium)
#   - shadow encounter responses
# -----------------------------

from animus_registry import get_pillars_by_mentor

# -----------------------------
# Mentor Profiles
# -----------------------------

MENTORS = {

    "KONG": {
        "title": "The Alpha",
        "domain": "Execution, Building, Physical Mastery",
        "role": "Primary guide for action-oriented pillars",
        "style": "direct",
        "description": "KONG speaks in short, powerful statements. He challenges you to act, build, and prove yourself through effort.",
        "pillars": None,  # populated at runtime via get_mentor_pillars()

        "guidance": {
            "core": [
                "Start moving. Thinking without doing is standing still.",
                "Strength is built, not born. Get to work.",
                "Your first step doesn't need to be perfect. It needs to exist.",
            ],
            "developed": [
                "You've got the basics. Now sharpen them into weapons.",
                "Discipline is what separates potential from power.",
                "Others talk about what they'll do. You're doing it. Keep going.",
            ],
            "ascended": [
                "You've earned this level. Now protect those coming up behind you.",
                "Mastery isn't the end. It's the beginning of responsibility.",
                "Your strength is a shield for others now. Carry it well.",
            ],
        },

        "form_responses": {
            "omega": "You've awakened. The real fight starts now.",
            "ultima": "Full power unlocked. Don't waste it on small things.",
            "eternium": "You've transcended. Lead by example — the world is watching.",
        },

        "shadow_encounter": [
            "Face it. Running from your shadow makes it stronger.",
            "This is the test. What you do next defines you.",
            "Your shadow isn't your enemy — it's your mirror. Look at it.",
        ],
    },

    "ODIN": {
        "title": "The Allfather",
        "domain": "Strategy, Knowledge, Structure",
        "role": "Mentor of cognition, long-term planning, and knowledge paths",
        "style": "strategic",
        "description": "ODIN speaks with measured wisdom. He asks questions that force you to think deeper, plan further, and see the bigger picture.",
        "pillars": None,

        "guidance": {
            "core": [
                "Before you act, ask: what are you trying to build?",
                "Knowledge without purpose is noise. Find your signal.",
                "The first lesson is patience. The second is observation.",
            ],
            "developed": [
                "You see patterns now. Use them — but question them too.",
                "Strategy is not control. It is preparation meeting opportunity.",
                "A good plan today beats a perfect plan tomorrow.",
            ],
            "ascended": [
                "You now see what others cannot. Use that sight wisely.",
                "The greatest strategist serves something larger than themselves.",
                "Wisdom is knowing when not to act. You've earned that clarity.",
            ],
        },

        "form_responses": {
            "omega": "Your mind has awakened. Now align it with purpose.",
            "ultima": "You command the full scope of your knowledge. Direct it.",
            "eternium": "You see across timelines. Guard the paths you open for others.",
        },

        "shadow_encounter": [
            "Your shadow holds a lesson. What is it trying to teach you?",
            "Do not fight it blindly. Understand it first, then decide.",
            "The shadow tests your strategy. Respond — don't react.",
        ],
    },

    "Hekete": {
        "title": "The Triple Goddess",
        "domain": "Transformation, Intuition, Pathways",
        "role": "Mentor of transformation, emotional intelligence, and hidden paths",
        "style": "reflective",
        "description": "Hekete speaks through questions and reflections. She guides you to look inward, trust your intuition, and embrace transformation.",
        "pillars": None,

        "guidance": {
            "core": [
                "What does your instinct tell you? Trust it before your logic.",
                "The crossroads is not a trap — it is an invitation to choose.",
                "Before you seek answers, ask if you're asking the right question.",
            ],
            "developed": [
                "You've learned to listen to yourself. Now listen to the silence.",
                "Transformation is not comfortable. That's how you know it's real.",
                "The path behind you shaped you. The path ahead is yours to shape.",
            ],
            "ascended": [
                "You stand at the crossroads as a guide now, not a traveller.",
                "Your light reaches others through the dark. Hold it steady.",
                "You've transformed. Now help others find the courage to begin.",
            ],
        },

        "form_responses": {
            "omega": "You've stepped onto the path. The crossroads will test you.",
            "ultima": "You carry the torch now. Others will follow your light.",
            "eternium": "You are the crossroads. Every path leads through you.",
        },

        "shadow_encounter": [
            "What is this shadow protecting you from? Look closer.",
            "Your shadow is not your enemy — it is the self you haven't met yet.",
            "Sit with this feeling. The answer comes when you stop running.",
        ],
    },

    "Lilith": {
        "title": "The Prime Origin",
        "domain": "Balance, Integration, Omega Oversight",
        "role": "Source of the Animus system — oversees balance between all mentors",
        "style": "absolute",
        "description": "Lilith speaks rarely and with finality. She appears at critical moments of integration, balance, or when a player reaches the threshold between light and shadow.",
        "pillars": None,

        "guidance": {
            "core": [
                "You exist between two forces. Neither is wrong.",
                "Creation and void are the same breath. Learn to hold both.",
                "I do not guide. I reveal. What you see is yours to carry.",
            ],
            "developed": [
                "The balance you seek is not stillness — it is motion between poles.",
                "You are not choosing light or shadow. You are choosing awareness.",
                "Every mentor has shown you a piece. I show you the whole.",
            ],
            "ascended": [
                "You have looked into the abyss and the abyss recognised you.",
                "There is nothing left to teach. Only what you choose to become.",
                "You are the balance now. The system lives through you.",
            ],
        },

        "form_responses": {
            "omega": "The first gate opens. You are seen.",
            "ultima": "The veil falls. You see yourself as you truly are.",
            "eternium": "You are Eternius. The origin and the destination are one.",
        },

        "shadow_encounter": [
            "This shadow is not separate from you. It is you, unintegrated.",
            "I will not protect you from yourself. That is your work.",
            "The shadow and the light were never enemies. You made them so.",
        ],
    },
}


# -----------------------------
# Helper Functions
# -----------------------------

def get_mentor_profile(mentor_name):
    """Return the full mentor profile dict, or None."""
    return MENTORS.get(mentor_name)


def get_mentor_guidance(mentor_name, tier):
    """
    Return guidance prompts for a mentor at a given tier.

    Parameters:
        mentor_name: "KONG", "ODIN", "Hekete", or "Lilith"
        tier:        "core", "developed", or "ascended"

    Returns:
        list of guidance strings, or None.
    """
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    if tier not in ("core", "developed", "ascended"):
        return None
    return mentor["guidance"].get(tier)


def get_mentor_form_response(mentor_name, form_name):
    """
    Return a mentor's response when a player unlocks a form.

    Parameters:
        mentor_name: "KONG", "ODIN", "Hekete", or "Lilith"
        form_name:   "omega", "ultima", or "eternium"

    Returns:
        Response string, or None.
    """
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    if form_name not in ("omega", "ultima", "eternium"):
        return None
    return mentor["form_responses"].get(form_name)


def get_shadow_encounter_response(mentor_name):
    """
    Return the shadow encounter prompts for a mentor.

    Returns:
        list of response strings, or None.
    """
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    return mentor.get("shadow_encounter")


def get_mentor_style(mentor_name):
    """Return the communication style for a mentor, or None."""
    mentor = MENTORS.get(mentor_name)
    if mentor is None:
        return None
    return mentor.get("style")


def get_mentor_pillars(mentor_name):
    """
    Return all pillar names assigned to a mentor (from the registry).

    Parameters:
        mentor_name: "KONG", "ODIN", "Hekete", or "Lilith"

    Returns:
        list of pillar name strings.
    """
    return get_pillars_by_mentor(mentor_name)


def get_all_mentor_names():
    """Return a list of all mentor names."""
    return list(MENTORS.keys())


def display_mentors():
    """Pretty-print all mentor profiles to the console."""
    print(f"\n{'='*60}")
    print(f"  ETERNIUS MENTOR SYSTEM")
    print(f"{'='*60}\n")

    for name, info in MENTORS.items():
        pillars = get_mentor_pillars(name)
        pillar_str = ", ".join(pillars) if pillars else "None assigned"
        print(f"  ⦿ {name} — {info['title']}")
        print(f"    Domain:  {info['domain']}")
        print(f"    Role:    {info['role']}")
        print(f"    Style:   {info['style']}")
        print(f"    Pillars: {pillar_str}")
        print(f"    {info['description']}")
        print()