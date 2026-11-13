# Editorial testing scope - user clarification V1870

The user's clarification governs the editorial goal and the next-thread handoff.

- Line-by-line review means offline comparison of every translation with clean Japanese and neighboring dialogue. It does not require naturally playing every scene or completing every route in-game.
- Prioritize capturing town/shared dialogue and random scenes as broadly as practical. Authorized isolated fixtures and cheats may speed access; disclose their scope rather than treating them as naturally earned progression.
- Build reusable, source-bound formatting and display rules for each native renderer/consumer: full control preambles, runtime substitutions, wrapping, leading/trailing characters, bounds, pagination and transitions. Apply these validated rules and automated native/preview checks across the prose being reviewed.
- Use targeted actual gameplay samples to establish and check those rules, especially distinct panel types, speaker/control types, substitutions, long text, page transitions and known regressions. Expand testing to resolve a concrete risk; do not require an individual live visit to every dialogue record or conditional story branch.
- When reviewing storylines, use the established rules and offline per-record checks, with representative gameplay samples and focused tests when evidence exposes a new case. Record which records were actually observed, which received automated/offline checks, and any unresolved risk accurately.
- Completion still requires full editorial coverage, faithful natural English, passing formatting/release checks, a registered cumulative ROM, an exact clean-input patch and documented representative gameplay evidence. It does not require an exhaustive natural playthrough. Graphics remains separate unfinished work.

This is consistent with docs/dialogue_delegation_protocol.md's representative deep-game sampling policy. For Stockholm, the 36 actual speeches, all51 native/font cases and source-bound control/reference evidence should be evaluated together. The15 unvisited conditional speeches are not automatically a blocker; require more live sampling only for a concrete unresolved presentation/control risk. Final reference approval, guarded production integration, patch reconstruction and required startup checks remain pending.
