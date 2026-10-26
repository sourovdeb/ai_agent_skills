# Code Smells Catalog

## Bloaters (Code that grows too large)

### Long Method
- **Signal:** Function > 50 lines
- **Fix:** Extract Method — split into smaller functions with clear names
- **Example:** A function that validates, processes, and saves data → split into `validate()`, `process()`, `save()`

### Large Class
- **Signal:** Class > 300 lines or > 10 methods
- **Fix:** Extract Class — split responsibilities
- **Example:** A `UserManager` that handles auth, profile, and notifications → split into `AuthService`, `ProfileService`, `NotificationService`

### Primitive Obsession
- **Signal:** Using primitives (string, int) instead of small objects
- **Fix:** Replace Data Value with Object
- **Example:** `phoneNumber: string` → `PhoneNumber` class with validation and formatting

### Long Parameter List
- **Signal:** Function with > 4 parameters
- **Fix:** Introduce Parameter Object or use builder pattern
- **Example:** `createUser(name, email, age, address, phone, role)` → `createUser({ name, email, profile: { age, address, phone }, role })`

### Data Clumps
- **Signal:** Same 3+ fields appearing together in multiple places
- **Fix:** Extract Class — group the clump into an object
- **Example:** `x, y, z` coordinates passed everywhere → `Point` class

## Object-Orientation Abusers

### Switch Statements
- **Signal:** Long switch/if-else chains on type codes
- **Fix:** Replace Type Code with Polymorphism or Strategy pattern
- **Example:** `switch(type) { case 'a': ...; case 'b': ...; }` → `handler[type].execute()`

### Temporary Field
- **Signal:** Class field only used in some methods
- **Fix:** Extract Class — move the field and its methods to a new class

### Refused Bequest
- **Signal:** Subclass overrides methods but doesn't use inherited behavior
- **Fix:** Replace Inheritance with Delegation, or push down what's not needed

### Alternative Classes with Different Interfaces
- **Signal:** Two classes do the same thing with different method names
- **Fix:** Rename methods to match, or extract common interface

## Change Preventers (Code that makes changes hard)

### Divergent Change
- **Signal:** One class changed for multiple unrelated reasons
- **Fix:** Extract Class — one class per reason for change

### Shotgun Surgery
- **Signal:** One change requires small edits in many classes
- **Fix:** Move Method/Field — consolidate the change into one class

### Parallel Inheritance Hierarchies
- **Signal:** Adding a subclass in one hierarchy requires adding one in another
- **Fix:** Eliminate one of the hierarchies

## Dispensables (Code that should be removed)

### Comments (Excessive)
- **Signal:** Comments explaining what the code does (not why)
- **Fix:** Rename to make code self-documenting, or delete the comment

### Dead Code
- **Signal:** Unreachable code, unused variables, commented-out code
- **Fix:** Delete it — version control preserves history

### Lazy Class
- **Signal:** Class that doesn't do enough to justify its existence
- **Fix:** Collapse Hierarchy or Inline Class

### Data Class
- **Signal:** Class with only fields and getters/setters, no behavior
- **Fix:** Move behavior into the data class, or use a record/struct

### Speculative Generality
- **Signal:** Abstract classes, unused parameters, "future-proofing" code
- **Fix:** Collapse Hierarchy, remove unused parameters, delete dead code

## Couplers (Excessive coupling)

### Feature Envy
- **Signal:** Method uses more of another class's data than its own
- **Fix:** Move Method — move it to the class it's envious of

### Inappropriate Intimacy
- **Signal:** Classes accessing each other's private members
- **Fix:** Move Method/Field, or make them formally related

### Message Chains
- **Signal:** `a.getB().getC().getD().doSomething()`
- **Fix:** Hide Delegate — create a method on `a` that encapsulates the chain

### Middle Man
- **Signal:** Class that just delegates to another class
- **Fix:** Remove Middle Man — call the delegate directly

## Quick Detection Checklist

- [ ] Any function > 50 lines?
- [ ] Any class > 300 lines?
- [ ] Any function with > 4 parameters?
- [ ] Any switch/if-else chain > 5 cases?
- [ ] Any nesting > 4 levels deep?
- [ ] Any commented-out code?
- [ ] Any unused variables/imports/exports?
- [ ] Any magic numbers (unnamed constants)?
- [ ] Any duplicated code blocks?
- [ ] Any class that only holds data (no behavior)?
- [ ] Any method that uses more of another class than its own?
- [ ] Any `a.getB().getC().getD()` chains?
