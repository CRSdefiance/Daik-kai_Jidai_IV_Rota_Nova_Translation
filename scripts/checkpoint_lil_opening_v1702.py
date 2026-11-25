"""Record native-approved opening layouts without promoting incomplete prose work."""
import json
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_checkpoint_v1702')
LEDGER=Path('translations/editorial_review_current_v1.json')
V2=Path('translations/lil_opening_editorial_manuscript_v2.json')


if __name__=='__main__':
    assert not ROOT.exists()
    doc=read(V2);approval_path=Path('work/analysis/lil_opening_review_v1700/approval_receipt.json');approval=read(approval_path)
    fonts=read(doc['native_font_proof']);reloc_path=Path('work/analysis/lil_opening_relocation_v1701/parity_and_native_command_research.json');reloc=read(reloc_path)
    assert approval['sha256']==sha(V2.read_bytes()) and len(doc['records'])==len(fonts['cases'])==49
    assert not doc['formatting_review_pending'] and all(all(r['review'].values()) for r in doc['records'])
    assert read(doc['visual_review'])['all7_sheets_and49_panels_actually_viewed']
    assert fonts['all_continuation_visible_origins_equal_first_row_zero']
    assert (reloc['old_block_bytes'],reloc['research_block_bytes'],reloc['block_growth'])==(3000,3292,292)
    assert not reloc['external_references_complete'] and reloc['all41_non_speech_commands_byte_exact_at_mapped_positions']
    tests_path=Path('work/analysis/lil_opening_checks_v1702/formatter_regression.xml')
    suites=ET.parse(tests_path).getroot().findall('testsuite')
    assert sum(int(t.get('tests')) for t in suites)==73
    assert all(int(t.get(k,0))==0 for t in suites for k in ('failures','errors','skipped'))
    raw=LEDGER.read_bytes();ledger=read(LEDGER)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1375,1568)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==144
    ids=[r['id'] for r in doc['records']]
    assert ledger['reviewed_but_incomplete_route_record_IDs']=={'/data/SC2.DK4':ids}
    rom=Path('out/all_routes_combined_v1676_candidate.nds')
    assert sha(rom.read_bytes())=='337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510'
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw)
    handoff=Path('docs/editorial_handoff_current.md');(ROOT/'handoff_before.md').write_bytes(handoff.read_bytes())
    summary=('V1702 resolves the native formatting gates for all49 Lil Amsterdam-opening drafts without shortening any prose. '
        'Actual fixture-free/no-save Lil New Game on V1676 stops normally6000;its complete RAM binds captain2 and default Lil macro. '
        'Current story calls use the existing registered catalog wrapper before53914,not unchanged direct calls. '
        '196 whole-paragraph and196 wrapped native macro/alignment cases preserve all4MiB memory,input/output guards and ABI. '
        'The opt-in lil-opening-editorial-native-v1 uses the already present V255 literal guards,retains IC/FI collisions and unsafe I-LF rejection, '
        'and preserves all historical profile defaults. Direct playable batching is blocked until a post-layer release binds the proven runtime. '
        '73 targeted formatter/relocation regressions pass.49 complete native/independent216x64 font planes and all7 actually viewed sheets verify complete letters,bounds and uniform visible x0 continuation origins. '
        'The source-matched buffered cursor helper,not glyph-fitting,explains removal of the guard indent. '
        'Manuscriptv2 keeps43 revisions6 retentions;15 automatic English/Japanese line-count differences have specific visual-review reasons. '
        'Parity-preserving research expansion is3000 to3292 bytes(+292),with49 speaker/header/parity contracts and all41 other command bytes preserved at mapped positions;all90 original command types/native extents are accounted for. '
        'Added single parity spaces repaint identical full font planes. External/interior reference classification remains incomplete;no release relocation map,registered ROM,patch or revised actual-scene approval yet. '
        'Counts stay1375 complete(1033 revised342 retained),1568 source/prose reviewed,144 pending COMMON plus49 pending route records and broader untouched prose. '
        'V1676 remains unchanged experimental,V1492 promoted. Full goal stays active;separate graphics/all18 plaques remain open.')
    record={'summary':summary,'approved_manuscript':str(V2),'native_macro_proof':doc['native_macro_proof'],
        'native_font_proof':doc['native_font_proof'],'visual_review':doc['visual_review'],'relocation_research':str(reloc_path),
        'regression_tests':str(tests_path),'regression_tests_passed':73,'completed_entries_added':0,'source_prose_reviews_added':0,
        'external_references_complete':False,'full_goal_complete':False}
    ledger['lil_opening_native_v1702']=record;ledger['latest_checkpoint']=summary
    drafts=ledger['active_source_prose_drafts'];drafts['manuscripts'].append(str(V2))
    drafts['route_record_subsets_pending']['translations/lil_opening_editorial_manuscript_v1.json']=[]
    # The older Windows-form path remains a provenance entry,not duplicate coverage.
    for key in list(drafts['route_record_subsets_pending']):
        if key.replace('\\','/')=='translations/lil_opening_editorial_manuscript_v1.json':drafts['route_record_subsets_pending'][key]=[]
    drafts['route_record_subsets_pending'][str(V2)]=ids
    drafts['note']='Earlier144 COMMON and49 native-approved Lil opening drafts remain incomplete. The opening needs external-reference mapping,registered runtime-bound integration,exact patch and full revised scene playback. Broader shared/routes/player prose remains open.'
    for unit in ledger['coverage_units']:
        if unit['id']=='Lil-Amsterdam-opening49-source-prose':
            unit.update(status='source-prose-native-font-approved;reference-map-integration-actual-pending',native_approved_manuscript=str(V2),
                native_font_proof=doc['native_font_proof'],visual_review=doc['visual_review'],relocation_research=str(reloc_path))
        if unit['id']=='all-route-scenes':unit['next']='Complete the Lil B22 external/interior reference map,registered runtime-bound integration and full revised opening/Bruges handoff. All other route scenes remain in scope.'
    temp=LEDGER.with_name('editorial_review_current_v1702_pending.json');assert not temp.exists()
    save(temp,ledger);assert read(temp)==ledger and LEDGER.read_bytes()==raw;os.replace(temp,LEDGER)
    text='# Current editorial handoff - V1702\n\n'+summary+'\n\n## Immediate next work\n\n'
    text+=('- Use translations/lil_opening_editorial_manuscript_v2.json;do not reauthor or rerun already approved49 font layouts unless prose/runtime changes. '
        'V1 and aborted1698/1699 probes remain immutable provenance. No live jobs remain:1697 emulator terminal6000;1699b font process terminal success.\n'
        '- Complete the reference map before registering resized B22. V1701 is explicitly incomplete. Native original source helpers already exist in '
        'scripts/trace_event_script_sources_v727.py and scripts/verify_script_handoff_v732.py. '
        'Their mapped CEventScriptBuffer cache selects SC block by index and hands SEventScript a PC at block+8;capacity0x2400. '
        'Verify current and expanded source through those original loaders/parent helpers,then classify the original90 command/control-flow paths and external entrants. '
        'A full current B22 resident copy is at0218F2B0 in the1697 snapshot;the stream descriptor at0218F2A0 has vtable021345B0 and PCblock+8. '
        'Do not infer ownership of neighboring stack words or classify raw pointer coincidences as callers.\n'
        '- Isolated research-only derived images can test original parser/complete revised scene before a release map is declared complete. '
        'They must preserve the current complete cumulative V1676 image,be labeled research-only,and never be handed off as a registered candidate. '
        'Registered delivery still uses the integrated builder and exact runtime/source locks. Never replace the canonical baseline or grow123040 staged payload.\n'
        '- Native literal policy does not permit literal IC/FI/FA/FO/FU collisions or I immediately followed by LF. '
        'The original FU getter updates its name cache;it is absent from this49-line opening and excluded from readonly controls after an explicit negative probe. '
        'A post-layer release must bind exact proven ARM9 before using the new profile;direct generic batching is deliberately rejected.\n'
        '- After integration,verify exact clean-input patch,startup and actual entire49-line opening,speakers,full letters,pagination and transitions through Bruges. '
        'No completion credit before these gates. Keep144 COMMON,beyond-opening routes and all other player prose in scope.\n\n'
        '## Current registered ROM\n\n'
        'V1676 experimental,all-routes-unified-v1676,out/all_routes_combined_v1676_candidate.nds;physical E:/Rota Nova translations/Generated/out/all_routes_combined_v1676_candidate.nds. '
        'SHA256337edf22ab6ee96536aadb15fb461652149b157e8d9bd1ef60db998f97608510;patch SHA2564609fc580635481203103b4be3eee4690c70bbef98e41121ab679c40484e802f. '
        'All473 manifest batches/114 accepted layers. Current parser dk4tool.patch.search_reports_editorial.current_entries. '
        'V1492 remains promoted. Canonical out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe unchanged.\n\n'
        '## Evidence\n\n'
        '- Native-approved manuscript:translations/lil_opening_editorial_manuscript_v2.json.\n'
        '- Complete clean/current source:work/analysis/lil_opening_editorial_v1694/complete_opening_source_context.json.\n'
        '- Actual-state macro proof:work/analysis/lil_opening_macro_v1698d/original_story_macro_proof.json.\n'
        '- Native fonts:work/analysis/lil_opening_fonts_v1699b/native_font_proof.json.\n'
        '- Visual review:work/analysis/lil_opening_review_v1700/visual_and_native_review.json.\n'
        '- Incomplete relocation:work/analysis/lil_opening_relocation_v1701/parity_and_native_command_research.json.\n'
        '- 73 regressions:work/analysis/lil_opening_checks_v1702/formatter_regression.xml.\n'
        '- Current1697 ordinary opening captures:E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_context_v1697_1676.\n'
        '- Last25 completed:work/analysis/editorial_completion_v1686/completion_receipt.json;registered proof work/analysis/search_reports_release_v1675/registered_release_verification.json.\n'
        '- Previous complete handoff:work/analysis/lil_opening_checkpoint_v1702/handoff_before.md.\n\n'
        '## Other persistent scope\n\n'
        'Full editorial goal active;1375 complete,1568 source/prose reviewed. Earlier144 COMMON stay open;49 Lil drafts are additional pending route records. '
        'Close-range sighting at1690 was a negative Syracuse dock-prompt test,normal No return5512;next context must be original open water. '
        '36C70 null for unloaded fleets is not inactivity proof. Armed Latina actual UI,successful Lookout shot,older750-752 caller context remain open. '
        'Do not repeat completed optional hot-spring/Search gameplay. Keep older-record re-audit queued after the full editorial goal. '
        'Graphics/all18 plaques remain separate and unfinished;accepted texture/borders do not close them. Four low-resolution Online bodies excluded,two brown marks retained. '
        'Natural-dialogue-v2,natural faithful en-US,Rafael/Joakim/Maria/Camille. sources/ read-only,no subagents authorized. '
        'Keep all generated ROMs;ROMs/screenshots on E:. Python C:/Python314/python.exe,PYTHONUTF8=1,PYTHONPATH=.;.deps. '
        'out/work-analysis junction toE;use lexical archive paths. Frozen producers/proofs use explicit successors. '
        'Earlier commit/push/promotion was fulfilled forV1492;automated tests do not authorize promotion.\n')
    handoff.write_text(text,encoding='utf-8')
    Path('docs/lil_opening_v1702_native_checkpoint.md').write_text(text.replace('# Current editorial handoff - V1702','# V1702 Lil opening native formatting checkpoint',1),encoding='utf-8')
    for name in ('docs/editorial_review_goal.md','docs/known_issues.md','docs/todo.md','docs/translation_progress.md'):
        with Path(name).open('a',encoding='utf-8') as f:f.write('\n\n## V1702 Lil opening49 native formatting\n\n'+summary+'\n\nSee [V1702 native checkpoint](lil_opening_v1702_native_checkpoint.md).\n')
    save(ROOT/'checkpoint_receipt.json',{'before_ledger_sha256':sha(raw),'after_ledger_sha256':sha(LEDGER.read_bytes()),
        'counts_unchanged':{'complete':1375,'source_prose_reviewed':1568,'COMMON_pending':144,'route_pending':49},
        'new_native_approved_rows':49,'regression_tests_passed':73,'reference_map_incomplete':True,
        'ROM_unchanged_sha256':sha(rom.read_bytes()),'no_live_jobs':True,'full_goal_complete':False,
        'evidence':{str(p):sha(p.read_bytes()) for p in (V2,approval_path,reloc_path,tests_path)},
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print('V1702 recorded:49 native-approved layouts,73 regressions and+292-byte research plan. No new completed entries or ROM;full goal active.')
