"""Record bounded native formatting approval without gameplay completion credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from unittest.mock import patch
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reinforcement_sniping_layout_v1024 import compiled, IDS, PROFILE
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/reinforcement_sniping_v1032')
OLD=Path('translations/reinforcement_sniping_editorial_manuscript_v1.json')
NEW=Path('translations/reinforcement_sniping_editorial_manuscript_v2.json')
FONT=Path('work/analysis/reinforcement_sniping_v1031/native_font_proof.json')
RUNTIME=Path('work/analysis/reinforcement_sniping_v1029/native_runtime_verification.json')


def main():
    assert not ROOT.exists() and not NEW.exists()
    doc,font,rt=read(OLD),read(FONT),read(RUNTIME)
    matrix=read(font['matrix'])
    assert matrix['manuscript_sha256']==sha(OLD.read_bytes())
    assert font['runtime_proof_sha256']==sha(RUNTIME.read_bytes())
    assert font['research_ARM9_sha256']==rt['research_ARM9_sha256']
    assert len(font['cases'])==694 and not font['boundary_findings']
    assert len(font['review_sheets'])==6
    records={r['message_id']:r for r in doc['records']}
    for case in font['cases']:
        n=case['message_ID'];row=records[n];arg=case['argument_case']
        assert compiled(row).hex()==case['compiled_hex']
        expected=row['english'].replace('%s',arg['label']) if arg else row['english']
        assert ' '.join(case['lines'])==expected
        assert case['whole228x64_native_independent_font_and_input_bitmap_guards_pass']
        assert case['all_leading_trailing_and_CP932_name_glyphs_complete']
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
    for sheet in font['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    controls={}
    base=deepcopy(records[1918])
    mutations={
        'prewrapped_I_LF_macro_collision':{'english':"I hear %s will help. I\nwill ask."},
        'authored_alignment':{'english':'Admiral!  %s will help.'},
        'leading_alignment':{'english':' Admiral! %s will help.'},
        'tab_control':{'english':'Admiral!\t%s will help.'},
        'full_width_I':{'english':'Ｉ hear %s will help.'},
        'unsupported_IC_command':{'english':'IC hear %s will help.'},
        'unsupported_FI_command':{'english':'FI hear %s will help.'},
        'extra_percent_command':{'english':'%s has 5% of them.'},
        'translator_markup':{'english':'%s will help.{LB}'},
        'oversized_scratch':{'english':'%s '+'A'*220},
        'missing_argument':{'english':'A fleet will help.'},
        'duplicated_argument':{'english':'%s and %s will help.'},
        'wrong_conversion':{'english':'%d will help.'},
        'argument_count_mismatch':{'native_argument_count':0},
        'unsupported_ID':{'message_id':1931},
    }
    for label,fields in mutations.items():
        try:compiled({**base,**fields})
        except ValueError:controls[label]=True
        else:raise AssertionError(label)
    with patch('dk4tool.rom.nds.NdsImage.open',side_effect=AssertionError('Pure paragraph compiler cannot open ROMs')):
        assert all(compiled(r)==b' '+r['english'].encode('ascii') for r in doc['records'])
    ROOT.mkdir(parents=True)
    visual=ROOT/'visual_review.json'
    save(visual,{'native_font_proof':str(FONT),'native_font_proof_sha256':sha(FONT.read_bytes()),
        'all20_templates_and_representative_extreme_name_canvases_visually_reviewed':True,
        'six_review_sheets':font['review_sheets'],
        'all694_complete_canvases_independently_compared_pixel_for_pixel':True,
        'manual_visual_review_scope':'Six sheets covering every template and representative shortest/longest/CP932 leading-F labels. Other matrix variants receive complete native pixel comparison,not individual manual-view claims.',
        'compiler_rejection_controls':controls,'pure_compilation_without_ROM_reads':True,
        'blocking_errors':0,'unwaived_warnings':0,'visual_review_pending':False,
        'runtime_proof':str(RUNTIME),'runtime_proof_sha256':sha(RUNTIME.read_bytes()),
        'not_registered_ROM_or_actual_scene_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    native=deepcopy(doc)
    native.update(formatting_review_pending=False,
        status='20-native-format-approved-registered-copy-patch-and-actual-scenes-pending',
        reviewed_research_manuscript=str(OLD),reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),
        visual_review_proof=str(visual),visual_review_proof_sha256=sha(visual.read_bytes()),
        native_runtime_proof=str(RUNTIME),native_runtime_proof_sha256=sha(RUNTIME.read_bytes()))
    for row in native['records']:
        row['review']['formatting']=True;row['compiled_hex']=compiled(row).hex()
    validate_natural_dialogue_batch(native)
    assert tuple(r['message_id'] for r in native['records'])==IDS
    assert native['consumer_layout_profile']==PROFILE
    save(NEW,native)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    assert ledger['active_source_prose_drafts']['manuscripts'][-1]==str(OLD)
    ledger['active_source_prose_drafts']['manuscripts'][-1]=str(NEW)
    ledger['reinforcement_sniping_v1032']={'status':native['status'],'manuscript':str(NEW),
        'runtime_proof':str(RUNTIME),'native_font_proof':str(FONT),'visual_review_proof':str(visual),
        'native_font_cases':694,'completed_entries_added':0,'source_prose_reviews_added':0}
    checkpoint=('V1032 approves native formatting for20 reinforcement,covering-fire and Lookout-shot paragraphs1911-1930. All694 exact argument/wrap/font cases pass,with no short-row or weak-boundary findings;all20 templates and representative extreme/leading-F names were visually inspected on six sheets.15 invalid compiler inputs fail closed.56696 source and56696 research selector/ABI cases,3668 unchanged modal outputs,238 wrong-parent controls,5 full-word edges and140 whole-status guards pass. Three exact announcement tables gain post-expansion balancing within unchanged212-byte public/128-byte modal allocations;all sections,BSS,cache and123040 staged bytes remain exact. No ROM or patch built;native repack/copies,registered integration and actual eligibility/announcements/dismissal/return remain pending. V997 stays current;1196 complete,1219 source/prose. Full editorial scope and separate unfinished graphics audit remain open.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V1032-reinforcement-sniping-native-formatting',
        'proof':str(visual),'manuscript':str(NEW),'completed_entries_added':0,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'progress:current ROM shop formatting reverified and watchlist updated',
        'this_goal_turn_classification':'progress:full runtime and694 native font cases plus explicit visual review and compiler guards',
        'full_goal_complete':False})
    for key in ('current_integrated_candidate','source_pins','current_native_relocation_reference','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles','formatting_watchlist'):
        assert ledger[key]==before[key]
    save(lp,ledger)
    docpath=Path('docs/reinforcement_sniping_v1032_native_checkpoint.md');assert not docpath.exists()
    docpath.write_text('# V1032: reinforcement and shot native formatting\n\n'+checkpoint+'\n\nThe failed V1026/V1028 census used a V772 internal-ownership list predating the modal allocation. V1029 proves exact two-instruction internal differences and preserves every external incoming reference. No runtime change was waived. Six sheets manually review all20 templates and representative extreme names;all694 full canvases independently match the native font including blank paper. No actual scene,earned outcome,actor identity,save or canonical acceptance claim.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V1032: reinforcement and shot native formatting\n\n'+checkpoint+' See [V1032 checkpoint](reinforcement_sniping_v1032_native_checkpoint.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V1032 Reinforcement and shot native formatting')
    assert not archive.exists()
    files=[OLD,NEW,FONT,RUNTIME,visual,docpath,lp,Path(__file__),Path('scripts/reinforcement_sniping_layout_v1024.py'),
        Path('scripts/reinforcement_sniping_runtime_v1025.py'),Path('scripts/verify_reinforcement_sniping_runtime_v1029.py'),
        Path('scripts/probe_reinforcement_sniping_layout_v1030.py'),Path('scripts/probe_reinforcement_sniping_fonts_v1031.py'),
        Path(font['matrix']),*map(Path,rt['all_completed_source_proofs']),Path(RUNTIME.parent/'internal_reference_changes.json')]
    files += [Path(r['preview']) for r in font['cases']]+[Path(r['path']) for r in font['review_sheets']]
    copied=[]
    for source in dict.fromkeys(files):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        assert not target.exists();copy2(source,target);assert source.read_bytes()==target.read_bytes()
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'native_previews':694,
        'actual_gameplay_screenshots':0,'completed_entries_added':0,'full_goal_complete':False})
    print('20 native-format-approved paragraphs;694 full font cases archived.1196 complete unchanged. Integration and actual scenes pending.',flush=True)


if __name__=='__main__':main()
