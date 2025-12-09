# Hugo Personal Website Project

## Table of Contents

**Quick Start:** [Development Environment](#development-environment) | [Common Tasks](#common-tasks)
**Standards:** [Git Commits](#git-commit-standards) | [Security](#security-standards) | [Code Quality](#code-quality-standards) | [Testing](#testing-requirements)
**Working with Claude:** [Workflow](#working-with-claude-code) | [Retrospectives](#retrospective-process)
**Reference:** [Architecture](#architecture) | [Build Process](#build-process) | [Resources](#resources)

## Project Overview

This is a Hugo-based static website with integrated testing infrastructure. The project emphasizes quality, maintainability, and comprehensive testing.

**Key Principles:**
- Security-first (client-side JavaScript focus)
- Test-driven development
- Atomic commits
- Framework best practices over hacks
- Regular retrospectives

## Architecture

- **Static Site Generator**: Hugo (extended version)
- **Content**: Markdown files in `content/` directory
- **Templates**: Hugo templates in `layouts/` directory
- **Static Assets**: Files in `static/` directory (copied as-is to output)
- **Build Output**: `public/` directory (git-ignored)
- **Testing**: pytest-based test suite in `tests/` directory
- **Development Environment**: Nix flake for reproducible builds

### Key Directories

```
.
├── content/          # Markdown content files
├── layouts/          # Hugo HTML templates
│   ├── partials/     # Reusable template components
│   └── _default/     # Default page templates
├── static/           # Static assets (images, CSS, JS, PDFs)
├── tests/            # Python-based test suite
├── utilities/        # Build scripts
└── flake.nix         # Nix development environment
```

## Development Environment

**IMPORTANT**: All build commands must run inside the Nix development environment:

```bash
# Enter development shell
nix develop

# Build the site
./build

# Run tests
pytest tests/

# Run htmltest validation
htmltest

# Run specific test markers
pytest tests/ -m meta
pytest tests/ -m "not external"

# Start local development server with live reload (recommended during development)
hugo server -D

# Or bind to specific address/port
hugo server --bind 0.0.0.0 --port 1313 -D
```

### Local Development Server

Hugo includes a built-in development server with **live reload** - changes to content, templates, or assets are automatically reflected in the browser without manual refresh.

**Starting the dev server:**
```bash
nix develop --command hugo server -D
```

**What it does:**
- Serves site at http://localhost:1313 by default
- Watches for file changes and rebuilds automatically
- Includes draft content with `-D` flag
- Shows build errors in real-time
- Fast rebuilds (typically < 100ms)

**IMPORTANT: Keep dev server running during all development work**

The Hugo dev server should be running continuously whenever you're actively developing. This provides instant feedback and catches errors immediately.

**Recommended workflow:**
1. **Start dev server first**: `nix develop --command hugo server -D`
2. **Leave it running** in a dedicated terminal window
3. Open browser to http://localhost:1313
4. Edit content, templates, or CSS in your editor
5. Changes appear instantly in browser (no manual refresh needed)
6. Watch terminal for build errors/warnings
7. When done with changes, run `./build` for full production build
8. Run tests before committing

**Differences from production build:**
- Dev server keeps content in memory (doesn't write to `public/`)
- Includes draft/future content with `-D` flag
- Faster builds (skips some optimizations)
- Always run `./build` before final testing and deployment

## Git Commit Standards

### Atomic Commits (CRITICAL)

**Each logical change MUST be a separate commit.** Never bundle multiple unrelated changes.

Examples of atomic commits:
- ✅ One commit: "Add favicon link to HTML head"
- ✅ One commit: "Fix MP3 file paths in digital music page"
- ✅ One commit: "Update htmltest ignore list for bot-blocking URLs"
- ❌ One commit: "Fix favicon, MP3 paths, and update ignore list" (TOO BROAD)

### Commit Message Format

Follow conventional commits style:

```
<type>: <description>

<optional body explaining why, not what>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Commit Process

1. Make changes for ONE logical unit of work
2. Review changes: `git status` and `git diff`
3. Stage files: `git add <files>`
4. Commit with descriptive message
5. Repeat for next logical change
6. **NEVER push without explicit user permission**

### Using HEREDOC for Commit Messages

Always use HEREDOC syntax for multi-line commit messages to ensure proper formatting:

```bash
git commit -m "$(cat <<'EOF'
Fix favicon link in static HTML files

Static HTML files weren't using Hugo templates, so they needed
the favicon link added manually to pass htmltest validation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## Testing Requirements

### Test Coverage Philosophy

**Every feature MUST have comprehensive unit tests.** When adding new functionality:

1. **Write tests FIRST or alongside implementation** (TDD approach preferred)
2. **Test both happy paths and edge cases**
3. **Aim for high code coverage** (check with `pytest --cov` if configured)
4. **Tests must be maintainable** - follow same code quality standards

### Test Categories (pytest markers)

- `@pytest.mark.meta` - HTML meta tags (Open Graph, Twitter Cards, canonical URLs)
- `@pytest.mark.structured_data` - JSON-LD structured data validation
- `@pytest.mark.html5` - HTML5 validation
- `@pytest.mark.content` - Content requirements (descriptions, titles, etc.)
- `@pytest.mark.accessibility` - Accessibility beyond alt text
- `@pytest.mark.external` - External URLs and network-dependent checks

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run without network-dependent tests
pytest tests/ -m "not external"

# Run specific test category
pytest tests/ -m accessibility -v

# Run with output for debugging
pytest tests/ -v -s
```

### Test Organization

Tests are organized by concern:
- `test_meta_tags.py` - SEO meta tags
- `test_accessibility.py` - WCAG compliance
- `test_html5_validation.py` - HTML structure
- `test_content_requirements.py` - Content quality
- `test_structured_data.py` - JSON-LD schemas
- `test_ignored_urls.py` - Validation of htmltest ignore list

### Pre-Push Testing

**ALWAYS run full test suite before pushing:**

```bash
# Complete validation
nix develop --command bash -c './build && htmltest && pytest tests/ -m "not external"'
```

All tests must pass before code can be pushed to remote.

## Code Quality Standards

### General Principles (Kernighan & Ritchie Style)

Following "The Elements of Programming Style" and "The C Programming Language" adapted for modern development:

1. **Write clearly** - Code should be self-documenting where possible
2. **Comment the why, not the what** - Explain reasoning, not obvious operations
3. **Choose clarity over cleverness** - Readable code beats terse code
4. **One purpose per function/component** - Single Responsibility Principle
5. **Avoid premature optimization** - Make it work, make it right, make it fast
6. **Test your code** - Write tests, don't just hope it works

### Documentation Standards

**When to comment:**
- Complex algorithms requiring explanation
- Non-obvious design decisions
- Public APIs and interfaces
- Workarounds for bugs or limitations
- Security-sensitive code sections

**When NOT to comment:**
- Self-evident code (`x = x + 1  # increment x` ❌)
- Redundant descriptions of function signatures
- Commented-out code (delete it, git remembers)

**Good commenting example:**

```python
def test_ignored_urls_are_reachable(self, ignored_urls):
    """Verify that ignored URLs return valid HTTP responses."""
    # 403 Forbidden means the resource exists but has very aggressive bot blocking
    # This is acceptable for ignored URLs, but worth noting
    if http_code == "403":
        blocked_urls.append((url, http_code))
```

### Python Code Standards

- **Style Guide**: PEP 8 (enforced via prettier/black if configured)
- **Imports**: Group stdlib, third-party, local (separated by blank lines)
- **Type Hints**: Use where helpful for clarity (especially public functions)
- **Docstrings**: Use for all public functions and classes
- **Line Length**: 88 characters (Black default) or 79 (PEP 8)
- **Testing**: pytest with descriptive test names

Example:

```python
def validate_url_accessibility(url: str, timeout: int = 10) -> tuple[str, bool]:
    """Test if URL is accessible with browser user agent.

    Args:
        url: The URL to test
        timeout: Request timeout in seconds

    Returns:
        Tuple of (http_code, is_accessible)
    """
    # Implementation
```

### HTML/CSS Standards

- **HTML5**: Use semantic elements (`<article>`, `<nav>`, `<main>`)
- **Accessibility**: WCAG 2.1 Level AA compliance
  - All images have alt text
  - Forms have labels
  - Headings are hierarchical
  - Color contrast meets standards
- **Meta Tags**: Include Open Graph, Twitter Cards, canonical URLs
- **CSS**: Use BEM naming or similar consistent methodology
- **Responsive**: Mobile-first approach

### JavaScript Standards

- **Modern ES6+**: Use const/let, arrow functions, async/await
- **No jQuery**: Use vanilla JS or modern frameworks
- **Accessibility**: Keyboard navigation support
- **Error Handling**: Always handle promise rejections

### Hugo Template Standards

- **Partials**: Extract reusable components to `layouts/partials/`
- **DRY**: Don't repeat template logic - use partials and shortcodes
- **Comments**: Explain non-obvious template logic
- **Whitespace**: Use `{{- -}}` to control whitespace in output

Example:

```go
{{- /* Structured data for search engines */ -}}
{{- partial "structured-data.html" . }}
```

## DRY (Don't Repeat Yourself) Principles

### When to Abstract

✅ **DO create abstractions when:**
- Logic is duplicated 3+ times
- Pattern is stable and well-understood
- Abstraction simplifies understanding
- Changes would affect multiple places

❌ **DON'T create abstractions when:**
- Only 2 instances exist (might be coincidental similarity)
- Requirements are still evolving
- Abstraction adds more complexity than it removes
- Performance is critical and abstraction adds overhead

### Refactoring Checkpoints

**Claude will periodically check in after:**
- Implementing 3+ related features
- Fixing multiple similar bugs
- Adding 200+ lines of code
- Noticing repeated patterns

**Questions to consider:**
- Are there repeated code patterns?
- Can components be extracted?
- Is naming consistent?
- Are tests covering new functionality?
- Is documentation up to date?

## Common Tasks

### Adding a New Blog Post

```bash
hugo new content/writing/my-post-title/index.md
```

### Creating New Tests

```python
# tests/test_new_feature.py
import pytest
from pathlib import Path
from bs4 import BeautifulSoup

@pytest.fixture(scope="session")
def public_dir():
    """Path to Hugo's public output directory."""
    return Path(__file__).parent.parent / "public"

@pytest.mark.content
def test_my_new_feature(public_dir):
    """Verify new feature works correctly."""
    # Test implementation
    pass
```

### Updating Dependencies

Dependencies are managed in `flake.nix`:

```nix
buildInputs = with pkgs; [
  hugo
  python3Packages.pytest
  # Add new dependencies here
];
```

## htmltest Configuration

Located in `.htmltest.yml`:

- **IgnoreDirs**: Directories to skip (e.g., generated content)
- **IgnoreURLs**: External URLs that block bots but work in browsers
- **CheckFavicon**: Ensures all pages have favicon
- **CheckImages**: Validates alt attributes

When adding URLs to ignore list, verify they:
1. Actually work with browser user agent
2. Actually block bot user agents (use test_ignored_urls.py)

## Important Files

- `.htmltest.yml` - HTML validation configuration
- `pytest.ini` - pytest configuration and markers
- `flake.nix` - Development environment specification
- `.gitignore` - Git ignore patterns
- `utilities/build.sh` - Main build script

## Build Process

The `./build` script:
1. Resets website repository state
2. Builds LaTeX documents (CV, PDFs)
3. Runs Hugo to generate static site
4. Formats HTML with prettier
5. Shows git status for both repositories

## CI/CD

GitHub Actions workflow validates:
- Hugo builds successfully
- htmltest passes (link validation, favicon, meta tags)
- pytest suite passes
- All commits follow standards

## Security Standards

### Client-Side Security for Static Sites

Since this is a static site, security focuses on **client-side JavaScript** and **content security**. Based on OWASP Top 10 Client-Side Security Risks and 2025 standards:

#### 1. Cross-Site Scripting (XSS) Prevention

**Risk**: Malicious scripts injected through user-controllable data or third-party dependencies.

**Mitigations**:
- ✅ Use Content Security Policy (CSP) headers in `layouts/partials/head.html`
- ✅ Never use `innerHTML` with untrusted data - use `textContent` or `createTextNode()`
- ✅ Avoid `eval()`, `Function()`, and inline event handlers (`onclick=""`)
- ✅ Sanitize any user input before rendering (though static sites rarely have user input)
- ✅ Use Hugo's built-in escaping in templates: `{{ . | safeHTML }}` only when absolutely necessary

**Example**: Email scrambler uses `textContent` for safe string assignment:
```javascript
emailDisplay.textContent = unscrambled; // Safe
// NOT: emailDisplay.innerHTML = unscrambled; // Unsafe
```

#### 2. Vulnerable JavaScript Libraries

**Risk**: Using outdated or compromised third-party JavaScript libraries.

**Mitigations**:
- ✅ Minimize third-party JavaScript dependencies
- ✅ Pin specific versions in package.json/flake.nix
- ✅ Review library code before including (especially for security-sensitive features)
- ✅ Use Subresource Integrity (SRI) for CDN-hosted scripts
- ✅ Keep dependencies updated via `nix flake update`

**Pre-commit check before adding new JavaScript library:**
1. Is it actively maintained? (check recent commits)
2. Does it have known vulnerabilities? (check npm audit or GitHub advisories)
3. Can we implement the feature without it?

#### 3. Sensitive Data in Client-Side Storage

**Risk**: Storing sensitive information in LocalStorage, SessionStorage, or browser cache.

**Mitigations**:
- ❌ Never store passwords, tokens, API keys, or PII in browser storage
- ❌ Never commit secrets to git (even in comments)
- ✅ Use memory-only variables for sensitive data that must exist client-side
- ✅ Clear sensitive data when no longer needed

**Pre-commit check for sensitive data exposure**:
```bash
# Check for common patterns that expose secrets:
grep -r "api[_-]?key" --include="*.js" --include="*.html"
grep -r "password" --include="*.js" --include="*.html"
grep -r "secret" --include="*.js" --include="*.html"
grep -r "token" --include="*.js" --include="*.html"

# For email obfuscation features, verify no plaintext emails in code:
grep -r "@.*\.com" --include="*.js" --include="*.md"
```

#### 4. Content Security Policy (CSP)

**Current CSP** (in `layouts/partials/head.html`):
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' https://stvhay.github.io;">
```

**CSP Principles**:
- ✅ Start with restrictive policy and relax only when necessary
- ❌ Avoid `'unsafe-inline'` and `'unsafe-eval'` in production
- ✅ Use external script files instead of inline `<script>` tags
- ✅ Use external stylesheets instead of inline `<style>` tags
- ✅ Whitelist specific domains rather than using wildcards

**When modifying CSP**:
1. Test in development first
2. Check browser console for CSP violations
3. Only add exceptions for legitimate use cases
4. Document why each exception is needed

#### 5. Supply Chain Security

**Risk**: Compromised build tools, dependencies, or development environment.

**Mitigations**:
- ✅ Use Nix flakes for reproducible builds (pinned dependencies)
- ✅ Review changes to `flake.nix` and `flake.lock` carefully
- ✅ Verify integrity of downloaded files (Nix does this automatically)
- ✅ Keep development environment updated: `nix flake update`
- ✅ Review Hugo shortcodes and templates from external sources

#### 6. Origin Control and Third-Party Code

**Risk**: Uncontrolled third-party scripts accessing site data or modifying DOM.

**Mitigations**:
- ✅ Minimize third-party scripts (analytics, fonts, etc.)
- ✅ Use CSP to restrict which domains can load scripts
- ✅ Host critical resources locally rather than from CDNs when possible
- ✅ Review any third-party code before including

**Pre-commit checklist for new third-party code:**
- [ ] Do we really need this third-party resource?
- [ ] Can we self-host it instead of using a CDN?
- [ ] Is the source trusted and actively maintained?
- [ ] Have we added it to CSP whitelist?
- [ ] Is it loaded over HTTPS?

### Security Pre-Commit Checklist

Run this checklist before committing changes that touch:
- JavaScript files
- HTML templates
- Authentication/contact forms
- Email obfuscation
- Content Security Policy

**Checklist**:

**1. Check for exposed sensitive data:**
- [ ] No plaintext emails in code (if we're trying to hide them)
- [ ] No API keys, tokens, or passwords anywhere
- [ ] No sensitive data in comments
- [ ] No test credentials or debug endpoints

**2. Verify JavaScript security:**
- [ ] No use of innerHTML with untrusted data
- [ ] No eval() or Function() calls
- [ ] No inline event handlers (onclick, onerror, etc.)
- [ ] All user input is sanitized/escaped
- [ ] Error messages don't leak sensitive info

**3. Check CSP compliance:**
- [ ] Scripts load from allowed domains only
- [ ] No inline scripts in production (use external files)
- [ ] No unsafe-inline or unsafe-eval
- [ ] CSP errors checked in browser console

**4. Verify dependencies:**
- [ ] No new unvetted third-party libraries
- [ ] All CDN resources use HTTPS
- [ ] Consider if resources can be self-hosted

**5. Test for XSS:**
- [ ] Try injecting `<script>alert('XSS')</script>` in any user input
- [ ] Verify special characters are escaped in output
- [ ] Check that textContent used instead of innerHTML

## Working with Claude Code

### Workflow Best Practices

#### 1. Framework Research ("Do It The Right Way")

**Before implementing**, check if the framework provides a built-in solution:

**For Hugo-specific tasks**:
- Adding custom HTML to markdown? → Use **shortcodes**, not `unsafe = true`
- Reusing HTML across pages? → Use **partials** in `layouts/partials/`
- Page-specific logic? → Use **front matter** and template conditionals
- Custom URLs/routing? → Use **aliases** in front matter

**For CSS tasks**:
- Adding colors? → Check if existing CSS variables can be reused
- Theming? → Use existing `:root` variables and media queries
- Layout? → Check if existing grid/flex patterns can be extended

**For Git tasks**:
- Editing previous commit? → Use `git commit --amend` (if not pushed)
- Fixing older commit? → Use `git rebase -i` (if not pushed)
- Don't manually edit commit hashes or metadata

**Red flags that suggest there's a better way**:
- Adding `unsafe = true` to config files
- Copying/pasting large blocks of code
- Fighting the framework's conventions
- Needing complex workarounds for simple tasks

#### 2. Commit Workflow

**Process** (user's preferred approach):
1. Make changes for one logical unit
2. Commit to working tree normally
3. User reviews commit with their tools
4. If changes needed:
   - Latest commit: Claude amends with `git commit --amend`
   - Earlier commit: Claude uses `git rebase -i` to fix the right one
5. History can be messy during work - clean up before push

**Key principles**:
- Each commit should be focused and atomic
- Commits should be small enough to review easily
- Claude is responsible for maintaining clean history during rebases
- No need to preview diffs before committing - user reviews the commit itself

#### 3. Security Review Process

For any commit touching security-sensitive code, run the **Security Pre-Commit Checklist** above.

**Security-sensitive areas**:
- JavaScript (any `.js` files)
- Contact forms or email handling
- Authentication/authorization
- CSP or security headers
- Third-party scripts or libraries

### Expected Workflow

1. User requests feature/fix
2. **Claude researches framework best practices** (if non-trivial)
3. Claude reviews relevant code
4. Claude writes tests for new functionality
5. Claude implements feature using framework patterns
6. **Claude runs security checklist** (if security-sensitive)
7. Claude runs tests to verify
8. Claude creates atomic commits (one per logical change)
9. Claude asks permission before pushing
10. After several features, Claude checks if refactoring is needed

### Things Claude Should Always Do

- ✅ Read files before editing them
- ✅ Run tests after making changes
- ✅ Create separate commits for each logical change
- ✅ Ask before pushing to remote
- ✅ Use `nix develop` for all build/test commands
- ✅ Write comprehensive tests for new features
- ✅ Follow DRY principles
- ✅ Document non-obvious code decisions
- ✅ Check for refactoring opportunities periodically
- ✅ Research framework best practices before implementing
- ✅ Run security checklist for security-sensitive code

### Things Claude Should Never Do

- ❌ Push to remote without explicit permission
- ❌ Bundle multiple unrelated changes in one commit
- ❌ Add features without corresponding tests
- ❌ Use commands outside nix environment
- ❌ Over-comment obvious code
- ❌ Create premature abstractions
- ❌ Skip running tests before committing
- ❌ Modify code without reading it first
- ❌ Use `unsafe = true` or similar config hacks without checking for proper solutions
- ❌ Commit sensitive data (even in comments)

## Retrospective Process

### When to Conduct Retrospectives

Hold a retrospective after:
- Major feature completion
- Significant refactoring
- Multiple iterations on the same code
- User request ("let's do a retrospective")
- Every 2-3 weeks of active development

### Three-Part Retrospective Structure

#### Part 1: Workflow Effectiveness Review

**Questions to address:**
1. **What did we accomplish?** (Brief summary of work done)
2. **What went well?** (Practices that worked)
3. **What could be improved?** (Specific pain points)
4. **Proposed improvements** (Concrete, actionable changes)

**Format:**
- Review the session's work chronologically
- Identify patterns (e.g., multiple architectural iterations, missed security issues)
- Suggest specific process improvements
- Get user feedback on proposals

**Example areas to examine:**
- Did we use the right tools/approaches upfront?
- Were there preventable mistakes?
- Did we follow the documented standards?
- Were commits atomic and well-organized?
- Was communication clear?

#### Part 2: Code Standards Review

**Questions to address:**
1. **Are current standards still appropriate?**
2. **Do standards need clarification or expansion?**
3. **Are there new patterns/practices to document?**
4. **Are standards being followed consistently?**

**Process:**
1. Review relevant sections of CLAUDE.md
2. Compare actual practices against documented standards
3. Identify gaps or outdated guidance
4. Propose updates to standards
5. Get user approval for changes

**Areas to review:**
- Code quality guidelines
- Testing requirements
- Security practices
- Framework usage patterns
- Documentation standards

#### Part 3: Whole Project Code Review

**Questions to address:**
1. **Are there code quality issues across the project?**
2. **Is there technical debt to address?**
3. **Are there security vulnerabilities?**
4. **Is documentation up to date?**

**Process:**
1. Review project structure and organization
2. Check for outdated dependencies
3. Look for security issues (run security checklist on existing code)
4. Identify code duplication or abstraction opportunities
5. Check test coverage and quality
6. Verify documentation accuracy
7. Create issues/tasks for identified problems

**Example automated checks:**
```bash
# Find potentially unsafe JavaScript patterns
find . -name "*.js" -exec grep -l "innerHTML" {} \;
grep -r "eval(" --include="*.js"

# Check for exposed sensitive data
grep -r "@.*\.com" --include="*.js" --include="*.md"

# Verify test coverage exists
pytest tests/ --cov --cov-report=term-missing -m "not external"
```

**Manual review items:**
- Code duplication (similar functions/components that could be abstracted)
- Missing tests (features without corresponding test coverage)
- Documentation accuracy (outdated comments or README sections)
- Dead code (unused functions or variables)

### Documenting Retrospective Outcomes

After each retrospective:
1. **Update CLAUDE.md** with new standards/practices
2. **Commit the updates** as a single logical change
3. **Create issues** for technical debt or improvements
4. **Share summary** with user for approval

### Retrospective Best Practices

- **Be specific**: "Check framework docs first" not "be better"
- **Be actionable**: Concrete steps, not vague goals
- **Be honest**: Acknowledge mistakes without defensiveness
- **Focus on process**: Fix the workflow, not blame
- **Get buy-in**: User must agree with proposed changes

## Maintaining This Document

### CLAUDE.md Best Practices

This file should follow its own standards for quality documentation:

**Structure:**
- **Table of Contents** - Keep updated as sections change
- **Logical flow** - Context → Setup → Standards → Meta → Reference
- **Scannable sections** - Use clear headings and concise paragraphs
- **Length** - Detail is valuable for AI, but keep sections focused

**Content Quality:**
- **Be specific** - "Use shortcodes, not `unsafe = true`" not "use best practices"
- **Show examples** - Code snippets and command examples for clarity
- **Be actionable** - Concrete steps, not abstract principles
- **Avoid redundancy** - Reference sections instead of repeating

**Code Blocks:**
- **Bash blocks** - Only for actual runnable commands
- **Checklists** - Use markdown checkboxes `- [ ]`, not bash comments
- **Examples** - Mark as examples and ensure they're correct

**When to Update:**
- After retrospectives (document new practices)
- When adding new tools or frameworks
- When practices change (old advice becomes wrong)
- When repetitive questions arise (document the answer)

**What NOT to include:**
- Temporary notes (use issues/TODOs instead)
- Implementation details (belongs in code comments)
- Extensive how-tos for third-party tools (link to official docs)
- Outdated information (remove rather than mark as old)

## Resources

### Framework Documentation
- Hugo Documentation: https://gohugo.io/documentation/
- htmltest: https://github.com/wjdp/htmltest
- pytest: https://docs.pytest.org/
- Nix Flakes: https://nixos.wiki/wiki/Flakes

### Security Standards
- [OWASP Top 10: 2025](https://owasp.org/Top10/)
- [OWASP Top 10 Client-Side Security Risks](https://owasp.org/www-project-top-10-client-side-security-risks/)
- [OWASP Top 10 2025 vs 2021 Comparison](https://equixly.com/blog/2025/12/01/owasp-top-10-2025-vs-2021/)

### Accessibility
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/

## Project-Specific Notes

- **Favicon**: Must be linked in both Hugo templates AND static HTML files
- **Static HTML**: Files in `static/` aren't processed by Hugo templates
- **Bot Blocking**: Some academic URLs (DOI, WorldCat) block bots - use IgnoreURLs
- **Generated Content**: `cns/` directory contains generated HTML from Jupyter notebooks
- **Testing**: Use `-m "not external"` to skip network-dependent tests during development
