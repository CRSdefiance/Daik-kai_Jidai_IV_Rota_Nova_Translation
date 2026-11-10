"""Qualify Lil B299–B311 terminology and prepare the final prose decisions."""
from collections import Counter
from pathlib import Path
import struct

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import string
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.extract_editorial_current_scope_reuse_v1 import qualify_scope
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT = Path('work/Lil278_B299_B311_clean_20261110')
PROSE = Path('translations/lil_B299_B311_contextual_review_v1.json')
NAMES = Path('translations/lil_B299_B311_scoped_names_v1.json')
NAME_REASONS = {
    2: 'Retain Lil Argot in both consumers and Lil in the FI address. Her panic, bravado and reluctant politeness remain distinct reactions in these exchanges.',
    9: 'Retain Camille Overijssel and full Camille Marinus Overijssel. He reassures Lil, leads the party during her flight and helps in the rescue without a newly inferred relationship.',
    95: 'Retain Patron for the tavern customer who relays the Basra guild message. The source role does not establish a personal name or an official appointment.',
    136: 'Retain Senior Monk for the distinguished monk who corrects Lil and sends her for tea and sugar. The source label establishes seniority and does not specify an abbot.',
    137: 'Retain Senior Monk for the source monk who tests Lil’s courtesy and gives the northern route clue. Preserve this separate native identity even though the displayed label matches actor 136.',
    148: 'Retain Guildmaster for the source guild head who commissions and pays for the Basra spice delivery. The context supports the established office without a personal or court title.',
    151: 'Retain Sailor for the spoken expedition nameplate. Preserve the established Retainer catalogue form for the source subordinate label. The startup role fallback does not establish later conditional assignments.',
    192: 'Retain Matilda for the established identity who tells Lil about the Colosseum. Genoa remains the source region field rather than a surname.',
    197: 'Retain Safia for the dancer who thanks Lil and mentions the mosque. Basra remains the source region field rather than a surname.',
    203: 'Retain Sakura for the established temple contact who accompanies Lil partway. Osaka remains the source region field rather than a surname.',
}


