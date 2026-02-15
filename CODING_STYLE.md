We're excited that you're interested in contributing to Ink/Stitch's code. Thanks for reading this guide.

This file focuses on coding style principles. For workflow and process details (setup, commands, validation matrix, debug workflow, docs workflow, PR standards), use **[DEVELOPERS.md](DEVELOPERS.md)**.

General
=======

A major goal of Ink/Stitch is to create a codebase that is **fun to work on** and **easy to understand** for programmers of all skill and experience levels.

Machine embroidery is a complex problem space, so some code will also be complex. When that happens, we prioritize clear structure, meaningful naming, and comments that explain why decisions are made.

Readability First
=================

1. Prefer explicit, descriptive code over clever or compact code.
2. Use variable and function names that communicate intent.
3. Split complex conditions and transformations into smaller, readable steps.
4. Optimize for speed/memory only when justified; document tradeoffs when readability is reduced.

Code Conventions
================

For Python, follow [PEP8](https://www.python.org/dev/peps/pep-0008/). For Javascript, keep [ESLint](https://eslint.org) clean.

Project formatting and lint settings are enforced by `make style` (Ruff) and staged-file Black checks in git hooks. See `DEVELOPERS.md` for the complete validation contract.

Comments and Docstrings
=======================

1. Add comments when logic is non-obvious, especially in stitch-generation code.
2. Prefer comments that explain **why**, not just what.
3. Keep comments concise and close to the logic they explain.
4. Use docstrings for public interfaces and behavior contracts.

Type Annotations
================

Type annotations are encouraged. They improve readability and tooling support.

Run `python -m mypy` as part of your validation flow. For project-specific expectations and current CI behavior, see `DEVELOPERS.md`.

Code Review Guidance
====================

All code changes should go through pull requests and constructive review.

When reviewing, prioritize:

1. Correctness and regression risk.
2. Clarity and maintainability.
3. Test coverage for behavior changes.

Feedback must always align with our [Code of Conduct](CODE_OF_CONDUCT.md).

Design Approach
===============

Object-oriented and functional approaches are both acceptable. Choose the approach that best communicates intent.

When shared logic grows, prefer reusable library modules (for example under `lib/stitches`) rather than duplicating behavior across classes.
