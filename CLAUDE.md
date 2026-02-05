# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Aristoi Institute Narrative Packet** proof of concept. A narrative packet is a dense, compressed narrative artifact that readers decompress collaboratively with an AI at their own aperture, from their own perspective, to their own depth.

*The Moonstone* by Wilkie Collins (1868) is the test case because Collins structured the novel as multiple witnesses testifying about the same events — the format is latent in the source material.

## Source Material

- `src/pg155.txt` — Full text of *The Moonstone* from Project Gutenberg

## Project Log

- `LOG.md` — Running log of what was requested, delivered, and why. **Update this at the end of every session.**

## Packet Architecture (Three Layers)

**Layer 1 — World State** (target: 3,000–5,000 words)
Perspective-independent description of setting, objects, timeline, and physical facts. Should read like something between prose and stage directions — evocative but precise. Every detail must be load-bearing (constrains or enables downstream generation).

Key extraction targets:
- Geography of the Verinder house, room layouts
- The Shivering Sand and its tidal behavior
- Timeline of events on the night of the birthday dinner
- The paint on the door
- Multi-functional details (the nightgown is evidence, emotional artifact, and class marker simultaneously)

**Layer 2 — Perspective Entry Points** (target: 500–800 words each)
Named perspectives specifying: what the character knows at start, what they can perceive, what they misunderstand, and emotional register. Initial set:
- Gabriel Betteredge (warm, digressive, limited view — the natural default)
- Sergeant Cuff (cold, observational, wide-angle, emotionally detached)
- Rosanna Spearman (desperate, observant, hiding something)
- Rachel Verinder (angry, principled, knows more than she's saying)
- The Moonstone itself (experimental non-human perspective)

**Layer 3 — Hidden Narrative Logic** (secret instructions)
Authorial intent the AI follows but doesn't reveal. Examples:
- "Rosanna is in love with Franklin Blake — let this inflect all her behavior but never state it until the reader discovers it."
- "Godfrey Ablewhite is performing virtue — every generous act has a subtle wrongness."

## Character Models to Extract

For each major character, document: what they know and when they learn it, what they want, what they're hiding, and what they misinterpret.

Key characters: Gabriel Betteredge, Sergeant Cuff, Rachel Verinder, Rosanna Spearman, Franklin Blake, Godfrey Ablewhite, Ezra Jennings

## Causal Chain

Map the actual causal sequence of events (distinct from revelation order). What happened, in what order, driven by what motivations. This backbone must survive any perspective shift or parameter change.

## Seams and Handles

Deliberately mark places where the narrative doesn't resolve — interaction points where readers are meant to pull. These need a notation system.

## Playtesting Protocols

- **Basic expansion test**: Pick a perspective, expand a scene, check for Collins's voice and coherence
- **Perspective switch test**: Same events from different perspectives should be recognizable but experienced differently
- **Parameter perturbation test**: Change setting/character/context to find what's structurally essential
- **Stress test hidden layer**: Adversarial probing to ensure secrets hold
- **Compression test**: Cut world state in half, find where coherence breaks
