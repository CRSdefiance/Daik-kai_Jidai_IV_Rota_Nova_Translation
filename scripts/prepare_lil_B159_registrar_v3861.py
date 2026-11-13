"""Derive registration after full V3819, with source-present controls and explicit native/name proof negatives."""
from pathlib import Path
import ast,re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/register_lil_B156_v3737.py');q=Path('scripts/register_lil_B159_v3861.py');assert not q.exists();t=p.read_text(encoding='utf-8');tree=ast.parse(t);removed=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='mutations' for a in node.targets):
            for elt in node.value.elts:
                if elt.elts[0].value in ['missing_C200','changed_C200_request','changed_C200_write']:removed.append(ast.get_source_segment(t,elt))
    assert len(removed)==3
    for text in removed:assert t.count(text+',')==1;t=t.replace(text+',','')
    assert t.count("PROFILE='all-routes-unified-v3738'")==1;t=t.replace("PROFILE='all-routes-unified-v3738'","PROFILE='all-routes-unified-v3862'")
    oldhash='48d3a0e0fa923a22e05bf7d14dcbd0625c8b9c644a24432983eb1052fe5dec45';assert oldhash in t
    description='Full V3819 cumulative stack plus41 reviewed Lil B159 Samwell elephant/vendor/cooking provocation and recruitment speeches;24 relative spans,six predicates,five actors,four resources,one effect,all source presentation controls andboth declared endwords preserved. Original Samwell Khan progressive label separately verified;no name asset edit.'
    t,n=re.subn(r"description='Full V3692[^']*'",'description='+repr(description),t);assert n==1
    changes={'lil_B156_editorial_v1':'lil_B159_editorial_v2','B156':'B159','v3737':'v3861','v3692':'v3819','V3692':'V3819','lil_ian':'lil_samwell','manuscript_v7':'manuscript_v5','lil_B156_layout_v4':'lil_B159_layout_v3',oldhash:sha(Path('translations/release_stack.json').read_bytes()),'editorial_handoff_verification_v3720':'editorial_handoff_verification_v3844','reference_approval_v3736':'reference_approval_v3860','loader_v3726':'loader_v3850','==76':'==41','positive_records=76':'positive_records=41','batches=531':'batches=534','expected_batches=531':'expected_batches=534',"('lost_Retainer98','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==152).update(source_selector=151))":"('lost_Samwell16','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==22).update(source_selector=20))",'all43_opaque_leaves_one_effect_fourteen_resources_C200_exact':'all23_opaque_leaves_one_effect_four_resources_no_C200_or_pause_exact','all43_source_current_target_nonrelative_nonspeech_leaves':'all23_source_current_target_nonrelative_nonspeech_leaves','current_final_stored_macro_alignment_cases=300':'current_final_stored_macro_alignment_cases=1640'}
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    needle="    for label,key,edit in mutations:";assert t.count(needle)==1;extra="""    mutations.extend([
        ('missing_native_complete_plane','native_font_proof',lambda d:d['cases'][0].update(complete_native_independent216x64_plane_equal=False)),
        ('wrong_native_glyph_order','native_font_proof',lambda d:d['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('wrong_native_row_bounds','native_font_proof',lambda d:d['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('wrong_Samwell_progressive_label','source_nameplate_consumer_proof',lambda d:d.update(source_current_progressive_nameplate='Wrong')),
        ('wrong_Samwell_native_case','source_nameplate_consumer_proof',lambda d:next(c for c in d['native_four_consumer_cases']['rows'] if c['actor_ID']==22 and c['consumer']=='progressive-nameplate').update(text='Wrong')),
        ('wrong_name_scratch_ownership','source_nameplate_consumer_proof',lambda d:d['native_four_consumer_cases']['rows'][0].update(source_owned_scratch_restoration_recovers_all4MiB=False)),
        ('missing_actual_Samwell_nameplate','representative_proof',lambda d:d.update(actual_Samwell16_original_progressive_nameplate_and_portrait_observed=False)),
        ('invented_C200_case','relocated_control_proof',lambda d:d['relocated_C200_pairs'].append({}))
    ])
""";t=t.replace(needle,extra+needle)
    needle="    native=read(doc['native_font_proof']);sample=read(doc['representative_proof']);";assert t.count(needle)==1;t=t.replace(needle,"    visual=read('work/analysis/lil_B159_transition_review_v3858/full_screen_transition_and_all7_sheet_review.json');deps.update(s['path'] for s in visual['viewed_full_screens']);deps.add(visual['paired_town_source']['path']);deps.add(doc['source_nameplate_consumer_proof'])\n"+needle)
    assert "PROFILE='all-routes-unified-v3862'" in t and "PARENT=Path('out/all_routes_combined_v3819_candidate.nds')" in t
    compile(t,str(q),'exec');q.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B159_registrar_tools_v3861');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(p),source_sha256=sha(p.read_bytes()),successor=str(q),successor_sha256=sha(q.read_bytes()),removed_absent_C200_tests=3,complete_native_plane_original_name_consumer_and_actual_nameplate_negatives_added=True,registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),no_registration_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
