# Hugo Personal Website Project

## Quick Reference

**Build & Test:**
- Build: `nix develop --command ./build`
- Test: `nix develop --command pytest tests/ -m "not external" -v` (includes htmltest)
- Dev server: `nix develop --command hugo server -D` (keep running during development)
- Full check: `nix develop --command bash -c './build && pytest tests/ -m "not external"'`

**Common Commands:**
- New post: `hugo new content/writing/post-title/index.md`
- Enter nix shell: `nix develop`
- Update dependencies: `nix flake update`

## Project Principles

- **Security-first**: Client-side JavaScript security (XSS, CSP, no sensitive data in storage)
- **Test-driven**: All features have comprehensive tests before merging
- **Atomic commits**: One logical change per commit, never bundle unrelated changes
- **Framework patterns**: Use Hugo shortcodes/partials, not hacks like `unsafe = true`
- **Regular retrospectives**: Review workflow, standards, and code quality periodically

## Architecture

- **Generator**: Hugo extended (static site)
- **Content**: Markdown in `content/`
- **Templates**: Hugo templates in `layouts/` (partials, shortcodes, default)
- **Assets**: Static files in `static/` (CSS, JS, images, PDFs)
- **Tests**: pytest in `tests/` with markers: `meta`, `structured_data`, `html5`, `content`, `accessibility`, `javascript`, `external`
- **Build**: Nix flake for reproducible environment
- **Output**: `public/` (git-ignored)

## Development Workflow

### Always Use Nix Environment
- ALL commands must run inside `nix develop`
- Dev server should run continuously during development (auto-rebuilds on file changes)
- Server runs at http://localhost:1313 with live reload

### Git Commit Standards

**Critical: Atomic Commits**
- One logical change = one commit
- ✅ Good: "feat: Add favicon link to HTML head"
- ✅ Good: "fix: Correct MP3 file paths in digital music page"
- ❌ Bad: "Fix favicon, MP3 paths, and update ignore list"

**Commit message format (type prefix required):**
```
<type>: <description>

<optional body explaining why, not what>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types (always use one):**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code change that neither fixes a bug nor adds a feature
- `test:` - Adding or updating tests
- `chore:` - Build process, dependencies, tooling

**Use HEREDOC for multi-line messages:**
```bash
git commit -m "$(cat <<'EOF'
<message here>
EOF
)"
```

**Never push without explicit user permission**

### Testing Requirements

- **Write tests first or alongside implementation** (TDD preferred)
- **Test both happy paths and edge cases**
- **All tests must pass before pushing**
- Use markers to run subsets: `pytest tests/ -m meta`, `pytest tests/ -m "not external"`
- Test files: `test_accessibility.py`, `test_content_requirements.py`, `test_email_scrambler.py`, `test_html5_validation.py`, `test_htmltest.py`, `test_ignored_urls.py`, `test_meta_tags.py`, `test_structured_data.py`
- **htmltest is integrated** into pytest suite via `test_htmltest.py` - validates all HTML links, images, and structure

## Security Standards (OWASP-based)

### 1. XSS Prevention
- ✅ Use `textContent`, never `innerHTML` with untrusted data
- ✅ No `eval()`, `Function()`, or inline event handlers (`onclick=""`)
- ✅ Maintain strict CSP in `layouts/partials/head.html`
- ✅ Hugo templates: use `{{ . | safeHTML }}` only when absolutely necessary

### 2. Content Security Policy
- Current: `default-src 'self'; script-src 'self' https://stvhay.github.io;`
- ❌ Never add `'unsafe-inline'` or `'unsafe-eval'` in production
- ✅ Use external script files, not inline `<script>` tags
- Test changes in dev first, check browser console for violations

### 3. JavaScript Dependencies
- ✅ Minimize third-party libraries
- ✅ Pin versions in flake.nix
- ✅ Review code before including
- ✅ Use SRI for CDN scripts
- Before adding library: Is it maintained? Any known vulnerabilities? Can we avoid it?

### 4. Sensitive Data
- ❌ Never store passwords, tokens, API keys, or PII in browser storage
- ❌ Never commit secrets (even in comments)
- ✅ Use memory-only variables for sensitive client-side data
- **Pre-commit check:** `grep -r "@.*\.com" --include="*.js" --include="*.md"` (for email obfuscation features)

### 5. Supply Chain
- ✅ Use Nix for reproducible builds (pinned dependencies)
- ✅ Review changes to `flake.nix` and `flake.lock`
- ✅ Keep updated: `nix flake update`

### Security Pre-Commit Checklist

Run for any commit touching JavaScript, HTML templates, contact forms, email handling, or CSP:

**1. Exposed sensitive data:**
- [ ] No plaintext emails (if hiding them)
- [ ] No API keys, tokens, passwords
- [ ] No secrets in comments

**2. JavaScript security:**
- [ ] No innerHTML with untrusted data
- [ ] No eval() or Function()
- [ ] No inline event handlers
- [ ] User input sanitized/escaped

**3. CSP compliance:**
- [ ] Scripts from allowed domains only
- [ ] No inline scripts in production
- [ ] No unsafe-inline or unsafe-eval

**4. Dependencies:**
- [ ] No unvetted third-party libraries
- [ ] CDN resources use HTTPS

**5. XSS testing:**
- [ ] Try injecting `<script>alert('XSS')</script>`
- [ ] Verify textContent used, not innerHTML

## Code Quality Standards

### General Principles
- **Write clearly** - Self-documenting code preferred
- **Comment the why, not the what** - Explain reasoning, not obvious operations
- **Clarity over cleverness** - Readable beats terse
- **Single Responsibility** - One purpose per function/component
- **Test your code** - Don't just hope it works

