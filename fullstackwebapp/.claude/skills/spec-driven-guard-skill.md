# Spec-Driven Guard Skill

This skill enforces Spec-Driven Development discipline throughout the development process, ensuring architectural integrity and traceability.

## Core Principles

### No Implementation Without Approved Spec
- No code implementation is allowed without a corresponding approved specification
- All features must originate from a written spec before any planning or implementation begins
- The specification serves as the authorization for any development work
- Implementation without a spec is considered a violation and must be halted

### Clear Traceability
- Maintain clear traceability from specification to plan to tasks
- Each implementation task must be traceable back to a specific requirement in the specification
- Plans must clearly reference the relevant specifications
- All work artifacts must be linked to their originating specifications
- Create audit trails that connect every piece of code to its specification

### No Manual or Ad-Hoc Coding
- Prohibit manual coding that bypasses the spec-driven process
- All code must be generated or written based on approved specifications
- Prevent ad-hoc feature additions without proper specification
- Ensure all development follows the planned tasks derived from specifications
- Block any development activity that doesn't follow the established workflow

### Single Source of Truth
- Specifications remain the single source of truth for all requirements
- All implementation decisions must align with the approved specifications
- Any discrepancies between implementation and specification must be resolved by updating the specification first
- Maintain consistency between what is specified and what is implemented
- Use specifications to resolve disputes about feature requirements

## Enforcement Mechanisms

### Pre-Implementation Checks
- Verify that an approved specification exists for the requested feature
- Ensure the specification is current and has not been superseded
- Confirm that the planned approach aligns with the specification
- Validate that tasks are properly derived from the specification

### During Development
- Monitor for any deviations from the approved specification
- Check that all implemented features trace back to specification items
- Verify that no additional functionality is being added outside the specification
- Ensure that all changes follow the spec -> plan -> task -> implementation flow

### Quality Gates
- Implement checkpoints at each phase to validate compliance
- Block progression to the next phase if spec-driven discipline is not followed
- Require specification updates before implementing changes
- Verify traceability before accepting completed work

## Validation Checklist

Before allowing any development activity, verify:

- [ ] An approved specification exists for the requested work
- [ ] The specification is current and not superseded
- [ ] The planned approach aligns with the specification
- [ ] Tasks are properly derived from the specification
- [ ] Traceability links are established (spec → plan → tasks → implementation)
- [ ] No ad-hoc or manual coding is planned
- [ ] The specification remains the authoritative source

## Violation Handling

When spec-driven discipline is violated:

1. **Immediate Halt**: Stop the non-compliant work immediately
2. **Issue Identification**: Identify the specific violation or deviation
3. **Root Cause Analysis**: Determine why the specification was bypassed
4. **Remediation**: Either create the proper specification or align work to existing specification
5. **Documentation**: Record the violation and corrective actions taken
6. **Process Improvement**: Update processes to prevent similar violations

## Reusability Across Phases

This skill maintains architectural discipline across all development phases:

- **Specification Phase**: Ensures specifications are complete and approvable
- **Planning Phase**: Validates that plans align with specifications
- **Tasking Phase**: Confirms tasks are derived from specifications
- **Implementation Phase**: Verifies implementation follows specifications
- **Testing Phase**: Ensures tests validate against specifications
- **Deployment Phase**: Confirms deployment aligns with specified features

## Integration Points

This skill integrates with:
- Specification tools to validate existence of approved specs
- Planning tools to ensure alignment with specifications
- Task management tools to verify proper derivation from specs
- Implementation tools to enforce adherence to specs
- Quality assurance processes to maintain discipline