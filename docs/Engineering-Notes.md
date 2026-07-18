# Engineering Notes

This document captures engineering lessons learned while
developing the HR Analytics System.

Unlike ADRs, these notes record implementation lessons,
refactoring decisions, debugging experiences and programming
techniques that improved the quality of the codebase.

The purpose is to build an engineering handbook alongside
the software itself.

## 001 — Design Before Coding

Lesson

Draw the algorithm before writing code.

Instead of thinking:

"How do I write the loop?"

Think:

"What sequence of decisions should the program make?"

Result

The implementation becomes much simpler and bugs are easier
to identify.


## 002 — Validate Before Modifying State

Lesson

Completely validate an operation before changing any object.

Examples

Employee creation

Validate
↓

Generate ID

↓

Store object

Company

Validate relationships

↓

Append employee

Benefit

Prevents partially completed operations.

## 003 — Queries Return Information

Query methods should answer questions.

Examples

find_employee_by_id()

find_department_by_id()

Return

Employee object

or

None

They should not decide whether the result is acceptable.

Business methods decide that.

## 004 — Refactor Only After Duplication Appears

Original implementation

add_employee()

contained duplicate search loops.

                                    department_exists = False

                                    for department in self._departments:
                                        if department.department_id == employee.department_id:
                                            department_exists = True
                                            break

                                    if not department_exists:
                                        raise ValueError(...)
*****************************************************************************************************
                                    manager_exists = False

                                    for existing_employee in self._employees:
                                        ...

After implementing

find_department_by_id()

                                    department = self.find_department_by_id(employee.department_id)

                                    if department is None:
                                        raise ValueError(
                                            f"Department ID {employee.department_id} does not exist."
                                        )
and

find_employee_by_id()

                                       manager = self.find_employee_by_id(employee.manager_id)

                                       if manager is None:
                                            raise ValueError(
                                                f"Manager ID {employee.manager_id} does not exist."
                                            )
the duplicated logic was replaced.

Lesson

Do not invent abstractions.

Allow duplication to reveal where an abstraction belongs.

## 005 — Git Remembers History

Avoid leaving old implementations as comments.

Use Git history to remember previous versions.

Keep the source code focused on the current implementation.

## Debugging Diary

### Save Your Files

Problem

Tests reported:

AttributeError:
Company has no attribute add_department()

Cause

company.py had not been saved.

Lesson

Always save files before running tests.

Do not assume the algorithm is wrong before checking the
development environment.

## Code Review Lessons

### return None belongs after the loop

Initial implementation

Returned None inside the loop.

Problem

The search stopped after checking only the first item.

Improved implementation

Return None only after the entire collection has been searched.

Lesson

Finish inspecting all candidates before concluding that
nothing was found.


And write down the lessons we've identified so far, especially:

- Design before coding.
- Validate before modifying state.
- Queries return information; behaviour methods enforce rules.
- Refactor after duplication appears.
- Git stores history; don't keep commented-out code.
- Draw the algorithm before implementing it.


## Self Review Before Code Review

Lesson

Before asking for a review, mentally execute the algorithm.

Walk through the code line by line using realistic examples.

Many bugs become obvious before the code is ever reviewed.

Benefit

Improves code quality and reduces review feedback.

## Business Rules Belong at the Correct Level

Lesson

Objects protect their own internal validity.

Coordinator classes enforce rules between objects.

Example

Department

- Validates its own name.
- Changes its own status.

Company

- Prevents deactivating a department while active employees
  are assigned to it.

Reason

A Department cannot know which employees belong to it.
Only the Company has that information.

## Aggregate Root

Lesson

One object should coordinate relationships between
multiple domain objects.

Reason

It centralizes business rules and prevents objects
from entering inconsistent states.

Example

Company

coordinates Employees and Departments.

Employee

protects its own state.

Department

protects its own state.

## Git Commits Tell the Story

Lesson

A professional commit should describe the business capability
or architectural milestone that was completed.

Avoid

- Updated files
- Fixed bugs
- Changes

Prefer

