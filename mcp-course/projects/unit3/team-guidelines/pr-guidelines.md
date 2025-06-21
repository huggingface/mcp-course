# PR Guidelines

## PR Size
- Keep PRs under 500 lines of changes
- Split large features into multiple PRs
- One logical change per PR
- Separate refactoring from feature changes

## PR Description
- Clearly explain what and why
- Include screenshots for UI changes
- List any breaking changes
- Add testing instructions
- Reference related issues/tickets

## Review Process
- At least one approval required
- Address all review comments
- Update PR description with changes made
- Resolve conflicts before requesting review
- Tag relevant team members

## Before Merging
- All CI checks must pass
- Update documentation if needed
- Verify no sensitive data is exposed
- Squash commits if necessary
- Delete feature branch after merge

## PR Title Format
- Use conventional commit format
- Be specific and descriptive
- Examples:
  - "feat(auth): Add OAuth2 support"
  - "fix(api): Handle null response in user endpoint"
  - "docs: Update installation guide"