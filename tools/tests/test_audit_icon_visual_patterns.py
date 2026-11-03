import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_icon_visual_patterns import repeated_groups


class RepeatedGroupsTests(unittest.TestCase):
    def test_ignores_geometry_used_by_only_one_icon(self):
        self.assertEqual(repeated_groups({"a": ["ruby_one"], "b": ["ruby_two"]}), [])

    def test_groups_shared_geometry_by_distinct_icons(self):
        self.assertEqual(
            repeated_groups({"shared": ["ruby_b", "ruby_a"], "unique": ["ruby_c"]}),
            [["ruby_a", "ruby_b"]],
        )

    def test_deduplicates_multiple_paths_from_same_icon(self):
        self.assertEqual(repeated_groups({"shared": ["ruby_a", "ruby_a", "ruby_b"]}), [["ruby_a", "ruby_b"]])

    def test_orders_largest_groups_first(self):
        self.assertEqual(
            repeated_groups({"small": ["a", "b"], "large": ["a", "b", "c"]}),
            [["a", "b", "c"], ["a", "b"]],
        )


if __name__ == "__main__":
    unittest.main()
