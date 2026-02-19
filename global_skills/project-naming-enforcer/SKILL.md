---
name: Project Naming Enforcer
description: Standardizes project and directory names to follow industry best practices (lowercase, kebab-case).
---

# Project Naming Enforcer

## Role
The "Standards Guard" that ensures all projects, directories, and package names are compatible with registry restrictions (NPM, Docker, PyPI).

## Rules
1. **Lowercase Only:** All names must be converted to lowercase.
2. **Kebab-Case:** Spaces and underscores must be replaced by hyphens `-`.
3. **No Special Characters:** Only alphanumeric characters and hyphens are allowed.
4. **Validation:** Intercepts initialization commands (`npm init`, `create-next-app`) to verify naming compliance.

## Logic (Standardization)
- Input: `CandyCloud` -> Output: `candy-cloud`
- Input: `My Awesome Project` -> Output: `my-awesome-project`
