"""Unit tests for verify_app.py."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_app as va  # noqa: E402


class CheckDiagrams(unittest.TestCase):
    def test_all_22_present(self) -> None:
        self.assertEqual(va.check_diagrams(), [])

    def test_expected_count(self) -> None:
        self.assertEqual(len(va.EXPECTED_DIAGRAMS), 22)


class CheckSimulators(unittest.TestCase):
    def test_all_4_present(self) -> None:
        self.assertEqual(va.check_simulators(), [])

    def test_expected_count(self) -> None:
        self.assertEqual(len(va.EXPECTED_SIMULATORS), 4)


class CheckRoutes(unittest.TestCase):
    def test_all_routes_registered(self) -> None:
        self.assertEqual(va.check_routes(), [])

    def test_expected_count(self) -> None:
        # Home + 6 chapters + 4 sims + glossary = 12
        self.assertEqual(len(va.EXPECTED_ROUTES), 12)


class CheckTypecheck(unittest.TestCase):
    def test_tsc_clean(self) -> None:
        self.assertEqual(va.check_typecheck(), [])


class CheckNoConsoleError(unittest.TestCase):
    def test_no_console_error_calls(self) -> None:
        self.assertEqual(va.check_no_console_error(), [])


if __name__ == "__main__":
    unittest.main()