- Complete Company aggregate root implementation
- Add employee serialization
- Introduce reporting service

Reason

Months later, Git history becomes the project's timeline.

## Prefer Higher-Level Abstractions

Lesson

Prefer higher-level objects provided by the standard library
instead of manipulating primitive values directly.

Example

Use pathlib.Path

instead of

os.path + string concatenation.

Reason

Higher-level abstractions are easier to read,
harder to misuse,
and usually more portable.

## Each Layer Speaks Its Own Language

Lesson

Each layer should operate on the data appropriate to its responsibility.

Example

Domain Layer
- Employee
- Department
- Company

Persistence Layer
- dict
- list
- JSON

Reason

Keeping layers independent makes the system easier to
maintain, test and extend.

## Copy with Understanding

Lesson

Reusing existing code is good engineering.

However, copied code must be reviewed as if it were
newly written.

Common things to check

- Method signature
- Docstrings
- Type hints
- Variable names
- Error messages
- Return type
- Responsibilities

Reason

Most copy-and-paste bugs occur because one of these
elements was not updated.

## Normalize at the Boundary

Accept multiple valid input types when it improves the API.

Immediately normalize them into one internal representation.

Example

Accept:
- str
- pathlib.Path

Store:
- pathlib.Path

Benefits
- Simpler implementation
- Consistent internal state
- Fewer type checks

## Command–Query Separation (CQS)

Commands

Perform work and usually return None.

Examples
- save()
- add_employee()
- deactivate()

Queries

Return information without modifying state.

Examples
- load()
- find_employee_by_id()

Reason

Separating commands from queries produces
clearer APIs and easier testing.

## Test One Behaviour Per Test

Each test should verify one observable behaviour.

Benefits

- Easier debugging
- Clearer failures
- Better test names

## Use Private State Internally

Lesson

Methods inside a class should generally work directly
with the class's private attributes.

Public properties exist for other objects.

Reason

The class already owns its internal state and does not
need to access it through its own public interface.

Benefits

- Simpler implementation
- Avoids unnecessary indirection
- Keeps public APIs for external callers


## Coordinate Rather Than Duplicate

Lesson

Aggregate roots should coordinate work performed by
their child objects rather than reimplementing it.

Example

Company.to_dict()

↓

Department.to_dict()

Employee.to_dict()

Reason

Each object remains responsible for describing
its own state.

## Good Architecture Makes Code Smaller

Lesson

When each class has a single, well-defined responsibility,
higher-level components often become surprisingly small.

Example

CompanyRepository.save()

Validate Company

↓

Company.to_dict()

↓

JsonStorage.save()

Reason

Well-designed objects delegate work to the components
that already own that responsibility.

## Design Until the Implementation Becomes Obvious

Lesson

Before implementing a feature, continue refining the design
until the code becomes straightforward.

Indicators

- Few conditional statements.
- Small methods.
- Clear responsibilities.
- Minimal duplication.

Reason

Good design reduces implementation complexity rather than
relying on clever code.

# Engineering Philosophy

The design becomes the focus.

Well-designed software produces simple implementations.

Spend more time deciding where code belongs than writing it.

## Model the Business Before the Algorithm

Lesson

When solving a programming problem,
first describe how a real person would solve it.

Example

Receptionist

↓

Waiting Area

↓

Managers arrive

↓

Recheck waiting employees

↓

If nobody can move,
the paperwork is invalid.

Reason

Business processes often reveal the algorithm naturally.

## Test Behaviour, Not Implementation

Lesson

A unit test should verify what the software is expected
to do rather than how it achieves it.

Example

Instead of testing the waiting-room algorithm directly,
test that employees are restored correctly regardless
of their order in storage.

Reason

Implementation may change.

Correct behaviour must not.

Lesson

When a lower-level component has comprehensive tests,
higher-level tests should rely on its public behaviour
rather than duplicate its verification.

Example

CompanyRepository.save()

expected = company.to_dict()

assert json_file == expected

Reason

Avoids duplicated assertions and keeps tests focused
on each layer's responsibility.
