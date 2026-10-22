"""Evidence-bound checkpoint; no new completed-entry or playable-ROM credit."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_aftermath_layout_v1250 import IDS
from scripts.battle_aftermath_native_plan_v1255 import compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_aftermath_checkpoint_v1264')
MANUSCRIPT = Path('translations/battle_aftermath_editorial_manuscript_v3.json')
PROOFS = {
    'source_context':'work/analysis/battle_aftermath_bindings_v1249/source_context_complete.json',
    'source_prose':'work/analysis/battle_aftermath_prose_v1250b/source_prose_review.json',
    'prose_count_recovery':'work/analysis/battle_aftermath_prose_v1250c/ledger_recovery.json',
    'refined_prose':'work/analysis/battle_aftermath_refinement_v1258/source_prose_refinement.json',
    'native_runtime':'work/analysis/battle_aftermath_runtime_v1254c/native_runtime_verification.json',
    'native_scope':'work/analysis/battle_aftermath_runtime_v1254c/scope_proof.json',
    'native_ISA_compiler':'work/analysis/battle_aftermath_isa_compiler_v1257b/isa_compiler_verification.json',
    'native_payload':'work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json',
    'native_fonts':'work/analysis/battle_aftermath_fonts_v1260/native_font_proof.json',
    'native_copies':'work/analysis/battle_aftermath_copies_v1261/all_native_copies_and_prefix_cache_sequence.json',
    'escape_regression':'work/analysis/battle_aftermath_escape_v1262/original_direct_escape_regression.json',
    'visual_review':'work/analysis/battle_aftermath_native_review_v1263/visual_and_native_review.json',
    'native_approval':'work/analysis/battle_aftermath_native_review_v1263/native_manuscript_approval.json',
    'current_shop_recheck':'work/analysis/user_shop_formatting_v1252/photographed_shop_formatting.json',
}


def main():
    assert not ROOT.exists()
    doc = read(MANUSCRIPT)
    proof = {k:read(p) for k,p in PROOFS.items()}
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    assert all(all(r['review'].values()) for r in doc['records']) and not doc['formatting_review_pending']
    assert sum(r['editorial_decision']=='revise' for r in doc['records']) == 58
    assert sum(r['editorial_decision']=='retain' for r in doc['records']) == 17
    assert proof['native_scope']['total_cases'] == 529273
    assert len(proof['native_fonts']['cases']) == 783
    assert proof['native_copies']['complete_native_copies'] == 7336
    assert len(proof['native_copies']['sequenced_cache_cases']) == 180
    assert len(proof['escape_regression']['all13_original_direct_pipeline_cases']) == 13
    for name in ('native_fonts','native_copies','escape_regression'):
        assert proof[name]['ARM9_sha256'] == proof['native_payload']['target_ARM9_sha256']
        assert proof[name]['COMMON_sha256'] == proof['native_payload']['target_COMMON_sha256']
    tested = {r['message_id']:r for r in read(proof['native_fonts']['manuscript'])['records']}
    assert all(compiled(r) == compiled(tested[r['message_id']]) for r in doc['records'])
    ROOT.mkdir(parents=True)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1260 and ledger['records_with_source_and_prose_pass'] == 1373
    save(ROOT/'coverage_before_checkpoint.json',ledger)
    before = deepcopy(ledger)
    drafts = ledger['active_source_prose_drafts']
    old_names = {'translations/battle_aftermath_editorial_manuscript_v1.json','translations/battle_aftermath_editorial_manuscript_v2.json'}
    drafts['manuscripts'] = [str(MANUSCRIPT) if p.replace('\\','/') in old_names else p for p in drafts['manuscripts']]
    subsets = drafts['manuscript_record_subsets_pending']
    for key in list(subsets):
        if key.replace('\\','/') in old_names:
            assert subsets.pop(key) == list(IDS)
    subsets[str(MANUSCRIPT)] = list(IDS)
    drafts['status'] = '75-native-font-approved-release-gameplay-pending-and38-older-reviewed-entries-open'
    drafts['note'] = ('75 aftermath paragraphs comprise58 revisions17 retained wordings. All75 have source,prose,native-font and CPU-consumer review;registered combined release,exact patch,cold boot and representative original gameplay/transitions remain pending. Older38 reviewed entries remain open;the broader shared/routes/raw-source inventory is also unfinished.')
    assert len(drafts['native_message_IDs']) == 113 and set(IDS) <= set(drafts['native_message_IDs'])
    summary = ('V1264 records75 aftermath/town-surrender/city-defense paragraphs:58 revisions17 retained. Source/prose totals1373;completed totals1260 unchanged. The exact bounded byte decoder retains all prior memberships and adds13 source-proven ones;529273 native dispatch/ABI/stack cases,3668 modal outputs238 parent5 edge controls,and140 whole-memory status cases pass. Its table uses184 of188 owned bytes and code168 of172;all sections/BSS/cache/ITCM and123040 staged bytes remain exact. All783 original speech-pipeline/full228x64 font cases pass,including684 real town-name expansions and30 synthetic ASCII/CP932 stress variants. Six visual sheets cover every75 ID;four prose refinements remove real/static isolated final words. Six remaining predicate-only tails are restricted to two synthetic oversized names. All7336 native copies180 cache sequences and13 earlier direct escape pipelines pass. Every3593 unselected message/native copy and opaque duel prefix remain exact. No new playable ROM,registry layer,patch,cold boot or battle outcome is claimed. Registered V1224,canonical baseline and prior whole-batch scene-verified V997 remain unchanged.113 reviewed COMMON entries remain incomplete,plus the broader editorial inventory. Global formatting,separate graphics/all18 plaques and the later older-record re-audit remain open;goal active.')
    checkpoint = ROOT/'native_checkpoint.json'
    save(checkpoint,{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'proofs':{k:{'path':p,'sha256':sha(Path(p).read_bytes())} for k,p in PROOFS.items()},
        'source_prose_records':1373,'completed_records':1260,'new_native_reviewed_records':75,
        'newly_completed_records':0,'reviewed_but_incomplete_COMMON_records':113,
        'no_ROM_registry_patch_or_gameplay_change':True,'summary':summary,
        'previous_goal_turn_classification':'progress: exact photographed shop676/677 native regression and authoritative watchlist updated',
        'this_goal_turn_classification':'progress: source-bound fixed-footprint native decoder,783 font cases,four faithful prose refinements,7336 copies,180 cache sequences,13 escape regressions and visual/native manuscript approval',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ledger['battle_aftermath_v1264_native_checkpoint'] = {'proof':str(checkpoint),'manuscript':str(MANUSCRIPT),
        'native_reviewed_records':75,'source_prose_records_added_this_checkpoint':0,'completed_entries_added':0,
        'next':'Register complete layer after V1224,build/audit combined ROM and clean-input patch,cold boot,then original source-family gameplay and transitions.'}
    ledger['latest_checkpoint'] = summary
    ledger['research_checkpoints'].append({'id':'V1264-aftermath75-native-checkpoint','proof':str(checkpoint),
        'manuscript':str(MANUSCRIPT),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ('current_integrated_candidate','current_native_relocation_reference','source_pins',
                'unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit'):
        assert ledger[key] == before[key],key
    save(ledger_path,ledger)
    doc_path = Path('docs/battle_aftermath_v1264_native_checkpoint.md')
    assert not doc_path.exists()
    doc_path.write_text('# V1264: aftermath native review checkpoint\n\n'+summary+'\n\n## Evidence\n\n'+
        '\n'.join('- **'+k.replace('_',' ')+':** `'+p+'`.' for k,p in PROOFS.items())+
        '\n\n## Research boundaries and retained failures\n\n'+
        'Original speech selection,loader,printf,macro expansion,formatter and fonts execute in CPU research. Successful file I/O and portrait construction are explicit host boundaries. Alternative role voices use original roster setters in CPU-only copies with exactly one duty byte changed;all actor objects,identity fields,RNG and other4MiB bytes remain exact. These are not earned gameplay outcomes.\n\n'+
        'V1254 used an obsolete V772 metadata ownership map;V1254b missed the already relocated status hook. V1254c binds later proved ownership and original status/IP behavior. V1256 compared full table pointers with low words and encountered the inactive base captain copy;V1256b uses complete pointers and original noncaptain voice objects. V1257 treated data words as Thumb ADR instructions;V1257b proves all six leads are unchanged source COceanScene vtable function pointers,with RTTI and actual object binding. No runtime was relaxed for these harness failures.\n\n'+
        'The V1258 note predicting one row for1995 was incorrect:the native planner may choose two balanced rows. V1263 corrects that note without changing the tested English. All six remaining single-word final rows use synthetic names longer than every real town name;their exact case decisions do not waive any real-name,missing-letter,bounds or gameplay requirement.\n\n'+
        'Next:registered integration/exact clean-input patch,ordinary startup and representative original aftermath,surrender,defense and withdrawal scenes with normal dismissal/transitions. The113 reviewed incomplete entries and broader unreviewed scope stay open.\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md'):
        path = Path('docs')/name
        with path.open('a',encoding='utf-8',newline='\n') as handle:
            handle.write('\n\n## V1264 aftermath native review checkpoint\n\n'+summary+'\n\nSee [evidence](battle_aftermath_v1264_native_checkpoint.md).\n')
    print('V1264 recorded:1260 complete1373 source/prose;75 native-approved drafts and38 older incomplete remain open. No ROM built.',flush=True)


if __name__ == '__main__':
    main()
