# Icon quality and visual review ledger

Last reviewed against `main`: `0ba4b6f2acfe7a22ca8b1b3099bbbdb3a3aef7fe`

## What is verified

- The device catalog contains 146 launcher activities.
- There are 146 matching `ruby_*.xml` vector resources.
- The generated Nova app filter contains 146 mappings.
- CI checks catalog/filter consistency and parses the vector resources.
- CI accepts the two established vector formats (48dp / 28 viewport and 108dp / 108 viewport).
- The Android debug build completed successfully for the reviewed commit.

These checks establish structural integrity and buildability, not visual fidelity.

## Visual review notes

| Icon | Current assessment | Follow-up |
| --- | --- | --- |
| YouTube | Play symbol is recognizable | Check at launcher icon size |
| TikTok | Note silhouette is recognizable | Check contrast at launcher icon size |
| Telegram | Paper-plane silhouette is recognizable | Check small-size legibility |
| CapCut | Crossed-ribbon mark is recognizable | Check small-size legibility |
| Spotify | Three sound-wave arcs are recognizable | Check spacing at small size |
| ChatGPT | Knot/rosette motif is recognizable | Check line clarity at small size |
| Instagram | Camera outline is recognizable | Check contrast |
| Gmail | Envelope/M silhouette is recognizable | Check small-size legibility |
| Duolingo | Owl face is recognizable but simplified | Compare proportions with current mark |
| Google | G-like mark is present but simplified | Review geometry and color segmentation |
| Acode | Generic A/code-editor motif | Compare against the app's current identity |
| AHA Games | Warning-triangle motif does not clearly identify the app | Replace only after confirming the app's actual brand mark |
| AnkiDroid | Flashcard with recall/star motif added in PR #28 | Visual/device review pending |
| Brave | Shield and stylized face added in PR #28 | Visual/device review pending |
| Crunchyroll | Crescent/star emblem refined in PR #28 | Visual/device review pending |
| Disney+ | Streaming arch and central mark refined in PR #28 | Visual/device review pending |

## Known limitations and next checks

1. No full 146-icon contact sheet has been reviewed at actual launcher size yet.
2. Mixed vector dimensions remain: 130 resources use 48dp / 28 viewport and 16 use 108dp / 108 viewport. The validator accepts both formats; this does not prove consistent rendered size.
3. CI does not assess logo accuracy, optical centering, stroke weight, or legibility on the TECNO POVA 4.
4. Nova Launcher installation and physical-device testing remain pending.
5. Before changing uncertain marks (especially AHA Games), confirm the app's current official identity rather than guessing.

## Acceptance criteria for future visual batches

- Preserve the existing Nova component mappings.
- Keep the dark Ruby palette coherent while retaining a distinctive app glyph.
- Prefer a recognizable app-specific silhouette over a generic decorative symbol.
- Inspect the rendered result at normal launcher size, not only as XML path data.
- Record unresolved identity questions as pending instead of presenting them as completed.
