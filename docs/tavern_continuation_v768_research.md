# V768 research: Tavern costs, rounds, treasures and fleet warnings

This is source and presentation research for COMMON851–882. No V768 playable ROM
or patch has been produced. V767 remains the current experimental combined ROM;
the canonical baseline and separate unfinished graphics audit are unchanged.

## Editorial review

All32 clean Japanese messages and nearby847–890 selections were compared with the
current English and actual native argument providers.28 drafts revise awkward or
incorrect English; four retain their wording:865,871,872,874.
The manuscript is `translations/tavern_continuation_editorial_manuscript_v2.json`.
All prose is one paragraph under natural-dialogue-v2, without authored alignment
or line breaks. Formatting approval remains false pending runtime and scene gates.

- 877 addresses the player as Sir/Ma'am; it does not ask if they know a person
  called Sir.878 receives an organization followed by that player vocative; the
  fleet is pursuing the player. Draft878 puts the vocative first and explicitly
  requires permutation[1,0] at the two original argument moves58070/58078.
- 875 receives the current admiral's surname.869 also receives that surname.
  871/872 still pass both surname and a gendered address; their established English
  intentionally prints only the surname. Do not invent a rank or treat the unused
  address as a lost name. The earlier V382872 localization is retained.
- 863/870 receive item regions, not towns. The original names are 北海,地中海,
  アフリカ,インド洋,東南アジア,東アジア,新大陸. Private dialogue phrases should read
  the North Sea,the Mediterranean,Africa,the Indian Ocean,Southeast Asia,East Asia,
  the New World. Short map/UI labels stay unchanged. Calling the named object a
  rare item/treasure avoids a singular article directly before plural item names.
- 852–858 restore spoken cost estimates and approval questions with appropriate
  voice. Amounts retain the original fullwidth native output; gold works for every
  amount. Familiar barkeep addresses in859–867 do not establish family relations.
- 879/880 describe a destination;881/882 describe an anchored fleet. Preserve the
  hearsay and formal/casual distinction. Organization names come from virtual+8,
  not surnames or guessed countries, and are not shortened to hide a repeated Fleet.

## Source and caller evidence

`work/analysis/tavern_continuation_v768/native_context_partial.json` records2591
original provider fragments,40 actual officer voice selections plus the null
fallback,and eight supplied four-captain round-table selections. The source code
spans are exact to clean Japanese. The initial source probe caught an incorrect
host assumption: supplied route changes can alter the native company-name getter.
Expected warning names now come from that getter after each supplied route change.
These supplied route states are not claimed to be normally earned game worlds.

`native_context_complete.json` adds7200 original source fleet-provider cases:
20 organizations ×90 towns ×two formal/casual modes ×destination/docked paths.
The paths use destination byte3F and original34674 dock getter/byte3C respectively;
the copied CPU-only dock fixture clears state bit08 in byte50. Original price
provider58350,role3/table02118400,actor selection,fullwidth numeric value,va_list,
and YesNo core54058/return53D24 are also verified. Only message loader5528C is
stubbed to return the exact selected current COMMON text before the original
wrapper reaches the core. These are native fragment tests,not activated scenes.

## Presentation evidence

`work/analysis/tavern_continuation_layout_v768_v2/verification.json` records14282
original printf/literal-formatter cases across all32 messages. Inputs cover
20 organization names and90 towns,218 item names with all seven region phrases,
both player vocatives,actual surname output and explicit rename length/parity
boundaries,and original amounts computed from all90 towns. Numeric boundary
fixtures include1 and2147483647; arbitrary item/region cross-products are width
tests and are not claimed valid world states.

Every case preserves complete printf output and words,buffer guards and the
callee-saved ABI,and passes four-row/35-byte bounds,weak-ending and short-tail
checks.115 complete228×64 font planes match independently decoded native glyphs;
all ten initial preview sheets were visually inspected. The second draft rewords seven fleet sentences to avoid Bergstrom Fleet's fleet without shortening any organization name. Its40 changed full planes were visually inspected on sheets00,06,07,08,09;the other75 planes are hash-identical to previously inspected previews. The initial draft and its113 font planes are preserved as superseded research. Fresh initialized CPU instances
are used every64 cases. These tests call the existing literal formatter directly;
they do not certify the future dispatcher,private region provider or actual scenes.

## Remaining work

1. Integrate an exactly scoped dispatcher for the new direct,queued cost and
   four-captain round callers,and the private full-region provider and878 reorder.
2. Prove source ownership and preservation without growing staged payloads,pools,
   sections or caches. Only16+8 bytes remain free in the previously inventoried
   village slots. The old Yard dispatch tail is still reached by Port fallback
   (`02132020 →02147C20 →02147E58`); it is not unused storage. The older ITCM
   paragraph formatter is also shared by country/market and other consumers.
3. Verify every inherited selector/provider,full native copies,registered combined
   integration and an exact clean-input patch.
4. Run targeted cold-boot scenes,complete visible glyph checks,dismissal and return,
   native state comparisons and New Game controls; archive final screenshots on E.

Completed editorial coverage remains198 messages (147 revised/51 retained).
Source/prose coverage is233,with35 active drafts including750–752. No draft is
counted as integrated or fully completed. The full editorial goal remains active.
