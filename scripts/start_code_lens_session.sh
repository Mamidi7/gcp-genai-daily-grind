#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATE_VALUE="${1:-$(date +%F)}"
SESSIONS_DIR="$ROOT_DIR/docs/code_lens_sessions"
OUT_FILE="$SESSIONS_DIR/session_${DATE_VALUE}.md"

mkdir -p "$SESSIONS_DIR"

if [[ -f "$OUT_FILE" ]]; then
  echo "Session already exists: $OUT_FILE"
  exit 0
fi

cat > "$OUT_FILE" <<EOF
# CODE-LENS Session - ${DATE_VALUE}

## Goal (1 line)

## ASCII Flow
\`\`\`text
Input -> Validate -> Core Logic -> External Call/DB -> Output
            |              |
         fail fast     timeout/retry/error map
\`\`\`

## CodeCard
### Purpose

### Inputs
- 

### Outputs
- 

### Core Flow
1. 
2. 
3. 

### Blocking/Slow Points
- 

### Design Choices
- Choice:
- Why:
- Alternative:

## BugCard
### Symptom

### Root Cause

### Fix

### Prevention

### Impact

## InterviewPack
### 30-second

### 90-second STAR
- Situation:
- Task:
- Action:
- Result:

### 3-minute deep dive
1.
2.
3.

## QuestionBank (5)
1. Q: 
   A:
2. Q: 
   A:
3. Q: 
   A:
4. Q: 
   A:
5. Q: 
   A:

## Tiny Exercise

## Check Question

EOF

echo "Created: $OUT_FILE"
echo "Next: open it and fill today's code piece."
