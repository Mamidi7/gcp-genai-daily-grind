---
version: alpha
name: GCP Prep Notebook
description: Interview-prep HTML design system — notebook paper aesthetic with dark mode, hard-offset shadows, and serif-mono-sans typography trio.
colors:
  # Surfaces
  paper: "#faf8f5"
  paper-2: "#f2ede6"
  paper-dark: "#1b1a18"
  paper-2-dark: "#242220"
  # Text
  ink: "#1a1410"
  ink-2: "#3d3528"
  ink-dim: "#8a7e6e"
  ink-faint: "#b8ad9a"
  ink-dark: "#f0ece9"
  ink-2-dark: "#c5bbb2"
  ink-dim-dark: "#9a9088"
  ink-faint-dark: "#6b625c"
  # Rule / Border
  rule: "#dcd0be"
  rule-dark: "#3a3430"
  # Accents
  accent: "#d94430"
  accent2: "#c93a26"
  accent-dark: "#e8704a"
  accent2-dark: "#d95a3a"
  # Semantic
  green: "#409a4e"
  green-dark: "#5bbd6b"
  blue: "#407abb"
  blue-dark: "#5b8fbd"
  yellow: "#c09030"
  yellow-dark: "#d4a84b"
  pink: "#c0406a"
  pink-dark: "#d96a8a"
  # Highlights
  highlight: "#ffe8a0"
  highlight-dark: "#7a5a3a"
  highlight-gold: "#fdebb3"
  highlight-gold-dark: "#8a7040"
  # Derived
  on-accent: "#faf8f5"
  on-green: "#faf8f5"
  on-blue: "#faf8f5"
  on-yellow: "#1a1410"
  on-pink: "#faf8f5"
typography:
  display:
    fontFamily: "Instrument Serif"
    fontSize: "58px"
    fontWeight: "400"
    lineHeight: "0.95"
    letterSpacing: "-0.025em"
  h1:
    fontFamily: "Instrument Serif"
    fontSize: "56px"
    fontWeight: "400"
    lineHeight: "1.0"
    letterSpacing: "-0.02em"
  h2:
    fontFamily: "Instrument Serif"
    fontSize: "26px"
    fontWeight: "400"
    lineHeight: "1.2"
    letterSpacing: "-0.01em"
  h3:
    fontFamily: "Inter"
    fontSize: "16px"
    fontWeight: "600"
    lineHeight: "1.3"
    letterSpacing: "0.02em"
  body:
    fontFamily: "Inter"
    fontSize: "15px"
    fontWeight: "400"
    lineHeight: "1.65"
  bodySm:
    fontFamily: "Inter"
    fontSize: "14px"
    fontWeight: "400"
    lineHeight: "1.7"
  label:
    fontFamily: "IBM Plex Mono"
    fontSize: "9px"
    fontWeight: "500"
    lineHeight: "1.2"
    letterSpacing: "0.15em"
    fontFeature: "case"
  labelMd:
    fontFamily: "IBM Plex Mono"
    fontSize: "10px"
    fontWeight: "500"
    lineHeight: "1.2"
    letterSpacing: "0.12em"
    fontFeature: "case"
  labelLg:
    fontFamily: "IBM Plex Mono"
    fontSize: "11px"
    fontWeight: "600"
    lineHeight: "1.3"
    letterSpacing: "0.08em"
    fontFeature: "case"
  monoCode:
    fontFamily: "IBM Plex Mono"
    fontSize: "13px"
    fontWeight: "400"
    lineHeight: "1.7"
  monoSm:
    fontFamily: "IBM Plex Mono"
    fontSize: "12px"
    fontWeight: "400"
    lineHeight: "1.6"
  serifItalic:
    fontFamily: "Instrument Serif"
    fontSize: "18px"
    fontWeight: "400"
    lineHeight: "1.4"
    fontStyle: "italic"
rounded:
  none: "0px"
  sm: "2px"
  md: "4px"
  lg: "6px"
  full: "9999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "20px"
  2xl: "24px"
  3xl: "32px"
  4xl: "40px"
  gutter: "24px"
  max-width: "1000px"
