# Search sailor-loss count

The Search notice **Sailors lost: 11.** now displays the count in the regular English font. The existing English and its single substitution remain intact. All five original Search callers share the same crew-loss routine and notice. The fix redirects its one number-format call. [Exact review and binding](../releases/all_routes_editorial_20261121_shore_loss_digits_candidate/verification/registered_review.json)

Paired DeSmuME runs used the same copied save, shoreline setup and temporary attack-variant selection. The before and after runs both removed 11 sailors and returned to the same sailing screen. Other Search outcomes and hardware were outside the replay. Offline checks covered 384 number-buffer cases and 12 complete, visually reviewed layouts. [Emulator comparison](../releases/all_routes_editorial_20261121_shore_loss_digits_candidate/verification/loss_notice_comparison.png)

Six startup holds, 24 protected getters and 17 focused tests passed. The clean-input patch reconstructs the candidate byte for byte. Only the four-byte ARM9 call changes. All 114 accepted layers carry forward. [Candidate and patch](../releases/all_routes_editorial_20261121_shore_loss_digits_candidate/README.md)
