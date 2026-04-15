/* =====================================================================
   CASS-AI SOVEREIGN NGO: GLOBAL CONSTITUTION API
   FILE: sovereign_ngo.h
   AUTHOR: The Architect (Stretford)
   LEGAL OVERSIGHT: The Sovereign Ethics Board (Counsel)
   LICENSE: AGPLv3 + Sovereign Ethical Mandate
===================================================================== */

#ifndef SOVEREIGN_NGO_H
#define SOVEREIGN_NGO_H

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

// --- CORE GLOBAL DEFINITIONS ---
#define JURISDICTION "Worldwide NGO"
#define CORE_LICENSE "GNU AGPLv3"
#define TOTAL_SDGS 17
#define MIN_HUMAN_RIGHTS_INDEX 1.0

// --- ENUMERATIONS (The Legal States) ---
typedef enum {
    LICENSE_ACTIVE,
    LICENSE_UNDER_AUDIT,
    LICENSE_REVOKED_BY_BOARD
} LicenseStatus;

typedef enum {
    TIER_1_COMMUNITY,   // Free, Open, High B_ROI
    TIER_2_INSTITUTION  // Gated, Audited, Subject to Systemic Tax
} DeploymentTier;

// --- STRUCTURES (The Entities) ---

// Struct defining the entity trying to use your code (e.g., Council, Developer)
typedef struct {
    char entity_name[100];
    DeploymentTier tier;
    bool is_cloud_backend;       // Triggers the AGPLv3 Server Loophole check
    double proposed_extraction;  // Must be offset by Systemic Tax
} Licensee;

// Struct defining the Legal Enforcers
typedef struct {
    char lead_counsel_name[100];
    bool has_veto_power;
} EthicsBoard;

// --- FUNCTION PROTOTYPES (The Legal Mechanisms) ---

/**
 * ARTICLE I & V: The Open-Source Safeguard
 * Checks if a Tier 2 Institution is hiding the code on a backend server.
 * If true, legally compels them to open-source the modifications under AGPLv3.
 */
bool enforce_agplv3_server_loophole(Licensee *target_entity, EthicsBoard *board);

/**
 * ARTICLE IV: The 17 SDG Mandate
 * Audits the target entity's project against the 17 UN Goals.
 * Returns true only if all goals are respected and Human Rights Index >= 1.0.
 */
bool audit_global_sdg_compliance(double project_sdg_impact[TOTAL_SDGS], double human_rights_index);

/**
 * ARTICLE II: The Biological Defense
 * Evaluates the Biological ROI (B_ROI). If Stress Extraction > Health + Agency,
 * the Board triggers an immediate injunction.
 */
bool audit_biological_safety(double delta_health, double delta_agency, double stress_extraction);

/**
 * ARTICLE III: The Revocation Hammer
 * The master function executed by your Barrister. 
 * If any audit fails, this function changes LicenseStatus to LICENSE_REVOKED_BY_BOARD.
 */
LicenseStatus execute_board_injunction(Licensee *target_entity, char *reason_for_revocation);

#endif // SOVEREIGN_NGO_H