components:
  topbar:
    backgroundColor: "{colors.paper}"
    borderBottom: "1px solid {colors.rule}"
    padding: "10px 0"
    backdropFilter: "blur(8px)"
  concept-card:
    backgroundColor: "{colors.paper-2}"
    border: "1px solid {colors.ink}"
    padding: "{spacing.xl}"
    boxShadow: "3px 3px 0 {colors.ink}"
  concept-card-hover:
    transform: "translate(-1px, -1px)"
    boxShadow: "5px 5px 0 {colors.ink}"
  cd-card:
    backgroundColor: "{colors.paper-2}"
    border: "1px solid {colors.ink}"
    padding: "10px 18px"
    boxShadow: "3px 3px 0 {colors.ink}"
  code-block:
    backgroundColor: "{colors.paper}"
    border: "1px solid {colors.rule}"
    padding: "{spacing.lg}"
    typography: "{typography.monoCode}"
  code-block-dark:
    backgroundColor: "{colors.ink}"
    textColor: "#e8d9c0"
  def-block:
    backgroundColor: "{colors.paper}"
    borderLeft: "3px solid {colors.accent}"
    padding: "12px 16px"
  key-item:
    backgroundColor: "{colors.paper}"
    border: "1px solid {colors.rule}"
    padding: "12px"
  tab-bar:
    display: "flex"
    gap: "0"
    border: "1px solid {colors.ink}"
    backgroundColor: "{colors.paper-2}"
  tab-item:
    fontFamily: "IBM Plex Mono"
    fontSize: "10px"
    letterSpacing: "0.12em"
    textTransform: "uppercase"
    padding: "7px 16px"
    background: "transparent"
    color: "{colors.ink-dim}"
    border: "none"
    cursor: "pointer"
  tab-item-active:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  tag:
    fontFamily: "IBM Plex Mono"
    fontSize: "9px"
    letterSpacing: "0.15em"
    textTransform: "uppercase"
    padding: "2px 8px"
    border: "1px solid {colors.ink}"
    color: "{colors.ink-dim}"
  tag-blue:
    borderColor: "{colors.blue}"
    textColor: "{colors.blue}"
  tag-green:
    borderColor: "{colors.green}"
    textColor: "{colors.green}"
  tag-yellow:
    borderColor: "{colors.yellow}"
    textColor: "{colors.yellow}"
  tag-red:
    borderColor: "{colors.accent}"
    textColor: "{colors.accent}"
  btn:
    fontFamily: "IBM Plex Mono"
    fontSize: "10px"
    letterSpacing: "0.12em"
    textTransform: "uppercase"
    padding: "7px 14px"
    border: "1px solid {colors.ink}"
    background: "{colors.paper}"
    color: "{colors.ink}"
    cursor: "pointer"
    transition: "all 0.2s"
  btn-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  btn-accent:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    borderColor: "{colors.accent}"
  btn-accent-hover:
    backgroundColor: "{colors.accent2}"
  quiz-card:
    backgroundColor: "{colors.paper-2}"
    border: "2px solid {colors.ink}"
    padding: "{spacing.xl}"
  quiz-dot:
    width: "24px"
    height: "24px"
    borderRadius: "{rounded.full}"
    border: "2px solid {colors.rule}"
    background: "{colors.paper}"
    color: "{colors.ink-faint}"
    fontFamily: "IBM Plex Mono"
    fontSize: "10px"
    cursor: "pointer"
    transition: "all 0.25s"
  quiz-dot-active:
    borderColor: "{colors.accent}"
    textColor: "{colors.accent}"
    fontWeight: "600"
  quiz-dot-correct:
    backgroundColor: "{colors.green}"
    borderColor: "{colors.green}"
    textColor: "{colors.on-green}"
  quiz-dot-wrong:
    backgroundColor: "{colors.accent}"
    borderColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
  q-opt:
    background: "{colors.paper}"
    border: "1px solid {colors.rule}"
    cursor: "pointer"
    color: "{colors.ink-2}"
    transition: "all 0.2s"
  q-opt-hover:
    borderColor: "{colors.ink}"
    backgroundColor: "{colors.paper-2}"
  q-opt-correct:
    borderColor: "{colors.green}"
  q-opt-wrong:
    borderColor: "{colors.accent}"
  note:
    background: "{colors.paper}"
    border: "1px solid {colors.green}"
    padding: "12px 16px"
  note-warn:
    borderColor: "{colors.yellow}"
  note-accent:
    borderColor: "{colors.accent}"
  interview-tip:
    background: "{colors.paper}"
    border: "1px solid {colors.blue}"
    padding: "12px 16px"
  star-block:
    background: "{colors.paper}"
    borderLeft: "3px solid {colors.yellow}"
    padding: "12px 16px"
  svg-wrap:
    background: "{colors.paper}"
    border: "1px solid {colors.rule}"
    padding: "20px"
  comp-table-header:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    fontFamily: "IBM Plex Mono"
    fontSize: "9px"
    letterSpacing: "0.15em"
    textTransform: "uppercase"
    padding: "8px 12px"
    fontWeight: "400"
  comp-table-cell:
    padding: "9px 12px"
    borderBottom: "1px solid {colors.rule}"
    color: "{colors.ink-2}"
  comp-table-highlight:
    backgroundColor: "{colors.highlight-gold}"
    textColor: "{colors.ink}"
