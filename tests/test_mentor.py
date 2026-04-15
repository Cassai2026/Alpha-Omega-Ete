import unittest
from mentor import (
    MENTORS,
    get_mentor_profile,
    get_mentor_guidance,
    get_mentor_form_response,
    get_shadow_encounter_response,
    get_mentor_style,
    get_mentor_pillars,
    get_all_mentor_names,
)

EXPECTED_MENTORS = ["KONG", "ODIN", "Hekete", "Lilith"]
VALID_TIERS = ("core", "developed", "ascended")
VALID_FORMS = ("omega", "ultima", "eternium")


class TestMentorDataStructure(unittest.TestCase):
    """Tests for the MENTORS data structure."""

    def test_has_four_mentors(self):
        self.assertEqual(len(MENTORS), 4)

    def test_all_expected_mentors_present(self):
        names = get_all_mentor_names()
        for mentor in EXPECTED_MENTORS:
            self.assertIn(mentor, names, f"Expected mentor '{mentor}'")

    def test_all_mentors_have_required_keys(self):
        required = {"title", "domain", "role", "style", "description",
                    "guidance", "form_responses", "shadow_encounter"}
        for name, entry in MENTORS.items():
            for key in required:
                self.assertIn(key, entry, f"'{name}' missing key '{key}'")

    def test_all_mentors_have_three_guidance_tiers(self):
        for name, entry in MENTORS.items():
            guidance = entry.get("guidance", {})
            for tier in VALID_TIERS:
                self.assertIn(tier, guidance,
                              f"'{name}' missing guidance tier '{tier}'")

    def test_all_guidance_tiers_have_three_entries(self):
        for name, entry in MENTORS.items():
            for tier in VALID_TIERS:
                prompts = entry["guidance"][tier]
                self.assertEqual(len(prompts), 3,
                                 f"'{name}.guidance.{tier}' should have 3 prompts")

    def test_all_guidance_entries_are_strings(self):
        for name, entry in MENTORS.items():
            for tier in VALID_TIERS:
                for prompt in entry["guidance"][tier]:
                    self.assertIsInstance(prompt, str,
                                         f"Guidance in '{name}.{tier}' is not a string")

    def test_all_mentors_have_three_form_responses(self):
        for name, entry in MENTORS.items():
            responses = entry.get("form_responses", {})
            for form in VALID_FORMS:
                self.assertIn(form, responses,
                              f"'{name}' missing form response for '{form}'")

    def test_all_form_responses_are_strings(self):
        for name, entry in MENTORS.items():
            for form in VALID_FORMS:
                response = entry["form_responses"].get(form)
                self.assertIsInstance(response, str,
                                      f"'{name}.form_responses.{form}' is not a string")

    def test_all_mentors_have_shadow_encounter_list(self):
        for name, entry in MENTORS.items():
            encounter = entry.get("shadow_encounter")
            self.assertIsInstance(encounter, list,
                                  f"'{name}.shadow_encounter' should be a list")
            self.assertEqual(len(encounter), 3,
                             f"'{name}.shadow_encounter' should have 3 prompts")

    def test_all_shadow_encounter_entries_are_strings(self):
        for name, entry in MENTORS.items():
            for prompt in entry["shadow_encounter"]:
                self.assertIsInstance(prompt, str)


class TestKnownMentorData(unittest.TestCase):
    """Tests for specific mentor content."""

    def test_kong_title(self):
        self.assertEqual(MENTORS["KONG"]["title"], "The Alpha")

    def test_odin_title(self):
        self.assertEqual(MENTORS["ODIN"]["title"], "The Allfather")

    def test_hekete_title(self):
        self.assertEqual(MENTORS["Hekete"]["title"], "The Triple Goddess")

    def test_lilith_title(self):
        self.assertEqual(MENTORS["Lilith"]["title"], "The Prime Origin")

    def test_kong_style(self):
        self.assertEqual(MENTORS["KONG"]["style"], "direct")

    def test_odin_style(self):
        self.assertEqual(MENTORS["ODIN"]["style"], "strategic")

    def test_hekete_style(self):
        self.assertEqual(MENTORS["Hekete"]["style"], "reflective")

    def test_lilith_style(self):
        self.assertEqual(MENTORS["Lilith"]["style"], "absolute")


