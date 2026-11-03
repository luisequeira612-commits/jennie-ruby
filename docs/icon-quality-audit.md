# Icon quality and visual review ledger

Last reviewed against `main` after PR #38 (2026-11-02).

## Verified structure and delivery

- The TECNO POVA 4 device catalog contains 146 launcher activities.
- The generated Nova app filter contains 146 mappings, synchronized from `device-app-catalog.tsv`.
- The 146 app icons have matching `ruby_*.xml` drawable resources; the separate JENNIE RUBY application launcher icon is not part of that catalog.
- CI validates vector XML structure, generated app-filter consistency, and builds the Android debug APK.
- CI accepts the two established app-icon vector formats (48dp / 28 viewport and 108dp / 108 viewport).
- The debug APK was installed on a TECNO POVA 4, and JENNIE RUBY was successfully discovered and applied in Nova Launcher (user-confirmed).
- PR #38 adds a separate Ruby monogram launcher icon for the JENNIE RUBY app itself.

Structural checks and a successful build do not establish visual fidelity for every icon.

## Recorded design refinements

The following changes are present in merged work. They are design refinements, not a claim of pixel-identical reproduction of proprietary marks.

| Icon(s) | Recorded change | Remaining check |
| --- | --- | --- |
| AnkiDroid, Brave, Crunchyroll, Disney+ | Refined app-specific symbols in PR #28 | Actual launcher-size review |
| AHA Games | Replaced the warning triangle with a game-controller motif in PR #30 | Confirm recognition at normal size |
| Acode | Replaced generic A/editor glyph with a directional mark in PR #31 | Compare with current app identity |
| Google | Refined segmented G mark in PR #32 | Check color segmentation at small size |
| Duolingo | Owl silhouette refined in PRs #32 and #37 | Confirm it reads as an owl, not a pig-like face, on device |
| Mnet Plus, MT Manager, MYTECNO | Distinct app-specific motifs in PR #35 | Review the three icons side by side |
| MT Manager+ | Connectivity/signal motif with plus badge in PR #36 | Check small-size legibility |
| JENNIE RUBY app | Separate dark Ruby monogram launcher icon in PR #38 | User/device visual review |

Earlier review notes for these icons are superseded by the merged refinements above.

## Open visual and mapping work

1. A complete 146-icon contact sheet has not yet been reviewed at actual launcher size.
2. Mixed app-icon vector dimensions remain: 130 resources use 48dp / 28 viewport and 16 use 108dp / 108 viewport. CI accepts both formats; consistent optical sizing is not yet proven.
3. CI does not assess logo accuracy, optical centering, stroke weight, contrast, or legibility on the TECNO POVA 4.
4. The device test confirms installation and theme application, but not the correctness of every individual icon.
5. The catalog includes the Nova Launcher app entry (`com.teslacoilsw.launcher/com.teslacoilsw.launcher.NovaShortcutHandler`). This is not the same as a confirmed Nova Settings activity. Do not add a Nova Settings mapping until its exact launcher component is verified on the device.
6. Wallpaper and KWGT widgets are separate theme deliverables; they are not installed by the icon-pack APK.

## Acceptance criteria for future visual batches

- Preserve existing Nova component mappings unless a device-verified correction is required.
- Keep the dark Ruby palette coherent while retaining a distinctive app glyph.
- Prefer recognizable app-specific silhouettes over generic decorative symbols.
- Inspect rendered icons at normal launcher size, not only as XML path data.
- Compare visually similar icons side by side.
- Record unresolved identity or component questions as pending instead of presenting them as completed.
