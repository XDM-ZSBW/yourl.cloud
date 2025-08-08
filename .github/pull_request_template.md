# Pull Request: [Brief Description]

## Local Files Management Checklist

Before submitting this PR, please verify that you have:

- [ ] Checked that no local configuration files are being committed
  - [ ] No `.env` files or environment-specific configurations
  - [ ] No `__pycache__` directories or `.pyc` files
  - [ ] No `.vscode` or IDE-specific settings (unless shared team configuration)
  - [ ] No local database files or data dumps
  - [ ] No log files or debug outputs

- [ ] Verified sensitive information is not exposed
  - [ ] No API keys or secrets in code
  - [ ] No personal access tokens
  - [ ] No internal URLs or endpoints
  - [ ] No user credentials or test accounts
  - [ ] No organization-specific configurations

- [ ] Confirmed local development settings
  - [ ] Development server configurations are generic
  - [ ] Test configurations use environment variables
  - [ ] Local paths are relative, not absolute
  - [ ] Debug flags are controlled via environment variables

## Pre-submission Verification

- [ ] Ran `git status` to verify no unintended files are staged
- [ ] Checked `.gitignore` is properly filtering local files
- [ ] Reviewed `git diff` for any accidentally committed sensitive data
- [ ] Ensured all environment variables are documented in `.env.example`
- [ ] Verified no temporary or backup files are included

## VS Code / IDE Settings

- [ ] Workspace settings are team-friendly
- [ ] Extension recommendations are appropriate
- [ ] Debug configurations are generic
- [ ] Task definitions are platform-agnostic

## Notes

- Remember: Always use environment variables for configuration that varies between deployments
- Document any new environment variables in `.env.example`
- Keep sensitive data in your local `.env` file only
- Use relative paths in scripts and configurations

## Related Issues

- List any related issues or tickets here

## Additional Context

- Add any other context about the PR here
