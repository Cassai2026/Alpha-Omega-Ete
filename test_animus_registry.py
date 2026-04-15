import unittest
from animus_registry import (
    ANIMUS_REGISTRY,
    get_pillar_registry,
    get_form,
    get_abilities,
    get_mentor,
    get_all_registry_names,
    get_pillars_by_mentor,
    get_animus_forms,
)

EXPECTED_PILLARS = [
    "Janus", "Jormungandr", "Anubis", "Apep",
    "Raven", "Ravana", "Vali", "Vritra",
    "Iris", "Iblis", "Sigyn", "Set",
    "Horus", "Morrigan",
]

VALID_MENTORS = {"KONG", "ODIN", "Hekete"}
VALID_FORMS = {"omega", "ultima", "eternium"}


class TestAnimusRegistryStructure(unittest.TestCase):
    """Tests for the ANIMUS_REGISTRY data structure."""

    def test_registry_has_fourteen_pillars(self):
        self.assertEqual(len(ANIMUS_REGISTRY), 14)

    def test_all_expected_pillars_present(self):
        names = get_all_registry_names()
        for pillar in EXPECTED_PILLARS:
            self.assertIn(pillar, names, f"Expected pillar '{pillar}' in registry")

    def test_all_pillars_have_required_keys(self):
        for name, entry in ANIMUS_REGISTRY.items():
            for key in ("virtue", "sin", "mentor", "forms"):
                self.assertIn(key, entry, f"'{name}' missing key '{key}'")

    def test_all_pillars_have_valid_mentor(self):
        for name, entry in ANIMUS_REGISTRY.items():
            mentor = entry.get("mentor")
            if mentor != "TBD":
                self.assertIn(mentor, VALID_MENTORS,
                              f"'{name}' has invalid mentor '{mentor}'")

    def test_all_pillars_have_three_forms(self):
        for name, entry in ANIMUS_REGISTRY.items():
            forms = entry.get("forms", {})
            for form_name in VALID_FORMS:
                self.assertIn(form_name, forms,
                              f"'{name}' missing form '{form_name}'")

    def test_all_forms_have_required_keys(self):
        for pillar_name, entry in ANIMUS_REGISTRY.items():
            for form_name, form in entry["forms"].items():
                self.assertIn("name", form,
                              f"'{pillar_name}.{form_name}' missing 'name'")
                self.assertIn("description", form,
                              f"'{pillar_name}.{form_name}' missing 'description'")
                self.assertIn("abilities", form,
                              f"'{pillar_name}.{form_name}' missing 'abilities'")

    def test_all_forms_have_three_abilities(self):
        for pillar_name, entry in ANIMUS_REGISTRY.items():
            for form_name, form in entry["forms"].items():
                abilities = form.get("abilities", [])
                self.assertEqual(len(abilities), 3,
                                 f"'{pillar_name}.{form_name}' should have 3 abilities, "
                                 f"got {len(abilities)}")

    def test_all_ability_names_are_strings(self):
        for pillar_name, entry in ANIMUS_REGISTRY.items():
            for form_name, form in entry["forms"].items():
                for ability in form.get("abilities", []):
                    self.assertIsInstance(ability, str,
                                         f"Ability in '{pillar_name}.{form_name}' is not a string")

    def test_total_abilities(self):
        total = sum(
            len(form["abilities"])
            for entry in ANIMUS_REGISTRY.values()
            for form in entry["forms"].values()
        )
        self.assertEqual(total, 126)  # 14 pillars × 3 forms × 3 abilities


