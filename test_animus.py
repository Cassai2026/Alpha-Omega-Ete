import os
import json
import copy
import unittest
from animus import (
    load_catalogue,
    save_catalogue,
    get_all_animus_names,
    get_animus,
    add_animus,
    update_animus,
    remove_animus,
    calculate_xp,
    CATALOGUE_FILE,
)

# Use a temp copy so tests never corrupt the real catalogue
TEST_CATALOGUE_FILE = os.path.join(os.path.dirname(__file__), "_test_catalogue.json")


class TestAnimusCatalogue(unittest.TestCase):
    """Tests for the Animus Catalogue system."""

    @classmethod
    def setUpClass(cls):
        """Create a test copy of the catalogue."""
        cls.original_data = load_catalogue(CATALOGUE_FILE)
        save_catalogue(cls.original_data, TEST_CATALOGUE_FILE)

    def setUp(self):
        """Reload a fresh copy before each test."""
        self.data = copy.deepcopy(self.original_data)
        save_catalogue(self.data, TEST_CATALOGUE_FILE)
                                                                                                                                        
    @classmethod
    def tearDownClass(cls):
        """Clean up the temp file."""
        if os.path.exists(TEST_CATALOGUE_FILE):
            os.remove(TEST_CATALOGUE_FILE)

    # ----- Loading & Structure -----

    def test_catalogue_loads(self):
        data = load_catalogue(TEST_CATALOGUE_FILE)
        self.assertIn("version", data)
        self.assertIn("animus_entries", data)

    def test_catalogue_has_system_field(self):
        self.assertEqual(self.data["system"], "Animus Cognitive Framework")

    def test_catalogue_has_entries(self):
        names = list(self.data["animus_entries"].keys())
        self.assertGreater(len(names), 0, "Catalogue should not be empty")

    def test_all_entries_have_required_keys(self):
        required = {"title", "class", "mentor", "description", "category",
                     "pillar_alignment", "strengths", "xp_bonus",
                     "xp_bonus_tasks", "shadow_trait_interaction",
                     "shadow_risk", "mentor_note"}
        for name, entry in self.data["animus_entries"].items():
            for key in required:
                self.assertIn(key, entry, f"'{name}' missing key '{key}'")

    # ----- Known Animus Checks (from main.py / MDs) -----

    def test_known_animus_present(self):
        expected = [
            "Autocognitus", "Cogniflux", "SuiMens", "Virtumind",
            "Animora", "Takwyn", "Animundi", "Chronoleap",
            "Synthara", "Emberion", "Lumina", "Terranova",
            "Noetica", "Aetherion",
        ]
        names = get_all_animus_names(self.data)
        for animus in expected:
            self.assertIn(animus, names, f"Expected '{animus}' in catalogue")

    def test_autocognitus_bonus(self):
        entry = get_animus("Autocognitus", self.data)
        self.assertEqual(entry["xp_bonus"]["type"], "multiplier")
        self.assertAlmostEqual(entry["xp_bonus"]["value"], 1.1)

    def test_virtumind_flat_bonus(self):
        entry = get_animus("Virtumind", self.data)
        self.assertEqual(entry["xp_bonus"]["type"], "flat")
        self.assertEqual(entry["xp_bonus"]["value"], 5)

    def test_emberion_shadow_interaction(self):
        entry = get_animus("Emberion", self.data)
        self.assertEqual(entry["shadow_trait_interaction"], "reduce_half")

    def test_suimens_shadow_bypass(self):
        entry = get_animus("SuiMens", self.data)
        self.assertEqual(entry["shadow_trait_interaction"], "bypass_once")

    # ----- Class & Mentor (Cognitive Framework) -----

    def test_autocognitus_class_and_mentor(self):
        entry = get_animus("Autocognitus", self.data)
        self.assertEqual(entry["class"], "Strategist")
        self.assertEqual(entry["mentor"], "ODIN")

    def test_cogniflux_class_and_mentor(self):
        entry = get_animus("Cogniflux", self.data)
        self.assertEqual(entry["class"], "Innovator")
        self.assertEqual(entry["mentor"], "KONG")

    def test_animora_class_and_mentor(self):
        entry = get_animus("Animora", self.data)
        self.assertEqual(entry["class"], "Connector")
        self.assertEqual(entry["mentor"], "Hekete")

    def test_all_mentors_are_valid(self):
        valid_mentors = {"KONG", "Hekete", "ODIN"}
        for name, entry in self.data["animus_entries"].items():
            self.assertIn(entry["mentor"], valid_mentors,
                          f"'{name}' has invalid mentor '{entry['mentor']}'")

    # ----- Strengths & Shadow Risks -----

    def test_all_strengths_are_lists(self):
        for name, entry in self.data["animus_entries"].items():
            self.assertIsInstance(entry["strengths"], list,
                                 f"'{name}' strengths should be a list")
            self.assertGreater(len(entry["strengths"]), 0,
                               f"'{name}' should have at least one strength")

    def test_all_shadow_risks_are_lists(self):
        for name, entry in self.data["animus_entries"].items():
            self.assertIsInstance(entry["shadow_risk"], list,
                                 f"'{name}' shadow_risk should be a list")
            self.assertGreater(len(entry["shadow_risk"]), 0,
                               f"'{name}' should have at least one shadow risk")

    def test_all_xp_bonus_tasks_are_lists(self):
        for name, entry in self.data["animus_entries"].items():
            self.assertIsInstance(entry["xp_bonus_tasks"], list,
                                 f"'{name}' xp_bonus_tasks should be a list")

    def test_autocognitus_strengths(self):
        entry = get_animus("Autocognitus", self.data)
        self.assertIn("strategy", entry["strengths"])
        self.assertIn("systems thinking", entry["strengths"])

    def test_animora_shadow_risks(self):
        entry = get_animus("Animora", self.data)
        self.assertIn("self doubt", entry["shadow_risk"])
        self.assertIn("emotional overload", entry["shadow_risk"])

    def test_cogniflux_xp_bonus_tasks(self):
        entry = get_animus("Cogniflux", self.data)
        self.assertIn("prototyping", entry["xp_bonus_tasks"])
        self.assertIn("game design", entry["xp_bonus_tasks"])

    # ----- XP Calculation -----

    def test_calculate_xp_multiplier(self):
        result = calculate_xp(10, "Autocognitus", self.data)
        self.assertEqual(result, 11)  # 10 * 1.1

    def test_calculate_xp_flat(self):
        result = calculate_xp(10, "Virtumind", self.data)
        self.assertEqual(result, 15)  # 10 + 5

    def test_calculate_xp_no_bonus(self):
        result = calculate_xp(10, "Takwyn", self.data)
        self.assertEqual(result, 10)  # 0 flat bonus

    def test_calculate_xp_unknown_animus(self):
        result = calculate_xp(10, "NonExistent", self.data)
        self.assertEqual(result, 10)  # returns base unchanged

    # ----- Add / Update / Remove -----

    def test_add_new_animus(self):
        new_entry = {
            "title": "Test Hero",
            "class": "Tester",
            "mentor": "KONG",
            "description": "Test ability",
            "category": "test",
            "pillar_alignment": ["Resilience"],
            "strengths": ["testing", "validation"],
            "xp_bonus": {"type": "flat", "value": 2, "condition": "test"},
            "xp_bonus_tasks": ["unit testing"],
            "shadow_trait_interaction": "default",
            "shadow_risk": ["over-testing"],
            "mentor_note": "Test mentor note.",
        }
        self.data = add_animus("TestAnimus", new_entry, self.data, auto_save=False)
        self.assertIn("TestAnimus", self.data["animus_entries"])

    def test_add_duplicate_raises(self):
        new_entry = {
            "title": "Dup", "class": "Dup", "mentor": "KONG",
            "description": "Dup", "category": "dup",
            "pillar_alignment": [], "strengths": [],
            "xp_bonus": {"type": "flat", "value": 0, "condition": "none"},
            "xp_bonus_tasks": [],
            "shadow_trait_interaction": "default",
            "shadow_risk": [], "mentor_note": "Dup",
        }
        with self.assertRaises(ValueError):
            add_animus("Autocognitus", new_entry, self.data, auto_save=False)

    def test_add_missing_keys_raises(self):
        incomplete = {"title": "Broken"}
        with self.assertRaises(ValueError):
            add_animus("Broken", incomplete, self.data, auto_save=False)

    def test_update_animus(self):
        self.data = update_animus(
            "Autocognitus",
            {"description": "Updated ability text"},
            self.data,
            auto_save=False,
        )
        entry = get_animus("Autocognitus", self.data)
        self.assertEqual(entry["description"], "Updated ability text")

    def test_update_nonexistent_raises(self):
        with self.assertRaises(KeyError):
            update_animus("FakeAnimus", {"title": "X"}, self.data, auto_save=False)

    def test_remove_animus(self):
        self.data = remove_animus("Aetherion", self.data, auto_save=False)
        self.assertNotIn("Aetherion", self.data["animus_entries"])

    def test_remove_nonexistent_raises(self):
        with self.assertRaises(KeyError):
            remove_animus("FakeAnimus", self.data, auto_save=False)

    # ----- Pillar Alignment -----

    def test_all_pillar_alignments_are_lists(self):
        for name, entry in self.data["animus_entries"].items():
            self.assertIsInstance(
                entry["pillar_alignment"], list,
                f"'{name}' pillar_alignment should be a list"
            )

    # ----- Persistence -----

    def test_save_and_reload(self):
        new_entry = {
            "title": "Persist Hero", "class": "Tester", "mentor": "KONG",
            "description": "Persists to disk", "category": "test",
            "pillar_alignment": ["Integrity"], "strengths": ["persistence"],
            "xp_bonus": {"type": "flat", "value": 1, "condition": "none"},
            "xp_bonus_tasks": ["saving"],
            "shadow_trait_interaction": "default",
            "shadow_risk": ["none"], "mentor_note": "Saved!",
        }
        add_animus("PersistTest", new_entry, self.data, auto_save=False)
        save_catalogue(self.data, TEST_CATALOGUE_FILE)

        reloaded = load_catalogue(TEST_CATALOGUE_FILE)
        self.assertIn("PersistTest", reloaded["animus_entries"])


if __name__ == "__main__":
    unittest.main()