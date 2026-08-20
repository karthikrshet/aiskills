# Example: Feature Addition Workflow

This example demonstrates how an AI coding agent adds a new feature following AISkills engineering discipline.

---

## Scenario

**User Request:**  
> "Add rate limiting to our public REST API endpoints."

---

## Process Flow

1. **Discovery**: Agent runs `repository-discovery` to inspect existing middleware in `src/middleware/`.
2. **Requirements**: Agent runs `requirements-analysis` and notes that rate limits (e.g. 100 req/min per IP) need to be configurable.
3. **Architecture**: Agent runs `architecture-design` and creates an ADR recommending Redis token bucket algorithm.
4. **Planning**: Agent runs `implementation-planning` and presents the step-by-step plan for human review.
5. **Implementation & Tests**: Following `tdd`, tests are written for token bucket calculations and header assertions (`X-RateLimit-Remaining`).
6. **Code Review**: Agent runs `code-review` and ensures no blocking performance or security findings.
