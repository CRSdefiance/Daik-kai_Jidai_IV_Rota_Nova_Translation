# V218 title artwork: live display and native resource review

## Result

V229 is a review iteration, **not a new ROM**. V218 remains the registered combined
candidate, SHA-256 `be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.
The preceding goal turn made progress on eight source-reviewed nonroute entries/
articles and their native identities. This turn completes additional title display,
resource-loading and source-view checks within the original graphics goal.

The actual opening draws M28 texture4 at **(0,48)** and texture5 at **(0,82)**.
The authoring composition used (0,50)/(0,84). The two-pixel difference is placement,
not a missing letter or a palette failure. Once measured placement is applied:

- All **4,941** blue “Uncharted Waters IV” foreground pixels match the source,
  including soft edges, complete initial/final letters and the Roman numeral.
- All **3,437** gold “Rota Nova” foreground pixels match, including the ornate N
  and its complete curves/edges. No source foreground is clipped at screen bounds.
- Native foreground bounds are blue **(40,49)-(216,91)** and gold
  **(37,91)-(203,143)**, inside the 256x192 upper screen.
- The **24,390** black-key padding pixels from both source textures do not paint
  opaque black over the water in the unfaded frame. This is observed color-key
  evidence, not a general GPU-alpha theorem for other resources or hardware.

Three focused blue-frame and two gold-frame comparisons cover **21,697** exact
foreground samples. In a separate uninterrupted 24,000-frame cold boot, the same
complete source foreground matches repeated displays: blue at frames800,900,
7400,7500,7600,14100,14200,20700,20800,20900; gold at900,7500,7600,14200,20800,20900.
All244 recorded PNG identities are checked. Fades remain normal movie effects;
a pale transition is not judged against the unfaded palette as a defect.

The ordinary title menu matches `/_pxl/title/title03.pxl` across **all49,152 pixels**
of the upper screen. Both logos, water/ship background, copyright and full bounds
are exact. This is stronger than a foreground-only title check.

## Seven native title resources

The original initializer registers **seven**, not six, title PXL resources. All
seven full source images were reviewed. The original image registration/cache and
view code is unchanged from clean. Each executes native registration, allocation,
resource-view construction, the scene's original virtual source-to-destination
copy, and complete file resolution. Only SDK open/read/seek/close is bridged to the
exact current ROM's data.

| Resource | Header extent | Reviewed content |
|---|---|---|
| title00 | 256x192 | Original ship/sky/water background; retain. |
| title01 | 256x13 | Existing English copyright; preserve. |
| title02 | 256x29 | Existing English START/touch instruction; preserve. |
| title03 | 256x192 | Complete English menu title over ship/sky; live full-screen match. |
| title04 | 256x192 | Original ocean/light background; retain. |
| title05 | 256x192 | Alternate complete English title over ocean; loading/view-copy verified. |
| title06 | 256x29 | Existing English A/touch-to-skip instruction; preserve. |

Complete headers, palettes and indices match the saved ROM in every native case.
Constructors, virtual copies, stack/register returns and both view-buffer guards
pass. No source header, owner, cache pointer or dimensions are substituted.

The resource views retain zero optional crop dimensions. An early verifier wrongly
treated those lazy fields as populated destination extents. Virtual slot+8 is a
view constructor, not a size getter; that assumption was also rejected. The final
check executes the actual virtual copy at slot+12 and verifies its complete source
resolution. Header dimensions and zero crop parameters are recorded separately;
an unobserved physical crop is not inferred from this fixture.

## Limits and remaining work

No full-screen title05 match appeared in the 24,000-frame no-input captures. The
standalone `/_pxl/logo.pxl` likewise is not established as the displayed source by
this test. No global “unused” claim follows from these observations or a negative
literal-reference search. Their actual alternate parents/display cases remain
separate. Native title05 loading/view copying is now proved, while its physical
display and alpha/crop composition remain open.

The dynamic background changes while the observed movie logos remain complete.
Indexed edge preblending is still an authoring approximation; the live source-pixel
match does not turn the estimated matte into a recovered original alpha channel.
The review does not prove every intermediate fade/reveal frame, all other movie
assets, every device or broad gameplay acceptance.

Four Online bodies, confirmed-name integration, raw/embedded/environmental
consumers, source-fidelity questions and final combined ROM/patch/gameplay remain
within the full goal. It stays active and incomplete. At completion, revisit the
older record-based checks as requested.

## Evidence

- `scripts/verify_title_display_v229.py` (Ruff passes).
- `work/analysis/graphics_review_v229/title_native_proof.json`.
- `work/analysis/graphics_review_v229/all_title_sources.png` and review sheets.
- `work/emulation_v193/graphics_review_v229/opening/`: focused unfaded captures.
- `work/emulation_v193/graphics_review_v229/full_movie/`: 24,000 frames, no input,
  savestate or RAM injection; read-only final RAM export.
- Existing V218 ordinary gameplay `no_target_v218/frame_001100_cold_boot.png`:
  exact menu-frame comparison, with its capture report and PNG identities checked.

The core is pinned DeSmuME git95b4d79, DLL SHA-256
`42160dbfef89adfb3cfd975070a3047d8ad0979cead55607ebdfd3b931046c2b`,
software rendering at native256x384, interpreter, one core, English firmware,
external BIOS disabled. All capture callback-error lists are empty. These are
emulator results, not physical-device verification or user candidate acceptance.

## Later physical display evidence

[V238](alternate_title_display_v238.md) identifies title05 in Extras/About Extras
and verifies its complete screen pixels and normal back navigation. The historical
no-input observation above remains accurate; standalone logo usage remains open.
