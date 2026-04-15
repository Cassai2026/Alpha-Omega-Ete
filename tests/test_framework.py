import os
import json
import copy
import unittest
from framework import (
    load_framework,
    save_framework,
    get_triad,
    get_triad_member,
    get_mentor_forms,
    get_all_pillars,
    get_pillar,
    get_pillar_by_virtue,
    get_pillar_by_sin,
    get_form,
    FRAMEWORK_FILE,
)

TEST_FRAMEWORK_FILE = os.path.join(os.path.dirname(__file__), "_test_framework.json")


class TestAnimusFramework(unittest.TestCase):
    """Tests for the Animus Framework (Celestial Triad + 12 Pillars)."""

    @classmethod
    def setUpClass(cls):
        cls.original_data = load_framework(FRAMEWORK_FILE)
        save_framework(cls.original_data, TEST_FRAMEWORK_FILE)

    def setUp(self):
        self.data = copy.deepcopy(self.original_data)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_FRAMEWORK_FILE):
            os.remove(TEST_FRAMEWORK_FILE)

    # ----- Loading & Structure -----

    def test_framework_loads(self):
        data = load_framework(FRAMEWORK_FILE)
        self.assertIn("celestial_triad", data)
        self.assertIn("pillars", data)

    def test_framework_has_system(self):
        self.assertEqual(self.data["system"], "CassAI Animus Framework")

    def test_total_entities(self):
        self.assertEqual(self.data["total_entities"], 15)

    # ----- Celestial Triad -----

    def test_triad_has_three_members(self):
        triad = get_triad(self.data)
        self.assertEqual(len(triad), 3)

    def test_triad_members_present(self):
        triad = get_triad(self.data)
        for name in ["Lilith", "Odin", "Hekete"]:
            self.assertIn(name, triad, f"Expected '{name}' in Celestial Triad")

    def test_lilith_is_prime_origin(self):
        lilith = get_triad_member("Lilith", self.data)
        self.assertEqual(lilith["tier"], "Prime Origin")
        self.assertEqual(lilith["role"], "Source of the Animus system")

    def test_odin_is_celestial_mentor(self):
        odin = get_triad_member("Odin", self.data)
        self.assertEqual(odin["tier"], "Celestial Mentor")

    def test_hekete_is_celestial_mentor(self):
        hekete = get_triad_member("Hekete", self.data)
        self.assertEqual(hekete["tier"], "Celestial Mentor")

    def test_triad_forms_have_three_types(self):
        for name in ["Lilith", "Odin", "Hekete"]:
            forms = get_mentor_forms(name, self.data)
            self.assertIn("prime", forms)
            self.assertIn("lumen", forms)
            self.assertIn("umbra", forms)

    def test_nonexistent_triad_member(self):
        result = get_triad_member("FakeMentor", self.data)
        self.assertIsNone(result)

    # ----- 12 Pillars -----

    def test_pillars_has_twelve(self):
        pillars = get_all_pillars(self.data)
        self.assertEqual(len(pillars), 12)

    def test_all_pillar_names_present(self):
        expected = [
            "Janus", "Jormungandr", "Anubis", "Apep",
            "Raven", "Ravana", "Vali", "Vritra",
            "Iris", "Irlis", "Sigyn", "Set",
        ]
        pillars = get_all_pillars(self.data)
        for name in expected:
            self.assertIn(name, pillars, f"Expected pillar '{name}'")

    def test_all_pillars_have_virtue_and_sin(self):
        for name, entry in get_all_pillars(self.data).items():
            self.assertIn("virtue", entry, f"'{name}' missing virtue")
            self.assertIn("sin", entry, f"'{name}' missing sin")

    def test_all_pillars_have_lumen_and_umbra(self):
        for name, entry in get_all_pillars(self.data).items():
            forms = entry.get("forms", {})
            self.assertIn("lumen", forms, f"'{name}' missing lumen form")
            self.assertIn("umbra", forms, f"'{name}' missing umbra form")

    def test_janus_virtue_and_sin(self):
        janus = get_pillar("Janus", self.data)
        self.assertEqual(janus["virtue"], "Wisdom")
        self.assertEqual(janus["sin"], "Deception")

    def test_anubis_forms(self):
        self.assertEqual(get_form("Anubis", "lumen", self.data), "Guardian of Souls")
        self.assertEqual(get_form("Anubis", "umbra", self.data), "Harbinger of Death")

    # ----- Lookup by Virtue / Sin -----

    def test_find_pillar_by_virtue(self):
        result = get_pillar_by_virtue("Justice", self.data)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Anubis")

    def test_find_pillar_by_sin(self):
        result = get_pillar_by_sin("Betrayal", self.data)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Set")

    def test_find_pillar_by_virtue_case_insensitive(self):
        result = get_pillar_by_virtue("wisdom", self.data)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Janus")

    def test_find_nonexistent_virtue(self):
        result = get_pillar_by_virtue("FakeVirtue", self.data)
        self.assertIsNone(result)

    # ----- Edge Cases -----

    def test_get_form_nonexistent_pillar(self):
        result = get_form("FakePillar", "lumen", self.data)
        self.assertIsNone(result)

    def test_get_form_nonexistent_type(self):
        result = get_form("Janus", "prime", self.data)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()