# Sound Setup Sirens title registered

Sound Setup now displays **Sirens** at the original effect index 32 between Dolphin and the rain effect. This uses the name already established in the sailing condition and the encounter. The original effect ID, volume logic, title position and controls carry forward. [Exact source and current references](../releases/all_routes_editorial_20261120_sound_sirens_candidate/verification/registered_review.json)

The native selector has 59 entries. The earlier 57-slot storage inventory included Replay, which this selector does not point to. It omitted Cancel, Message and Sirens. Cancel and Message already had English labels. The new offline check executed the original painter for all 59 entries and checked Up and Down at every index against the game’s effect table. [Selector and glyph evidence](../releases/all_routes_editorial_20261120_sound_sirens_candidate/verification/selector_verification.json)

The paired ordinary title-menu replays matched the complete rendered text at every selectable effect, including wraparound and the exit to title. **Sirens** is the only visual difference. The replay issued Play at Sirens. Audio output was outside the comparison, and the earlier tested volume path continues to account for the observed Sound Setup controls. Potential other uses of the stored COMMON 102, 330 and 331 remain open. [Before and after](../releases/all_routes_editorial_20261120_sound_sirens_candidate/verification/sirens_gameplay.png)

Six startup holds, 24 protected name getters and 30 focused tests passed. Two optional legacy tests skipped. The clean-input patch rebuilds the cumulative candidate byte for byte. [Candidate and patch](../releases/all_routes_editorial_20261120_sound_sirens_candidate/README.md)
