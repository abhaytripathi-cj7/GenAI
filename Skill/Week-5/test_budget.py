"""Week 5 - Tests for the Token Economics budget planner (guide Section 7).

Verifies the cost calculation and the capacity/budget checks without
calling any LLM API.

Run:  python -m unittest test_budget.py -v   (or: python test_budget.py)
Expected: all 4 tests pass.
"""
import unittest

from budget import FeatureBudget


class TestFeatureBudget(unittest.TestCase):
    def make_budget(self, **overrides):
        values = dict(
            requests_per_day=1000,
            avg_input_tokens=1000,
            avg_output_tokens=500,
            peak_requests_per_minute=10,
            input_price_per_million=1.0,
            output_price_per_million=2.0,
            rpm_limit=100,
            tpm_limit=50000,
            monthly_budget_usd=100,
            daily_budget_usd=5,
            safety_margin_percent=20,
        )
        values.update(overrides)
        return FeatureBudget(**values)

    def test_cost_estimate(self):
        result = self.make_budget().calculate()
        self.assertAlmostEqual(result["daily_cost_usd"], 2.0)
        self.assertAlmostEqual(result["monthly_cost_usd"], 60.0)

    def test_capacity_passes(self):
        result = self.make_budget().calculate()
        self.assertTrue(result["rpm_ok"])
        self.assertTrue(result["tpm_ok"])

    def test_rpm_limit_fails(self):
        result = self.make_budget(rpm_limit=5).calculate()
        self.assertFalse(result["rpm_ok"])

    def test_monthly_budget_fails(self):
        result = self.make_budget(monthly_budget_usd=20).calculate()
        self.assertFalse(result["monthly_budget_ok"])


if __name__ == "__main__":
    unittest.main()
