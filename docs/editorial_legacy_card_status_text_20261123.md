# Legacy memory-card status text

The original status helper at `020EEFD0` combines eleven nonempty memory-card, system-data, action and result fragments. The clean and registered Sound Setup builds share the exact selector code, token pointers and terminal routine. Their format templates differ, with three substitutions for completed actions and two for progress. The native verifier matched the full formatted bytes for all 84 valid input combinations in each ROM. [Exact table and native cases](../translations/editorial_checkpoints/shared_display_20261123/legacy_card_status_text_20261123.json)

Every case passes the assembled buffer to `020EF068`, which executes a single return instruction. Preserve those strings for this verified caller. The proof is offline and covers that entry point. Keep the source and current addresses for any future caller that reaches a visible DS surface. [Related Continue warning path](editorial_continue_legacy_calls_20261115.md)
