#!/usr/bin/env bash
# RBI Grade B Fact Verification Script
# Usage: ./scripts/rbi-fact-verify.sh <path-to-html-or-md>
# Exit 0 = all clean, Exit 1 = stale or missing data found

set -euo pipefail

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
    echo "Usage: $0 <path-to-html-or-md>"
    exit 1
fi

ERRORS=0
WARNINGS=0

fail() {
    echo "  FAIL: $1"
    ERRORS=$((ERRORS + 1))
}

warn() {
    echo "  WARN: $1"
    WARNINGS=$((WARNINGS + 1))
}

pass() {
    echo "  PASS: $1"
}

echo "=== RBI Fact-Check: $FILE ==="
echo ""

# --- 1. STALE RATE CHECKS ---
echo "[1] Checking for stale policy rates..."

if grep -iE 'repo rate.*6\.00|repo.*6\s*%|repo rate.*6\.50' "$FILE" >/dev/null; then
    fail "Stale Repo Rate found (6.00% or 6.50%). Current: 5.25%"
else
    pass "No stale Repo Rate found"
fi

if grep -iE 'MSF.*6\.25|bank rate.*6\.25' "$FILE" >/dev/null; then
    fail "Stale MSF/Bank Rate found (6.25%). Current: 5.50%"
else
    pass "No stale MSF/Bank Rate found"
fi

if grep -iE 'CRR.*4\.00|cash reserve.*4\.00' "$FILE" >/dev/null; then
    fail "Stale CRR found (4.00%). Current: 4.50%"
else
    pass "No stale CRR found"
fi

if grep -iE 'SLR.*18\.50|statutory liquidity.*18\.50' "$FILE" >/dev/null; then
    fail "Stale SLR found (18.50%). Current: 18.00%"
else
    pass "No stale SLR found"
fi

# --- 2. OFFICIALS CHECKS ---
echo ""
echo "[2] Checking RBI officials..."

if grep -i 'Shaktikanta Das' "$FILE" >/dev/null; then
    fail "Old Governor name found (Shaktikanta Das). Current: Sanjay Malhotra"
else
    pass "No old Governor name found"
fi

for OLD_DG in "M. Patra" "Rajeshwar Rao" "Rabi Sankar" "T. Rabi Sankar"; do
    if grep -i "$OLD_DG" "$FILE" >/dev/null; then
        fail "Old Deputy Governor found ($OLD_DG). Verify against current list."
    fi
done
if [ "$ERRORS" -eq 0 ] || ! grep -iE 'M\. Patra|Rajeshwar Rao|Rabi Sankar' "$FILE" >/dev/null; then
    pass "No old Deputy Governor names found"
fi

if grep -i 'Sanjay Malhotra' "$FILE" >/dev/null; then
    pass "Current Governor name present"
else
    warn "Current Governor name (Sanjay Malhotra) not found — verify if section is present"
fi

# --- 3. BUDGET YEAR CHECKS ---
echo ""
echo "[3] Checking budget year references..."

if grep -iE 'budget 2025|fy25.*current|fy26.*current.*budget' "$FILE" >/dev/null; then
    fail "Stale budget year reference found. Current: FY27 (Budget 2026-27)"
else
    pass "No stale budget year references found"
fi

if grep -iE 'fiscal deficit.*4\.4.*%|capex.*11\.11|expenditure.*51\.61' "$FILE" >/dev/null; then
    fail "Old FY26 RE numbers found where FY27 BE expected"
else
    pass "No old FY26 RE numbers found"
fi

# --- 4. FORMULA TRAPS ---
echo ""
echo "[4] Checking formula traps..."

if grep -iE 'money multiplier.*1/CRR|money multiplier.*1\s*/\s*CRR' "$FILE" >/dev/null; then
    fail "Wrong money multiplier formula (1/CRR). RBI exam: M3/M0"
else
    pass "No incorrect money multiplier formula found"
fi

# --- 5. INSTITUTIONAL CHECKS ---
echo ""
echo "[5] Checking institutional facts..."

if grep -iE 'NEFT.*NPCI|NEFT operator.*NPCI' "$FILE" >/dev/null; then
    fail "Wrong NEFT operator (NPCI). NEFT is operated by RBI."
else
    pass "No wrong NEFT operator found"
fi

# --- 6. REQUIRED CURRENT DATA ---
echo ""
echo "[6] Checking required current data is present..."

if grep -iE '5\.25.*%|5\.25%' "$FILE" >/dev/null; then
    pass "Current Repo Rate (5.25%) appears in document"
else
    warn "Current Repo Rate (5.25%) NOT found — verify if rates section exists"
fi

if grep -iE '4\.50.*%|4\.50%' "$FILE" >/dev/null; then
    pass "Current CRR (4.50%) appears in document"
else
    warn "Current CRR (4.50%) NOT found — verify if rates section exists"
fi

if grep -i 'Sanjay Malhotra' "$FILE" >/dev/null; then
    pass "Current Governor mentioned"
else
    warn "Current Governor (Sanjay Malhotra) NOT found"
fi

# --- SUMMARY ---
echo ""
echo "=== SUMMARY ==="
if [ "$ERRORS" -eq 0 ]; then
    echo "ERRORS: 0"
    echo "WARNINGS: $WARNINGS"
    echo "RESULT: PASS — safe to commit."
    exit 0
else
    echo "ERRORS: $ERRORS"
    echo "WARNINGS: $WARNINGS"
    echo "RESULT: FAIL — fix errors before committing."
    exit 1
fi
