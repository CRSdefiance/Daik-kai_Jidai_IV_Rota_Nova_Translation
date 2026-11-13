"""Close ordinary name-consumer scope and the verified diplomatic prose family."""

import shutil
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.arrival_notices_editorial import current_entries
from dk4tool.patch.item_diplomacy_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/scheme_consumer_scope_v793')
DOC=Path('docs/diplomacy_scope_v793_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
IDS=tuple(range(1097,1146))
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V793 Diplomatic prose and ordinary name-consumer closure')


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    scope=read(ROOT/'source_and_native_scope.json')
    assert scope['ordinary_selectors_have_no_discovered_CSchemes_kind13_source']
    assert len(scope['all201_original_map_object_provider_cases'])==201 and len(scope['twelve_original_fixed_kind_list_prefixes'])==12
    assert scope['dynamic_map_loop_three_real_virtual_providers_kind_getters_index_getters_encoder_execute']
    rom=NdsImage.open('out/all_routes_combined_v792_candidate.nds');old=NdsImage.open('out/all_routes_combined_v788_candidate.nds')
    c,a=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    oc,oa=old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin')
    entries,prior=current_entries(c,a),previous_entries(oc,oa)
    blocks,old_blocks=IlnkContainer.parse(c).blocks,IlnkContainer.parse(oc).blocks
    used=sorted({entries[n].block for n in IDS})
    assert all(entries[n]==prior[n] for n in IDS)
    assert all(blocks[b]==old_blocks[b] for b in used)
    assert a[0x53CB0:0x5408C]==oa[0x53CB0:0x5408C]
    assert a[0x93D28:0x93D6C]==oa[0x93D28:0x93D6C]
    for p in ('work/analysis/item_diplomacy_runtime_v785/runtime_plan.json',
              'work/analysis/item_diplomacy_context_v786/nominal_provider_research.json'):
        for r in read(p)['patches']:
            at=r['address']-0x02000000;data=bytes.fromhex(r['target_hex'])
            assert a[at:at+len(data)]==oa[at:at+len(data)]==data
    assert a[0x9145C:0x91460]==oa[0x9145C:0x91460]==bytes.fromhex('1800a0e3')
    paths=[Path(p) for p in (
        'work/analysis/item_diplomacy_integration_v788/registered_verification.json',
        'work/analysis/item_diplomacy_integration_v788/production_layout/verification.json',
        'work/analysis/item_diplomacy_integration_v788/consumer_routing.json',
        'work/analysis/item_transactions_v789/qualified_outcomes.json',
        'work/analysis/item_transactions_v789/daily_update_control.json',
        'work/analysis/letter_eligibility_v790/native_eligibility_verification.json',
        'work/analysis/letter_eligibility_v790/actual_letter_dialogs.json',
        'work/analysis/letter_eligibility_v790/cancellation_outcomes.json',
        'work/analysis/letter_delivery_v791/delivery_verification.json',
        'work/analysis/arrival_notices_v792/gameplay_verification.json',
        'work/analysis/scheme_name_width_v787/native_width_verification.json',
        'work/analysis/scheme_name_width_v787/selector_entry_closure.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    doc=read('translations/item_diplomacy_editorial_manuscript_v2.json')
    rows=[r for r in doc['records'] if r['message_id'] in IDS]
    assert len(rows)==49 and sum(r['decision']=='revise' for r in rows)==36
    assert sum(r['decision']=='retain' for r in rows)==13
    assert all(all(r['review'][g] for g in ('source','context','localization','naturalness','formatting')) for r in rows)
    proof={'candidate_sha256':sha(Path('out/all_routes_combined_v792_candidate.nds').read_bytes()),
        'completed_IDs':list(IDS),'revised':36,'retained':13,'unchanged_COMMON_entries_and_blocks_since_V788':used,
        'private_runtime_and_nominal_provider_bytes_exact':True,'earlier_source_native_actual_evidence_hashes':evidence,
        'ordinary_virtual_name_consumer_scope':str(ROOT/'source_and_native_scope.json'),
        'actual_document_object_GPU_menu_not_claimed':'No ordinary discovered selector produces class13. Native row/width proof remains CPU coverage;actual paragraph substitutions for all six types are verified in V790.',
        'family_sample_not_every_voice_or_branch_individually_activated':True,
        'whole_game_full_route_and_graphics_completion_not_claimed':True,'full_goal_complete':False}
    save(ROOT/'diplomacy_family_completion.json',proof)
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==447 and ledger['records_revised_and_integrated']==323
    assert ledger['retained_wordings_editorially_completed']==124 and ledger['records_with_source_and_prose_pass']==499
    completed={r['message_id'] for f in ledger['completed_editorial_families'] for r in f['records']};assert not completed.intersection(IDS)
    save(ROOT/'editorial_ledger_before_v793.json',ledger)
    family={'id':'Guild-diplomatic-drafting-and-letters1097-1145','native_message_IDs':list(IDS),'records':[]}
    for row in rows:
        family['records'].append({'message_id':row['message_id'],'decision':row['decision'],'english':row['english'],
            'source_meaning':row['source_meaning'],'context':row['context'],'source_hex':row['source_hex'],
            'native_and_gameplay_family_evidence':str(ROOT/'diplomacy_family_completion.json'),
            'full_source_native_coverage_and_actual_consumer_family_samples':True,
            'individual_voice_activation_not_claimed':True})
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=496;ledger['records_revised_and_integrated']=359
    ledger['retained_wordings_editorially_completed']=137
    active=ledger['active_source_prose_drafts'];assert len(active['native_message_IDs'])==52
    active['native_message_IDs']=[n for n in active['native_message_IDs'] if n not in IDS]
    assert active['native_message_IDs']==[750,751,752]
    active['manuscripts']=[p for p in active['manuscripts'] if 'item_diplomacy_editorial' not in p]
    active['status']='750-752-context-unmapped'
    active['note']='All76 integrated item/diplomacy entries are complete under source/native coverage and actual consumer-family samples.750-752 remain source/prose drafts awaiting mapped context. Wider shared text,all routes and other prose are not yet reviewed.'
    summary=('V793 closes ordinary generic name-consumer scope through366 original RTTI types,all constructor/typed-ID reference edges,'
        '201 native map-provider cases,12 fixed-kind list prefixes,three item-prefix cases and the original mixed-map loop. '
        'Ordinary discovered selectors produce items,factions,fleets,towns or village records;no class13 document list is supplied. '
        'The pending virtual-menu gate is resolved by this source scope,without invented GPU playback. All six actual nominal dialogue '
        'phrases and diplomatic eligibility,cancellations,registration and representative delivery were previously verified and remain '
        'exact in V792.49 diplomatic entries complete(36 revised/13 retained);496 total(359 revised/137 retained),499 source/prose,'
        'three reviewed pending750-752. Class-number erratum:items are3,actors1. V792 ROM/exact patch unchanged;wider editorial and separate graphics audits remain active.')
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['completed_families'].append('Guild-diplomatic-drafting-and-letters1097-1145')
    ledger['coverage_units'][0]['next']='Review Palace1146 onward against clean Japanese and original native context;map750-752,then all routes and remaining player-facing prose. Continue formatting watchlist and preserve separate graphics audit.'
    ledger['native_selector_class_number_erratum']={'evidence':str(ROOT/'source_and_native_scope.json'),
        'correction':'Earlier discussion identifying class3 as actor was incorrect. Executed original manager vtables give actor1,item3,company4,town5,fleet8,scheme13,village-map-record19. Earlier source fragments at4AB50 and their class3 lists are item selectors.',
        'no_ROM_or_translation_change':True}
    ledger['current_integrated_candidate'].update({'details':str(DOC),'supplemental_verification':str(ROOT/'diplomacy_family_completion.json'),
        'remaining_in_this_registered_batch':'V792 arrival family and inherited76 item/diplomacy entries complete under full native coverage and actual family samples. Three reviewed contexts750-752 and wider prose remain unfinished.',
        'latest_research_checkpoint':str(DOC)})
    ledger['research_checkpoints'].append({'id':'V793-diplomacy-family-and-ordinary-consumer-scope-closed',
        'documentation':str(DOC),'new_editorially_completed':49,'new_ROM_or_prose_changes':False,'full_goal_complete':False})
    save(LEDGER,ledger);save('out/editorial_review_latest.json',ledger['current_integrated_candidate'])
    DOC.write_text('''# V793: diplomatic prose and ordinary name-consumer scope

## Completion accounting

The49-entry diplomatic drafting/letter family1097-1145 is editorially complete:
36 revisions and13 retained wordings. All76 item/diplomacy entries1070-1145 now
have source/native coverage and actual consumer-family samples. Total496 complete
(359 revised/137 retained),499 source/prose reviewed,three reviewed drafts750-752.
These three are not the entire project's remaining text. Palace1146 onward,
other shared text,all routes,help/other prose and the separate graphics audit
remain unfinished. The full goal stays active.

V792 ROM/profile/exact clean-input patch remain current and byte-identical.
No new ROM,patch,prose or canonical promotion is created here. All49 COMMON
records,complete backing blocks,Guild wrappers,private runtime,nominal providers
and24-cell class width are exact to their verified V788 production components.
V792's unrelated three-notice repair and its actual samples remain intact.

## Why the remaining menu gate is closed

The unresolved gate was actual SDK/GPU display of a CScheme class13 name list.
The complete discovered ordinary constructor/reference paths have now been
traced to their supplied typed IDs:

| Producer | Source-bound kind |
| --- | --- |
|4AB40 item-list prefix|3,item.|
|406E4 existing fleet list|8,fleet.|
|9AC54 fixed-kind list|8,fleet.|
|9AEF4 fixed-kind list|4,faction/company.|
|9B144 fixed-kind list|5,town.|
|96704 dynamic map-hit list|8 fleet,5 town,19 village-map record.|
|97910 default map target|8,fleet.|

All six original selector-constructor edges,three9B36C inputs,the sole96704
caller and all seven21478 typed-ID producer calls are accounted for in clean
source and V792. There are no additional discovered ARM,Thumb,ADR or callable
pointer leads into those factories. One current unaligned21478 pointer pattern
is executed through the original Giant Squid class initializer:it overlaps the
aligned creature-name pointer and an unchanged adjacent numeric field. Its native
consumer returns Giant Squid. It is not discarded solely for being unaligned.

The source dynamic_cast in96A00 admits CSeaAreaMapObject and exactly its three
derived classes CSeaAreaFleetView,CSeaAreaTownView,CSeaAreaVillageView. The full
366-object RTTI graph has all inheritance edges resolved,including standard and
structure/interface roots. Every base-reference lead is accounted for. Route
sprites and area views are outside this family. Original providers execute for
all63 fleet,114 town and24 village-cache indices(201 cases),returning native kinds
8,5,19 with exact indices. The base provider returns NULL. All8MiB bytes outside
declared CPU object/call-stack fields remain exact. Source-filtering source spans
and RTTI remain unchanged in V792.

Twelve original fixed-list prefixes verify zero,one,20 and21 supplied entries
and the native20-entry cap. Three original item prefixes verify zero,one and218
declared CPU item inputs. The actual dynamic-map loop executes all three virtual
providers,kind/index getters and the original21478 encoder. The default map-target
prefix executes its original fleet selection and kind8 encoding. These are native
CPU field tests,not real inventory,map menu playback or quest progression.

No ordinary discovered selector supplies a kind13 document object. Therefore an
actual document-object GPU list is not available on these normal source paths.
No injected/debug/corrupted list is used to claim normal gameplay. The native
CScheme width/bitmap proofs remain useful CPU evidence for that class API;their
SDK/GPU menu playback is not claimed. This scope is ordinary static/runtime-source
closure,not a proof about arbitrary indirect jumps or memory corruption.

## Actual prose evidence retained

V788 source review and production checks cover76 complete paragraphs,2774 native
layouts,76 independent font planes,2080 original voice selections and1260 Guild
wrapper bindings. V789 actual registration/decline/fee tests and controlled daily
input proofs,V790 all-six-type eligibility/cancellations/complete nominal phrases,
V791 two original courier arrivals,and V792 exact revised arrival/return/startup
proofs remain the actual scene evidence. All six document phrases are actually
displayed in their proper dialogue consumers. Delivery,eligibility and virtual
name-list scope are now closed at their respective evidence levels.

This completes the diplomatic family under complete native coverage and actual
consumer-family sampling. It does not claim individual emulator activation of
every voice or branch,earned qualifications,all diplomatic outcomes,a full route
or physical-device verification. Original conversation RNG divergence between
V783/V788 remains documented;source-scope closure does not waive it or claim
identical uncontrolled daily objects. The later V788/V792 paired arrival run
does preserve all43 observed full native object pairs exactly.

## Class-number correction

An earlier note called class3 actors. Original native manager vtables now prove
actor1,item3,company4,town5,fleet8,scheme13,village-map-record19. Thus4AB50's
literal3 identifies an item selector. The earlier actor-label interpretation is
superseded. This is a source-classification correction;no English/name/ROM
change is required. Rafael,Joakim,Maria,Camille remain locked.

## Preserved open work and reproduction

The18 original plaques remain in the separate graphics audit. Online low-resolution
screenshot bodies remain excluded and brown comic marks retained. Left margins,
complete first/last letters,independent selection fragments,bounds and pagination
remain in every prose review. Revisit older record-based checks after the full
editorial goal completes. Continue with Palace1146 onward and the unresolved
750-752 contexts before the route-wide and remaining-prose passes.

Reproduce scripts/verify_scheme_consumers_v793.py,then inspect
work/analysis/scheme_consumer_scope_v793/source_and_native_scope.json and
diplomacy_family_completion.json. The latter binds every inherited evidence file
by SHA256. complete_diplomacy_scope_v793.py is one-shot. Evidence,producers and
ledger are archived on E with exact-copy receipts. No new guide screenshot,
commit or push is made. All test processes are terminal.
''',encoding='utf-8')
    heading='## V793: diplomatic prose and ordinary name-consumer scope complete'
    for name in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        p=Path(name);text=p.read_text(encoding='utf-8');assert heading not in text
        p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V793 checkpoint](diplomacy_scope_v793_checkpoint.md).\n',encoding='utf-8')
    save(ROOT/'checkpoint.json',{'summary':summary,'completed':496,'source_prose':499,'pending_reviewed':3,
        'candidate':ledger['current_integrated_candidate'],'new_editorially_completed':49,
        'previous_turn_classification':'progress:three arrival notices repaired,integrated and actual verified',
        'this_turn_classification':'progress:ordinary virtual consumer scope resolved and49 diplomatic entries completed',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    paths=[p for p in ROOT.glob('*.json') if p.name!='archive_receipt.json']+[DOC,LEDGER,
        Path('scripts/verify_scheme_consumers_v793.py'),Path('scripts/complete_diplomacy_scope_v793.py')]
    copied=[]
    for p in paths:
        dest=ARCHIVE/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        assert sha(p.read_bytes())==sha(dest.read_bytes())
        copied.append({'source':str(p),'copy':str(dest),'sha256':sha(p.read_bytes())})
    receipt={'copies':copied,'all_copies_SHA256_exact':True};save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'49 diplomatic entries complete;496 total,three reviewed drafts. {len(copied)} artifacts archived;V792 ROM unchanged;full goal active.',flush=True)


if __name__=='__main__':main()
