# Contributing

Contributions are welcome and encouraged.
To keep gatenet stable and predictable, please follow the guidelines below.

---

## Contribution Guidelines

### 1. Code Style & Quality

- Follow existing formatting, naming, and structure
- Write clear docstrings for all public functions and classes
- Add comments where intent may not be obvious
- Avoid unrelated or drive-by changes

### 2. Tests

- Add or update tests when behavior changes
- All tests must pass before a PR will be merged
- Test locally before pushing

### 3. Commit Messages

Commit frequently with clear, descriptive messages.

Format:
`(<type>) <short description>`

Types (recommended, not enforced):

- `fix` – correctness or bug fixes
- `tweak` – minor improvements
- `feat` – new features
- `docs` – documentation changes
- `patch` – bug fixes tied to an issue
- `refactor` – restructuring without behavior change
- `deps` – dependency updates
- `test` – test-only changes

---

## Branching Strategy

### Branch Roles

- `dev` – active development
- `master` – released and published code only

Direct commits to `master` are **not allowed**.

---

### Development Workflow

1. Start from `dev`

```bash
git checkout dev
git pull origin dev
```

2, (Optional) Create a feature branch

```bash
git checkout -b feat/your-feature-name
```

3. Make changes and commit.
4. Push to your branch

```bash
git push origin feat/your-feature-name
```

5. Open a Pull Request targeting `dev`.
