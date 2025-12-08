# Hugo Personal Website Project

## Project Overview

This is a Hugo-based static website with integrated testing infrastructure. The project emphasizes quality, maintainability, and comprehensive testing.

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
```

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

## Working with Claude Code

### Expected Workflow

1. User requests feature/fix
2. Claude reviews relevant code
3. Claude writes tests for new functionality
4. Claude implements feature
5. Claude runs tests to verify
6. Claude creates atomic commits (one per logical change)
7. Claude asks permission before pushing
8. After several features, Claude checks if refactoring is needed

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

### Things Claude Should Never Do

- ❌ Push to remote without explicit permission
- ❌ Bundle multiple unrelated changes in one commit
- ❌ Add features without corresponding tests
- ❌ Use commands outside nix environment
- ❌ Over-comment obvious code
- ❌ Create premature abstractions
- ❌ Skip running tests before committing
- ❌ Modify code without reading it first

## Resources

- Hugo Documentation: https://gohugo.io/documentation/
- htmltest: https://github.com/wjdp/htmltest
- pytest: https://docs.pytest.org/
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- Nix Flakes: https://nixos.wiki/wiki/Flakes

## Project-Specific Notes

- **Favicon**: Must be linked in both Hugo templates AND static HTML files
- **Static HTML**: Files in `static/` aren't processed by Hugo templates
- **Bot Blocking**: Some academic URLs (DOI, WorldCat) block bots - use IgnoreURLs
- **Generated Content**: `cns/` directory contains generated HTML from Jupyter notebooks
- **Testing**: Use `-m "not external"` to skip network-dependent tests during development
