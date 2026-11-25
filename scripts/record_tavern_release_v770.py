"""Record complete Tavern continuation,precise gameplay scope and E archive."""

import ast
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_tavern_release_v770 import ROOT,RESEARCH,CONFIG,MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v770_candidate.nds')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/tavern_continuation_v770_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V770 Tavern continuation')
SHOTS=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V770 Tavern continuation')


def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    assert sha(source.read_bytes())==sha(target.read_bytes())


def main():
    registered=read(ROOT/'registered_verification.json');patch=read(ROOT/'patch_proof.json')
    pilot=read(ROOT/'pilot_gameplay_verification.json');game=read(ROOT/'accept_gameplay_verification.json')
    doc=read(MANUSCRIPT);config=read(CONFIG);manifest=read(ROM.with_suffix('.manifest.json'))
    digest=sha(ROM.read_bytes());assert registered['candidate_sha256']==patch['candidate_sha256']==pilot['candidate_sha256']==game['candidate_sha256']==digest
    assert patch['byte_exact_reconstruction'] and game['native_payment_receipt']['displayed_cost']==314
    actual=sorted({r['message_id'] for r in pilot['two_actual_cost_prompt_holds']+game['six_actual_round_path_holds']})
    assert actual==[852,865,870,872,874]
    protected={
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv':'d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132',
        'E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv':'d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'}
    for path,h in protected.items():assert sha(Path(path).read_bytes())==h
    latest={'path':str(ROM),'sha256':digest,'profile':manifest['profile'],
        'MESFILE_sha256':config['target_common_sha256'],'ARM9_sha256':config['target_arm9_sha256'],
        'patch_sha256':patch['patch_sha256'],'status':'experimental','manifest':str(ROM.with_suffix('.manifest.json')),
        'initial_source_pins_retained_as_V743_reference_not_overwritten':True,'details':str(DOC),'full_goal_complete':False}
    ledger=read(LEDGER)
    assert ledger['records_editorially_completed']==198 and ledger['records_with_source_and_prose_pass']==233
    save(ROOT/'editorial_ledger_before_v770.json',ledger)
    family='Tavern-cost-rounds-treasure-and-fleet-rumor-replies851-882'
    assert not any(r['id']==family for r in ledger['completed_editorial_families'])
    records=[]
    for row in doc['records']:
        n=row['message_id']
        records.append({'message_id':n,'decision':'revised-and-integrated' if row['decision']=='revise' else 'retain-wording',
            'manuscript':str(MANUSCRIPT),'source_native_context_and_complete_font_verified':True,
            'ordinary_actual_display_verified':n in actual,
            'actual_display_scope':'Actual ordinary round cost/payment/treasure path sample;other27 entries source/native/font with family sampling',
            'runtime_argument_contract':row['source_native_arguments'],'English_argument_source_indices':row['English_argument_source_indices']})
    assert sum(r['decision']=='revised-and-integrated' for r in records)==28
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':list(range(851,883)),'records':records})
    ledger['records_editorially_completed']=230;ledger['records_revised_and_integrated']=175
    ledger['retained_wordings_editorially_completed']=55
    ledger['current_integrated_candidate']={k:v for k,v in latest.items() if k not in('details','full_goal_complete')}
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'source-prose-only-context-activation-unmapped-not-integrated',
        'note':'Map actual caller/packed-script context before integration;an absent literal reference does not prove unused text.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next']='Review883 onward and remaining750-752 caller contexts;then broader shared/Lil/all routes and remaining player-facing prose. Preserve the separate graphics audit and older-record follow-up.'
    ledger['latest_checkpoint']='V770 integrates32 Tavern continuation entries:230 complete (175 revised/55 retained);233 source/prose with3 drafts.55284 paired dispatch/ABI cases,14282 new scoped outputs,38957 inherited Tavern layouts,14400 leader cases,1124 Yard/40 Port/180 controls,282 native provider fragments,263 region values and7336 full native copies pass. Eight actual holds across five IDs,cost/payment/returns/native objects and seven New Game frames pass.750-752,883 onward,wider shared/Lil/all routes/other prose and graphics remain open.'
    for finding in ledger['findings']:
        if finding['id'] in('COMMON-877-878-player-vocative-versus-target','COMMON-863-870-region-abbreviations-in-prose'):
            finding['status']='source-native-reviewed-integrated-V770-with-family-gameplay-sample'
            finding['resolution_proof']=str(ROOT/'registered_verification.json')
            finding['actual_display_scope']=actual
    ledger['formatting_watchlist']['reference_case']+=' V770 exact repaired676/677 bytes preserved;all32 new entries pass prospective and scoped native wrap/font checks,with actual cost/round/treasure glyph and normal return samples. No new actual activation of676/677 is claimed.'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',latest)
    controls=len(pilot['whole_screen_controls'])+len(game['whole_screen_controls'])
    state_pairs=len(pilot['paired_native_state_object_frames'])+len(game['paired_native_state_object_frames'])
    DOC.write_text(f'''# V770: Tavern costs,rounds,treasure tips and fleet warnings

32 entries851–882 complete this editorial family:28 revised,4 retained(865,871,872,874).
Overall230 messages are complete(175 revised/55 retained);233 have source/prose review,
with750–752 still drafts pending caller context. Wider shared prose,all route scenes,
other player-facing prose and the separate graphics audit remain unfinished. Goal active.

## Source and English

The clean Japanese and actual native caller fragments determine every argument.
877 addresses the player;878 warns that a company fleet is pursuing the player.
The two original878 argument moves are reordered[1,0],with both values preserved.
875/869 receive the admiral surname.871/872 intentionally omit a gendered address
from printed English while the original caller still supplies both arguments;
no new rank or relationship is invented. Four-captain rounds retain their source
route selection. Cost voices retain the original numeric amount with natural gold
phrasing. Fleet sentences preserve complete organization names while avoiding
Bergstrom Fleet's fleet. Heading toward a town and being docked there stay distinct.

863/870 use private full phrases:the North Sea,the Mediterranean,Africa,the Indian
Ocean,Southeast Asia,East Asia,the New World. The original eight short UI labels
remain exact. Named-item phrasing works for singular,mass and plural item names.
All prose remains one paragraph under natural-dialogue-v2 with generated wrapping.
The frozen release manuscript predates actual scene verification;this ledger and
the current gameplay reports record the later completed verification.

## Runtime and storage

55284 paired dispatch/ABI cases prove only direct851–882,the exact queued cost
parent/table,and two four-captain round tables gain the literal path. All old
memberships,register inputs,SP/LR and callee-saved registers remain exact. The
44-byte gift selector uses Thumb interworking through a source-owned8-byte stub;
the existing168-byte main gate is retained. The new prefix and region helper use
13 documented allocation tails/retired spans. Current active C strings and NULs
are preserved. A live interior Load pointer at169F48 and three live Ship-format
tail pointers were excluded;the ambiguous Online intro tail is not used.

The owned80-byte region allocation holds seven unchanged short labels and a new
private pointer table;the identical active Africa constant supplies the eighth
UI label. All native label getters,copies and48-byte metadata remain exact.
All main/autoload/overlay/ARM7 absolute references,ARM branches,ADR targets and
crossing C strings were checked for the new tails. No section,pool,staged123040-byte
payload,cache,startup or allocator limit grows. The global region getter is unchanged.

Full English needs275 more visible bytes. Repacking only blocks2–20 left eight
messages/261 bytes;extensions through21/22 still spilled. Existing blocks2–23
hold the complete2151 selections164–2314 without shortening prose or adding a block.
All3636 unselected visible strings,19 other blocks,and opaque whole1854/1865 copy
spans remain exact. All7336 cold/warm selections execute the original native copy
with explicit ARM946 alignment and complete post-NUL payload comparisons. One
exact directory digest is added;five earlier configurations use explicit identical-
output parser replays. Their frozen originals remain unchanged.

## Presentation and actual scenes

- All14282 new scoped printf/wrap outputs match the reviewed native literal-path
  matrix.115 independently decoded full font planes are covered:40 revised planes
  visually inspected and75 byte-identical to earlier inspected planes.
- All38957 prior Tavern outputs,14400 leader-name layouts,1124 Yard outputs,40 Port
  cases and180 earlier controls remain exact.282 changed-provider caller fragments
  and263 valid/invalid region values pass. No native immutable-storage writes occur.
- Two ordinary paired6001-frame cold boots decline Treat Everyone. Two further
  paired8201-frame cold boots accept it and proceed through the normal dialogue.
  No RAM fixture,savestate or original-save edit is used. The donor is copied into
  isolated save folders and its original hash is preserved.
- Eight recorded holds across852,865,872,874,870 have exact resident templates,
  original printf arguments,complete independent native glyph planes and blank-paper
  cells. All pixels outside the text plane,including Yes/No/advance controls,match.
  {controls} other whole-frame controls and{state_pairs} native state/model/object pairs match.
  Displayed314 gold corresponds to8371→8057 at the actual charge;the next ordinary
  drink deducts5. Declining preserves8371. Black Rapier's complete Mediterranean tip
  displays naturally and dismisses to the Tavern menu. Other27 IDs have native/source/
  font coverage with family gameplay sampling;individual actual activations are not claimed.
- Seven fixture-free New Game frames are byte-identical through title,captain
  selection and introduction. These are targeted automated emulator checks,not a
  full route playthrough or hardware verification. All18 original plaques remain open.

## Experimental build and exact patch

- ROM:`{ROM}`;SHA-256:`{digest}`.
- Canonical base:`out/raphael_natural_v2_accepted_base.nds`;
  SHA-256:`{protected['out/raphael_natural_v2_accepted_base.nds']}`.
- Profile:`{manifest['profile']}`. All470 batches and114 accepted layers plus the
  inherited experimental stack and new Tavern continuation are present. No promotion.
- Only`/COMMON/MESFILE.DK4` and`/__arm9__.bin` differ from V767;all other files,
  overlays,ARM7 and prior graphics remain exact.
- COMMON:`{config['target_common_sha256']}`;ARM9:`{config['target_arm9_sha256']}`.
- Patch:`{ROM.with_suffix('.xdelta')}`;SHA-256:`{patch['patch_sha256']}`.
- Clean input:`work/clean.nds`;SHA-256:`{protected['work/clean.nds']}`.
  Reconstruction matches the complete candidate byte for byte.
- Verifiers:`verify_tavern_ownership_v769.py`,`verify_tavern_runtime_v769.py`,
  `verify_tavern_outputs_v769.py`,`verify_tavern_earlier_v769.py`,
  `verify_tavern_copies_v769.py`,`verify_tavern_release_v770.py`,
  `verify_tavern_pilot_v770.py`,`verify_tavern_accept_v770.py`.
- User acceptance remains pending:cold-boot title/New Game,Tavern round cost/decline/
  purchase,treasure tips,fleet warnings and normal return. Work can continue without
  additional preview approval. Earlier Online-body exclusion,preserved brown marks,
  separate graphics audit and unclassified ordinary name slots are unchanged.

ROM,manifest,patch,evidence and six native guide-candidate screenshots are saved on E.
''',encoding='utf-8')
    section='\n\n## V770: integrated Tavern continuation\n\n32 entries complete(28 revised/4 retained):230 reviewed overall(175 revised/55 retained). Full private region phrases,faithful player-target warnings,natural cost/round/fleet English.55284 paired scope/ABI cases,14282 new layouts,all prior Tavern/leader/Yard/Port controls and7336 whole native copies pass. Eight actual holds across five IDs,314-gold payment,normal returns/native objects and seven New Game frames pass.470/114 layers,all other files/graphics retained;exact clean patch reconstructs the ROM.750-752,883 onward,wider shared/Lil/all routes/other prose and graphics remain open. Experimental;canonical/donors unchanged. See [V770 checkpoint](tavern_continuation_v770_checkpoint.md).\n'
    for name in('translation_progress.md','todo.md','known_issues.md'):
        path=Path('docs')/name;text=path.read_text(encoding='utf-8')
        assert '## V770: integrated Tavern continuation' not in text
        path.write_text(text.rstrip()+section,encoding='utf-8')
    selected=[(pilot['two_actual_cost_prompt_holds'][0]['capture'],'Cost_314_gold_V770.png')]
    for n,title in((865,'Drinks_for_everyone'),(872,'Barkeep_round'),(874,'Patron_thanks'),(870,'Treasure_Black_Rapier_Mediterranean')):
        selected.append((next(r['capture'] for r in game['six_actual_round_path_holds'] if r['message_id']==n),title+'_V770.png'))
    capture_path=Path('E:/Rota Nova translations/Generated/work/emulation_v193/tavern_round_v770_accept_v770/capture_report.json')
    selected.append((next(r for r in read(capture_path)['frames_captured'] if r['frame']==7000),'Tavern_menu_after_round_V770.png'))
    provenance=[]
    for row,name in selected:
        source=Path(row['path']);assert sha(source.read_bytes())==row['PNG_sha256']
        target=SHOTS/name;copy(source,target)
        provenance.append({'path':str(target),'PNG_sha256':row['PNG_sha256'],'source_capture':row,
            'ROM_sha256':digest,'native_unedited_capture':True,'experimental_guide_candidate_not_publication_approval':True})
    save(SHOTS/'provenance.json',provenance)
    reports=[ROOT/name for name in('registered_verification.json','patch_proof.json','pilot_gameplay_verification.json',
        'accept_gameplay_verification.json','native_integration.json','explicit_parser_replays.json')]
    save(ROOT/'proof.json',{'candidate_sha256':digest,'completed_total':230,'revised':175,'retained':55,
        'new_completed_IDs':list(range(851,883)),'actual_display_IDs':actual,'protected_hashes':protected,
        'previous_goal_turn':'progress:32 clean-source/context/prose drafts and full literal-path layout/font review',
        'this_goal_turn':'progress:owned runtime,complete copies,registered ROM/exact patch,actual scenes and six guide candidates',
        'report_hashes':{str(path):sha(path.read_bytes()) for path in reports},'goal_status':'active','full_goal_complete':False})
    producers=[Path('scripts')/name for name in('tavern_continuation_runtime_v769.py','verify_tavern_ownership_v769.py',
        'verify_tavern_runtime_v769.py','verify_tavern_outputs_v769.py','verify_tavern_earlier_v769.py',
        'prepare_tavern_common_research_v769.py','verify_tavern_copies_v769.py','prepare_tavern_release_v770.py',
        'verify_tavern_release_v770.py','verify_tavern_pilot_v770.py','verify_tavern_accept_v770.py','record_tavern_release_v770.py')]
    for path in producers:ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    files=[ROM,ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta'),DOC,LEDGER,MANUSCRIPT,CONFIG,
        Path('out/editorial_review_latest.json'),Path('translations/release_stack.json'),*producers,
        Path('dk4tool/patch/tavern_continuation_runtime.py'),Path('dk4tool/patch/tavern_continuation_editorial.py'),
        Path('dk4tool/script/common_message_table.py'),Path('scripts/build_integrated_release.py')]
    files +=[p for p in ROOT.iterdir() if p.is_file() and p.suffix in('.json','.py')]
    files +=[p for p in RESEARCH.iterdir() if p.is_file() and p.suffix in('.json','.py','.bin')]
    files +=[RESEARCH/'native_copies'/f'native_copies_block_{k:02d}.json' for k in range(41)]
    for path in files:copy(path,ARCHIVE/path.as_posix())
    capture_paths=set(pilot['capture_reports']+game['capture_reports'])
    for name in capture_paths:
        source=Path(name);copy(source,ARCHIVE/'capture_reports'/source.parent.name/source.name)
    save(ARCHIVE/'provenance.json',{'files':{p.relative_to(ARCHIVE).as_posix():sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()},
        'guide_screenshot_provenance':str(SHOTS/'provenance.json'),'goal_status':'active','full_goal_complete':False})
    for path,h in read(ARCHIVE/'provenance.json')['files'].items():assert sha((ARCHIVE/path).read_bytes())==h
    print('V770 ROM/patch/evidence and6 guide screenshots hash-archived on E.230 reviewed;3 drafts;goal active.',flush=True)


if __name__=='__main__':main()
