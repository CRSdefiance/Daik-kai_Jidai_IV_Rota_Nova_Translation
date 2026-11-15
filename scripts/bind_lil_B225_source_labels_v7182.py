"""Resolve the original shared Sailor branch and correct the provisional second-child gloss."""
import struct
from copy import deepcopy
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.generic_speaker_label_data_v1 import BASE,cstring
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B225_source_labels_v7182');SOURCE=Path('work/analysis/lil_B225_source_v7178/thirteen_clean_current_children_heroes_exchange_source_references.json');CONSUMER=Path('work/analysis/lil_B225_consumers_v7179/thirteen_effective_bodies26_dispatches_four_actors_eight_name_consumers.json');GLOSS=Path('work/analysis/lil_B225_clean_context_v7177/all13_clean_children_hero_play_and_remembrance_glosses_before_old_English.json');OUTPUT=Path('translations/lil_B225_clean_context_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();p,c,g=map(read,[SOURCE,CONSUMER,GLOSS]);clean,current=[NdsImage.open(s).read_file('/__arm9__.bin') for s in ['work/clean.nds',p['current_ROM']]]
    assert sha(current)==p['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a';assert sha(clean)==g['clean_ARM9_sha256']
    spans=[(0x7ED88,0x7EDD4),(0x7EE08,0x7EE20),(0x7F1F4,0x7F220)];assert all(clean[a:b]==current[a:b] for a,b in spans)
    pointer=struct.unpack_from('<I',clean,0x7EDD0)[0];assert pointer==struct.unpack_from('<I',current,0x7EDD0)[0]==0x021484D4
    a,b=[cstring(v,pointer-BASE) for v in [clean,current]];assert a[:-1].decode('cp932')=='水夫' and b==b'Sailor\0'
    rows=c['native_eight_distinct_name_consumers']['rows'];assert [(r['consumer'],r['text'],r['pointer']) for r in rows if r['actor_ID']==151]==[('progressive-nameplate','Sailor',pointer),('full-catalogue','Retainer',0x02387E48)]
    decoded=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str) for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(clean[0x7ED88:0x7EDD0],BASE+0x7ED88)]
    assert [(i['mnemonic'],i['operands']) for i in decoded[3:8]]==[('cmp','r0, #0x97'),('blt','#0x207eda8'),('cmp','r0, #0x9f'),('ldrle','r0, [pc, #0x28]'),('pople','{r4, pc}')]
    ROOT.mkdir(parents=True);proof=ROOT/'original_waterman_shared151_159_branch_not_invented_child_or_role.json'
    save(proof,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),current_consumer=str(CONSUMER),current_consumer_sha256=sha(CONSUMER.read_bytes()),clean_ARM9_sha256=sha(clean),current_ARM9_sha256=sha(current),original_code_spans=[dict(start=a,end=b,hex=clean[a:b].hex(),sha256=sha(clean[a:b])) for a,b in spans],source_progressive_getter_disassembly=decoded,original_shared_ID_interval=[151,159],literal_pointer_field=BASE+0x7EDD0,source_current_literal_pointer=pointer,source_label_hex=a.hex(),source_Japanese='水夫',current_label_hex=b.hex(),current_English='Sailor',catalogue_primary_Japanese='配下',catalogue_current_English='Retainer',source_name_fields=c['source_name_fields'],original_progressive_literal_distinct_from_catalogue_primary=True,no_inferred_second_child_identity_or_new_speaker_rank=True,source_children_phrase_does_not_authorize_global151_relabel=True,original630B_effect_not_used_to_invent_role_assignment=True,current_headers_actual_pending_and_full_catalogue_UI_unvisited=True,broader151_role_contexts_catalogue_wording_and_full207_review_open=True,no_name_asset_ROM_registry_ledger_or_credit_change=True,evidence={str(x):sha(x.read_bytes()) for x in [SOURCE,CONSUMER,GLOSS,Path(__file__)]},full_goal_complete=False))
    out=deepcopy(g);out.update(previous_clean_gloss=str(GLOSS),previous_clean_gloss_sha256=sha(GLOSS.read_bytes()),source_label_binding=str(proof),source_label_binding_sha256=sha(proof.read_bytes()),all13_initial_clean_glosses_preceded_old_English=True,prior_English_unread=False,contextual_annotation_after_current_structural_comparison=True,initial_second_child_interpretation_preserved_as_unproven_history=True,source_progressive151_waterman_not_relabelled_from_children_phrase=True)
    for r in out['records']:
        r['historical_initial_clean_gloss']=r['fresh_source_gloss'];r['prior_English_unread']=False
        if r['source_record_index']==9:r['fresh_source_gloss']='Selector97 cries that it hurts,repeats the cry,surrenders,andstammers a drawn-out retreat. The complete exchange concerns children playing heroes,but the source itself routes this speaker through the shared151-159 progressive label水夫/Sailor while the catalogue primary is配下/Retainer. Do not assert that this speaker is another child,rename the original cast,or invent a new military rank or fleet-surrender event. Preserve the comic reply andretreat;actual portrait/scene behavior still needs observation.'
        r['whole_exchange_context']+=' Original name-consumer binding now proves selector97 uses the original shared水夫/Sailor progressive branch;the initial gloss\'s assumption that it identifies the other child remains historical andunproven. Keep the children\'s-play topic without silently recasting this particular speaker or treating the catalogue配下/Retainer field as its progressive label.'
    out['whole_exchange_context']=out['records'][0]['whole_exchange_context'];save(OUTPUT,out)
    print('Original151-159 progressive branch says水夫/Sailor,distinct fromcatalogue配下/Retainer. Provisional second-child gloss corrected without changing source cast,labels orcredits;actual scene remains pending.')
