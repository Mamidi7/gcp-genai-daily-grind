# Integrated Explainer Patterns
## Borrowed from visual-explainer + html-artifacts + Our Teaching Triad

## 1. Universal Rules (from html-artifacts)

Every HTML artifact must satisfy ALL of these:
1. **Single self-contained `.html` file** — No build step, no bundler, no npm install.
2. **Works offline** — No required network calls at view time.
3. **Mobile responsive** — `<meta name="viewport">` + layout survives narrow viewport.
4. **Real layout, not stacked headers** — Comparisons in columns, timelines drawn, diffs rendered.
5. **Readable on its own** — Title + one-paragraph TL;DR before substance.
6. **Tasteful** — Legible serif/sans body, comfortable line length (60-75ch), generous spacing, restrained color.
7. **Dark-mode-friendly** via `prefers-color-scheme: dark`.

## 2. When to Reach for HTML (from html-artifacts)

Reach for HTML when ANY is true:
- **Comparison** — Side-by-side beats stacked.
- **Spatial information** — Position carries meaning (diffs, flowcharts, timelines, before/after).
- **Interaction matters** — Sliders, toggles, live code preview.
- **Reference material** — Non-linear navigation (tabs, collapsible, jump links).
- **Color carries meaning** — Severity tags, status colors, syntax highlighting.
- **One-off editor** — User manipulates state and round-trips.
- **Reader will share it** — HTML is more likely to be read than markdown.
- **Length** — Beyond ~100 lines, HTML's layout earns its keep.

## 3. Aesthetic Palettes (from visual-explainer)

### Palette A: Blueprint (Technical)
- Deep slate/blue palette
- Monospace labels
- Subtle grid background
- Precise borders
- Use for: architecture, system design, flowcharts

### Palette B: Editorial (Refined)
- Serif headlines (Instrument Serif / Crimson Pro)
- Generous whitespace
- Muted earth tones or deep navy + gold
- Use for: long-form explanations, deep dives

### Palette C: Paper/ink (Warm)
- Warm cream `#faf7f5` background
- Terracotta/sage accents
- Informal, approachable feel
- Use for: teaching explainers, interview prep

### Palette D: IDE-inspired (Named scheme)
- Dracula, Nord, Catppuccin, Solarized, Gruvbox, One Dark, Rosé Pine
- Commit to actual palette — don't approximate
- Use for: code-heavy topics

### Forbidden (produces AI slop)
- Neon dashboard (cyan + magenta + purple on dark)
- Gradient mesh (pink/purple/cyan blobs)
- Inter font + violet/indigo accents + gradient text
- Glass morphism on everything

## 4. Font Pairings (from visual-explainer)

| Pairing | Use Case |
|---------|----------|
| DM Sans + Fira Code | Tech explainer, code-heavy |
| Instrument Serif + JetBrains Mono | Editorial, refined |
| IBM Plex Sans + IBM Plex Mono | Reliable, readable |
| Bricolage Grotesque + Fragment Mono | Bold, characterful |
| Plus Jakarta Sans + Azeret Mono | Rounded, approachable |

**Forbidden as body fonts:** Inter, Roboto, Arial, Helvetica, system-ui alone.

## 5. Our Teaching Triad (Own pattern)

Every explainer MUST include these three sections:

```
┌──────────────────────────────────────┐
│  INTERACTIVE DEMO / PLAYGROUND       │ ← TOP (above fold)
│  - Sliders, toggles, live readout    │
│  - User experiments, not reads       │
├──────────────────────────────────────┤
│  CONCEPT EXPLANATION (block-by-block) │
│  - SVG diagrams with annotations     │
│  - Code-in-Context flow              │
│  - Common Mistake + Fix              │
├──────────────────────────────────────┤
│  INTERVIEW ANSWERS (3 depths)        │
│  - 30-second answer                  │
│  - 90-second STAR answer             │
│  - 3-minute technical walkthrough    │
└──────────────────────────────────────┘
```

## 6. Mermaid Integration (from visual-explainer)

When using Mermaid in explainers:
- Always use `theme: 'base'` with custom `themeVariables`
- Always use diagram-shell container with zoom/pan controls
- Never use bare `<pre class="mermaid">`
- Center with `display: flex; justify-content: center`
- For 10+ nodes, increase fontSize to 18-20px

## 7. Round-trip Editor Pattern (from html-artifacts)

For playground/interactive sections:
- Every interactive element must have export capability
- "Copy as markdown" / "Copy as text" button
- State is in JavaScript memory, not localStorage (Claude.ai limitation)

## 8. Carve-outs (from html-artifacts)

Stay in markdown for:
- Short conversational replies
- Code-only outputs (single function/config block)
- Terminal/command-flavored answers
- Quick three-bullet summaries (scan-once-and-discard)
- Files that need clean git diffs

## 9. SVG Sizing Rules (from our html-learn-explainer skill)

| Element | Height | Width Rule | Notes |
|---------|--------|------------|-------|
| Single-line node | 44px | (chars × 8px) + 48px padding | Labels ≤ 20 chars |
| Two-line node | 56px | (chars × 8px) + 48px padding | Title + subtitle |
| Box-to-box gap | 60px | — | Between related components |
| Arrowhead gap | 10px | — | Before marker tip |

## 10. Category-Specific Templates (curated from both)

### Comparison page
- Side-by-side columns (CSS Grid, 3 columns max)
- Each option: numbered badge + title + description block + code sample + pro/con table + metric table
- Footer: recommendation box with left accent border

### Concept explainer
- Title + TL;DR paragraph before technical content
- Core insight as a single emphasized sentence
- Live interactive demo (sliders/toggles adjust diagram state)
- Comparison table (this vs naive approach)
- "Where you'll meet it" — real systems
- Glossary (inline or marginal)

### Educational playground
- Controls row: toggles/selectors + sliders/inputs + error simulators
- Output pane: live request preview + live code preview
- Status bar: color changes based on mode (green=OK, red=error)
- Copy-as-text export button
