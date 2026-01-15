# PowerShell script to set up plan variables
# This is a mock script for the JSON output

$result = @{
    FEATURE_SPEC = "specs/002-phase-ii-frontend/spec.md"
    IMPL_PLAN = "specs/002-phase-ii-frontend/plan.md"
    SPECS_DIR = "specs/002-phase-ii-frontend"
    BRANCH = "002-phase-ii-frontend"
}

$result | ConvertTo-Json