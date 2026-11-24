# Authored fleet-order docking lookup

In a story order with a zero order byte, the game copies the active captain's docking byte into the destination field at `0x02035A28`. The selector first calls `0x02034674`. When that getter reports 115, the selector reads the raw docking byte at fleet offset `0x3C`. That second read matters when the fleet flag makes the getter return 115. It also preserves a genuine saved 115 value. The clean assembler, installed assembler, and registered startup memory match across the checked instructions and literals. [Exact code and values](../translations/editorial_checkpoints/shared_display_20261123/fleet_authored_fallback_20261124.json)

An isolated native run exercised all 256 byte values with the flag clear and set. The writer preserved surrounding bytes in all 512 cases. The two earlier ordinary save holds supply dock 7 in Copenhagen and dock 58 in Nagasaki. Applying the native branch offline to those exact snapshots yields both saved docking bytes. The story commands remain unvisited in gameplay.

The marker scan matched 11 usual-format zero-order candidates in the clean and installed retail story archives. The report records both offsets where relocation moved a match. This narrows the remaining question to which dock values actual story and alternate saved inputs can supply. Direct headquarters inputs and command reachability remain open.
