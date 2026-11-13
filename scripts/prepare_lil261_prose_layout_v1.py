"""Bind Lil's remaining terms, prose gates and native formatting inputs."""

import argparse
from collections import Counter
from pathlib import Path
import struct
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.extract_editorial_current_scope_reuse_v1 import qualify_scope
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil278_layout_v1 import CAPTAIN_FORMATTER, CAPTAIN_PLANNER, run_prose_gate
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.save_lil261_clean_part_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text


PROSE = Path('translations/lil_B323_B335_contextual_review_v1.json')
NAMES = Path('translations/lil_B323_B335_scoped_names_v1.json')
NAME_REASONS = {
    2: 'Retain Lil Argot and the native FI and FA forms Lil and Argot. The guild commission and the expedition address the same captain without changing her role.',
    9: 'Retain Camille Overijssel and the catalogue form Camille Marinus Overijssel. His dry reply to Lil’s boast fits the continuing crew relationship.',
    18: 'Retain Charles Rochefort and the catalogue form Charles Jean Rochefort. Lil addresses him by his given name in the exchange about the Alchemy Book.',
    22: 'Retain Samwell Khan on the nameplate and Samwell da Khan in the catalogue. The cave line identifies the speaker by the original selector and the two native consumers preserve the approved forms.',
    147: 'Retain Guildmaster for the role that commissions the tomato trend, provides progress updates and directs payment. The exchanges supply no personal name.',
    151: 'Retain Sailor for the speech nameplate and Retainer for the distinct catalogue label. The Sofala handoff and initialized fallback do not identify a particular person.',
    161: 'Retain Villager for the source label in the sextant exchange and the separate gift handoff. Use the surrounding text to convey age or familiarity without putting either in the role label.',
    179: 'Retain Villager for the source label on the ruins contact and the villager who recounts the monk’s story. The shared selector does not establish that they are the same person.',
    206: 'Retain Isabel, who passes on a customer’s account and asks Lil to inquire about the missing monk. The source supplies no surname or title.',
}


def prepare_prose():
    proposals_path = ROOT / 'all261_contextual_comparisons_v1.json'
    current_path = ROOT / 'current_v1/current_effective.json'
    terms_path = ROOT / 'scoped_terms_reference_v1.json'
    config_path = ROOT / 'prose_config_v1.json'
    assert not terms_path.exists() and not config_path.exists()
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
        source, current = [string(raw, struct.unpack_from('<I', arm, offset)[0])
                           for arm, raw in ((clean, clean), (ctx.arm, ctx.raw))]
        assert (source['text'], current['text']) == (japanese, english)
        return dict(pointer_field_offset=offset, source=source, current=current,
                    source_field_hex=clean[offset:offset + 4].hex(), current_field_hex=ctx.arm[offset:offset + 4].hex())

    item_path = Path('translations/all_item_names_arm9_v1.json')
    item_rows = {r['id']: r for r in load(item_path)['records']}
    items = []
    for ident, offset, japanese, english in (
        ('DK4_ITEM_POINTER_013', 1172296, '錬金術の書', 'Alchemy Book'),
        ('DK4_ITEM_POINTER_125', 1174984, '六分儀', 'Sextant'),
        ('DK4_ITEM_POINTER_172', 1176112, '古代都市遺跡への地図', 'Ancient City Map'),
    ):
        label = item_rows[ident]
        assert (label['offset'], label['english']) == (offset, english)
        item = field(offset, japanese, english)
        assert item['source_field_hex'] == label['source_hex'].lower()
        items.append(dict(registered_record=ident, **item))
    commodity_path = Path('translations/commodity_name_manuscript_v343.json')
    commodities = [field(offset, japanese, english) for offset, japanese, english in (
        (1437572, 'トマト', 'Tomato'), (1437848, 'カカオ', 'Cocoa'),
        (1437860, 'タバコ', 'Tobacco'), (1437932, '銀', 'Silver'),
    )]
    help_path = Path('translations/help_deck30_Coerce33_active_terms_final_review_v1.json')
    chapel = next(row for row in load(help_path)['records'] if row.get('heading') == 'Chapel')
    assert all(word in chapel['english'] for word in ('Missionary', 'Distribute Goods', 'square'))
    save(terms_path, dict(runtime=runtime, exact_native_context_reuse=receipt, items=items, commodities=commodities,
        shipboard_procedure=dict(help_record=chapel['id'], exact_English=chapel['english']),
        native_pointer_readbacks_not_widget_gameplay=True,
        evidence={str(p): digest(p) for p in (item_path, commodity_path, help_path, current_path, Path(__file__))}, new_credit=0))
    kinds = Counter('typed-choice-label' if row['kind'] == 'typed-menu-caption' else
                    'system-FE' if row.get('source_selector') == 254 else 'progressive' for row in proposals['records'])
    assert kinds['typed-choice-label'] == 6 and sum(kinds.values()) == 261
    contexts = {
        323: 'Apparent sailor fatigue and elapsed day', 324: 'Apparent sailor injuries and fatigue',
        325: 'Elapsed day during the crossing', 329: 'Gold and Havana market-share rewards',
        330: 'Search advance', 332: 'Transfer of the sextant', 333: 'Alternate survey funding notices',
    }
    assert set(contexts) == {row['block'] for row in proposals['records'] if row.get('source_selector') == 254}
    counts = [proposals['revised'], proposals['retained']]
    save(config_path, dict(proposals=str(proposals_path), names=str(ROOT / 'scoped_names_macros_v2.json'),
        terms=str(terms_path), roles=str(ROOT / 'dynamic_roles_all_v1.json'),
        objects=str(ROOT / 'current_objects_v1/current_objects.json'), source_objects=261,
        proposal_counts=counts, final_counts=counts, item_bindings=3, file_path='/data/SC2.DK4',
        name_reasons=NAME_REASONS, scope_id='LIL_SC2_B323_B335_261', amendments={},
        name_context='Thirteen complete clean/current exchanges. Names and roles use the qualified initialized native context.',
        FE_contexts=contexts, kind_counts=dict(kinds), out=str(PROSE), names_out=str(NAMES),
        proof_out=str(ROOT / 'prose_gates_v1.json')))
    env = {**run_prose_gate.__globals__, 'ROOT': ROOT, 'PROSE': PROSE, '__file__': __file__}
    FunctionType(run_prose_gate.__code__, env)()


