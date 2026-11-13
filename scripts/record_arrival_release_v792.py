"""Record the completed three-notice repair without closing broader audits."""

import shutil
from pathlib import Path

from dk4tool.patch.arrival_notices_editorial import ROOT,IDS
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/arrival_notices_v792_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V792 Repaired courier arrival notices')


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    proof=read(ROOT/'registered_verification.json');game=read(ROOT/'gameplay_verification.json');native=read(ROOT/'native_verification.json')
    assert len(game['holds'])==3 and len(game['strict_whole_screen_controls'])==43 and not game['unapproved_other_frame_differences']
    assert len(game['native_pairs'])==43
    assert all(r['models_exact'] and r['actors_towns_items_goods_exact'] and r['full_financial_state_exact'] for r in game['native_pairs'])
    startup=read(ROOT/'newgame_regression.json');assert len(startup['whole_screen_frame_pairs'])==7
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==444 and ledger['records_revised_and_integrated']==320
    assert ledger['retained_wordings_editorially_completed']==124 and ledger['records_with_source_and_prose_pass']==499
    completed={r['message_id'] for f in ledger['completed_editorial_families'] for r in f['records']}
    assert len(completed)==444 and not completed.intersection(IDS)
    save(ROOT/'editorial_ledger_before_v792.json',ledger)
    manuscript=read('translations/arrival_notices_editorial_manuscript_v3.json')
    family={'id':'Independent-courier-arrival-and-relationship-notices346-348','native_message_IDs':list(IDS),'records':[]}
    for row in manuscript['records']:
        family['records'].append({'message_id':row['message_id'],'decision':'revise','english':row['english'],
            'source_hex':row['source_hex'],'context':row['context'],'source_meaning':row['source_meaning'],
            'native_layout_evidence':str(ROOT/'native_verification.json'),'integration_evidence':str(ROOT/'registered_verification.json'),
            'gameplay_evidence':str(ROOT/'gameplay_verification.json'),
            'individually_activated_in_actual_scene':row['message_id'] in (347,348),
            'entry346_complete_native_consumer_and_family_sample_only':row['message_id']==346})
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=447;ledger['records_revised_and_integrated']=323
    ledger['records_with_source_prose_drafts']=499
    active=ledger['active_source_prose_drafts'];assert len(active['native_message_IDs'])==55
    active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    active['manuscripts']=[p for p in active['manuscripts'] if 'arrival_notices' not in p]
    assert len(active['native_message_IDs'])==52
    active['status']='750-752-context-unmapped;1097-1145-CScheme-virtual-name-menu-scope-open'
    active['note']='Arrival346-348 complete with native coverage and actual family samples;346 not individually activated.49 diplomatic entries retain six-type eligibility,cancellation,registration and representative delivery evidence. Actual CScheme virtual-name menu scope remains;750-752 context remains unmapped.'
    current={'path':proof['candidate'],'sha256':proof['candidate_sha256'],'profile':proof['profile'],
        'MESFILE_sha256':proof['COMMON_sha256'],'ARM9_sha256':proof['ARM9_sha256'],'patch_sha256':proof['patch_sha256'],
        'manifest':str(Path(proof['candidate']).with_suffix('.manifest.json')),'status':'experimental',
        'details':str(DOC),'supplemental_verification':str(ROOT/'gameplay_verification.json'),
        'remaining_in_this_registered_batch':'Arrival family complete under native coverage and representative gameplay. Earlier49 diplomatic entries still need CScheme virtual-name-menu scope closure;wider prose remains unfinished.',
        'full_goal_complete':False}
    ledger['current_integrated_candidate']=current
    summary=('V792 completes three revised independent arrival/relationship notices346-348,removing the split R/elations defect. '
        'Full V788 stack,470 batches and114 accepted layers remain. Native checks cover3668 modal IDs,84 other-parent controls,'
        '49 faction/number layouts,seven full-font planes and936 complete warm/cold copies across six repacked blocks. '
        'Actual corrected347 twice and348 once match complete glyphs/blank paper/bounds;43 other whole screens and43 complete '
        'financial/model/actor/town/item/goods/courier pairs match V788,with original fees,pact cancellation,goodwill and town return. '
        'Seven ordinary New Game/first-story whole frames pass;the clean-input patch reconstructs exactly. '
        '447 complete(323 revised/124 retained),499 source/prose,52 pending. Wider editorial and separate graphics goals remain active.')
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Close original CScheme virtual-name-menu consumer scope for49 integrated diplomatic entries;then Palace1146 onward,750-752,all routes and remaining prose. Continue independent-notice and left-margin checks.'
    ledger['coverage_units'][0]['completed_families'].append('Independent-courier-arrival-and-relations346-348')
    for finding in ledger['findings']:
        if finding['id']=='COMMON347-348-split-Relations-across-independent-notices':
            finding['status']='source-native-reviewed-integrated-and-actual-family-verified-V792'
            finding['repaired_gameplay_proof']=str(ROOT/'gameplay_verification.json')
    watch=ledger['formatting_watchlist']
    watch['requirements']=[s.replace('actual347/348 is a confirmed unfinished example','actual347/348 was corrected and actual-display verified in V792') for s in watch['requirements']]
    watch['reference_case']+=' V792 preserves repaired676/677 bytes;new modal scope changes only346-348. No fresh shop676/677 activation claimed.'
    save(ROOT/'user676_677_preserved.json',{'candidate_sha256':proof['candidate_sha256'],
        'logical_bytes_exact_to_V788':True,'modal_scope_delta_only346_348':True,
        'earlier_actual_shop_capture':'E:/Rota Nova translations/Generated/work/emulation_v193/product_pitches_v747_new/frame_004200_cold_boot.png',
        'no_fresh_shop_activation_claim':True,'formatting_watchlist_remains_ongoing':True})
    watch['latest_reference_proof']=str(ROOT/'user676_677_preserved.json')
    checkpoint={'id':'V792-independent-arrival-notices-complete','documentation':str(DOC),'new_editorially_completed':3,
        'actual_complete_holds':3,'strict_whole_screen_controls':43,'native_state_pairs':43,'full_goal_complete':False}
    ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER,ledger);save('out/editorial_review_latest.json',current)
    DOC.write_text(f'''# V792: independent courier arrival and relationship notices

## Experimental combined candidate

ROM: {proof['candidate']}

SHA256: {proof['candidate_sha256']}

Profile: {proof['profile']}. The neighboring manifest records the complete470
inherited batches and114 accepted layers. This extends V788 through the registered
builder. Canonical parent remains out/raphael_natural_v2_accepted_base.nds,
SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
Only /COMMON/MESFILE.DK4 and /__arm9__.bin change from V788. Every other ROM file,
component,earlier graphic and route remains exact. All prior profiles and pinned
dependencies are retained. The source COMMON directory parser is unchanged;
this layer has its own exact-version reader. No canonical promotion,commit or push.

Patch: {proof['patch']}

Patch SHA256: {proof['patch_sha256']}

Applying it to the clean Japanese ROM SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d
reconstructs the candidate byte for byte. ROM/patch/manifest reside on E through
the existing out junction. User acceptance is still required for canonical promotion.

## Prose and original display path

Three natural-dialogue-v2 paragraphs restore independent original meanings:

| ID | Final wording | Source intent |
| --- | --- | --- |
|346|%s refused the letter.|Recipient refuses receipt of the letter.|
|347|%s received the letter.|Letter arrived;does not imply agreement to its proposal.|
|348|Relations rose by %s points.|Relationship score increased by the unchanged native amount.|

V791 actual347 placed a stray R after the delivery notice while348 began elations.
These independent selections have intervening recipient responses. No letter is
borrowed between records. Earlier V791 wording for346 was retained at draft time;
final V792 uses a natural standalone revision. All three therefore count as revised.
Draftv1 is preserved;reviewed v2 records the refinement,and v3 is the production
manuscript with complete per-record review gates. No translator-authored breaks
or alignment spaces are added;the compiler supplies the native guard.

These are system modal notices:original546B8 enters54774 with parent546E8.
They do not use the actor dialogue selector. The existing128-byte modal allocation
is replaced without growth,retaining every older selection. Only346-348 use the
already integrated balanced paragraph helper. Existing prompts keep their previous
helper and byte-exact output. Original macro expansion/native printf remain intact.
The new wrapper uses ARMv5 ARM/Thumb interworking and reserves a stable default-width
argument separately from its240-byte buffer,with aligned stack space. No section,
BSS,arena,cache or123040-byte staged payload grows or changes. COMMON is repacked
inside existing blocks0-5;all3665 other logical strings and opaque payloads remain.

## Evidence

- All3668 modal IDs:only346-348 gain wrapping;3665 preserve original output.
-84 other-parent controls and12 old empty/failure controls preserve original behavior.
-49 original printf/layout cases cover all supplied real faction names,a disclosed
23-character stress name,and full-width numeric amounts0,1,5,9,10,99,100.
- Seven independent complete native font planes are visually reviewed;whole words,
leading/trailing letters,left margins,all row boundaries and bounds pass.
-936 complete original warm/cold copies cover every entry in repacked blocks0-5.
Unselected blocks and their directory/offset metadata are unchanged;earlier V788
full-copy evidence remains the source for those unchanged selections.
- Three connected original modal consumers bind actual Castor Co./numeric getters,
execute original printf/macro expansion and the new wrapper,and stop before SDK
widget construction. Only COMMON lookup selection is bridged in that isolated
consumer probe;complete native copies are independently verified.
- Actual20000-frame cold boot replays the exact V791 input/fixture journal. Revised
347 at17200/18000 and348 at19200 match complete independent font/blank-paper planes
and every pixel outside the text region. No blink exclusions or phase windows.
-43 other whole screens match V788 exactly. All43 paired financial/model/actor/
town/item/goods/courier snapshots match. Original two1000-coin fees,two1-coin stays,
192 calendar ticks,pact cancellation,two inactive couriers and goodwill+5 remain.
Final cash6369;normal town return20000. Original DSV stays exact.
- Seven ordinary fresh New Game/first-story whole frames match V788 exactly. The
inherited verifier console says V780;the saved proof correctly identifies V788 as
its supplied reference. This is targeted emulator coverage,not a full route/hardware
playthrough.346 has complete native coverage and this family sample;it was not
individually activated in the emulator.

## Failed research and corrected assumptions

An initial probe omitted the staged pool needed by the original fallback. The first
Thumb wrapper also exposed the original helper's return-state width convention;
its argument initially shared the output buffer and altered an earlier paragraph.
The exhaustive comparison rejected it. The final separate argument/buffer preserves
all old outputs. Existing balanced formatting is reused only for the three new
notices;greedy drafts with isolated letter/name suffixes were rejected. The native
bound is the established two-million-instruction limit for balanced retries.
Oversized negative tests allocate a separate guard after their full old expander
output;they do not approve overlong production paragraphs. No failed probe is
counted as final evidence.

## Progress and follow-up

447 editorially complete(323 revised/124 retained),499 source/prose reviewed,52
pending750-752 and1097-1145. These52 are only already reviewed pending entries;
they are not the entire project's remaining text. CScheme virtual-name-menu
consumer scope remains open. Palace1146 onward,other shared text,all routes,
help/other prose and the separate graphics audit remain unfinished.18 original
plaques remain in audit;Online low-resolution screenshot bodies stay excluded and
brown comic marks preserved. Rafael/Joakim/Maria/Camille remain locked. Revisit
older record-based checks after the full editorial goal completes.

The user's repaired676/677 cooking/fashion pitches remain exact to V788. Their
earlier V747 actual screenshot remains evidence;no fresh shop activation is claimed.
The independent-notice/left-margin/complete-glyph watchlist stays active.

## Reproduction and user check

Registered builder: scripts/build_integrated_release.py --profile
all-routes-unified-v792 --out out/all_routes_combined_v792_candidate.nds.
Verifiers: verify_arrival_native_v792.py,verify_arrival_copies_v792.py,
verify_arrival_consumer_v792.py,verify_arrival_release_v792.py,
replay_arrival_delivery_v792.py and verify_arrival_gameplay_v792.py. Registration
and record scripts are one-shot. Exact reports,plans,hashes and archive receipts
are under work/analysis/arrival_notices_v792 on E. Two corrected actual screenshots
are saved as Guide candidates with fixture provenance. User testing should cold-boot
New Game,check ordinary town UI and a letter arrival/relationship notice. All test
processes are terminal;the full editorial goal stays active.
''',encoding='utf-8')
    heading='## V792: independent courier-status prose and formatting repaired'
    for name in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        p=Path(name);text=p.read_text(encoding='utf-8');assert heading not in text
        p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V792 checkpoint](arrival_notices_v792_checkpoint.md).\n',encoding='utf-8')
    shots=[]
    for frame,label in ((17200,'V792 Letter delivered'),(19200,'V792 Relations gained')):
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193/arrival_v792_delivery')/f'frame_{frame:06d}_navigation.png'
        dest=Path('E:/Rota Nova translations/Screenshots/Guide candidates')/(label+'.png');dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,dest);assert sha(source.read_bytes())==sha(dest.read_bytes())
        shots.append({'source':str(source),'copy':str(dest),'sha256':sha(dest.read_bytes()),
            'actual_ROM_framebuffer':True,'synthetic_qualification_and_deadline_acceleration_disclosed':True,
            'earned_prerequisites_travel_or_full_route_not_claimed':True})
    save(ROOT/'guide_candidates.json',{'screenshots':shots,'gameplay_proof':str(ROOT/'gameplay_verification.json')})
    assert len({r['message_id'] for f in ledger['completed_editorial_families'] for r in f['records']})==447
    save(ROOT/'checkpoint.json',{**checkpoint,'summary':summary,'completed':447,'source_prose':499,'pending':52,
        'candidate':current,'previous_turn_classification':'progress:two completed original courier lifecycles and new split-word defects/source drafts',
        'this_turn_classification':'progress:three complete revised notices integrated,patched and native/actual verified',
        'all_processes_terminal':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    paths=[p for p in ROOT.glob('*.json') if p.name!='archive_receipt.json']
    paths += [DOC,LEDGER,Path('dk4tool/patch/arrival_notices_editorial.py'),Path('scripts/build_integrated_release.py')]
    paths += list(Path('scripts').glob('*arrival*v792.py'))
    paths += list(Path('translations').glob('arrival_notices_editorial_*.json'))
    paths += list((ROOT/'native_copies').glob('*.json'))+[ROOT/'all_fonts_2x.png']
    receipts=[]
    for p in paths:
        dest=ARCHIVE/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        assert sha(p.read_bytes())==sha(dest.read_bytes())
        receipts.append({'source':str(p),'copy':str(dest),'sha256':sha(p.read_bytes())})
    receipt={'copies':receipts,'all_copies_SHA256_exact':True};save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'V792 complete for3 notices;447 total,52 pending. {len(receipts)} artifacts and two guide candidates saved. Full goal active.',flush=True)


if __name__=='__main__':main()
