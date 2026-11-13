# Contributing Guidelines

## Code of Conduct

Be respectful, inclusive, and professional. We're building something great together.

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Commit with clear messages: `git commit -m "feat: describe your change"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Open a Pull Request

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style (formatting, missing semicolons)
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `test:` Adding/updating tests
- `chore:` Maintenance tasks
- `ci:` CI/CD changes
- `security:` Security fixes

### Example
```
feat(auth): implement JWT refresh token rotation

- Add token refresh endpoint
- Implement automatic token rotation
- Add tests for token refresh flow

Closes #123
```

## Code Standards

### Backend (Python/FastAPI)
- Use Black for code formatting
- Follow PEP 8
- Type hints required
- Docstrings for all functions
- Minimum 80% test coverage

### Frontend (TypeScript/React)
- Use Prettier for formatting
- Use ESLint
- TypeScript strict mode
- Component documentation
- Tests for business logic

### Mobile (Swift/Kotlin)
- Follow language conventions
- Use provided formatters
- Document public APIs
- Unit tests required
- UI tests for critical flows

## Pull Request Process

1. **Update Documentation** - Update README if needed
2. **Add Tests** - All changes require tests
3. **Pass Checks** - All CI/CD checks must pass
4. **Code Review** - Wait for approval from maintainers
5. **Merge** - Use squash commits for clean history

## Testing Requirements

- **Backend:** `pytest` with minimum 80% coverage
- **Frontend:** React Testing Library + Vitest
- **iOS:** XCTest
- **Android:** JUnit + Espresso

Run tests before submitting:
```bash
# Backend
pytest tests/ --cov=app

# Frontend
npm run test

# iOS
xcodebuild test -scheme YatraDiscover

# Android
./gradlew test
```

## Security

- Never commit secrets or API keys
- Use `.env.example` for environment variables
- Report security issues privately to security@yatradiscover.com
- Review OWASP Top 10 security risks

## Documentation

- Update docs for new features
- Use clear, concise language
- Include code examples
- Update diagrams if architecture changes
- Keep README.md current

## Performance

- Optimize for mobile-first
- Target: Lighthouse score > 90
- Profile before optimizing
- Monitor Core Web Vitals
- Test with real devices

## Release Cycle

- **Weeks 1-3:** Development
- **Week 4:** Testing & QA
- **Week 5:** Bug fixes
- **Week 6:** Release preparation
- **Week 7:** Production release
- **Week 8:** Monitoring & fixes

## Questions?

- Open an issue for bugs
- Start a discussion for features
- Tag issues appropriately
- Provide context and examples

---

**Thank you for contributing to YatraDiscover AI! 🚀**
