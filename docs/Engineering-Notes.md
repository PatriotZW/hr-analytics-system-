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