class TestKnownPillarData(unittest.TestCase):
    """Tests for specific pillar content."""

    def test_janus_virtue_and_sin(self):
        entry = ANIMUS_REGISTRY["Janus"]
        self.assertEqual(entry["virtue"], "Wisdom")
        self.assertEqual(entry["sin"], "Deception")

    def test_janus_mentor(self):
        self.assertEqual(ANIMUS_REGISTRY["Janus"]["mentor"], "ODIN")

    def test_anubis_virtue_and_sin(self):
        entry = ANIMUS_REGISTRY["Anubis"]
        self.assertEqual(entry["virtue"], "Justice")
        self.assertEqual(entry["sin"], "Judgment")

    def test_kong_pillars(self):
        kong_pillars = {"Apep", "Ravana", "Vali", "Vritra", "Set"}
        actual = set(get_pillars_by_mentor("KONG"))
        for p in kong_pillars:
            self.assertIn(p, actual, f"Expected '{p}' under KONG")

    def test_odin_pillars_include_horus(self):
        odin_pillars = get_pillars_by_mentor("ODIN")
        self.assertIn("Horus", odin_pillars)

    def test_hekete_pillars_include_morrigan(self):
        hekete_pillars = get_pillars_by_mentor("Hekete")
        self.assertIn("Morrigan", hekete_pillars)

    def test_horus_virtue_and_sin(self):
        entry = ANIMUS_REGISTRY["Horus"]
        self.assertEqual(entry["virtue"], "Vision")
        self.assertEqual(entry["sin"], "Ego")

    def test_morrigan_virtue_and_sin(self):
        entry = ANIMUS_REGISTRY["Morrigan"]
        self.assertEqual(entry["virtue"], "Fate")
        self.assertEqual(entry["sin"], "Despair")

    def test_janus_omega_form_name(self):
        form = get_form("Janus", "omega")
        self.assertEqual(form["name"], "Gatekeeper Omega")

    def test_janus_eternium_abilities(self):
        abilities = get_abilities("Janus", "eternium")
        self.assertIn("destiny_rewrite", abilities)
        self.assertIn("omniscient_gate", abilities)
        self.assertIn("eternal_crossroads", abilities)

    def test_horus_omega_form_name(self):
        form = get_form("Horus", "omega")
        self.assertEqual(form["name"], "Eye of Horus Omega")

    def test_morrigan_ultima_abilities(self):
        abilities = get_abilities("Morrigan", "ultima")
        self.assertIn("prophecy_weave", abilities)

    def test_set_mentor_is_kong(self):
        self.assertEqual(get_mentor("Set"), "KONG")


class TestRegistryHelperFunctions(unittest.TestCase):
    """Tests for the registry helper functions."""

    def test_get_pillar_registry_known(self):
        result = get_pillar_registry("Vali")
        self.assertIsNotNone(result)
        self.assertEqual(result["virtue"], "Strength")

    def test_get_pillar_registry_unknown(self):
        result = get_pillar_registry("FakePillar")
        self.assertIsNone(result)

    def test_get_form_valid(self):
        form = get_form("Iris", "omega")
        self.assertIsNotNone(form)
        self.assertIn("abilities", form)

    def test_get_form_invalid_pillar(self):
        result = get_form("FakePillar", "omega")
        self.assertIsNone(result)

    def test_get_form_invalid_form_name(self):
        result = get_form("Janus", "prime")
        self.assertIsNone(result)

    def test_get_abilities_valid(self):
        abilities = get_abilities("Vritra", "ultima")
        self.assertIsInstance(abilities, list)
        self.assertEqual(len(abilities), 3)

    def test_get_abilities_invalid_pillar(self):
        result = get_abilities("FakePillar", "omega")
        self.assertIsNone(result)

    def test_get_abilities_invalid_form(self):
        result = get_abilities("Janus", "nonexistent")
        self.assertIsNone(result)

    def test_get_mentor_valid(self):
        self.assertEqual(get_mentor("Iris"), "Hekete")
        self.assertEqual(get_mentor("Raven"), "ODIN")

    def test_get_mentor_invalid(self):
        result = get_mentor("FakePillar")
        self.assertIsNone(result)

    def test_get_all_registry_names_count(self):
        names = get_all_registry_names()
        self.assertEqual(len(names), 14)

    def test_get_pillars_by_mentor_odin(self):
        pillars = get_pillars_by_mentor("ODIN")
        self.assertIsInstance(pillars, list)
        self.assertGreater(len(pillars), 0)
        for p in pillars:
            self.assertEqual(ANIMUS_REGISTRY[p]["mentor"], "ODIN")

    def test_get_pillars_by_mentor_unknown(self):
        result = get_pillars_by_mentor("FakeMentor")
        self.assertEqual(result, [])

    def test_get_animus_forms_valid(self):
        forms = get_animus_forms("Sigyn")
        self.assertIsNotNone(forms)
        self.assertIn("omega", forms)
        self.assertIn("ultima", forms)
        self.assertIn("eternium", forms)

    def test_get_animus_forms_invalid(self):
        result = get_animus_forms("FakePillar")
        self.assertIsNone(result)

    def test_mentor_coverage(self):
        odin = set(get_pillars_by_mentor("ODIN"))
        kong = set(get_pillars_by_mentor("KONG"))
        hekete = set(get_pillars_by_mentor("Hekete"))
        all_assigned = odin | kong | hekete
        self.assertEqual(len(all_assigned), 14,
                         "All 14 pillars should be assigned to a mentor")


if __name__ == "__main__":
    unittest.main()
