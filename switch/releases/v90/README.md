# Switch v90

v90 revises the English dialogue for Kyotaro Saiki, Abraham ibn Woodin, and Tial
Waman Chasca on Japanese Switch update 1.0.2. The offline editorial pass covered
753 scenes, including 14,896 speeches, 217 choice captions, and 451 alternate
voice lines. The review used the DS natural-dialogue-v2 standard, preserving
Japanese meaning, speaker controls, substitutions, and native event and choice
logic. The Switch formatter handles dialogue wrapping.

The [manifest](manifest.json) identifies the 18 overlay files, the input hashes,
and the hashes of the IPS and xdelta patches. The overlay was rebuilt from
the Japanese 1.0.2 inputs and all 18 outputs matched the manifest.

## Runtime verification

- Kyotaro's opening and sailing tutorial were verified in the saved Eden
  checkpoint. Woodin's opening and fleet tutorial and Tial's opening and
  Portobelo tutorial were verified on v90. Tial received the 50,000-gold loan,
  paid 400 gold for supplies, and departed aboard Lauca.
- Woodin's Market choice opened Niyadi's trade lesson, and declining the
  Shipyard lesson opened the Shipyard menu. His native Basra ending triggered
  from the prepared save, reached the credits, and returned to the title.
- Kyotaro's and Tial's ending scenes reached the credits in Eden nightly.
  The QA build played the byte-identical release scenes from the two opening
  slots to exercise dialogue, scene transitions, and the credits. This check
  covered scene playback. It bypassed the normal campaign prerequisites.
- Eden nightly `4089cfcffd` with Vulkan and Accurate GPU rendering gave the
  better coastline and city rendering in the Woodin comparison. During v90
  testing, Eden stable 0.2.1 retained parts of the Market and Shipyard panels
  until another screen opened. Eden was the emulator used for release QA.
- The v90 build retains the v89 stat and fleet-power notice formats. The
  native Intellect labels and their call sites match the verified v89 build.
