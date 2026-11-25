"""Bind only the three spoken item terms and Sofala; keep generic map and gift references generic."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hodram_B311_B324_contextual_v1 import ROOT, CURRENT, OUT as PROSE

TERMS = ROOT / 'scoped_terms_v1.json'

def main():
    assert not TERMS.exists()
    current, prose = map(load, [CURRENT, PROSE])
    runtime = current['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=1)
    assert ctx.receipt() == runtime
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    asset = Path('translations/all_item_names_arm9_v1.json')
    items = []
    for index, jp, english in [(13, '錬金術の書', 'Alchemy Book'), (125, '六分儀', 'Sextant'),
                               (145, '高麗青磁の香炉', 'Goryeo Incense Burner')]:
        original = next(r for r in load(asset)['records'] if r['id'] == f'DK4_ITEM_POINTER_{index:03d}')
        at = original['offset']
        sp, tp = [struct.unpack_from('<I', raw, at)[0] for raw in [clean, ctx.arm]]
        source = clean[sp-0x02000000:clean.index(0, sp-0x02000000)]
        target = cstring(ctx.raw, tp)
        assert source.decode('cp932') == jp and target.decode('ascii') == english == original['english']
        assert clean[at+4:at+24] == ctx.arm[at+4:at+24]
        items.append(dict(index=index, pointer_field=at, source_pointer=sp, source_hex=source.hex(),
                          source_Japanese=jp, current_pointer=tp, current_hex=target.hex(), current_term=english,
                          all_nonname_item_metadata_exact=True, label_reference_not_new_item_orcatalogue_UI_approval=True))
    aliases = []
    for entry in WORLD_CITY_ENTRIES:
        if entry.japanese != 'ソファラ':
            continue
        assert entry.suggested_english == 'Sofala'
        assert clean[entry.offset:entry.offset+entry.source_length] == entry.expected_bytes
        raw = ctx.arm[entry.offset:entry.offset+entry.slot_size]
        assert raw == b'Sofala' + bytes(entry.slot_size-6)
        aliases.append(dict(profile_ID=entry.row_id, offset=entry.offset, source_hex=entry.expected_bytes.hex(),
                            current_span_hex=raw.hex(), current_term='Sofala'))
    assert len(aliases) == 2
    byid = {r['id']: r for r in prose['records']}
    assert 'Goryeo Incense Burner' in byid['DK4_MES_B314_R0010']['english']
    assert 'celadon' in byid['DK4_MES_B314_R0010']['english']
    assert 'You handed over the Sextant.' == byid['DK4_MES_B321_R0014']['english']
    assert 'Alchemy Book' in byid['DK4_MES_B324_R0065']['english']
    assert 'Sofala guild' in byid['DK4_MES_B322_R0083']['english']
    save(TERMS, dict(runtime=runtime, spoken_item_terms=items, Sofala_aliases=aliases,
        individual_findings=[
            dict(source='高麗青磁の香炉', decision='existing-title-plus-source-material',
                 reason='Use the registered Goryeo Incense Burner title; explicitly preserve celadon in the surrounding speech rather than silently omitting the material.'),
            dict(source='古代の絵地図', decision='generic-pictorial-map-description',
                 reason='This reported map description does not establish which numbered or named catalogue map it is. Do not infer an item identity or purchase location.'),
            dict(source='六分儀', decision='retain-Sextant',
                 reason='Preserve the established instrument and outgoing handover, while leaving the return gift unnamed.'),
            dict(source='錬金術の書', decision='retain-Alchemy-Book',
                 reason='Use the public title where Charles identifies it; the monk’s unseen ore remains unnamed.'),
            dict(source='ソファラのギルド', decision='retain-Sofala-guild',
                 reason='The report is to the existing Sofala guild; the survey has only just begun and no result is asserted.'),
            dict(source='金貨１０００枚', decision='1000-gold-coins-provided',
                 reason='Preserve the exact amount and coin unit as outgoing initial expenses, not reward or income.')],
        geographic_cultural_forms={'東アジア': 'East Asia', '北欧のスウェーデン': 'Sweden, in northern Europe',
            '新大陸': 'New World', 'インドニシキヘビ': 'Indian python'},
        contextual_limits=['The python identification remains Samwell’s uncertain comic claim.',
            'Mineral poison is the witness’s vague account; no specific substance or external medical explanation is added.',
            'Messenger of God is spoken praise, not canonization.',
            'Regional fleet command is explicitly offered; no modern formal admiral grade is invented.'],
        source_fictional_statements_not_external_historical_orbiological_verification=True,
        full_item_andcity_catalogue_UI_unvisited=True, no_ROM_orprose_changes=True, new_credit=0,
        evidence={str(p): digest(p) for p in [CURRENT, PROSE, asset, ROOT/'draft_item_reference_v1.json', Path(__file__)]}))
    print('Bound three item terms and two Sofala aliases. Generic map, gifts and ore remain unnamed.')

if __name__ == '__main__':
    main()
