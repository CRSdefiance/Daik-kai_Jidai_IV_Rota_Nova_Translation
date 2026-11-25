"""Revisit item-advice line wrapping across four related catalog groups."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import register_shore_loss_digits_20261121 as parent
from scripts import review_item_production_advice_v1 as advice
from scripts import stage_bubble_portrait_wraps_20261120 as portrait
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.source_locked_derivation_v5118 import checked_text


base, batch = parent.base, parent.batch
ARM, COMMON, CLEAN = portrait.ARM, portrait.COMMON, portrait.CLEAN
ROOT = Path('work/item_advice_phrase_wraps_20261121/staged_v2')
ROM, PROOF = ROOT / 'Item_Advice_Phrase_Wraps_STAGED.nds', ROOT / 'staged.json'
PATCH, REBUILT = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
CHECKPOINTS = parent.stage.CHECKPOINTS
TRIAGE = CHECKPOINTS / 'shared_ascii_early_break_triage_20261121_v4.json'
CONTEXTS = tuple(CHECKPOINTS / f'{stem}.json' for stem in (
    'item_production_advice_context_v3', 'crew_equipment_advice_context_v2',
    'figurehead_navigation_gift_advice_context_v2', 'proof_and_relic_advice_context_v3'))
IDS = tuple(n for a, b in ((3046, 3051), (3128, 3139), (3147, 3159), (3163, 3173), (3188, 3194))
            for n in range(a, b + 1))
LEADS = {3047, 3129, 3131, 3136, 3147, 3148, 3152, 3164, 3171, 3192}
EDITS = {
    3047: ("In Africa and East Asia, glass is prized.", ["In Africa and East Asia,","glass is prized."],
           "Keep both markets and the adviser’s appraisal in a single sentence with the locations together."),
    3048: ("Silk has long been a mainstay of East Asian trade.", ["Silk has long been a mainstay","of East Asian trade."],
           "Keep silk's longstanding place in East Asian trade and remove the break between “one” and “of.”"),
    3129: ("Any shipwright would be glad to have a saw this sharp.", ["Any shipwright would be glad to have","a saw this sharp."],
           "Admiration for the saw’s exceptional edge leads directly to its value for a shipwright."),
    3131: ("An edge like this does wonders for a shipwright.", ["An edge like this does wonders","for a shipwright."],
           "The plane’s cutting edge is a practical advantage for the shipwright. Let the opening thought run without a false pause."),
    3136: ("Put on a cook's apron. Somehow, you feel like you could make a fine meal.", ["Put on a cook's apron.","Somehow, you feel like","you could make a fine meal."],
           "The apron gives the wearer an amusing feeling of confidence. Keep the meal as something imagined."),
    3147: ("The whole fleet should go faster. Fit it to any ship.", ["The whole fleet should go faster.","Fit it to any ship."],
           "State the qualified fleetwide effect, then give the freedom to fit it to any ship."),
    3148: ("They say hunger sets in more slowly on a ship fitted with this.", ["They say hunger sets in more slowly","on a ship fitted with this."],
           "Keep the reported effect and restrict it to sailors on the fitted ship."),
    3152: ("Fit it to any ship in the fleet. They say we'll all be able to spot things farther away.", ["Fit it to any ship in the fleet.","They say we'll all be able to","spot things farther away."],
           "Retain the choice of ship and the reported increase in spotting range for the whole fleet."),
    3164: ("I imagine art from the East would intrigue people in Western Europe.", ["art from the East","intrigue people in Western Europe."],
           "Keep the adviser’s speculation and the implied curiosity about unfamiliar art."),
    3169: ("The Mediterranean is known for the finest stained glass. Someone from there should appreciate this.", ["The Mediterranean is known for","the finest stained glass.","Someone from there","should appreciate this."],
           "Retain the appraisal and the regional gift clue. Keep the description of the glass together."),
    3171: ("I recall a story I heard in a tavern in some Indian Ocean town. A woman was learning to dance.", ["I recall a story I heard in a tavern","in some Indian Ocean town.","A woman was learning to dance."],
           "Make the tavern the place where the adviser heard the story. The woman’s location remains unspecified."),
    3188: ("It marks the site of the North Sea's Proof of Conquest.", ["It marks the site of the","North Sea's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
    3189: ("It marks the site of the Mediterranean's Proof of Conquest.", ["It marks the site of the","Mediterranean's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
    3190: ("It marks the site of Africa's Proof of Conquest.", ["It marks the site of","Africa's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
    3191: ("It marks the site of the Indian Ocean's Proof of Conquest.", ["It marks the site of the","Indian Ocean's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
    3192: ("It marks the site of Southeast Asia's Proof of Conquest.", ["It marks the site of","Southeast Asia's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
    3193: ("It marks the site of East Asia's Proof of Conquest.", ["It marks the site of","East Asia's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
    3194: ("It marks the site of the New World's Proof of Conquest.", ["It marks the site of the","New World's Proof of Conquest."],
           "Match the other completed maps and keep the region and its Proof of Conquest together. The map marks the location."),
}
RETAINED = {
    3046: 'The advice offers a possibility and leaves the potential new product unidentified.',
    3049: 'Both regions fit together. “Room to grow” is a natural way to describe the industry’s potential.',
    3050: 'The tentative forecast keeps East Asia as another possible source.',
    3051: 'The adviser attributes the observation to something heard and keeps the point about unusual remedies.',
    3128: 'The three rows preserve both the tentative assessment and the extreme focus the arrow inspires.',
    3130: 'The appreciative exclamation leads naturally to a shipwright wanting the sharp chisel.',
    3132: 'The measured appraisal preserves the older medical arts and their achievement.',
    3133: 'The plain statement preserves anatomical knowledge as the basis of medical practice.',
    3134: 'The skill of Islamic medicine remains a reported observation from the adviser.',
    3135: 'The admiring pause leads into the idea of a cook’s ideal pot.',
    3137: 'The adviser recognizes difficult work and hopes the item can make it easier.',
    3138: 'The spoken compliment leads into the practical benefit and preserves the tentative claim.',
    3139: 'The understated opening suits the adviser and preserves the missionaries’ admiration.',
    3149: 'Two complete statements distinguish the uncertain effect from a choice of ship.',
    3150: 'The recommendation preserves which ship matters to the player and avoids choosing one for them.',
    3151: 'The command restates the ship-selection criterion as the strongest guns.',
    3153: 'The advice preserves the choice of ship and the two tentative benefits.',
    3154: 'The hesitation fits a warning that the mounting is permanent.',
    3155: 'The recommendation to choose a ship with more sailors precedes the attributed boarding benefit.',
    3156: 'The line preserves the religious reference and qualifies the possible protection from illness.',
    3157: 'The short observation gives the tool’s practical use and names the Surveyor role.',
    3158: 'The concise appraisal names the original role and characterizes the sextant as basic equipment.',
    3159: 'The adviser gives one clear recommendation and retains both kinds of discovery.',
    3163: 'The practical requirement and the attributed Northern European gift clue both remain explicit.',
    3165: 'The adviser describes how Arabian clothing looks to Europeans without changing the cultural perspective.',
    3166: 'The admiration for the poem leads into the region’s romantic view of ancient Greece.',
    3167: 'The possibility that a person raised around these ruins might be interested is stated without a guarantee.',
    3168: 'The four separate thoughts reflect the statue’s broad familiarity, appeal and the adviser’s admiration.',
    3170: 'The recollection keeps the encounter in China and the girl’s strong interest.',
    3172: 'The story retains the fleet, the destination and the distinctly reported explanation of jade’s significance.',
    3173: 'The line preserves the qualified observation about Indian classics and Southeast Asia.',
}


def main():
    assert not PROOF.exists()
    release, ledger = map(base.load, (parent.RELEASE, base.LEDGER))
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    runtime = portrait.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    arm, common = runtime.arm, runtime.common
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    ja = portrait.common_message_entries(clean.read_file(COMMON), clean_arm)
    en = portrait.owned_entries(common, arm, sha256(arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET]).hexdigest())

    notes = {}
    for path in CONTEXTS:
        doc = base.load(path)
        assert doc['source_ROM_sha256'] == release['clean_input_sha256']
        notes.update({r['message_ID']: (r, path) for r in doc['records']})
    assert set(IDS) == EDITS.keys() | RETAINED.keys() and EDITS.keys().isdisjoint(RETAINED)
    triage = base.load(TRIAGE)
    assert triage['candidate_sha256'] == release['candidate_sha256']
    flagged = {r['message_ID']: r for r in triage['records']}
    assert flagged.keys() & set(IDS) == LEADS
    credited = {(r['file_path'], r['id']) for r in ledger[base.CONTEXT]['integrated_record_keys']}
    rows = {}
    for n in IDS:
        old, installed, (prior, path) = ja[n], en[n], notes[n]
        assert (COMMON, prior['id']) in credited and old.text.hex() == prior['source_hex']
        assert prior['item_ID'] == n - advice.FIRST and prior['original_substitutions'] == []
        assert b'%' not in old.text and b'%' not in installed.text
        if n in flagged:
            assert old.text.hex() == flagged[n]['clean_hex'] and installed.text.hex() == flagged[n]['current_hex']
            assert portrait.reference(old) == flagged[n]['clean_reference'] and portrait.reference(installed) == flagged[n]['current_reference']
        old_english = portrait.unwrapped(installed.text)
        assert old_english == prior['english'], (n, old_english, prior['english'])
        english, phrases, note = EDITS[n] if n in EDITS else (old_english, (), RETAINED[n])
        rows[n] = dict(id=prior['id'], file_path=COMMON, message_ID=n, speaker=prior['speaker'], context=prior['context'],
                       item_ID=prior['item_ID'], item_name=prior['item_name'], related_item_description=prior['related_item_description'],
                       clean_Japanese=old.text.decode('cp932'), source_meaning=prior['source_meaning'],
                       source_hex=old.text.hex(), current_hex=installed.text.hex(),
                       source_reference=portrait.reference(old), current_reference=portrait.reference(installed),
                       previous_English=old_english, english=english, localization_note=note, protected_phrases=phrases,
                       original_substitution_count=0, prior_context=str(path), review=dict.fromkeys(portrait.GATES, True),
                       decision='revision' if english != old_english else 'wrap revision' if n in EDITS else 'retention')

    wrap = FunctionType(portrait.compile_layouts.__code__, portrait.compile_layouts.__globals__ |
                        {'PHRASES': {n: phrases for n, (_, phrases, _) in EDITS.items() if phrases}})
    changes = wrap({n: rows[n] for n in EDITS})
    for n, text in changes.items():
        assert en[n].text != text, n
    deployed, rebound, allocation = owned_deployment(common, arm, en, changes)
    ctx = portrait.with_components(runtime, arm, deployed)
    # The historical helper's total is local to 24 records. Retain its branch, name and roster assertions.
    source = checked_text(getsource(advice.bind_advice_callers), {'len(cases) == 144': 'len(cases) == 6 * len(IDS)'})
    env = vars(advice) | {'IDS': IDS}
    exec(compile(source, __file__ + '::six-advice-selector-branches', 'exec'), env)
    selectors = env['bind_advice_callers'](clean_arm, ctx)

    pending = base.load(parent.PENDING)['records']
    shifted_indices = {}
    for row in pending:
        n = row['message_ID']
        before, after = row['current_reference'], portrait.reference(rebound[n])
        assert portrait.reference(en[n]) == before and rebound[n].text.hex() == row['current_hex']
        assert before | {'record_index': after['record_index']} == after
        if before != after:
            shifted_indices[n] = dict(before=before, after=after)
    assert set(shifted_indices) == set(range(3289, 3294))

    painter, _, font = portrait.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    pages = []
    for n, row in rows.items():
        payload = rebound[n].text
        group = dict(consumer=advice.DISPATCH, table=n, original_role_argument=None)
        rendered, proofs = [], []
        for actor in advice.ADVISERS:
            native = portrait.portrait_case(ctx, row, group, payload, actor)
            display = native.pop('display')
            lines = [line.strip() for line in display.decode('ascii').splitlines()]
            assert 1 <= len(lines) <= 4 and portrait.unwrapped(display) == row['english']
            assert all(any(phrase in line for line in lines) for phrase in row['protected_phrases'])
            ink, glyphs = portrait.render_portrait(painter, arm, kanji, display)
            codes = [g['code'] for g in glyphs]
            assert codes == portrait.glyph_codes(display)
            assert codes[0] == ord(row['english'][0]) and codes[-1] == ord(row['english'][-1])
            rendered.append((display, lines, ink))
            proofs.append(dict(adviser_ID=actor, glyph_count=len(codes), **native))
        display, lines, ink = rendered[0]
        assert (display, lines, ink) == rendered[1]
        row.update(staged_hex=payload.hex(), staged_reference=portrait.reference(rebound[n]), visible_lines=lines,
                   display_hex=display.hex(), expected_pages=1, ink_sha256=sha256(ink).hexdigest(), adviser_proofs=proofs)
        if n in changes:
            print(n, lines, flush=True)
            pages.append((f'{n}  {row["item_name"]}', ink))

    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON, deployed)
    target = bytes(image.rom.save())
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == target
    else:
        ROM.write_bytes(target)
    if not PATCH.exists():
        make_xdelta(CLEAN, ROM, PATCH)
    if not REBUILT.exists():
        apply_xdelta(CLEAN, PATCH, REBUILT)
    assert REBUILT.read_bytes() == target
    proof = dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
                 clean_input_sha256=release['clean_input_sha256'], stored_COMMON_sha256=batch.digest(deployed),
                 target_COMMON_sha256=batch.digest(deployed), target_ARM9_sha256=batch.digest(arm),
                 research_ROM_sha256=base.digest(ROM), research_ARM9_sha256=batch.digest(arm),
                 allocation=allocation, original_selector_cases=selectors, native_font=font,
                 parent_inverse=True, clean_reconstruction_exact=True, patch_sha256=base.digest(PATCH),
                 translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                 review_gates=list(portrait.GATES), records=list(rows.values()), sheets=portrait.portrait_sheets(ROOT, pages),
                 source_receipts={str(f): base.digest(f) for f in (*CONTEXTS, TRIAGE)},
                 unchanged_pending_records=len(pending), shifted_pending_record_indices=shifted_indices, new_contextual_credit=0)
    validate_natural_dialogue_batch(proof)
    base.save(PROOF, proof)


if __name__ == '__main__':
    main()

