# Skill: subagent-driven-development
**Description:** Execute implementation plans by dispatching fresh subagents per task with two-stage review.

## The Process
1. **DISPATCH:** Fresh subagent per atomic task.
2. **IMPLEMENT:** Subagent implements, tests, and commits.
3. **SPEC REVIEW:** Confirm code matches the original specification.
4. **QUALITY REVIEW:** Approve code quality and standards.
5. **ITERATE:** Fix gaps until both reviews are ✅.

## Advantages
- Fresh context per task (no pollution).
- Parallel-safe execution.
- Review loops ensure fixes actually work.
- Prevents over/under-building.
