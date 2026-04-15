import unittest
from shadow_traits import (
    PILLAR_TRAITS,
    get_pillar_traits,
    get_traits_by_alignment,
    get_traits_by_tier,
    get_all_pillar_names,
    count_total_traits,
)

EXPECTED_PILLARS = [
    "Janus", "Jormungandr", "Anubis", "Apep",
    "Raven", "Ravana", "Vali", "Vritra",
    "Iris", "Iblis", "Sigyn", "Set",
    "Horus", "Morrigan",
]

VALID_ALIGNMENTS = ("light", "shadow")
VALID_TIERS = ("core", "developed", "ascended")


class TestShadowTraitsDataStructure(unittest.TestCase):
    """Tests for the PILLAR_TRAITS data structure."""

    def test_has_fourteen_pillars(self):
        self.assertEqual(len(PILLAR_TRAITS), 14)

    def test_all_expected_pillars_present(self):
        names = get_all_pillar_names()
        for pillar in EXPECTED_PILLARS:
            self.assertIn(pillar, names, f"Expected pillar '{pillar}' in trait system")

    def test_all_pillars_have_virtue_and_sin(self):
        for name, entry in PILLAR_TRAITS.items():
            self.assertIn("virtue", entry, f"'{name}' missing 'virtue'")
            self.assertIn("sin", entry, f"'{name}' missing 'sin'")

    def test_all_pillars_have_light_and_shadow(self):
        for name, entry in PILLAR_TRAITS.items():
            self.assertIn("light", entry, f"'{name}' missing 'light' alignment")
            self.assertIn("shadow", entry, f"'{name}' missing 'shadow' alignment")

    def test_all_alignments_have_three_tiers(self):
        for name, entry in PILLAR_TRAITS.items():
            for alignment in VALID_ALIGNMENTS:
                for tier in VALID_TIERS:
                    self.assertIn(tier, entry[alignment],
                                  f"'{name}.{alignment}' missing tier '{tier}'")

    def test_all_tiers_have_three_traits(self):
        for name, entry in PILLAR_TRAITS.items():
            for alignment in VALID_ALIGNMENTS:
                for tier in VALID_TIERS:
                    traits = entry[alignment][tier]
                    self.assertEqual(len(traits), 3,
                                     f"'{name}.{alignment}.{tier}' should have 3 traits, "
                                     f"got {len(traits)}")

    def test_all_traits_have_name_and_description(self):
        for name, entry in PILLAR_TRAITS.items():
            for alignment in VALID_ALIGNMENTS:
                for tier in VALID_TIERS:
                    for trait in entry[alignment][tier]:
                        self.assertIn("name", trait,
                                      f"Trait in '{name}.{alignment}.{tier}' missing 'name'")
                        self.assertIn("description", trait,
                                      f"Trait in '{name}.{alignment}.{tier}' missing 'description'")

    def test_all_trait_names_are_strings(self):
        for name, entry in PILLAR_TRAITS.items():
            for alignment in VALID_ALIGNMENTS:
                for tier in VALID_TIERS:
                    for trait in entry[alignment][tier]:
                        self.assertIsInstance(trait["name"], str)
                        self.assertIsInstance(trait["description"], str)

    def test_total_traits_count(self):
        self.assertEqual(count_total_traits(), 252)  # 14 pillars × 18 traits


