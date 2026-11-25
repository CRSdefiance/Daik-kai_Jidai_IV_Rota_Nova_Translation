"""Derive registration after full V3778, testing only source-present controls and typed FE behavior."""
from pathlib import Path
import ast,re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    p=Path('scripts/register_lil_B157_v3777.py');q=Path('scripts/register_lil_B158_v3818.py');assert not q.exists();t=p.read_text(encoding='utf-8');tree=ast.parse(t)
    removed=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='mutations' for a in node.targets):
            for elt in node.value.elts:
                if elt.elts[0].value in ['missing_C200','changed_C200_request','changed_C200_write']:removed.append(ast.get_source_segment(t,elt))
    assert len(removed)==3
    for text in removed:assert t.count(text+',')==1;t=t.replace(text+',','')
    assert t.count("PROFILE='all-routes-unified-v3778'")==1;t=t.replace("PROFILE='all-routes-unified-v3778'","PROFILE='all-routes-unified-v3819'")
    oldhash='97d243c2a5c5177444a5e2e0f810ae88dd09352199aa5b23b75359b7caf1090c';assert oldhash in t
    description="Full V3778 cumulative stack plus19 reviewed Lil B158 Cristina tavern, music, spontaneous dance, patron cheers and applause objects;24 relative spans, six predicates, four static actors, four null-actor FE panels, four resource sites, both source art pauses and one declared end preserved."
    t,n=re.subn(r"description='Full V3738[^']*'",'description='+repr(description),t);assert n==1
    changes={
        'B157':'B158','v3777':'v3818','v3738':'v3778','V3738':'V3778','lil_carlo':'lil_dance','manuscript_v6':'manuscript_v5',oldhash:sha(Path('translations/release_stack.json').read_bytes()),'editorial_handoff_verification_v3760':'editorial_handoff_verification_v3801','reference_approval_v3776':'reference_approval_v3816','loader_v3766':'loader_v3807',
        'lil_B157_transition_review_v3775/full_screen_transition_and_all13_sheet_review':'lil_B158_transition_review_v3815/full_screen_transition_and_all4_sheet_review','==75':'==19','positive_records=75':'positive_records=19','batches=532':'batches=533','expected_batches=532':'expected_batches=533',
        "('lost_Carlo13','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==19).update(source_selector=20))":"('lost_Cristina07','manuscript',lambda d:next(r for r in d['records'] if r['source_selector']==7).update(source_selector=2))",
        'all27_opaque_leaves_two_effects_three_resources_two_C200_C281_4885_pause_exact':'all22_opaque_leaves_four_resources_two_pauses_picture_music_exact','all27_source_current_target_nonrelative_nonspeech_leaves':'all22_source_current_target_nonrelative_nonspeech_leaves','B157_both_declared_endwords_preserved':'B158_single_declared_endword_preserved','source_pause_and_resume_preserved':'source_two_pause_and_resume_pairs_preserved','missing_double_end_gate':'missing_single_end_gate','missing_second_end_map':'missing_declared_end_map',
        'changed_C281_leaf':'changed_4650_leaf','0xC281':'0x4650','changed_4885_leaf':'changed_4660_leaf','0x4885':'0x4660',
    }
    for a in changes:assert a in t,a
    t=re.sub('|'.join(re.escape(a) for a in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],t)
    assert "PROFILE='all-routes-unified-v3819'" in t and "PARENT=Path('out/all_routes_combined_v3778_candidate.nds')" in t
    compile(t,str(q),'exec');q.write_text(t,encoding='utf-8',newline='\n');root=Path('work/analysis/lil_B158_registrar_tools_v3818');assert not root.exists();root.mkdir(parents=True);save(root/'source_derivation.json',dict(source=str(p),source_sha256=sha(p.read_bytes()),successor=str(q),successor_sha256=sha(q.read_bytes()),removed_no_source_C200_tests=3,source_4650_4660_real_pause_single_end_and_FE_tests_preserved=True,registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),no_registration_yet=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
