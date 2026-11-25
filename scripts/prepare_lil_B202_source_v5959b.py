"""Prepare source-bound B202 context and four-speaker proofs without inheriting B201 roles."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B202_source_tools_v5959')
if __name__=='__main__':
    assert not ROOT.exists();prior=read('work/analysis/editorial_handoff_verification_v5958/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==prior['ledger_sha256']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    registry=read('translations/release_stack.json');profile=registry['profiles'][prior['profile']]
    assert profile['status']=='experimental' and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    rows=[derive('scripts/map_lil_B200_source_v5826.py','scripts/map_lil_B202_source_v5959.py',{
      'B200':'B202','source_v5826':'source_v5959','verification_v5822':'verification_v5958','clean_context_v5825':'clean_context_v5956',
      'all19_clean_collapse_inn_recovery_declined_reward_and_Charm_glosses.json':'all19_clean_unsolicited_book_handoff_pursuit_and_self_interested_request_glosses.json',
      'len(known)==6263':'len(known)==6308','blocks[200]':'blocks[202]','block=200':'block=202',
      'len(old)==31':'len(old)==26','[19,172,254]':'[2,18,147,157]','[19,172]':'[2,18,147,157]',
      '[0x632D,0x4301,0x4600,0x4381,0x4830,0x4735,0x6003,0x632E,0xA000,0xA000,0x4640,0]':'[0x632A,0x632A,0x4835,0xA000,0x4721,0xA000,0]',
      'lil_B199_runs_v5818':'lil_B201_runs_v5949','FE_panels=2':'FE_panels=0','ordinary_source_speeches=17':'ordinary_source_speeches=19',
      'system_FE_panels=2':'system_FE_panels=0','source_native_commands=31':'source_native_commands=26',
      'B200 bound:19 speeches/two distinct FE/17 progressive,31 commands/no FI;two source actors and actual V5816 opening snapshot.No old-English speech comparison or credit.':
      'B202 bound:19 progressive speeches/26 commands/no FE or FI;four source actors and actual V5947 opening snapshot.No old-English speech comparison or credit.'})]
    rows.append(derive('scripts/reconcile_lil_B201_voices_v5903.py','scripts/reconcile_lil_B202_voices_v5960.py',{
      'B201':'B202','voices_v5903':'voices_v5960','source_v5902':'source_v5959','all26_clean_current_complete_context_with_two_choice_labels.json':'all19_clean_current_complete_context.json',
      '[2,19,105]':'[2,18,147,157]','fresh3_actor_names':'fresh4_actor_names','len(fresh)==3':'len(fresh)==4',
      'three_source_selectors':'four_source_selectors','the three B201 actors from actual V5891 RAM':'the four B202 actors from actual V5947 RAM'}))
    rows.append(derive('scripts/prove_lil_B201_names_v5907.py','scripts/prove_lil_B202_names_v5961.py',{
      'B201':'B202','names_v5907':'names_v5961','source_v5902':'source_v5959','voices_v5903':'voices_v5960',
      'all26_clean_current_complete_context_with_two_choice_labels.json':'all19_clean_current_complete_context.json',
      'three_source_selectors':'four_source_selectors','[2,19,105]':'[2,18,147,157]','fresh3_actor_names':'fresh4_actor_names',
      "len(native['rows'])==6":"len(native['rows'])==8",'native_six_consumer_cases':'native_eight_consumer_cases',
      'six_original_progressive':'eight_original_progressive','Six source-owned':'Eight source-owned'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_preparation.json',dict(tools=rows,prior_verified_handoff='work/analysis/editorial_handoff_verification_v5958/verified_handoff.json',previous_goal_turn_classification='progress',profile=prior['profile'],no_ROM_ledger_or_registry_change=True,full_goal_complete=False))
    print('B202 exact26-command context and four-speaker current-name proofs prepared. Previous turn progress verified;no credit.')
