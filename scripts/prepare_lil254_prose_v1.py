"""Bind Lil B312–B319 terminology and finish the scoped prose decisions."""

from collections import Counter
from pathlib import Path
import struct

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.extract_editorial_current_scope_reuse_v1 import qualify_scope
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_lil254_clean_v1 import ROOT


PROSE = Path('translations/lil_B312_B319_contextual_review_v1.json')
NAMES = Path('translations/lil_B312_B319_scoped_names_v1.json')
NAME_REASONS = {
    0: 'Retain Rafael Castor in both name consumers for source selector 00. Both B317 replies use that exact clean command. The initialized getter binds the name and a representative B317 replay still needs to verify its displayed speaker.',
    2: 'Retain Lil Argot and the FI form Lil. The source fixes her as the expedition leader and the trader exchange preserves FO as the company she heads.',
    9: 'Retain Camille Overijssel and the catalogue form Camille Marinus Overijssel. Lil calls him Camille after overhearing his aside about the wolf.',
    35: 'Retain Fernan Silveira in both name consumers and the source surname Silveira in the trader’s account.',
    36: 'Retain Geronimo Espinosa on the nameplate and Geronimo de Espinosa in the catalogue. The three conditional branches distinguish Espinosa as a person from the Espinosa Company.',
    104: 'Retain Trader for the source trading-post role. His familiarity with local commerce and informal address establish neither a higher title nor a relationship to Lil.',
    151: 'Retain Sailor as the spoken role and Retainer as the distinct catalogue label. The initialized fallback does not establish later expedition assignments.',
    201: 'Retain Mihwa, the contact who shares the city-gate location discreetly. Her Hangzhou field records a place and supplies no surname.',
    204: 'Retain Verisa, the contact who requests the burner and offers a reading. Her Sao Jorge field records a place and supplies no surname or professional title.',
    205: 'Retain Silvia, the contact who reports the illustrated map. Her Veracruz field records a place and supplies no surname.',
}


def main():
    terms = ROOT / 'scoped_terms_reference_v1.json'
    config = ROOT / 'prose_config_v1.json'
    assert not terms.exists() and not config.exists()
    proposals_path = ROOT / 'all254_contextual_comparisons_v1.json'
    current_path = ROOT / 'current_v1/current_effective.json'
    proposals, current = map(load, (proposals_path, current_path))
    runtime = current['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=2)
    assert ctx.receipt() == runtime == proposals['runtime']
    reuse = current['exact_native_context_reuse']
    target, release, receipt = qualify_scope(ctx, current, reuse['target_release'])
    assert receipt == reuse == proposals['exact_native_context_reuse']
    assert release['candidate_sha256'] == current['current_ROM_sha256'] == proposals['current_ROM_sha256']
    assert target.read_file('/GRP/KANJI.FNT') == ctx.image.read_file('/GRP/KANJI.FNT')
    assert digest('work/clean.nds') == release['clean_input_sha256']
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')

    def field(offset, japanese, english):
        source, active = [string(raw, struct.unpack_from('<I', arm, offset)[0])
                          for arm, raw in ((clean, clean), (ctx.arm, ctx.raw))]
        assert source['text'] == japanese and active['text'] == english
        return dict(pointer_field_offset=offset, source=source, current=active,
                    source_field_hex=clean[offset:offset + 4].hex(), current_field_hex=ctx.arm[offset:offset + 4].hex())

    item_path = Path('translations/all_item_names_arm9_v1.json')
    label = next(row for row in load(item_path)['records'] if row['id'] == 'DK4_ITEM_POINTER_145')
    assert label['offset'] == 1175464 and label['english'] == 'Goryeo Incense Burner'
    item = field(label['offset'], '高麗青磁の香炉', label['english'])
    assert item['source_field_hex'] == label['source_hex'].lower()
    item['registered_record'] = label['id']
    commodities = [field(1437920, '金', 'Gold'), field(1438220, '象牙', 'Ivory')]
    precedent = Path('translations/hodram_B311_B324_integrated_final_review_v1.json')
    anchor = next(row for row in load(precedent)['records'] if row['id'] == 'DK4_MES_B314_R0010')
    assert 'Goryeo Incense Burner' in anchor['english'] and 'celadon' in anchor['english'] and all(anchor['review'].values())
    save(terms, dict(
        runtime=runtime, exact_native_context_reuse=receipt, items=[item], commodities=commodities,
        historical_dialogue_alias='Goryeo Celadon Burner', descriptive_celadon_material_retained=True,
        parallel_registered_dialogue=dict(id=anchor['id'], english=anchor['english'], path=str(precedent),
                                         source_reference=anchor['source_reference']),
        native_pointer_readbacks_not_widget_gameplay=True, new_credit=0,
        evidence={str(path): digest(path) for path in (item_path, precedent, current_path, Path(__file__))},
    ))
    changes = {
        'DK4_MES_B317_R0010': dict(
            before="Say, FI, have you heard of the Goryeo Celadon Burner? It's supposed to be somewhere in East Asia.",
            after="Say, FI, have you heard of the Goryeo Incense Burner? It's made of celadon, and they say it's somewhere in East Asia.",
            reason='Use the registered item name. Keep celadon as the material and preserve the reported East Asian location.'),
        'DK4_MES_B316_R0391': dict(
            before='It looks like there are injuries among the sailors.',
            after='It looks like some of the sailors were injured.',
            reason='Use a natural status message that keeps the injury uncertain and gives no exact count.'),
        'DK4_MES_B319_R0100': dict(
            before='But if we had a local good that cost less per unit, anyone could get into the trade and make an honest living.',
            after='But with a cheaper local specialty, anyone could get into the trade and do business honestly.',
            reason='Keep the local product and lower purchase cost in the trader’s spoken register. The following line separately makes the case for profit.'),
    }
    kinds = Counter('typed-choice-label' if row['kind'] == 'typed-menu-caption' else
                    'system-FE' if row.get('source_selector') == 254 else 'progressive' for row in proposals['records'])
    assert kinds == {'progressive': 239, 'system-FE': 7, 'typed-choice-label': 8}
    save(config, dict(
        proposals=str(proposals_path), names=str(ROOT / 'scoped_names_macros_reference_v1.json'),
        terms=str(terms), roles=str(ROOT / 'dynamic_roles_all_v1.json'),
        objects=str(ROOT / 'current_objects_v1/current_objects.json'), source_objects=254,
        proposal_counts=[151, 103], final_counts=[151, 103], item_bindings=1, file_path='/data/SC2.DK4',
        name_reasons=NAME_REASONS, scope_id='LIL_SC2_B312_B319_254', amendments=changes,
        name_context='Eight clean/current Lil exchanges. The name and role bindings use the qualified initialized startup.',
        FE_contexts={312: 'Wolf injury and fatigue notices', 314: 'Apparent injuries and elapsed day',
                     316: 'Scorpion treatment, luggage impact and apparent sailor injury'},
        kind_counts=dict(kinds), out=str(PROSE), names_out=str(NAMES), proof_out=str(ROOT / 'prose_gates_v1.json'),
    ))
    print('Bound Goryeo Incense Burner, Gold and Ivory to exact clean and current native fields.')


if __name__ == '__main__':
    main()