def format_input():
    source = checked_text(CAPTAIN_FORMATTER.read_text(encoding='utf-8'), {
        "args.root/'dynamic_roles_current_v1.json'": "args.root/'dynamic_roles_all_v1.json'",
        "args.root/'scoped_names_macros_reference_v1.json'": "args.root/'scoped_names_macros_v2.json'",
        "    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']":
            "    assert ctx.receipt()==runtime\n"
            "    from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context\n"
            "    assert qualified_current_native_context(doc,ctx)==current['exact_native_context_reuse']",
    })
    previous_fe = 'work/Lil254_B312_B319_clean_20261110/formatting_v2/native_macro_measurements.json'
    sys.argv = [sys.argv[0], '--root', str(ROOT), '--prose', str(PROSE),
                '--FE-source-macros', previous_fe, '--captain', '2']
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})


def plan(remaining):
    entry = "    source = checked_text(Path('scripts/plan_maria301_v1.py').read_text(encoding='utf-8'), {"
    identity = "    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==doc['runtime']['candidate_sha256']"
    scope = """    from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
    from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
    runtime = doc['runtime']
    ctx = RegisteredRuntime(runtime['release_proof'], runtime['startup_proof'], captain=runtime['captain'])
    assert ctx.receipt() == runtime
    assert digest(doc['current_ROM']) == doc['current_ROM_sha256']
    assert qualified_current_native_context(doc, ctx) == current['exact_native_context_reuse']"""
    source = checked_text(CAPTAIN_PLANNER.read_text(encoding='utf-8'), {
        entry: f'{entry}\n        {identity!r}: {scope!r},',
    })
    sys.argv = [sys.argv[0], '--root', str(ROOT), *remaining]
    exec(compile(source, __file__, 'exec'), {'__file__': __file__, '__name__': '__main__'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('stage', choices=('prose', 'format', 'plan'))
    args, remaining = parser.parse_known_args()
    if args.stage == 'plan':
        plan(remaining)
    else:
        assert not remaining
        {'prose': prepare_prose, 'format': format_input}[args.stage]()
