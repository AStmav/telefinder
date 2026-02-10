<!--
Sync Impact Report:
Version: 0.0.0 → 1.0.0
Change Type: MAJOR - Initial constitution ratification
Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (5 principles)
  - Technology Stack
  - Development Workflow
  - Governance
Templates Status:
  ✅ plan-template.md - reviewed, no updates needed (uses generic constitution check)
  ✅ spec-template.md - reviewed, no updates needed (technology-agnostic)
  ✅ tasks-template.md - reviewed, compatible with commit-per-task principle
Follow-up TODOs: None
-->

# TeleFinder Constitution

## Core Principles

### I. Technology Stack (NON-NEGOTIABLE)

The project MUST use the following technology stack:
- **Backend**: Python FastAPI for API development
- **Frontend**: Vue.js with TypeScript for type safety
- **Styling**: Tailwind CSS for UI components
- **Integration**: Telegram Bot API for publication and bot functionality

**Rationale**: This stack ensures modern development practices, type safety, rapid UI development, and seamless Telegram integration. Any deviation requires constitutional amendment.

### II. Telegram Bot API Integration

All publication and communication features MUST use the official Telegram Bot API.
- Bot functionality must be modular and testable
- API interactions must be properly abstracted
- Error handling for Telegram API failures is mandatory

**Rationale**: Telegram is the core publishing platform; proper API integration ensures reliability and maintainability.

### III. Markdown Processing & Validation (NON-NEGOTIABLE)

The system MUST include a Markdown converter with syntax validation:
- Markdown input must be validated before processing
- Conversion errors must be caught and reported clearly
- Support for standard Markdown and relevant extensions
- Output must be properly formatted for target platform

**Rationale**: Markdown is likely the primary content format; validation prevents errors and ensures consistent output quality.

### IV. Environment-Based Configuration (NON-NEGOTIABLE)

All tokens, secrets, and sensitive configuration MUST be stored in environment variables:
- NO hardcoded credentials in source code
- `.env.example` file must document all required variables
- Application must fail fast on missing required environment variables
- Separate configurations for development, testing, and production

**Rationale**: Security best practice to prevent credential leaks and enable environment-specific configuration without code changes.

### V. Atomic Git Commits (NON-NEGOTIABLE)

One task equals one commit:
- Each task from tasks.md results in exactly one commit
- Commit message must reference the task ID (e.g., "T001: Create project structure")
- Commits must be atomic and self-contained
- No partial work or multi-task commits allowed

**Rationale**: Ensures clean git history, easy rollback, clear traceability between tasks and code changes, and simplified code review process.

## Technology Stack

**Backend**:
- Language: Python 3.10+
- Framework: FastAPI
- Package Management: pip with requirements.txt (or Poetry if preferred)
- API Documentation: Auto-generated via FastAPI/OpenAPI

**Frontend**:
- Framework: Vue.js 3
- Language: TypeScript (strict mode)
- Styling: Tailwind CSS
- Build Tool: Vite (recommended for Vue 3 + TypeScript)

**Integration**:
- Telegram Bot API (official Python library: python-telegram-bot or aiogram)

**Configuration**:
- Environment variables via python-dotenv
- .env files for local development (gitignored)
- .env.example committed to repository

## Development Workflow

### Task-Driven Development

1. Tasks are defined in `/specs/[###-feature-name]/tasks.md`
2. Each task is implemented completely
3. Upon task completion, create ONE commit with format: `T###: [task description]`
4. Task commits must be atomic - no mixing of multiple tasks
5. All tests (if any) related to the task must pass before commit

### Code Organization

**Repository Structure** (Web Application):

```
backend/
├── src/
│   ├── api/          # FastAPI routes
│   ├── models/       # Data models
│   ├── services/     # Business logic
│   ├── telegram/     # Telegram Bot API integration
│   ├── markdown/     # Markdown converter & validator
│   └── config/       # Configuration management
├── tests/
└── requirements.txt

frontend/
├── src/
│   ├── components/   # Vue components
│   ├── pages/        # Vue pages/views
│   ├── services/     # API clients
│   ├── types/        # TypeScript type definitions
│   └── assets/       # Static assets
├── tests/
└── package.json

.env.example          # Template for environment variables
.gitignore            # Must include .env
```

### Security Requirements

- All environment variables must be documented in `.env.example`
- Never commit actual `.env` files
- Validate all environment variables on application startup
- Use TypeScript strict mode to catch type errors early
- Validate and sanitize all user inputs (Markdown, API requests)

### Quality Standards

- Python code must follow PEP 8 guidelines
- TypeScript code must pass strict type checking
- Markdown validation must catch syntax errors before publishing
- Telegram API calls must include proper error handling
- One commit per task (referenced by task ID)

## Governance

### Amendment Process

1. Constitutional changes require documentation of rationale
2. Version must be incremented according to semantic versioning:
   - **MAJOR**: Breaking changes to principles, tech stack, or workflow
   - **MINOR**: New principles or sections added
   - **PATCH**: Clarifications, typo fixes, non-semantic changes
3. All affected templates and documentation must be updated
4. Team review required for MAJOR changes

### Compliance

- All pull requests must verify compliance with this constitution
- Non-negotiable principles (I, III, IV, V) cannot be violated
- Tech stack principle (I) can only change via constitutional amendment
- Code reviews must check: environment variables usage, commit atomicity, Markdown validation, TypeScript strictness

### Version Control

- Git history must be clean and atomic (one task = one commit)
- Branch naming: `###-feature-name` (based on task tracking)
- Commit message format: `T###: [description]` for task commits
- No force pushes to main/master branch without team consensus

**Version**: 1.0.0 | **Ratified**: 2026-02-09 | **Last Amended**: 2026-02-09
