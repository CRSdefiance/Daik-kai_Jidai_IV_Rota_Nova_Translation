# Clifford’s declaration response

The final question now reads “they can beat me?” on a single row. Clifford’s words, speaker, and three-row layout are preserved. The original portrait renderer passed all eight declaration responses. All seven alternatives matched their previous text and pixels. [Source and registered review](../releases/all_routes_editorial_20261121_clifford_declaration_wrap_candidate/verification/registered_review.json)

The paired emulator run verified all the letters in the revised line and the two surrounding rows. The original controls, 44 text callbacks, and 21 other framebuffers matched, including the duel and victory rewards. The copied save used the documented 40-byte fleet-position setup. The archived attack prompts remain open. [Revised gameplay frame](../releases/all_routes_editorial_20261121_clifford_declaration_wrap_candidate/verification/frame_006120_cold_boot.png)

The candidate passed the startup and text checks. The clean-input patch reconstructs it byte for byte. [Testing ROM and patch](../releases/all_routes_editorial_20261121_clifford_declaration_wrap_candidate/README.md)

The Drive copy was updated in place on November 21, 2026 at 14:38 UTC. The authenticated 60,555,016-byte readback matched the registered SHA-256 `e113a54bcbd090e223c261dbd4d6c17daf30128caa8532709c902c4b81418605`. It is the folder’s only `.nds`. [Latest Build on Drive](https://drive.google.com/file/d/1vM8IXRtSIMvFR4F-TR3oPLtcuhFobGwa/view?usp=drivesdk)

Checkpoint cleanup removed 12 test files totaling 61,092,890 bytes. They included the duplicate patch reconstruction, two copied emulator saves, and unit-test scratch files. The staged and registered candidates and gameplay evidence remain available. [Cleanup receipt](../work/clifford_declaration_wrap_20261121/checkpoint_cleanup.json)
