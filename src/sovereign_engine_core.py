# -----------------------------
# Eternius — Sovereign Engine Core
# The mathematical heart of the Eternius simulation.
#
# Implements:
#   - SovereignEngine class (Pentad Equations)
#   - Sovereign Unified Equation (SUE)
#   - Biological ROI calculation
# -----------------------------

import json


# -----------------------------
# SovereignEngine
# -----------------------------

class SovereignEngine:
    """
    Mathematical engine for auditing every player decision
    across the 5 Pentad dimensions of the Eternius simulation.

    Parameters:
        node_id: Unique identifier for the player node / simulation session.
    """

    def __init__(self, node_id):
        self.node_id = node_id

    # ── Pentad Equation 1 ────────────────────────────────────────────────────
    def social_impact(self, reach, engagement_index):
        """
        Measure social impact from community reach and engagement depth.

        Parameters:
            reach:            Total number of people influenced.
            engagement_index: Quality of engagement (0.0 – 1.0 scale).

        Returns:
            float: Social impact score.
        """
        return reach * engagement_index

    # ── Pentad Equation 2 ────────────────────────────────────────────────────
    def environmental_impact(self, canopy_sqm, air_quality_delta, flood_risk):
        """
        Measure environmental impact from ecological restoration metrics.

        Parameters:
            canopy_sqm:       Green canopy area in square metres.
            air_quality_delta: Change in air quality (positive = improvement).
            flood_risk:       Flood risk reduction factor (0.0 – 1.0).

        Returns:
            float: Environmental impact score.
        """
        return (canopy_sqm * 0.4) + (air_quality_delta * 0.4) + ((1 - flood_risk) * 0.2 * 100)

    # ── Pentad Equation 3 ────────────────────────────────────────────────────
    def economic_impact(self, local_spend, grant_funding, debt_ratio):
        """
        Measure economic impact weighted against debt burden.

        Parameters:
            local_spend:   Total local economic spend generated.
            grant_funding: Public/grant funding attracted.
            debt_ratio:    Debt-to-asset ratio (0.0 – 1.0; higher = worse).

        Returns:
            float: Economic impact score.
        """
        return (local_spend + grant_funding) * (1 - debt_ratio)

    # ── Pentad Equation 4 ────────────────────────────────────────────────────
    def generational_impact(self, youth_education_hours, legacy_asset_value):
        """
        Measure long-term generational impact through education and legacy assets.

        Parameters:
            youth_education_hours: Total education hours delivered to youth.
            legacy_asset_value:    Monetary value of legacy assets created.

        Returns:
            float: Generational impact score.
        """
        return (youth_education_hours * 0.6) + (legacy_asset_value * 0.4)

    # ── Pentad Equation 5 ────────────────────────────────────────────────────
    def biological_impact(self, health_index, toxicity_ppm):
        """
        Measure biological impact based on community health versus toxin load.

        Parameters:
            health_index:  Composite community health score (0 – 100).
            toxicity_ppm:  Environmental toxicity in parts per million.

        Returns:
            float: Biological impact score.
        """
        return health_index - (toxicity_ppm * 0.1)


# -----------------------------
# Sovereign Unified Equation (SUE)
# -----------------------------

def calculate_sovereign_index(s, e, n, g, b):
    """
    The Sovereign Unified Equation (SUE).

    Aggregates all 5 Pentad dimension scores into a single Sovereign Index.
    Divides by 5 to normalise, then classifies the node status.

    Parameters:
        s: Social impact score.
        e: Environmental impact score.
        n: Economic impact score.   (N for ecoNomic)
        g: Generational impact score.
        b: Biological impact score.

    Returns:
        dict:
            node_id        - placeholder "N/A" (use SovereignEngine for node-bound calls)
            social         - s
            environmental  - e
            economic       - n
            generational   - g
            biological     - b
            total_value    - mean of the 5 scores
            status         - "SOVEREIGN GROWTH" | "ADMINISTRATIVE SLOTH"
    """
    total_value = (s + e + n + g + b) / 5

    status = "SOVEREIGN GROWTH" if total_value > 75 else "ADMINISTRATIVE SLOTH"

    result = {
        "node_id": "N/A",
        "social": s,
        "environmental": e,
        "economic": n,
        "generational": g,
        "biological": b,
        "total_value": round(total_value, 4),
        "status": status,
    }

    return result


# -----------------------------
# Biological ROI
# -----------------------------

def calculate_biological_roi(agency, systemic_stress):
    """
    Biological ROI formula:  B-ROI = Agency - Systemic Stress

    Measures the net personal sovereignty of a player or community node
    after accounting for environmental and systemic pressures.

    Parameters:
        agency:          Degree of autonomous action and decision-making power (0 – 100).
        systemic_stress: Compounded systemic / environmental stress load (0 – 100).

    Returns:
        dict:
            agency          - input value
            systemic_stress - input value
            b_roi           - net biological ROI
            status          - "POSITIVE ROI" | "NEGATIVE ROI"
    """
    b_roi = agency - systemic_stress
    status = "POSITIVE ROI" if b_roi >= 0 else "NEGATIVE ROI"

    return {
        "agency": agency,
        "systemic_stress": systemic_stress,
        "b_roi": round(b_roi, 4),
        "status": status,
    }


# -----------------------------
# Node-bound helpers on SovereignEngine
# -----------------------------

def engine_calculate_sovereign_index(engine, s, e, n, g, b):
    """
    Node-bound wrapper: runs calculate_sovereign_index and stamps the node_id.

    Returns:
        JSON string of the result dict.
    """
    result = calculate_sovereign_index(s, e, n, g, b)
    result["node_id"] = engine.node_id
    return json.dumps(result, indent=2)


# Attach as a method so callers can do: engine.calculate_sovereign_index(...)
SovereignEngine.calculate_sovereign_index = engine_calculate_sovereign_index
SovereignEngine.calculate_biological_roi = staticmethod(calculate_biological_roi)