class TestMentorHelperFunctions(unittest.TestCase):
    """Tests for the mentor helper functions."""

    def test_get_mentor_profile_known(self):
        profile = get_mentor_profile("KONG")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["title"], "The Alpha")

    def test_get_mentor_profile_unknown(self):
        result = get_mentor_profile("FakeMentor")
        self.assertIsNone(result)

    def test_get_mentor_guidance_valid(self):
        guidance = get_mentor_guidance("ODIN", "core")
        self.assertIsInstance(guidance, list)
        self.assertEqual(len(guidance), 3)

    def test_get_mentor_guidance_all_tiers(self):
        for mentor in EXPECTED_MENTORS:
            for tier in VALID_TIERS:
                result = get_mentor_guidance(mentor, tier)
                self.assertIsNotNone(result,
                                     f"get_mentor_guidance('{mentor}', '{tier}') returned None")

    def test_get_mentor_guidance_invalid_mentor(self):
        result = get_mentor_guidance("FakeMentor", "core")
        self.assertIsNone(result)

    def test_get_mentor_guidance_invalid_tier(self):
        result = get_mentor_guidance("KONG", "legendary")
        self.assertIsNone(result)

    def test_get_mentor_form_response_valid(self):
        for mentor in EXPECTED_MENTORS:
            for form in VALID_FORMS:
                response = get_mentor_form_response(mentor, form)
                self.assertIsNotNone(response,
                                     f"get_mentor_form_response('{mentor}', '{form}') returned None")
                self.assertIsInstance(response, str)

    def test_get_mentor_form_response_invalid_mentor(self):
        result = get_mentor_form_response("FakeMentor", "omega")
        self.assertIsNone(result)

    def test_get_mentor_form_response_invalid_form(self):
        result = get_mentor_form_response("KONG", "prime")
        self.assertIsNone(result)

    def test_get_shadow_encounter_response_valid(self):
        for mentor in EXPECTED_MENTORS:
            result = get_shadow_encounter_response(mentor)
            self.assertIsNotNone(result)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 3)

    def test_get_shadow_encounter_response_invalid(self):
        result = get_shadow_encounter_response("FakeMentor")
        self.assertIsNone(result)

    def test_get_mentor_style_valid(self):
        self.assertEqual(get_mentor_style("KONG"), "direct")
        self.assertEqual(get_mentor_style("ODIN"), "strategic")
        self.assertEqual(get_mentor_style("Hekete"), "reflective")
        self.assertEqual(get_mentor_style("Lilith"), "absolute")

    def test_get_mentor_style_invalid(self):
        result = get_mentor_style("FakeMentor")
        self.assertIsNone(result)

    def test_get_mentor_pillars_kong(self):
        pillars = get_mentor_pillars("KONG")
        self.assertIsInstance(pillars, list)
        self.assertGreater(len(pillars), 0)
        for p in ("Apep", "Ravana", "Vali", "Vritra", "Set"):
            self.assertIn(p, pillars, f"Expected '{p}' in KONG's pillars")

    def test_get_mentor_pillars_odin(self):
        pillars = get_mentor_pillars("ODIN")
        for p in ("Janus", "Jormungandr", "Anubis", "Raven", "Horus"):
            self.assertIn(p, pillars, f"Expected '{p}' in ODIN's pillars")

    def test_get_mentor_pillars_hekete(self):
        pillars = get_mentor_pillars("Hekete")
        for p in ("Iris", "Iblis", "Sigyn", "Morrigan"):
            self.assertIn(p, pillars, f"Expected '{p}' in Hekete's pillars")

    def test_get_mentor_pillars_lilith_empty(self):
        pillars = get_mentor_pillars("Lilith")
        self.assertEqual(pillars, [],
                         "Lilith has no assigned pillars in the registry")

    def test_get_mentor_pillars_unknown(self):
        result = get_mentor_pillars("FakeMentor")
        self.assertEqual(result, [])

    def test_get_all_mentor_names_returns_four(self):
        names = get_all_mentor_names()
        self.assertEqual(len(names), 4)
        for mentor in EXPECTED_MENTORS:
            self.assertIn(mentor, names)


if __name__ == "__main__":
    unittest.main()
