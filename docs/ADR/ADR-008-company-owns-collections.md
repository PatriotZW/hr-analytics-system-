ADR-008 — Company Owns Collections

Context

The Company class coordinates Employees and Departments.

A decision is required on whether collections should be publicly accessible.

Decision

The Company class shall maintain private collections of employees and departments.

Objects may only be added, removed or searched through Company methods.

Consequences

Advantages
Preserves Company invariants.
Prevents bypassing business rules.
Centralizes coordination logic.
Supports future validation without changing callers.
Trade-offs
Slightly more code than exposing lists directly.
All modifications must go through Company methods.

Rationale

The Company is the aggregate root for Employees and Departments.

It is responsible for maintaining a consistent organisational state.

I actually like this ADR because it introduces a new concept we haven't formally discussed before:

Aggregate Root.

We don't need to study Domain-Driven Design yet, but you've naturally arrived at one of its core ideas.

Sprint 4 – PR-001

Now we can freeze the module skeleton.

I propose:

"""
Company Module

Purpose
-------
Represents the organisation within the HR Analytics System.

Responsibilities
----------------
- Coordinate employees and departments.
- Maintain organisational state.
- Enforce company-level business rules.

Does Not
--------
- Validate employee details.
- Validate department details.
- Persist data.
- Generate reports.
- Perform analytics.
"""

Imports:

from models.employee import Employee
from models.department import Department

Constructor:

def __init__(self, name: str):
    """
    Creates a new Company object.
    """

    self.name = self._validate_name(name)

    self._employees = []
    self._departments = []

Notice something interesting.

This is the first class where validation is minimal.

We're not validating employees.

We're validating the company itself.