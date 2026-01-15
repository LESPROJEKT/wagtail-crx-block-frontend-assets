# Compatibility Guide

This guide is a checklist for adding and maintaining multi-version support across
Python and framework dependencies.

## 1) Define the support policy

- Decide which Python and framework/library versions are supported.
- Prefer LTS releases where possible.
- Treat "supported" as "tested in CI" to avoid mismatches.

## 2) Choose a matrix strategy

Recommended: a hybrid matrix with both locked and floating sets.

- Locked: fully pinned framework + plugin/library versions.
- Floating: pin only the framework + key dependencies; let the rest float within
  allowed ranges.

This keeps CI reproducible while still catching upcoming breakages.

## 3) Add constraint files

Create a constraint file per tox environment in `constraints/`.

Locked example:

```
Django>=3.2,<4.2
some-framework==1.2.*
some-plugin>=2.0,<3
```

Floating example:

```
some-framework==1.2.*
some-plugin>=2.0,<3
```

## 4) Update tox environments

Add envs to `tox.ini`:

- `py39-framework12-plugin2`
- `py39-framework12-plugin2-float`

Each env should install requirements + the matching constraint file.

## 5) Keep test settings version-safe

Ensure the test settings work across versions:

- Provide required settings or defaults for framework initialization.
- Guard optional apps or modules if they were removed in newer versions.

## 6) Add minimal tests

Focus on core behaviors that must work across versions:

- Primary API behavior
- Integration points (hooks, plugins, adapters)
- Template or rendering output if applicable

Keep tests small and stable.

## 7) Update CI

Add every tox env to the CI matrix. Each entry should run:

```
tox -e <env>
```

## 8) Document tested versions

Keep a short section in `README.md` that points to the badges or matrix.
If badges are present, avoid duplicating the same list in text.

## 9) Add a new supported version (quick checklist)

1. Decide supported ranges for framework/dependencies/Python.
2. Add a locked constraint file.
3. Add a floating constraint file.
4. Add tox envs.
5. Add CI matrix entries.
6. Update README badges or notes.
7. Run `tox`.
