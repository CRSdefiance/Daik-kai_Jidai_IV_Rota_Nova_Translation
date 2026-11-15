"""Bind forecast and spoken item terminology to clean fields and the current own snapshot."""
import struct
import ast
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.bind_hodram_B191_B210_identities import cstring
from scripts.audit_native_given_name_table import string
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')
RELEASE = Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')


if __name__ == '__main__':
    output = ROOT / 'source_current_term_checkpoint_v1.json'
    assert not output.exists()
    ctx = RegisteredRuntime(RELEASE, RELEASE.with_name('own_registered_startup_verification.json'))
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    goods_asset = Path('translations/commodity_name_manuscript_v343.json')
    fidelity_asset = Path('translations/commodity_fidelity_v2.json')
    entity_asset = Path('translations/entity_ship_names_arm9_v2.json')
    goods, fidelity, entities = map(load, [goods_asset, fidelity_asset, entity_asset])
    rows = []
    for index in [8, 29, 33, 37, 41, 42, 78, 79]:
        approved = next(r for r in goods['records'] if r['index'] == index)
        final = next(r for r in fidelity['records'] if r['index'] == index)
        field = approved['pointer_field']
        original = string(clean, struct.unpack_from('<I', clean, field)[0])
        pointer = struct.unpack_from('<I', ctx.arm, field)[0]
        raw = cstring(ctx.raw, pointer)
        assert original['text'] == approved['Japanese'] == final['Japanese']
        assert raw.decode('cp932') == final['English']
        assert clean[field + 4:field + 12] == ctx.arm[field + 4:field + 12] == bytes.fromhex(approved['metadata_hex'])
        rows.append(dict(index=index, source_Japanese=original['text'], source_hex=original['hex'], pointer_field=field,
            current_pointer=pointer, current_hex=raw.hex(), current_term=raw.decode('cp932'), all_nonname_metadata_exact=True))
    cities = []
    prior_city_bindings = {}
    prior_city_evidence = []
    for name in ['187_terms_v5194', '188_terms_v5238', '189_terms_v5279', '190_terms_v5320',
        '191_terms_v5364b', '192_terms_v5412', '193_terms_v5453', '194_terms_v5496', '195_terms_v5547']:
        producer = Path('scripts/reconcile_lil_B' + name + '.py')
        tree = ast.parse(producer.read_text(encoding='utf-8-sig'))
        root = next(Path(ast.literal_eval(node.value.args[0])) for node in ast.walk(tree)
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ROOT' for t in node.targets))
        docs = [(p, load(p)) for p in root.glob('*.json')]
        path, doc = next((p, d) for p, d in docs if d.get('city'))
        aliases = doc.get('two_source_current_city_aliases', [doc.get('one_source_current_city_alias')])
        assert aliases and all(a and 'pointer_field' in a for a in aliases)
        prior_city_bindings[doc['city']] = aliases
        prior_city_evidence.extend([producer, path])
    for ja, en in [('マラッカ', 'Malacca'), ('大坂', 'Osaka'), ('ハンブルク', 'Hamburg'), ('ハバナ', 'Havana'),
        ('カリカット', 'Calicut'), ('イスタンブール', 'Istanbul'), ('京城', 'Seoul'), ('杭州', 'Hangzhou'), ('ヴェラクルス', 'Veracruz')]:
        aliases = []
        for row in prior_city_bindings[en]:
            field = row['pointer_field']
            original = string(clean, struct.unpack_from('<I', clean, field)[0])
            assert original.get('text') == ja
            pointer = struct.unpack_from('<I', ctx.arm, field)[0]
            raw = cstring(ctx.raw, pointer)
            assert raw.decode('cp932') == en
            aliases.append(dict(pointer_field=field, clean_pointer=struct.unpack_from('<I', clean, field)[0],
                source_hex=original['hex'], current_pointer=pointer, current_hex=raw.hex()))
        assert aliases, (ja, en)
        cities.append(dict(source_Japanese=ja, current_term=en, source_qualified_typed_aliases=aliases))
    items_asset = Path('translations/all_item_names_arm9_v1.json')
    items = []
    for index, ja, en in [(14, 'ガラスの製法辞典', 'Glassmaking Guide'), (116, '鯱の像', 'Shachihoko')]:
        approved = next(r for r in load(items_asset)['records'] if r['id'] == f'DK4_ITEM_POINTER_{index:03d}')
        field = approved['offset']
        original = string(clean, struct.unpack_from('<I', clean, field)[0])
        pointer = struct.unpack_from('<I', ctx.arm, field)[0]
        raw = cstring(ctx.raw, pointer)
        assert original['text'] == ja and raw.decode('cp932') == en
        assert clean[field + 4:field + 24] == ctx.arm[field + 4:field + 24]
        items.append(dict(index=index, source_Japanese=ja, source_hex=original['hex'], pointer_field=field,
            current_pointer=pointer, current_hex=raw.hex(), current_term=en,
            historical_legacy_item_asset_not_current_name_authority=index == 116))
    terms_path = Path('guide/research/player-terminology-reference.json')
    terms = load(terms_path)
    attributes = [next(r for r in terms if r['japanese'] == ja and r['english'] == en)
        for ja, en in [('魅力', 'Charm'), ('知力', 'Wits'), ('精神', 'Spirit')]]
    shachihoko = Path('translations/shachihoko_item116_editorial_release_v1.json')
    portrait = Path('translations/common_artwork_name_captions_v1.json')
    # Rocco is a project spelling already approved in the earlier contextual
    # review; no external historical identity or official Latin name is claimed.
    rocco_proof = Path('work/analysis/lil_B199_comparison_v5783/complete_clean_context_actual_source_and_project_name_reconciliation.json')
    if not rocco_proof.exists():
        rocco_proof = Path('work/analysis/lil_B199_comparison_v5783b/complete_clean_context_actual_source_and_project_name_reconciliation.json')
    rocco = load(rocco_proof)['portrait_subject_name']
    assert rocco['project_English'] == 'Rocco Alemkel'
    save(output, dict(runtime=ctx.receipt(), goods=rows, cities=cities, spoken_item_terms=items,
        source_categories=[dict(index=13, Japanese='薬', prose='medicine'), dict(index=14, Japanese='染料', prose='dyes')],
        medicine_anddyes_are_categories_not_specific_commodity_orbrand=True, attributes=attributes,
        portrait_subject=dict(source_Japanese='ロッコ・アレムケル', project_English='Rocco Alemkel', prior_proof=str(rocco_proof), prior_proof_sha256=sha(rocco_proof.read_bytes())),
        cultural_terms=dict(giyaman='Retain the source name and its explicit glass explanation; no etymology or cut-glass claim.',
            Namahage='Retain the named figure and bad-child chant without inventing folklore or resolving the dream.',
            Shachihoko='Preserve the source distinction from Jam\'s mistaken figurehead interpretation.'),
        category_stat_anditem_UI_fidelity_review_not_newly_closed=True,
        native_pointer_readbacks_not_new_widget_gameplay=True, no_current_story_English_extraction=True,
        new_credit=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [goods_asset, fidelity_asset, entity_asset, items_asset, terms_path, shachihoko, rocco_proof, *prior_city_evidence, Path(__file__)]}))
    print('Bound eight goods, nine forecast cities, Glassmaking Guide/Shachihoko and Charm/Wits/Spirit. No new UI approval or credit.')
