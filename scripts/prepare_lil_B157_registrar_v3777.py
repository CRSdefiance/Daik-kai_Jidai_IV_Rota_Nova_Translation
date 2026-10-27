"""Derive a new registrar, preserving every prior release and producer."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    src=Path('scripts/register_lil_B156_v3737.py');dst=Path('scripts/register_lil_B157_v3777.py');assert not dst.exists();t=src.read_text(encoding='utf-8')
    replacements={
        'V3692':'V3738','v3692':'v3738','V3738 stack':'V3738 stack',
        'all-routes-unified-v3738\'\nPARENT':'all-routes-unified-v3778\'\nPARENT',
        'v3737':'v3777','B156':'B157','lil_B156_layout_v4':'lil_B157_layout_v2','lil_ian':'lil_carlo',
        'editorial_manuscript_v7':'editorial_manuscript_v6',
        '48d3a0e0fa923a22e05bf7d14dcbd0625c8b9c644a24432983eb1052fe5dec45':sha(Path('translations/release_stack.json').read_bytes()),
        'editorial_handoff_verification_v3720':'editorial_handoff_verification_v3760',
        'reference_approval_v3736':'reference_approval_v3776','loader_v3726':'loader_v3766',
        '==76':'==75','positive_records=76':'positive_records=75','batches=531':'batches=532','expected_batches=531':'expected_batches=532',
        "('lost_Retainer98','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==152).update(source_selector=151))":"('lost_Carlo13','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==19).update(source_selector=20))",
        'all43_opaque_leaves_one_effect_fourteen_resources_C200_exact':'all27_opaque_leaves_two_effects_three_resources_two_C200_C281_4885_pause_exact',
        'all43_source_current_target_nonrelative_nonspeech_leaves':'all27_source_current_target_nonrelative_nonspeech_leaves',
        "('invented_pause_map','reference_map',lambda d:d['blocks'][0]['original2000_pause_and_resume_maps'].append(dict(old_offset=8,new_offset=8,source_resume=10,target_resume=10)))":"('missing_pause_map','reference_map',lambda d:d['blocks'][0]['original2000_pause_and_resume_maps'].pop()),('wrong_pause_resume','reference_map',lambda d:d['blocks'][0]['original2000_pause_and_resume_maps'][0].update(target_resume=0)),('lost_pause_gate','reference_map',lambda d:d.update(source_pause_and_resume_preserved=False))",
        'current_final_stored_macro_alignment_cases=300':'current_final_stored_macro_alignment_cases=304',
        'plus76 reviewed Lil B156 Ian tavern,harassment,rescue andrecruitment speeches;12 relative spans,three predicates,C200,ten actors,14 resource sites,all source controls andboth declared endwords preserved.':'plus75 reviewed Lil B157 Carlo bargaining, concern, grief and chosen-family invitation speeches; eight relative spans, two predicates, two C200 controls, C281,4885, source pause/picture, seven actors, two FE recollections, three resource sites, two later effects and both declared endwords preserved.'
    }
    # The predecessor's profile literal must move while its parent references move separately.
    replacements.pop('all-routes-unified-v3738\'\nPARENT')
    replacements.pop('V3738 stack')
    t=t.replace("PROFILE='all-routes-unified-v3738'","PROFILE='all-routes-unified-v3778'")
    for old in replacements:assert old in t,old
    t=re.sub('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)),lambda m:replacements[m.group()],t)
    # Overlapping generic B156 replacement must not obscure the typed formatter reference.
    assert 'lil_B157_layout_v2.py' in t and "PROFILE='all-routes-unified-v3778'" in t and "PARENT=Path('out/all_routes_combined_v3738_candidate.nds')" in t
    needle="    for label,key,edit in mutations:"
    extra="""    mutations.extend([
        ('lost_FE_selector','manuscript',lambda d:next(r for r in d['records'] if r['kind']=='system-FE').update(source_selector=2)),
        ('wrong_FE_kind','manuscript',lambda d:next(r for r in d['records'] if r['kind']=='system-FE').update(kind='progressive')),
        ('lost_FE_null_actor','relocated_control_proof',lambda d:next(r for r in d['relocated_dispatch_cases'] if r['source_selector']==254).update(resolved_actor_ID=19)),
        ('wrong_FE_native_geometry','native_font_proof',lambda d:next(r for r in d['cases'] if r['geometry']==[228,64]).update(geometry=[216,64])),
        ('wrong_FE_logical_pitch','native_font_proof',lambda d:next(r for r in d['cases'] if r['geometry']==[228,64]).update(logical_row_pitch=16)),
        ('wrong_FE_physical_pitch','native_font_proof',lambda d:next(r for r in d['cases'] if r['geometry']==[228,64]).update(physical_row_pitch=12)),
        ('incomplete_FE_input','native_font_proof',lambda d:next(r for r in d['cases'] if r['geometry']==[228,64]).update(one_native_page_consumes_complete_target=False)),
        ('invented_FE_actor','native_font_proof',lambda d:next(r for r in d['cases'] if r['geometry']==[228,64])['current_native_macro_pipelines'][0]['cases'][0].update(null_source_actor=False)),
        ('missing_FE_master_proof','native_font_proof',lambda d:d.update(source_FE_null_actor_logical228x48_physical228x64_complete_one_page_proven=False)),
        ('missing_FE_scope','native_font_proof',lambda d:d.update(FE_planes=0)),
        ('changed_C281_leaf','reference_map',lambda d:next(c for c in d['blocks'][0]['mapped_native_commands'] if c['word']==0xC281).update(new_offset=0)),
        ('changed_4885_leaf','reference_map',lambda d:next(c for c in d['blocks'][0]['mapped_native_commands'] if c['word']==0x4885).update(new_native_extent=2))
    ])
"""
    assert t.count(needle)==1;t=t.replace(needle,extra+needle)
    needle="    native=read(doc['native_font_proof']);sample=read(doc['representative_proof']);"
    extra="    visual=read('work/analysis/lil_B157_transition_review_v3775/full_screen_transition_and_all13_sheet_review.json');deps.update(s['path'] for s in visual['viewed_full_screens']);deps.add(visual['paired_town_source']['path'])\n"
    assert t.count(needle)==1;t=t.replace(needle,extra+needle)
    compile(t,str(dst),'exec');dst.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B157_registrar_derivation_v3777');assert not root.exists();root.mkdir(parents=True)
    save(root/'source_derivation.json',dict(source=str(src),source_sha256=sha(src.read_bytes()),successor=str(dst),successor_sha256=sha(dst.read_bytes()),registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),typed_FE_and_real_pause_negatives_added=True,no_registration_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Derived registrar with typed FE, real pause and C281/4885 negatives; full V3738 parent.')
