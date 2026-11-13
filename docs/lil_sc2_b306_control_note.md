# Lil SC2 B306 river control note

V114 translates 39 records and retains two packed event payloads:

- R0028 `05 60 60 46 89 80 3E 63`, identical to SC0B320R0029,
  SC1B304R0028 and SC3B274R0027.
- R0063 `1E 63 94 46 8F 80`, native operation/state data with no prose.

R0159 has real state 97; R0081 starts with Japanese 97AC, meaning flow.
R0081 is translated as bare prose in V115 with a separate profile.
Bridge/Wade choices, upstream log bridge, detour day and sailor fatigue,
100-gold ferry and final crossing check retained. Four sheets plus one
refinement reviewed. 68 Lil tests and saved-ROM checks pass. Runtime pending.
