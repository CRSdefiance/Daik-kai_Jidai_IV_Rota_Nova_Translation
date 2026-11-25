"""Archive source/native draft progress without advancing the playable candidate."""

import ast
import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_tavern_continuation_v768 import ROOT, MANUSCRIPT, RETAINED
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/tavern_continuation_v768_research.md')
LAYOUT = Path('work/analysis/tavern_continuation_layout_v768_v2')
LEDGER = Path('translations/editorial_review_current_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V768 Tavern continuation research')


def main():
    manuscript = read(MANUSCRIPT)
    context = read(ROOT/'native_context_complete.json')
    partial = read(context['prior_provider_proof'])
    native = read(LAYOUT/'verification.json')
    latest = read('out/editorial_review_latest.json')
    assert latest['profile'] == 'all-routes-unified-v767'
    assert sha(Path(latest['path']).read_bytes()) == latest['sha256']
    assert sha(MANUSCRIPT.read_bytes()) == native['manuscript_sha256']
    assert context['prior_provider_proof_sha256'] == sha(Path(context['prior_provider_proof']).read_bytes())
    assert not context['remaining_context_gates']
    assert len(partial['original_provider_fragments']) == 2591
    assert len(context['original_fleet_provider_cases']) == 7200
    assert native['complete_native_layouts'] == 14282
    assert len(native['complete_font_planes']) == 115 and len(native['preview_sheets']) == 10
    for row in native['complete_font_planes'] + native['preview_sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    assert {r['message_id'] for r in manuscript['records']} == set(range(851,883))
    assert sum(r['decision'] == 'revise' for r in manuscript['records']) == 28
    assert {r['message_id'] for r in manuscript['records'] if r['decision'] == 'retain'} == RETAINED
    assert all(not r['review']['formatting'] for r in manuscript['records'])
    protected = {
        'work/clean.nds': 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds': '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        latest['path']: latest['sha256'],
        'E:/Rota Nova translations/Saves/hodram-istanbul-golden-cutlass-blue-oak-v474.dsv': 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'}
    for path, digest in protected.items(): assert sha(Path(path).read_bytes()) == digest
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 198
    assert ledger['records_revised_and_integrated'] == 147
    assert ledger['retained_wordings_editorially_completed'] == 51
    assert ledger['records_with_source_and_prose_pass'] in (201,233)
    ledger['records_with_source_and_prose_pass'] = 233
    ledger['records_with_source_prose_drafts'] = 233
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750,751,752,*range(851,883)],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status': 'not-integrated-not-editorially-complete',
        'groups': [
            {'native_message_IDs':[750,751,752], 'status':'source-prose-only-context-activation-unmapped'},
            {'native_message_IDs':list(range(851,883)), 'status':'source-context-prose-and-prospective-literal-layout-reviewed-runtime-gameplay-integration-pending',
             'native_layout_proof':str(LAYOUT/'verification.json')}],
        'note':'Keep caller mapping gates on750-752. New32 drafts have source/context/native literal evidence but no future dispatcher/provider or gameplay release approval.'}
    checkpoint = {'id':'V768-Tavern-cost-rounds-treasure-fleet-source-native-research',
        'documentation':str(DOC),'manuscript':str(MANUSCRIPT),'source_prose_records':32,
        'draft_revisions':28,'retained_wordings':4,'new_editorially_completed':0,'new_ROM':False,
        'original_provider_fragments':2591,'original_fleet_provider_cases':7200,
        'complete_native_layouts':14282,'independent_complete_font_planes':115,
        'all115_planes_newly_inspected_or_exact_to_previously_inspected':True,
        'evidence':str(LAYOUT/'verification.json'),'context_proof':str(ROOT/'native_context_complete.json'),
        'remaining_gates':manuscript['remaining_gates'][1:]}
    ledger['research_checkpoints'] = [r for r in ledger['research_checkpoints'] if r['id'] != checkpoint['id']] + [checkpoint]
    ledger['latest_checkpoint'] = 'V768 research reviews32 Tavern continuation entries (28 revised drafts/4 retained).2591 original provider fragments,7200 fleet contexts,original queued price binding,14282 native literal layouts and115 independent full-font planes pass;40 revised font planes visually inspected and75 byte-identical to previously inspected planes. Source/prose233;35 drafts;completed198 (147 revised/51 retained). V767 stays current;new runtime/private region provider,registered patch and actual scenes pending. Wider shared/Lil/all routes/other prose and separate graphics audit remain open.'
    ledger['coverage_units'][0]['next'] = 'Integrate and verify851-882 runtime/private full-region providers and878 argument order;resolve750-752 caller contexts;then883 onward and broader shared/Lil/all routes/other prose.'
    findings = [
        {'id':'COMMON-877-878-player-vocative-versus-target','native_message_ids':[877,878],
         'status':'source-native-reviewed-revision-drafted-not-integrated',
         'detail':'Sir/Ma\'am addresses the player.877 is a question to that player;878 warns that an organization fleet is pursuing the player. Draft878 requires exact native argument permutation[1,0],not a changed argument value.'},
        {'id':'COMMON-863-870-region-abbreviations-in-prose','native_message_ids':[863,870],
         'status':'source-native-reviewed-full-region-prose-drafted-private-provider-pending',
         'detail':'Native item region supplies N. Sea/Med./Indian/SE Asia/E Asia labels. Draft uses full Japanese-bound region phrases privately,while global map/UI abbreviations remain unchanged.'}]
    ids={r['id'] for r in findings}
    ledger['findings']=[r for r in ledger['findings'] if r['id'] not in ids]+findings
    save(LEDGER,ledger)
    section = '\n\n## V768 research: Tavern continuation\n\n32 source/context/prose drafts (28 revisions/4 retained),2591 original provider fragments,7200 fleet contexts,original queued price binding,14282 native literal layouts and115 independent full-font planes. 40 revised font planes visually inspected;75 byte-identical to previously inspected planes. Player-vocative/target errors and abbreviated region prose have reviewed fixes drafted. Runtime selector/private region provider,registered integration/patch and actual scenes remain pending. Completed198 (147 revised/51 retained);source/prose233 with35 drafts. V767 remains current;graphics audit unchanged. See [V768 research](tavern_continuation_v768_research.md).\n'
    for name in ('translation_progress.md','todo.md','known_issues.md'):
        path=Path('docs')/name; original=path.read_text(encoding='utf-8')
        if '## V768 research: Tavern continuation' in original:
            original=original.split('## V768 research: Tavern continuation')[0].rstrip()
        path.write_text(original.rstrip()+section,encoding='utf-8')
    producers=[Path('scripts')/name for name in ('context_tavern_continuation_v768.py',
        'context_tavern_queues_fleets_v768.py','review_tavern_continuation_v768.py',
        'probe_tavern_continuation_layout_v768.py','record_tavern_research_v768.py')]
    for path in producers: ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    save(ROOT/'progress_proof.json',{'previous_goal_turn':'progress:V767 photographed formatting rechecked and persistent watchlist updated',
        'this_goal_turn':'progress:32 clean-source/native-context/prose drafts and full prospective native layout/font review',
        'completed_unchanged':198,'source_and_prose_total':233,'active_drafts':35,
        'no_ROM_emitted':True,'current_playable_candidate_unchanged':latest,
        'all115_planes_newly_inspected_or_exact_to_previously_inspected':True,'protected_hashes':protected,
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'native_proof_sha256':sha((LAYOUT/'verification.json').read_bytes()),
        'goal_status':'active','full_goal_complete':False})
    files=[DOC,MANUSCRIPT,LEDGER,*producers,Path('out/editorial_review_latest.json')]
    files += [p for folder in (ROOT,LAYOUT) for p in folder.iterdir() if p.is_file()]
    archived={}
    for path in files:
        destination=ARCHIVE/path.as_posix();destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,destination);assert sha(path.read_bytes())==sha(destination.read_bytes())
        archived[path.as_posix()]=sha(destination.read_bytes())
    save(ARCHIVE/'provenance.json',{'files':archived,'research_only_no_new_ROM_or_gameplay_capture':True,
        'current_candidate':latest,'goal_status':'active','full_goal_complete':False})
    print('V768 draft/context/layout/font evidence hash-archived on E.198 completed,233 source/prose,35 active drafts;V767 remains current.',flush=True)


if __name__ == '__main__': main()
