# Cumulative testing candidate with Abandon Ship

Use the local testing ROM `out\promotion_ready_20261110_ship_command_v1\Translation_DS_All_Routes_Abandon_Ship_20261110_candidate.nds` and its adjacent manifest. Apply `translation.xdelta` to the clean Japanese ROM with SHA-256 `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`. The expected candidate hash is `383f02b89501a23c48246e01b754957b9f7178f8e377700ad6c763f824dda4a5`. Patch SHA-256 is `dba4df0afd109e8c218d5f41ba54474b64480427e62cf0f542c0c778a2ea8d48`.

The native Assign Sailors menu now displays Abandon Ship. Six complete live caption masks match the native render. Back opens the ship confirmation, and No restores the same menu while retaining the ship. The emulator test used an isolated fleet save and set one secondary ship's crew count to zero. Hardware and confirmed abandonment remain unvisited.

The candidate preserves all 731 predecessor entries and 114 accepted layers, including Rafael's tutorials, the Market Trade-screen correction and the ASCII right-bound fix. Its own cold boot, 24 protected name getters, 67 release checks and 27 selected repository tests passed. Main V4701 awaits user cold-boot acceptance.
