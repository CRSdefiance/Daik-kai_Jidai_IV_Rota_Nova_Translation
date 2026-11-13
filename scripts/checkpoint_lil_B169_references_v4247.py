"""Stage exact B169 reference/actual coverage and pins without completion credit."""
import json
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.checkpoint_lil_B169_v4231 import FAMILY
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_reference_checkpoint_v4247')
INPUT = Path('translations/lil_B169_editorial_manuscript_v4.json')
DOC = Path('translations/lil_B169_editorial_manuscript_v5.json')
APPROVAL = Path('work/analysis/lil_B169_reference_approval_v4246/approval_receipt.json')
NEXT = 'Create and validate the source-bound atomic B169 compiler with negative controls, register a cumulative profile after the complete V4204 stack, build only through build_integrated_release.py, verify the exact clean-input patch and fresh registered New Game/town startup, then integrate/complete the36 pending reviews once those gates pass. Source/native/reference/content checks are sealed; do not unnecessarily repeat them. Continue B170-B180 and every wider editorial family. Preserve V4204 as promoted main and every ROM/translation/draft/executed producer/proof/failure. V4249 and later are free.'
SUMMARY = '''V4247 seals36 Lil B169 whole-exchange reviews for registered integration:19 revisions and17 individually justified retentions. Every clean Japanese speech and fresh gloss preceded predecessor English comparison. Preserve Camille's flustered self-correction, full source-spoken Mikhail Letzel naturalist address, unwanted-touch threats, optional Julio/Ian/Fernando reactions, seven treasures/Seven Sages/location marks on differently shaped maps, hearsay and future map destiny, influential people often holding clues, conditional evil holder, sealed Proof mysteries, nearby ruins, Women follow-up, sailors' worldwide daily tales, probable payment and shared treasure-value give-and-take. Current reviewed Help title Proof of Conquest is bound; older exact-record term consistency stays open. No degree,kinship,rank,specific blow,map assembly,military-only threshold,immediate award,price,gift,source port or romance is invented.

All36 native216x64 planes,288 logical/compiled and144 stored alignment cases pass complete leading/internal/final glyphs,unique cells,zero row origins,four-row bounds and single-page behavior. Stored proofs include100 fresh parity-tail cases/25 planes and44 exact reused cases/11 planes. All five native sheets were viewed.21 source-consumer,two missing-macro and14 formatter negatives pass. Fourteen narrow row-count notes exempt no glyph,bounds,pagination,control,macro,weak-ending,orphan or blank-page issue. Three phrase-flow findings were resolved without wording waiver,authored breaks,padding or shared guard/metric changes. Every17 retained wording has an individual contextual justification.

Relocation changes only B169 from2564 to2588 stored bytes;logical2562 becomes2588. All53 source commands,twelve spans/60 target native skips,three predicates,five leaves,one later A000 and the single end2558 mapped to2584 are intact. Inverse restoration recovers every predecessor logical byte;all335 other SC2 blocks and every other file/component,ARM9,COMMON,font,graphic,cache/BSS and123040 staged bytes are exact. Both images pass336 whole original loads/cache hits and672 parent modes;three entry censuses,two poisoned-guard end decodes and36 relocated dispatches pass. Twelve source-bound name consumers retain owned scratch writes/rings and all4MiB restoration. FI5/FO2 and selectors2/6/9/20/21/76 stay source-owned. No FE,typed choice,resource,presentation or pause object is invented. Hex0029/0001 operands mean decimal41/1. V4243 explicitly supersedes three derivation metadata lists that accidentally wrote decimal29/1;all source/current/target/fixture command bytes were already exact. Preserve those historical producers/proofs and the amendment. No recruitment or earned event-flag semantics are inferred. The later older-record technical re-audit remains open.

Two fresh20001-frame Japanese/English cold boots exercise complete B169 content at initialized B22. All53 source commands plus nine original B22 init commands/four A000s are stored intact;none is omitted,flattened or forced. Both actual paths select33 speeches and53 fixture commands with all three unforced queries returning0. Every English panel matches complete native ink/gray masks and paired Japanese portrait/name/upper regions,with zero differences. FI5/FO1 actually display;the other FO belongs to Ian's offline remark. All six actual sheets,three English full screens and two Japanese counterparts were viewed. The original hex0029/0001 A000 returns[3,0] after the final give-and-take and before the single end. Source/English exits10776/10773;town-return frame10810 matches whole RGB exactly. Six of twelve relative sites are observed. Julio R67,Ian R82 and Fernando R97 have complete offline source,name,branch,stored and native coverage only;no actual display or byte-identical reuse claim. Initialized Amsterdam is a content fixture,not a source-location statement. Natural event169 eligibility,earned flag effects,complete route or hardware verification are not claimed.

Coverage remains5692 fresh rereads:5656 integrated/completed and36 pending;source/prose5695,including3839 SC2 and64 SC3;route reviewed/completed4093/4057. Historical completed decisions remain3595 revised/2061 retained. This checkpoint adds zero source/prose or completion credit. Registered cumulative V4204 remains promoted main with544 manuscript batches/114 accepted layers and its byte-exact clean-input patch. B169 is research/reference-approved and is not yet in a registered candidate. Atomic compiler/registration,cumulative build,exact clean-input patch and fresh registered startup remain. Three new research ROMs are pinned;deleted0. All jobs terminal.

Remaining B170-B180 has231 physical speeches and zero typed-choice-command leads,not a full Lil/project denominator. Every wider storyline,shared shop/town dialogue,random scene,Help and other player-facing prose stays open. Preserve COMMON750-752,canonical Maria32 SC3 B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques remain separate;retain the later older-record technical re-audit/queued0D gap. Full goal active.'''

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    assert sha(lp.read_bytes()) == read('work/analysis/editorial_handoff_verification_v4232/verified_handoff.json')['ledger_sha256']
    approval,doc = read(APPROVAL),read(DOC)
    assert approval['manuscripts'] == {str(DOC):sha(DOC.read_bytes())}
    fresh = ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release']) == (5692,5656,36)
    pending = fresh['pending_contextual_families'][0]
    assert pending['id'] == FAMILY and pending['manuscript'] == str(INPUT)
    paths = [APPROVAL,DOC,Path(__file__)]
    for key in ['reference_map','representative_proof','final_padding_proof','relocated_control_proof','termination_decode_proof','source_effect_operand_notation_amendment']:
        p = Path(doc[key])
        assert sha(p.read_bytes()) == doc[key+'_sha256']
        paths.append(p)
    paths += [Path(p) for p in approval['evidence']]
    evidence = {str(p):sha(p.read_bytes()) for p in paths}
    pending.update(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),manuscripts=approval['manuscripts'],pending=NEXT,
        actual_sampled_display_IDs=approval['actual_sampled_display_IDs'],offline_only_display_IDs=approval['offline_only_display_IDs'],new_emulator_runs=2)
    fresh.update(latest_contextual_manuscript=str(DOC),latest_pending_contextual_family=FAMILY,
        coverage_note='5692 rereads/5656 integrated/36 pending;B169 reference/native/representative approved. No additional source/prose/completion credit;registered integration remains.')
    active = ledger['active_source_prose_drafts']
    assert active['route_record_subsets_pending'][str(INPUT)] == [r['id'] for r in doc['records']]
    active['manuscripts'].append(str(DOC))
    active['route_record_subsets_pending'][str(INPUT)] = []
    active['route_record_subsets_pending'][str(DOC)] = [r['id'] for r in doc['records']]
    active.update(status='3-reviewed-COMMON-incomplete;36-Lil-B169-reference-approved-pending-registered-release',note=fresh['coverage_note'])
    for unit in ledger['coverage_units']:
        if unit['id'] == FAMILY:
            unit.update(**pending,status=doc['status'],actual_new_cold_boot_runs=2,actual_complete_native_panels=33,registered_release_pending=True)
        elif unit['id'] == 'all-route-scenes':
            unit['next'] = NEXT
    oldscope = ledger['unfinished_editorial_scope_v4231']
    assert sha(Path(oldscope['path']).read_bytes()) == oldscope['sha256']
    inventory = deepcopy(read(oldscope['path']))
    inventory.update(next_focus=NEXT)
    inventory['B169_reference_and_actual_coverage_v4247'] = pending
    inventory['B169_hex0029_operand_notation_amendment_v4243'] = dict(path=doc['source_effect_operand_notation_amendment'],sha256=doc['source_effect_operand_notation_amendment_sha256'],decimal_operands=[41,1])
    ROOT.mkdir(parents=True)
    inv = ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4247'] = {**oldscope,'path':str(inv),'sha256':sha(inv.read_bytes())}
    ledger['lil_B169_reference_reconciliation_v4247'] = dict(summary=SUMMARY,evidence=evidence,pending_family=pending,
        source_prose_reviews_added=0,completion_credit_added=0,actual_new_cold_boot_runs=2,full_goal_complete=False)
    ledger['latest_checkpoint'] = SUMMARY
    pins_path = Path('translations/rom_retention_pins.json')
    pins = read(pins_path)
    roms = [Path('out/lil_B169_reference_v4236_RESEARCH_ONLY.nds')]
    fixture = read('work/analysis/lil_B169_display_fixture_v4241/complete_effect_preserving_B22_fixtures.json')
    roms += [Path(row['research_ROM']) for row in fixture['fixtures']]
    for rom in roms:
        pins.append(dict(path=str(rom.resolve()),reason='V4247 B169 source-bound reference/content proof input;preserve every ROM under user goal;no pruning. SHA-256 '+sha(rom.read_bytes())))
    docs = [Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    for path in [lp,pins_path,*docs]:
        copy2(path,ROOT/(path.name+'.before'))
    planned = {lp:(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode(),
               pins_path:(json.dumps(pins,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()}
    section = '## V4247:36 B169 reviews reference-approved;registered integration pending\n\n'+SUMMARY+'\n\nApproval: '+APPROVAL.as_posix()+'. Unfinished scope: '+inv.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for index,path in enumerate(docs):
        first,rest = path.read_text(encoding='utf-8').split('\n',1)
        planned[path] = (('# Current editorial handoff - V4247' if index==0 else first)+'\n\n'+section+rest).encode()
    staged = ROOT/'staged'
    staged.mkdir()
    plan = []
    for index,(path,data) in enumerate(planned.items()):
        out = staged/(str(index)+'.planned')
        out.write_bytes(data)
        plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(out.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable = ['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4247',evidence=evidence,new_source_prose_reviews=0,new_completed_records=0,
        preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},new_emulator_runs=2,actual_complete_native_panels=33,
        reviewed_sheets=6,English_fullscreens=3,Japanese_fullscreens=2,ROMs_pinned=3,ROMs_deleted=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4247 staged:36 reference-approved pending records;33 actual panels/two boots;3 ROMs pinned. Registry/main/credit unchanged.')
