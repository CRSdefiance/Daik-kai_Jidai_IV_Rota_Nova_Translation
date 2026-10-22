# DS sailing and crew-help review

Added 2026-10-12. Sources are local reviewed game-help translations, not PSP/HD manuals or a new full playthrough.

- `translations/navigation_help_manuscript_v2.json`: topics 76, 83, 101, 104; Auto Move requirements, normal sailing/sails/touch, and Route Map.
- `translations/general_help_manuscript_v2.json`: topic 103; X shared commands.
- `translations/sailing_mode_panels_manuscript_v1.json`: information/search/war panels; Y context and A search; unsuccessful search fatigue +3, desertion/animal risks, ally-war restriction.
- `translations/interface_help_manuscript_v1.json`: topic 139; crew allocation and minimum crew effects.
- `translations/crew_help_manuscript_v1.json`: topics 111–126; room requirements and stated effects.

Skill aliases are normalized to current guide labels: Health/vitality -> Vigor, Social/persuasion -> Speech, Tactics/schemes -> Guile. Source-meaning fields for 116, 118, 121, 126 were inspected to avoid mistaking vitality for temporary Health. The guide preserves an alias note for differing help wording.

Requirements are quoted as DS-help statements, not newly executed eligibility probes. No exact prevention percentage, repair/cure time, search success rate, or visibility range is invented. Individual companion restrictions remain relevant. Boarding Leader/Gunner eligibility and all disease remedies still need their own evidence.

The generator for reference sections must preserve the new 07.7–07.10 player instructions rather than regenerate the old placeholder. No ROM/save/screenshot/translation records changed; full guide remains incomplete.