### When to Comment
- ✅ Complex algorithms
- ✅ Non-obvious design decisions
- ✅ Public APIs
- ✅ Security-sensitive code
- ✅ Workarounds for bugs/limitations
- ❌ Self-evident code
- ❌ Redundant function descriptions
- ❌ Commented-out code (delete it, git remembers)

### Python
- Follow PEP 8
- Use type hints for public functions
- Docstrings for all public functions/classes
- Imports: stdlib, third-party, local (separated by blank lines)

### HTML/CSS
- Semantic HTML5 elements (`<article>`, `<nav>`, `<main>`)
- WCAG 2.1 Level AA compliance (alt text, labels, heading hierarchy, color contrast)
- Include Open Graph, Twitter Cards, canonical URLs
- Mobile-first responsive design

### JavaScript
- Modern ES6+ (const/let, arrow functions, async/await)
- No jQuery
- Keyboard navigation support
- Always handle promise rejections

### Hugo Templates
- Extract reusable components to `layouts/partials/`
- Use shortcodes for custom HTML in markdown (not `unsafe = true`)
- Comment non-obvious template logic
- Control whitespace with `{{- -}}`

## Working with Claude

### Before Implementing (Framework Research)
Check if framework provides built-in solution:
- Custom HTML in markdown? → Shortcodes, not `unsafe = true`
- Reusing HTML? → Partials in `layouts/partials/`
- Page logic? → Front matter + template conditionals
- Custom URLs? → Aliases in front matter
- Colors? → Existing CSS variables
- Git edits? → `git commit --amend` or `git rebase -i`

**Red flags suggesting better way exists:**
- Adding `unsafe = true` to configs
- Copying/pasting large code blocks
- Fighting framework conventions
- Complex workarounds for simple tasks

### Commit Workflow
1. Make changes for one logical unit
2. Commit normally
3. User reviews commit
4. If changes needed: amend latest commit or rebase for earlier commits
5. Claude maintains clean history during rebases
6. No need to preview diffs before committing - user reviews the commit

### Expected Workflow
1. User requests feature/fix
2. **Research framework best practices** (if non-trivial)
3. Review relevant code
4. Write tests for new functionality
5. Implement using framework patterns
6. **Run security checklist** (if security-sensitive)
7. Run tests to verify
8. Create atomic commits
9. Ask permission before pushing
10. Periodically check for refactoring opportunities

### Always Do
- ✅ Read files before editing
- ✅ Run tests after changes
- ✅ Atomic commits with type prefix (feat:, fix:, refactor:, etc.)
- ✅ Ask before pushing
- ✅ Use nix develop for all commands
- ✅ Write comprehensive tests
- ✅ Research framework best practices
- ✅ Run security checklist for sensitive code
- ✅ Document non-obvious decisions

### Never Do
- ❌ Push without permission
- ❌ Bundle unrelated changes
- ❌ Add features without tests
- ❌ Use commands outside nix
- ❌ Over-comment obvious code
- ❌ Premature abstractions
- ❌ Skip tests before committing
- ❌ Modify code without reading first
- ❌ Use unsafe config hacks without checking for proper solutions
- ❌ Commit sensitive data

## DRY Principles

**Create abstractions when:**
- Logic duplicated 3+ times
- Pattern is stable and well-understood
- Abstraction simplifies understanding
- Changes would affect multiple places

**Don't create abstractions when:**
- Only 2 instances exist
- Requirements still evolving
- Abstraction adds more complexity
- Performance critical and abstraction adds overhead

**Refactoring checkpoints after:**
- 3+ related features
- Multiple similar bugs
- 200+ lines of code
- Noticing repeated patterns

## Retrospective Process

### When to Hold Retrospectives
- After major feature completion
- After significant refactoring
- After multiple iterations on same code
- User request
- Every 2-3 weeks of active development

### Three-Part Structure

**Part 1: Workflow Effectiveness**
- What did we accomplish?
- What went well?
- What could be improved?
- Propose specific, actionable improvements

**Part 2: Code Standards Review**
- Are current standards appropriate?
- Do standards need clarification?
- New patterns to document?
- Standards followed consistently?

**Part 3: Whole Project Code Review**
- Code quality issues?
- Technical debt?
- Security vulnerabilities?
- Documentation accuracy?

**Automated checks:**
```bash
find . -name "*.js" -exec grep -l "innerHTML" {} \;
grep -r "eval(" --include="*.js"
grep -r "@.*\.com" --include="*.js" --include="*.md"
pytest tests/ --cov --cov-report=term-missing -m "not external"
```

**After retrospective:**
1. Update CLAUDE.md with new practices
2. Commit updates as single logical change
3. Create issues for technical debt
4. Get user approval

## Project-Specific Notes

- **Favicon**: Must be in both Hugo templates AND static HTML files
- **Static HTML**: Files in `static/` not processed by Hugo templates
- **Bot blocking**: Academic URLs (DOI, WorldCat) block bots - use IgnoreURLs in `.htmltest.yml`
- **Generated content**: `cns/` has generated HTML from Jupyter notebooks
- **htmltest config**: See `.htmltest.yml` for IgnoreURLs, IgnoreDirs, validation settings
- **Build process**: `./build` script resets website repo, builds LaTeX docs, runs Hugo, formats HTML

## Resources

**Framework docs:**
- Hugo: https://gohugo.io/documentation/
- htmltest: https://github.com/wjdp/htmltest
- pytest: https://docs.pytest.org/
- Nix Flakes: https://nixos.wiki/wiki/Flakes

**Security:**
- [OWASP Top 10: 2025](https://owasp.org/Top10/)
- [OWASP Client-Side Security Risks](https://owasp.org/www-project-top-10-client-side-security-risks/)

**Accessibility:**
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