def main():
    terms_path = ROOT / 'scoped_terms_reference_v1.json'
    config = ROOT / 'prose_config_v1.json'
    assert not terms_path.exists() and not config.exists()
    proposals_path = ROOT / 'all278_contextual_comparisons_v1.json'
    current_path = ROOT / 'current_v1/current_effective.json'
    proposals, current = map(load, [proposals_path, current_path])
    runtime = proposals['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=2)
    assert ctx.receipt() == runtime == current['runtime']
    reuse = current['exact_native_context_reuse']
    target, release, receipt = qualify_scope(ctx, current, reuse['target_release'])
    assert receipt == reuse == proposals['exact_native_context_reuse']
    assert release['candidate_sha256'] == current['current_ROM_sha256'] == proposals['current_ROM_sha256']
    assert target.read_file('/GRP/KANJI.FNT') == ctx.image.read_file('/GRP/KANJI.FNT')
    assert digest('work/clean.nds') == release['clean_input_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    goods_path = Path('translations/commodity_name_manuscript_v343.json')
    fidelity_path = Path('translations/commodity_fidelity_v2.json')
    goods = {r['index']: r for r in load(goods_path)['records']}
    fidelity = {r['index']: r for r in load(fidelity_path)['records']}

    def bind(field, source_text, current_text):
        original = string(clean, struct.unpack_from('<I', clean, field)[0])
        pointer = struct.unpack_from('<I', ctx.arm, field)[0]
        raw = cstring(ctx.raw, pointer)
        assert original['text'] == source_text and raw.decode('cp932') == current_text, (field, original, raw)
        return dict(field_offset=field, source=original,
            current=dict(pointer=pointer, text=current_text, hex=raw.hex()))

    commodities = []
    for index in [1, 11, *range(21, 30), 31]:
        row, final = goods[index], fidelity[index]
        field = row['pointer_field']
        assert row['Japanese'] == final['Japanese']
        result = bind(field, row['Japanese'], final['English'])
        metadata = bytes.fromhex(row['metadata_hex'])
        assert clean[field + 4:field + 12] == ctx.arm[field + 4:field + 12] == metadata
        commodities.append(dict(index=index, **result, nonname_metadata_hex=metadata.hex()))
    city_path = Path('translations/hodram_B171_B190_scoped_names_andterms_v1.json')
    basra = next(r['typed_field'] for r in load(city_path)['records'] if r['id'] == 'SC1_B180_B190_CITY_38')
    assert basra['source_Japanese'] == 'バスラ' and basra['current_label'] == 'Basra'
    town = bind(basra['field_offset'], 'バスラ', 'Basra')
    prior_terms = Path('work/Lil361_B283_B298_clean_20261110/scoped_terms_reference_v1.json')
    proof_term = load(prior_terms)['full_Proof_term']
    ref = proof_term['approved_integrated_reference']
    anchor_path = Path(ref['path'])
    anchor = load(anchor_path)
    assert digest(anchor['target_ROM']) == anchor['target_ROM_sha256']
    original = IlnkContainer.parse(NdsImage.open(anchor['target_ROM']).read_file('/data/SC3.DK4')).blocks[53]
    current_block = IlnkContainer.parse(target.read_file('/data/SC3.DK4')).blocks[53]
    assert original == current_block and all(ref['review'].values())
    position = ref['current_reference']['offset']
    raw = bytes.fromhex(ref['current_reference']['exact_stored_hex'])
    assert current_block[position:position + len(raw) + 1] == raw + b'\0'
    proof_aliases = [bind(1295216, '覇者の証', 'Proof'), bind(1503776, '覇者の証', 'Conq Proof')]
    help_path = Path('translations/help_town23_contextual_final_review_v2.json')
    assert '[[24|Market Info]]' in help_path.read_text(encoding='utf-8')
    save(terms_path, dict(runtime=runtime, exact_native_context_reuse=receipt, items=[],
        commodities=commodities, Basra=town, full_Proof_term=proof_term, short_Proof_fields=proof_aliases,
        market_command='Market Info', native_pointer_readbacks_not_widget_gameplay=True, new_credit=0,
        evidence={str(p): digest(p) for p in [goods_path, fidelity_path, city_path, prior_terms, anchor_path,
            help_path, current_path, Path(__file__)]}))
    changes = {
        'DK4_MES_B304_R0051': dict(
            before="The New World and Southeast Asia are especially well known for their spices. Check the market information if you get stuck. I'm counting on you.",
            after="The New World and Southeast Asia are especially well known for their spices. Check Market Info if you get stuck. I'm counting on you.",
            reason='Use the approved command label Market Info so the player can find it in the market.'),
        'DK4_MES_B310_R0110': dict(
            before='Huh? I can keep it? ...May I really?',
            after='Huh? Can I keep it? I mean... may I?',
            reason='The read-aloud pass gives Lil a clear self-correction from casual speech to the courtesy the monk expects.'),
        'SC2_B311_STYLE_8_716': dict(
            before="Admiral, I've been wondering about the map to the Proof. Shall we visit the village where its guardians are said to live? It was... far to the northeast of China, as I recall.",
            after="Admiral, I've been wondering about the map to the Proof. Shall we visit the village where the clan guarding it is said to live? It was... far to the northeast of China, as I recall.",
            reason='Keep the guardians explicitly a clan in the formal elder’s reminder.'),
    }
    kinds = Counter('typed-choice-label' if r['kind'] == 'typed-menu-caption' else
        'system-FE' if r.get('source_selector') == 254 else 'progressive' for r in proposals['records'])
    assert kinds == {'progressive': 264, 'system-FE': 8, 'typed-choice-label': 6}
    save(config, dict(proposals=str(proposals_path), names=str(ROOT / 'scoped_names_macros_reference_v1.json'),
        terms=str(terms_path), roles=str(ROOT / 'dynamic_roles_all_v1.json'),
        objects=str(ROOT / 'current_objects_v1/current_objects.json'), source_objects=278,
        proposal_counts=[170, 108], final_counts=[170, 108], item_bindings=0, file_path='/data/SC2.DK4',
        name_reasons=NAME_REASONS, scope_id='LIL_SC2_B299_B311_278', amendments=changes,
        name_context='Thirteen clean and current Lil exchanges. The two name consumers and the roles are bound in the initialized startup context.',
        FE_contexts={299: 'Apparent injury and fatigue notices', 301: 'Elapsed day and fatigue recovery notice',
            305: 'Basra payment and market-share notices', 306: 'Elapsed day, apparent fatigue and ferry fare notices',
            310: 'Temple errand reimbursement and reward notice'},
        kind_counts=dict(kinds), out=str(PROSE), names_out=str(NAMES), proof_out=str(ROOT / 'prose_gates_v1.json')))
    print('Bound 12 commodities, Basra, both short Proof fields and the approved Market Info label.')


if __name__ == '__main__':
    main()