class TestKnownPillarTraits(unittest.TestCase):
    """Tests for known pillar content."""

    def test_janus_virtue_and_sin(self):
        entry = PILLAR_TRAITS["Janus"]
        self.assertEqual(entry["virtue"], "Wisdom")
        self.assertEqual(entry["sin"], "Deception")

    def test_janus_light_core_trait_names(self):
        traits = PILLAR_TRAITS["Janus"]["light"]["core"]
        names = [t["name"] for t in traits]
        self.assertIn("decisiveness", names)
        self.assertIn("honesty", names)
        self.assertIn("true_guidance", names)

    def test_janus_shadow_core_trait_names(self):
        traits = PILLAR_TRAITS["Janus"]["shadow"]["core"]
        names = [t["name"] for t in traits]
        self.assertIn("indecision", names)
        self.assertIn("deception", names)

    def test_janus_ascended_shadow_traits(self):
        traits = PILLAR_TRAITS["Janus"]["shadow"]["ascended"]
        names = [t["name"] for t in traits]
        self.assertIn("fate_corruption", names)

    def test_horus_virtue_and_sin(self):
        entry = PILLAR_TRAITS["Horus"]
        self.assertEqual(entry["virtue"], "Vision")
        self.assertEqual(entry["sin"], "Ego")

    def test_horus_light_core_traits(self):
        traits = PILLAR_TRAITS["Horus"]["light"]["core"]
        names = [t["name"] for t in traits]
        self.assertIn("clarity_of_sight", names)
        self.assertIn("purposeful_vision", names)
        self.assertIn("sky_awareness", names)

    def test_horus_shadow_ascended_traits(self):
        traits = PILLAR_TRAITS["Horus"]["shadow"]["ascended"]
        names = [t["name"] for t in traits]
        self.assertIn("ego_eclipse", names)
        self.assertIn("tyrant_vision", names)
        self.assertIn("horus_corrupted", names)

    def test_morrigan_virtue_and_sin(self):
        entry = PILLAR_TRAITS["Morrigan"]
        self.assertEqual(entry["virtue"], "Fate")
        self.assertEqual(entry["sin"], "Despair")

    def test_morrigan_light_core_traits(self):
        traits = PILLAR_TRAITS["Morrigan"]["light"]["core"]
        names = [t["name"] for t in traits]
        self.assertIn("fate_acceptance", names)
        self.assertIn("prophetic_sight", names)
        self.assertIn("death_unafraid", names)

    def test_morrigan_shadow_ascended_traits(self):
        traits = PILLAR_TRAITS["Morrigan"]["shadow"]["ascended"]
        names = [t["name"] for t in traits]
        self.assertIn("despair_sovereign", names)
        self.assertIn("morrigan_unchained", names)
        self.assertIn("fate_destroyer", names)

    def test_set_virtue_and_sin(self):
        entry = PILLAR_TRAITS["Set"]
        self.assertEqual(entry["virtue"], "Survival")
        self.assertEqual(entry["sin"], "Betrayal")


class TestShadowTraitsHelperFunctions(unittest.TestCase):
    """Tests for shadow_traits helper functions."""

    def test_get_pillar_traits_valid(self):
        result = get_pillar_traits("Janus")
        self.assertIsNotNone(result)
        self.assertIn("light", result)
        self.assertIn("shadow", result)

    def test_get_pillar_traits_unknown(self):
        result = get_pillar_traits("FakePillar")
        self.assertIsNone(result)

    def test_get_pillar_traits_does_not_expose_virtue_sin(self):
        result = get_pillar_traits("Janus")
        self.assertNotIn("virtue", result)
        self.assertNotIn("sin", result)

    def test_get_traits_by_alignment_light(self):
        result = get_traits_by_alignment("Vali", "light")
        self.assertIsNotNone(result)
        for tier in VALID_TIERS:
            self.assertIn(tier, result)

    def test_get_traits_by_alignment_shadow(self):
        result = get_traits_by_alignment("Vali", "shadow")
        self.assertIsNotNone(result)

    def test_get_traits_by_alignment_invalid_pillar(self):
        result = get_traits_by_alignment("FakePillar", "light")
        self.assertIsNone(result)

    def test_get_traits_by_alignment_invalid_alignment(self):
        result = get_traits_by_alignment("Janus", "neutral")
        self.assertIsNone(result)

    def test_get_traits_by_tier_valid(self):
        result = get_traits_by_tier("Iris", "light", "core")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

    def test_get_traits_by_tier_all_combinations(self):
        for alignment in VALID_ALIGNMENTS:
            for tier in VALID_TIERS:
                result = get_traits_by_tier("Anubis", alignment, tier)
                self.assertIsNotNone(result,
                                     f"get_traits_by_tier('Anubis', '{alignment}', '{tier}') returned None")
                self.assertEqual(len(result), 3)

    def test_get_traits_by_tier_invalid_pillar(self):
        result = get_traits_by_tier("FakePillar", "light", "core")
        self.assertIsNone(result)

    def test_get_traits_by_tier_invalid_alignment(self):
        result = get_traits_by_tier("Janus", "neutral", "core")
        self.assertIsNone(result)

    def test_get_traits_by_tier_invalid_tier(self):
        result = get_traits_by_tier("Janus", "light", "legendary")
        self.assertIsNone(result)

    def test_get_all_pillar_names_count(self):
        names = get_all_pillar_names()
        self.assertEqual(len(names), 14)

    def test_count_total_traits(self):
        self.assertEqual(count_total_traits(), 252)

    def test_each_pillar_has_eighteen_traits(self):
        for pillar_name in get_all_pillar_names():
            entry = PILLAR_TRAITS[pillar_name]
            count = sum(
                len(entry[alignment][tier])
                for alignment in VALID_ALIGNMENTS
                for tier in VALID_TIERS
            )
            self.assertEqual(count, 18,
                             f"'{pillar_name}' should have 18 traits, got {count}")


if __name__ == "__main__":
    unittest.main()