---

## Overview

The GCP Prep Notebook design system evokes the feeling of a well-loved engineering notebook — warm cream paper, sharp ink annotations, and structural clarity that comes from handwritten margin notes turned digital.

The aesthetic is **Editorial Engineering** — halfway between a printed technical journal and a modern web app. It rejects soft gradients and rounded everything in favor of hard edges, offset shadows, and a deliberate three-font hierarchy that mirrors how actual notebooks separate voice (serif headlines), body (sans prose), and annotations (mono labels).

A distinctive feature is the **dual-mode paper system**: light mode simulates fresh cream paper under daylight; dark mode switches to charcoal paper with warm ink. Both modes preserve the same structural shadows and border language.

## Colors

The palette is built around paper-and-ink logic rather than brand primaries.

- **Paper (#faf8f5):** Warm cream base. Not pure white — it has a hint of wheat to reduce eye strain during long study sessions.
- **Paper-2 (#f2ede6):** Slightly darker cream for cards and secondary surfaces. Creates depth through tonal shift, not shadow.
- **Ink (#1a1410):** Warm black — not pure #000000. It carries a brown undertone that harmonizes with the cream paper.
- **Ink-2 (#3d3528):** Secondary text. Used for body paragraphs and descriptions.
- **Ink-dim (#8a7e6e):** Tertiary text — labels, captions, metadata.
- **Ink-faint (#b8ad9a):** Ghost text — disabled states, placeholders, divider labels.
- **Rule (#dcd0be):** The notebook margin line. Used for borders, dividers, and subtle separators. Should feel like a faint pencil line, not a harsh digital border.
- **Accent (#d94430):** The red pen. Used for emphasis, errors, primary CTAs, and the single wavy underline that marks active concepts. This is the only saturated color in the core palette.
- **Green (#409a4e):** Success states, correct quiz answers, positive indicators.
- **Blue (#407abb):** Information blocks, interview tips, neutral emphasis.
- **Yellow (#c09030):** STAR answer blocks, warnings, progress markers.
- **Pink (#c0406a):** Rare accent for code syntax highlighting.
- **Highlight (#ffe8a0):** Inline code background and table row selection. Must never be used for large surfaces.

### Dark Mode

When `data-theme="dark"` is applied, every surface and ink color swaps to its dark counterpart:
- Paper becomes charcoal (#1b1a18), Paper-2 becomes slightly lighter charcoal (#242220)
- Ink becomes warm off-white (#f0ece9), maintaining the brown undertone
- Rule becomes dark brown-gray (#3a3430)
- Accent shifts to a warmer coral (#e8704a) to remain visible against dark backgrounds
- All semantic colors brighten by ~20% to maintain contrast

## Typography

Three typefaces, three jobs. Never mix them randomly — each has a structural purpose.

- **Instrument Serif** (display, h1, h2, serif-italic): The voice. Used for all headlines, hero text, and italic subheadings. It gives the interface its journal-like personality. Headlines use light weights (400) with tight tracking to feel confident, not shouty.
- **Inter** (body, h3, UI): The workhorse. Used for all body text, section labels, and interface elements. Chosen for its excellent on-screen legibility at small sizes and its neutrality that does not fight the serif headlines.
- **IBM Plex Mono** (labels, code, metadata): The annotation layer. Used exclusively for uppercase labels, code blocks, tab labels, tags, and any text that describes rather than narrates. Always uppercase with wide letter-spacing (0.08em to 0.15em) to feel like stamped or typewritten annotations.

### Scale Rules

- Display text (hero): 32–58px, Instrument Serif 400, line-height 0.95. This is intentionally tight — it creates tension.
- H1: 56px, Instrument Serif 400. Only one per page.
- H2: 26px, Instrument Serif 400. Section headers. Can have a wavy underline in accent color.
- H3: 16px, Inter 600. Subsection headers. The only sans-serif heading.
- Body: 15px, Inter 400, line-height 1.65. Generous leading for reading comfort.
- Body-sm: 14px, Inter 400. Used inside cards and compact areas.
- Labels: 9–11px, IBM Plex Mono 500, uppercase, letter-spacing 0.08–0.15em. These are not "small text" — they are a separate voice layer.
- Code: 13px, IBM Plex Mono 400, line-height 1.7. Inside bordered blocks with horizontal scroll.

## Layout

The layout follows a **centered single-column** model with a sticky topbar.

- **Max width:** 1000px centered with auto margins. Never full-bleed except for the topbar and hero.
- **Gutter:** 24px horizontal padding on desktop, 14px on mobile.
- **Section spacing:** 40px between major sections. Use 3xl (32px) for subsection breaks.
- **Grid:** Content uses single-column flow. Only key-item grids and comparison tables use multi-column layouts (`auto-fit, minmax(220px, 1fr)`).
- **Topbar:** Sticky, z-index 50, full-width. Contains brand (left) and actions (right). Border-bottom uses `rule` color. Backdrop-filter blur at 8px for glass effect over scrolling content.

### Paper Texture

The body background is never flat. It combines:
1. Two radial gradients at 15% and 85% positions (very subtle warm glow, 10–12% opacity)
2. A repeating linear gradient that creates faint horizontal lines every 28–29px (simulating notebook ruling lines at ~3% opacity)

This gives the surface depth without using any blurred shadows.

## Elevation

This system **rejects soft drop shadows**. All depth is created through **hard offset shadows** that simulate a physical object lifted slightly off a page.

- **Level 1 (cards, buttons):** `2px 2px 0 var(--ink)` — subtle lift
- **Level 2 (concept cards, cd-cards):** `3px 3px 0 var(--ink)` — standard card elevation
- **Level 3 (hover state):** `5px 5px 0 var(--ink)` with `translate(-1px, -1px)` — the card physically moves up-left as the shadow grows down-right

The shadow color is always `ink` (not a gray), which makes the shadow feel like an ink stamp rather than ambient occlusion. In dark mode, the same logic applies but the shadow is the light ink color against dark paper — creating a "glow offset" effect.

No blur-radius shadows anywhere. No box-shadow with spread. The aesthetic is print-like, not digital-glass.

## Shapes

- **Border radius:** Almost universally 0px (sharp corners). This is intentional — it reinforces the paper/document metaphor.
- **Exceptions:**
  - Quiz dots: `full` (circular)
  - Code inline highlights: `sm` (2px)
  - SVG diagram containers: `md` (4–6px) for internal elements only
- **Borders:** 1px solid `rule` for subtle separators, 1px solid `ink` for strong containers, 2px solid `ink` for quiz cards and playgrounds (these are "work areas" that need heavier definition).
- **Dividers:** Prefer border-bottom on the topbar and section headers over horizontal rules. The 2px solid `ink` underline on hero subtitles is a signature element.

## Components

### Buttons

All buttons use the label-md typography (IBM Plex Mono, 10px, uppercase, wide tracking). This makes every button feel like a stamped instruction.

- **Default button:** 1px border `ink`, paper background, ink text. Hover: ink background, paper text. This is a complete inversion — the button "fills in" on hover like a stamp pressing down.
- **Accent button:** Solid accent background, paper text, accent border. Hover: accent2 background. No inversion — accent buttons are already "pressed."
- **Primary/Playground buttons:** 2px border instead of 1px. These are inside the "work area" and need heavier visual weight.

### Cards

- **Concept card:** The primary content container. Paper-2 background, 1px ink border, 3px 3px 0 ink shadow. Contains a label (mono uppercase), a serif h4 headline, and body-sm explain text. Hover lifts to 5px shadow.
- **CD card (countdown/data):** Compact stat card. Paper-2 background, ink border, 3px shadow. Contains a large italic serif number and a mono label below.
- **Key item:** Grid cell. Paper background, rule border, no shadow. Simpler than concept cards because they appear in groups of 3–4.

### Tabs

- **Tab bar:** Flex container, no gap, 1px ink border wrapping the whole group, paper-2 background.
- **Tab item:** Mono label-md, uppercase. No border-radius. Adjacent tabs separated by 1px ink border-left. Active tab: ink background, paper text. Inactive: transparent, ink-dim text.
- This is a **segmented control** pattern, not rounded pill tabs. It should feel like a filing folder divider.

### Code Blocks

- **Block:** Paper background, rule border, 16px padding. Mono-code typography. Horizontal scroll enabled. Tab-size 2.
- **Inline:** Paper-2 background, 1px rule border, 1px 4px padding. Or highlighted with `highlight-gold` background for emphasis.
- **Dark variant:** Ink background with `#e8d9c0` text (warm cream, not pure white) for code blocks that need contrast.

### Quiz

- **Quiz card:** Paper-2 background, 2px ink border (heavier than concept cards — this is an interactive workspace).
- **Dots:** Circular indicators, 24px, rule border. Active: accent border + text. Correct: green fill. Wrong: red fill. Transition all 0.25s.
- **Options:** Paper background, rule border, flex row with letter circle. Hover: ink border + paper-2 background. Correct: green border. Wrong: red border.
- **Results:** Centered score display, large italic serif number, mono label.

### Tags

Small inline labels. Mono label typography, 1px border, 2px 8px padding. Variants: default (ink border), blue, green, yellow, red. Never filled — always outlined.

### Definition Blocks

Left border accent (3px), paper background, 12px 16px padding. Term label in mono accent uppercase. Description in body-sm. Used for "What is X?" callouts.

### Notes & Tips

- **Note:** Paper background, 1px green border. For positive guidance.
- **Note-warn:** Yellow border. For cautions.
- **Note-accent:** Red border. For critical warnings.
- **Interview tip:** Paper background, 1px blue border, tip-label in mono blue uppercase. For interview-specific callouts.
- **STAR block:** Paper background, 3px left yellow border. For behavioral answer frameworks.

### SVG / Diagrams

- **SVG wrap:** Paper background, rule border, 20px padding, overflow-x auto. Caption below in mono uppercase ink-faint.
- **Diagrams:** Use CSS variables (`var(--paper)`, `var(--ink)`, etc.) inside SVG so they automatically respect dark mode. Use `rx="6"` for internal rectangles only — the container itself is sharp.
- **Animation classes:** `.pulse` (opacity pulse), `.flow` (stroke dashoffset), `.pop` (scale + fade), `.fade` (translateY + opacity). All use CSS keyframes with cubic-bezier easing.

### Comparison Tables

- **Header:** Ink background, paper text, mono label uppercase.
- **Cells:** 9px 12px padding, rule border-bottom, ink-2 text.
- **Highlight row:** Highlight-gold background, ink text. Used to call attention to a specific comparison point.

### Interactive Toggles

- **Toggle bar:** Flex wrap, 8px gap.
- **Buttons:** Mono label, 1px rule border, paper background. Active: ink background, paper text. Hover (inactive): accent text, accent border.
- **Panels:** Hidden by default. Active panel shows paper-2 background, rule border, 14px padding.

## Animation

All motion is purposeful and print-inspired.

- **fade-up:** opacity 0→1, translateY 8px→0. Duration 0.4s, ease. Used for sections entering the viewport.
- **pop-in:** scale 0→1.1→1, opacity 0→1. Duration 0.5s, cubic-bezier(0.15, 0.75, 0.3, 1). Used for dots, badges, markers.
- **pulse-glow:** opacity 0.7→1→0.7. Duration 2s, ease-in-out, infinite. Used for active indicators in diagrams.
- **flow-right:** stroke-dashoffset 200→0. Duration 2s, linear, infinite. Used for pipeline arrows in SVGs.
- **Section reveal:** opacity 0→1, translateY 16px→0. Duration 0.5s, cubic-bezier(0.15, 0.75, 0.3, 1). Triggered by IntersectionObserver.

No parallax. No spring physics. No blur transitions. The motion should feel like pages turning and stamps pressing, not like liquid UI.

## Do's and Don'ts

### Do
- Use serif for all headlines and hero text. This is the system's personality.
- Use mono uppercase labels for any text that describes, categorizes, or annotates.
- Apply hard offset shadows (2px/3px/5px with 0 blur) to all cards and buttons.
- Maintain the paper texture background on body — never use flat white or gray.
- Use the accent red sparingly. It is the "red pen" — if everything is marked, nothing is marked.
- Ensure all SVG diagrams reference CSS variables so dark mode works automatically.
- Use 2px borders for interactive workspaces (quiz, playground) and 1px for content containers.

### Don't
- Use border-radius on cards, buttons, or tabs. Sharp corners are non-negotiable.
- Use soft Gaussian blur shadows. No `box-shadow: 0 4px 20px rgba(0,0,0,0.1)` anywhere.
- Mix more than three typefaces. The trio (Serif + Sans + Mono) is the system.
- Use pure black (#000000) or pure white (#ffffff). The palette is always warmed with brown undertones.
- Apply highlight-gold to large surfaces. It is for inline code and table rows only.
- Forget the dark mode counterpart for every color you introduce. The system is dual-mode by design.