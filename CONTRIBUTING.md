# Contributing to OtterStax Skills

Thank you for your interest in contributing to OtterStax Skills for Claude Code!

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Include environment details (OS, Claude Code version)
- Provide steps to reproduce bugs

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test your changes locally
5. Commit with clear messages: `git commit -m "Add: new feature description"`
6. Push to your fork: `git push origin feature/my-feature`
7. Open a Pull Request

### Command Guidelines

When adding new commands:

1. **Place in correct namespace:**
   - `commands/data/` - Data operations (query, analyze)
   - `commands/infra/` - Infrastructure (deploy, connect)
   - `commands/dev/` - Development utilities

2. **Follow the template:**
   ```markdown
   # Command Name

   Brief description.

   ## Arguments
   - `$ARGUMENTS` - Description

   ## Instructions

   Detailed instructions for Claude...

   ### Examples
   ```
   /namespace:command example
   ```
   ```

3. **Include:**
   - Clear description
   - Code examples
   - Error handling guidance
   - Usage examples

### Code Style

- Use clear, descriptive names
- Include comments for complex logic
- Follow existing patterns in the codebase

### Testing

Before submitting:

1. Test commands manually with Claude Code
2. Verify install.sh works
3. Check documentation renders correctly

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/claude-skills.git
cd claude-skills

# Install locally for testing
./install.sh

# Test a command
claude
> /data:query SELECT 1
```

## Questions?

Open an issue or discussion on GitHub.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
