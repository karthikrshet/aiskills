---
name: tdd
description: |
  Use this skill to practice test-driven development — writing tests before
  implementation, using tests to drive design, and validating implementation
  against pre-written tests. Activates when implementing new functionality,
  refactoring code, or fixing bugs where regression coverage is needed.
version: "0.1.0"
category: testing
tags: [testing, tdd, test-driven-development, unit-tests, design, quality]
risk: low
status: alpha
related-skills:
  - implementation-planning
  - code-review
  - bug-diagnosis
---

# Test-Driven Development (TDD)

## Purpose

AI-generated code frequently lacks adequate test coverage. Agents write tests as an afterthought, often testing only the happy path of a function they've already written — not the edge cases, failure modes, or contract the code is supposed to satisfy.

Test-driven development inverts this: tests are specifications written first, before implementation. They define *what the code must do*, not *what the code does*. This produces better design (tests reveal interface problems early), higher coverage (edge cases are defined before they're forgotten), and more reliable implementations.

## When to Use

- Implementing new functionality
- Implementing a bug fix (write a failing test that reproduces the bug first)
- Refactoring existing code (ensure tests pass before and after)
- Building an API or service interface
- Any case where the agent would otherwise write tests after implementation

## When Not to Use

- Exploratory code / prototypes where the interface is unknown (explore first, TDD the real implementation)
- One-off scripts with no production use
- Infrastructure configuration (Dockerfile, CI config) — different validation approaches apply

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Requirements / acceptance criteria | ✅ | What the code must do |
| Implementation plan | ✅ | What is being built |
| Existing test suite and test framework | ✅ | Must know how tests are run |

## Preconditions

- [ ] Test framework is identified and working (`pytest`, `jest`, `go test`, etc.)
- [ ] Existing tests pass before starting (run the test suite to verify baseline)
- [ ] Requirements are specific enough to write testable assertions

## Workflow

### Step 1: Verify the Baseline

Before writing any code, run the existing test suite:

```bash
pytest tests/          # Python
npm test               # Node.js
go test ./...          # Go
```

**All tests must pass before starting.** If any fail, stop and report to human.

### Step 2: Write Failing Tests First

For each acceptance criterion, write a test that:
1. Calls the function/method as it should be used (not as it's currently implemented)
2. Asserts the expected output
3. Fails because the implementation doesn't exist yet

**TDD rule:** Never write production code before a failing test exists for it.

**Test structure (Arrange-Act-Assert):**
```python
def test_email_notification_sent_on_report_completion():
    # Arrange
    mock_email_service = MockEmailService()
    report = Report(status="complete", user_email="user@example.com")

    # Act
    notify_report_complete(report, email_service=mock_email_service)

    # Assert
    assert mock_email_service.sent_count == 1
    assert mock_email_service.last_recipient == "user@example.com"
```

### Step 3: Cover These Cases for Every Unit

- **Happy path:** the expected normal case
- **Edge cases:** empty input, zero, null/None, empty string, empty list
- **Boundary cases:** minimum and maximum valid values
- **Error cases:** invalid input, service unavailable, unexpected exceptions
- **Security cases:** if the unit handles user input, include injection-like strings

### Step 4: Write Minimal Implementation to Pass the Test

Write the simplest code that makes the failing test pass.

**TDD discipline:**
- Do not write code that is not needed to pass the current failing test
- Do not optimize prematurely
- Do not add features not required by a test

Run tests after each small change.

### Step 5: Refactor Under Green Tests

Once tests pass:
- Refactor for clarity, performance, and maintainability
- Run tests after every refactor step — they must stay green
- Do not change test assertions during refactoring (that changes what is being tested)

### Step 6: Write Integration Tests

After unit tests pass, write integration tests for the seam between components:

- Does the component work correctly with its real dependencies?
- Does the data flow correctly end-to-end?
- Are side effects (database writes, API calls) correctly triggered?

Use realistic (but not production) test data.

## Decision Points

| Condition | Tier | Action |
|-----------|------|--------|
| Existing test suite is failing before we start | Inform | Report to human; get confirmation to proceed or fix baseline first |
| A requirement cannot be expressed as a test | Consult | "Requirement FR-005 ('should feel responsive') is not testable as written. Can you specify a measurable criterion?" |
| Test requires accessing production data | Approve | Never use production data in tests — ask for a representative test dataset |

## Safety Constraints

- Never modify test assertions to make a test pass — fix the implementation
- Never use real credentials, production databases, or production APIs in tests
- Never skip writing tests for error cases because "they're unlikely"
- Always run the full test suite before declaring a step complete
- Do not mock what you're testing — mock only external dependencies

## Expected Output

- A test file (or additions to existing test files) covering:
  - Happy path
  - Edge cases
  - Error cases
- Implementation code that passes all tests
- Green test suite

## Validation

- [ ] `pytest tests/ -v` (or equivalent) runs with 0 failures
- [ ] New tests existed as failing tests before implementation was written
- [ ] Edge cases are explicitly tested (not just happy path)
- [ ] No tests use real external services or credentials
- [ ] Test names clearly describe what is being tested

## Failure Handling

| Failure | What to do |
|---------|------------|
| Test cannot be written because interface is unclear | Redesign the interface; vague interfaces produce vague tests |
| Test is flaky (sometimes passes, sometimes fails) | Investigate and fix flakiness before proceeding — do not ignore it |
| Test requires mocking something very complex | Possible design smell — consider simplifying the interface under test |
| Coverage drops after change | Investigate which branch is uncovered; add test |

## Examples

### Example 1: TDD for a chunking function in a RAG pipeline

**Requirement:** "The chunking function must split text into chunks of at most 512 tokens, with 50-token overlap."

**Tests written first:**
```python
def test_chunk_splits_long_text():
    text = "word " * 1000  # 1000 words
    chunks = chunk_text(text, max_tokens=512, overlap=50)
    assert all(len(tokenize(c)) <= 512 for c in chunks)

def test_chunk_overlap_is_correct():
    text = "word " * 600
    chunks = chunk_text(text, max_tokens=512, overlap=50)
    # The beginning of chunk 2 should match the end of chunk 1
    assert chunks[1].startswith(chunks[0][-50:].strip())

def test_chunk_empty_text():
    assert chunk_text("", max_tokens=512, overlap=50) == []

def test_chunk_text_shorter_than_max():
    text = "short text"
    chunks = chunk_text(text, max_tokens=512, overlap=50)
    assert len(chunks) == 1
    assert chunks[0] == text
```

Implementation written after these tests exist.

## Related Skills

- `implementation-planning` — defines what to implement; run before this skill
- `code-review` — review implementation quality after tests pass
- `bug-diagnosis` — use when a failing test reveals an existing bug
