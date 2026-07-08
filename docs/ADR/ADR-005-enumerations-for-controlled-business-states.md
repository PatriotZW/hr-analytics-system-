ADR-005

I think this deserves another ADR.

Title

Use Enumerations for Controlled Business States

Context

Certain business attributes have a fixed number of valid values.

Examples include employee status and future approval states.

Decision

The system shall use Python Enum classes for business-controlled values rather than unrestricted strings.

Rationale
Prevents invalid values.
Improves readability.
Makes business rules explicit.
Simplifies validation.
Easier to extend.
Consequences

Advantages:

Stronger type safety.
Consistent values throughout the application.
Fewer bugs caused by spelling mistakes.

Trade-off:

Developers must use the defined enumeration values rather than arbitrary strings.