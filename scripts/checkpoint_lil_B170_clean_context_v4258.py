"""Stage the next clean-only exchange lead without new editorial or completion credit."""
import json
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_clean_checkpoint_v4258')
SOURCE = Path('work/analysis/lil_B170_clean_context_v4257/all33_complete_B170_exchange_and_fresh_glosses.json')
PRIOR = Path('work/analysis/editorial_handoff_verification_v4256/verified_handoff.json')
NEXT = 'Bind B170 current static actor25/progressive/full names,voices,source preambles,45 commands,pause,resource/presentation words,later A000,C200 and both ends;reconcile reviewed Daoist-training terminology,then compare predecessor English and author all33 speeches as one exchange under natural-dialogue-v2. Clean Japanese/gloss pass V4257 is complete;do not repeat it unnecessarily. Continue every remaining storyline/shared town/shop/random/Help/player-facing prose family. V4204 remains promoted main;V4251 is the latest verified experimental cumulative build. Preserve all ROMs,translations,drafts,executed producers/proofs/failures,graphics separation and later older-record technical re-audit.'

if __name__ == '__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json')
    ledger=read(lp)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    source=read(SOURCE)
    assert source['all33_clean_source_read_and_individually_glossed_before_predecessor_English']
    assert source['no_predecessor_English_exposed'] and source['total_editorial_objects']==33
    assert source['source_prose_or_completion_credit_added']==source['new_emulator_runs']==0
    lead=dict(path=str(SOURCE),sha256=sha(SOURCE.read_bytes()),physical_speeches=33,
        source_glosses_before_predecessor_English=True,current_English_unexposed=True,
        current_names_voices_terms_controls_native_actual_and_registered_release_pending=True,
        source_prose_or_completion_credit_added=0,source_commands=45,source_selectors=[2,25],FI=1,FO=1,
        context='Collision/argument,apology/flattery,Admiral/FO boast,Daoist training and unspecified-gender teacher,resolve and request to join;familiar female-stranger address creates no kinship.',
        next=NEXT)
    ledger['lil_B170_clean_context_only_uncredited_v4257']=lead
    summary=ledger['latest_checkpoint']+'\n\nV4258 preserves the verified B169 completion and adds a separate clean-first full-exchange pass and33 fresh source glosses for B170. Predecessor English remains unexposed;current names,voices,terms,controls,native layout,actual behavior and registered integration remain pending. This lead adds zero source/prose or completion credit and zero emulator runs. Remaining B170-B180 still contains231 physical speech leads,not a full-project denominator. B169 remains complete in V4251;V4204 remains main. Full goal active.'
    ledger['latest_checkpoint']=summary
    scope=ledger['unfinished_editorial_scope_v4255']
    assert sha(Path(scope['path']).read_bytes())==scope['sha256']
    inventory=deepcopy(read(scope['path']))
    inventory.update(next_focus=NEXT)
    inventory['next_B170_clean_context_only_uncredited_v4257']=lead
    ROOT.mkdir(parents=True)
    inv=ROOT/'unfinished_editorial_scope_inventory.json'
    save(inv,inventory)
    ledger['unfinished_editorial_scope_v4258']={**scope,'path':str(inv),'sha256':sha(inv.read_bytes())}
    docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V4255')
    for path in [lp,*docs]:
        copy2(path,ROOT/(path.name+'.before'))
    planned={lp:(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')}
    section='## V4258:B169 completed in V4251;B170 clean-first33-gloss lead\n\n'+summary+'\n\nB169 verification: '+PRIOR.as_posix()+'. B170 clean context: '+SOURCE.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for index,path in enumerate(docs):
        first,rest=path.read_text(encoding='utf-8').split('\n',1)
        planned[path]=(('# Current editorial handoff - V4258' if index==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged'
    staged.mkdir()
    plan=[]
    for index,(path,data) in enumerate(planned.items()):
        output=staged/(str(index)+'.planned')
        output.write_bytes(data)
        plan.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(output.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable=['translations/release_stack.json','translations/promoted_build.json','scripts/build_integrated_release.py','translations/rom_retention_pins.json']
    save(ROOT/'staged_receipt.json',dict(checkpoint='V4258',source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        prior=str(PRIOR),prior_sha256=sha(PRIOR.read_bytes()),preserved_release_files={p:sha(Path(p).read_bytes()) for p in stable},
        new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V4258 staged:B169 completion unchanged,B17033 clean glosses uncredited;zero new credit or emulator runs.')
