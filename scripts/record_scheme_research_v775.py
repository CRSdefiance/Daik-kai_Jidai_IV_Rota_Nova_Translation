"""Checkpoint scheme research without granting integration or completion credit."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_schemes_layout_v775_v3')
DOC=Path('docs/tavern_schemes_v775_research.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V775 Scheme research')


def main():
    v3=read(ROOT/'verification.json')
    legal=read(ROOT/'legal_name_boundary_layouts.json')
    bounds=read(ROOT/'company_name_bound.json')
    selector=read('work/analysis/tavern_scheme_selector_v775/scope_proof.json')
    plan=read('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json')
    targets=read('work/analysis/tavern_scheme_targets_v775/source_contract.json')
    assert v3['real_catalog_cases']==39730 and v3['real_catalog_findings']==0
    assert legal['count']==8704 and len(legal['findings'])==1582
    assert all(r['findings']==['weak_line_end'] for r in legal['findings'])
    assert bounds['capacity']==18 and bounds['serialized_bytes']==19 and len(bounds['cases'])==27
    assert selector['cases']==34343 and selector['table_bytes']==100 and selector['gate_bytes']==140
    assert len(targets['all400_first_target_exclusions'])==400 and len(targets['all8000_second_target_exclusions'])==8000
    assert plan['all_section_BSS_cache_and_staged_payload_geometry_exact']
    latest=read('out/editorial_review_latest.json')
    assert sha(Path(latest['path']).read_bytes())==latest['sha256']=='4b799e769123620bd4574b2dd6fc10ea38ce87d3d28ebc797a78349b1897415b'
    protected=read('work/analysis/recruitment_owned_v772/research_checkpoint.json')['protected_files_unchanged']
    for name,h in protected.items():assert sha(Path(name).read_bytes())==h
    manuscript='translations/tavern_schemes_editorial_manuscript_v3.json'
    assert v3['manuscript_sha256']==sha(Path(manuscript).read_bytes())
    assert all(not r['review']['formatting'] for r in read(manuscript)['records'])
    ledger_path=Path('translations/editorial_review_current_v1.json')
    ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==255 and ledger['records_with_source_and_prose_pass']==314
    ledger['active_source_prose_drafts']['manuscripts']=[
        'work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',manuscript]
    ledger['active_source_prose_drafts']['status']='750-752-context-unmapped;908-963-V3-prose-native-catalog-reviewed-target-closure-ownership-integration-gameplay-pending'
    ledger['active_source_prose_drafts']['note']='56 scheme drafts remain open.39730 real-name catalog layouts are clean.18-byte field-bound stress cases still have1582 weak-ending warnings;source target lists exclude the editable player faction,but full external-caller/name-pointer closure is not yet complete. No waiver or formatting approval has been granted.'
    ledger['coverage_units'][0]['next']='Close original scheme target/caller and static-name contracts;resolve applicable layout findings;revalidate existing private selector ownership;reblock/register/reconstruct and verify representative scheme gameplay. Then964 onward,750-752 and all remaining shared/routes/prose. Preserve graphics audit and older-record follow-up.'
    ledger['latest_checkpoint']='V775 scheme research:56 V3 drafts,39730 catalog layouts clean,8704 legal-field-sized stress layouts with1582 weak-ending warnings pending source reachability closure.27 editor/save/load cases prove18-byte bound;400/8000 target exclusions and20 real name getters mapped.34343 native selector/SP/register/LR cases;two-patch ARM9 research image preserves every other byte and all geometry. No new ROM or completion credit:255 complete(191 revised/64 retained),314 source/prose,59 active drafts. Full editorial and graphics goals remain unfinished.'
    item={'id':'V775-scheme-layout-source-targets-and-compact-selector',
        'documentation':str(DOC),'manuscript':manuscript,'new_editorially_completed':0,'new_ROM':False,
        'real_catalog_layouts':39730,'legal_field_boundary_layouts':8704,
        'remaining_boundary_weak_end_findings':1582,'native_selector_scope_cases':34343,
        'source_target_exclusion_cases':8400,'evidence':str(ROOT/'verification.json'),
        'remaining_gates':['Complete source target/caller and name-pointer contracts;resolve relevant layout findings',
            'Current private-storage reference revalidation and complete registered integration/patch',
            'Representative native scene/gameplay/return verification']}
    if not any(r['id']==item['id'] for r in ledger['research_checkpoints']):ledger['research_checkpoints'].append(item)
    ledger['formatting_watchlist']['latest_scheme_research']={
        'proof':str(ROOT/'verification.json'),'legal_name_stress_proof':str(ROOT/'legal_name_boundary_layouts.json'),
        'formatting_approval':False,'note':'Native text/word preservation and bounds pass;name-related weak-ending warnings remain open until applicable source inputs are proven.'}
    save(ledger_path,ledger)
    latest['latest_research_checkpoint']=str(DOC)
    save('out/editorial_review_latest.json',latest)
    DOC.write_text('''# V775 research: scheme prose, layout and original target contracts

The current playable ROM remains V773,unchanged.255 entries are editorially
complete(191 revised/64 retained);314 have source/prose drafts and59 remain active.
All56 scheme entries908-963 remain open. There is no new playable ROM,registered
scheme layer,exact scheme patch or completion credit at this checkpoint.

## English and native formatting

The V1 draft's41882 native layouts exposed308 weak-ending/orphan warnings,203
with captured catalog names. V2 improves eight confirmations as natural direct
questions;the final V3 neutral polite940 deliberately shares947's complete
confirmation. Both source voices permit that ordinary polite English. The full
V3 catalog has39730 clean native layouts.2394 changed940 cases were reexecuted
and equal the same-table947 outputs;unchanged55 records reuse pinned V2 results.

V1's75 independent full-font planes were visually reviewed. V2 has77 planes:
61 byte-identical to reviewed V1 images and16 newly reviewed changes. V3's940
planes equal the reviewed947 planes. Complete words,NULs,leading/trailing glyphs,
guard cells and four-row/35-cell bounds pass these native examples. This is
prospective native printf/literal wrapping,not production-selector gameplay.

The oversized23-byte custom name was not a proven input limit. Current V773
matches all ten clean-source editor/setter/save/load spans.27 native cases prove
an18-byte editor and19-byte serialized field,including NUL. Four maximal18-byte
names with different spaces and mixed conflict pairs give8704 additional layouts.
1582 warnings remain,all weak endings;no width or four-row overflow or orphaned
tail is present. Some warnings concern an initial A inside a player-authored
name,others prepositions before long names. None has been silently waived.
The23-byte cases remain retained stress research,not legal editor inputs.

An experiment adding from to the balancer changed no output:from was already in
the native weak-word list. It is excluded from fix claims. A native trace shows
the existing balancer can exhaust its420 first/continuation-width combinations
and use the readable fallback. No production formatter was changed.

## Source input reachability

Original first-target selection51BD4 excludes the current faction at51C24.
Forge Papers calls51A28 mode4;its51ABC comparison excludes both the current
faction and the first selected target.400 first-target and8000 second-target
comparison cases verify these branches across supplied IDs0-19. The real London
snapshot's20 name getters use mutable shared-state+1A39 only for the current
faction;every other getter returns its object's original name pointer.

These findings suggest edited-player-name warnings are outside the ordinary
scheme inputs. Complete external caller and name-pointer mutation closure still
needs verification before relying on that conclusion to close formatting. The
8400 branch cases are isolated native fragments,not8400 actual game scenes.

## Compact selector and no-growth research

The first prototype used a124-byte table and172-byte gate,which would overlap
existing status constants. It is retained as superseded research. The revised
table packs twelve-bit numeric lows/four-bit interval deltas,and rejects every
unaligned pointer before dividing exact pointer keys by16. Split intervals cover
exactly their original numeric members;no pointer range is broadened. The table
is100 bytes and gate140 bytes,inside the existing128/144-byte allocations.

34343 native cases at the actual production addresses verify all new five
narration/three confirmation tables,intermediate-address rejection,unreviewed
021182E0 rejection,prior ID/parent contracts,and register/SP/LR preservation.
ARMv5 BLX exits pop the original return address through the existing ARM exits.
Adjacent status constants and packed phrase pointers remain exact.

An exact two-patch ARM9 research image changes only the100-byte contract prefix
and140-byte gate prefix. Every other ARM9 byte,all other sections,section/BSS/
cache geometry and the123040-byte staged payload stay unchanged. This is not a
playable ROM or authorization to skip current-reference ownership revalidation.
Registered reblocking,complete copies,reconstruction patch and actual scheme
menus/portraits/dismissal/return verification remain required.

Canonical ROM,original saves,all inherited translations and the current V773 ROM
are unchanged. The graphics audit,including the18 original plaques,is separate
unfinished work. Research and review images are on E:/Rota Nova translations.
''',encoding='utf-8')
    section='''
## V775 research: scheme layouts and source target contracts

56 V3 scheme drafts have39730 clean catalog layouts. The18-byte editor bound is
verified;8704 maximal-name stress layouts leave1582 weak-ending warnings pending
full target/caller/name-pointer closure.400/8000 native target exclusions and20
real getters are mapped. A compact100-byte table/140-byte gate passes34343 native
scope/SP/register/LR cases;two exact ARM9 research patches preserve all other bytes
and geometry. No new playable ROM or completion credit:255 complete,314 source/
prose,59 drafts. Integration,patch,gameplay and broader shared/routes/prose/graphics
remain unfinished. See [V775 research](tavern_schemes_v775_research.md).
'''
    for name in ('docs/todo.md','docs/translation_progress.md','docs/known_issues.md'):
        path=Path(name)
        text=path.read_text(encoding='utf-8')
        if '## V775 research: scheme layouts' not in text:path.write_text(text+section,encoding='utf-8')
    files=[DOC,ledger_path,Path(manuscript),Path('out/editorial_review_latest.json'),
        ROOT/'verification.json',ROOT/'company_name_bound.json',ROOT/'legal_name_boundary_layouts.json',
        Path('work/analysis/tavern_scheme_selector_v775/scope_proof.json'),
        Path('work/analysis/tavern_scheme_selector_v775/two_patch_plan.json'),
        Path('work/analysis/tavern_scheme_targets_v775/source_contract.json')]
    files+=[Path('scripts')/n for n in ('probe_tavern_schemes_layout_v775.py','research_scheme_selector_v775.py',
        'prepare_scheme_runtime_v775.py','context_scheme_targets_v775.py','verify_scheme_name_bounds_v775.py',
        'verify_scheme_confirmation_v775.py','review_tavern_schemes_v775.py','record_scheme_research_v775.py')]
    for source in files:
        target=ARCHIVE/source
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
    for folder,pattern in (('tavern_schemes_layout_v775','complete_fonts_*_2x.png'),
                           ('tavern_schemes_layout_v775_v2','changed_fonts_*_2x.png')):
        for source in (Path('work/analysis')/folder).glob(pattern):
            target=ARCHIVE/'Research previews'/folder/source.name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
    save(ROOT/'research_checkpoint.json',{'completed_entries_unchanged':255,
        'source_prose_unchanged':314,'all56_scheme_formatting_gates_still_false':True,
        'protected_files_unchanged':protected,'archive':str(ARCHIVE),
        'documentation':str(DOC),'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('V775 research recorded on E;all56 scheme drafts remain open,V773 and protected files unchanged.',flush=True)


if __name__=='__main__':main()
