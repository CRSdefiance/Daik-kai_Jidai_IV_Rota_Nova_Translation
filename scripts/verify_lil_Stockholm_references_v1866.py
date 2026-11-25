"""Fresh shipped entry census and complete102-command Stockholm mapping."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.prepare_lil_Stockholm_research_v1862 import ROM,PARENT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_reference_census_v1866')
RELOC=Path('work/analysis/lil_Stockholm_relocation_v1861/nested_source_relocation_research.json')
LOADER=Path('work/analysis/lil_Stockholm_loader_v1863/whole_SC2_and_B27_initial_entry_proof.json')
CONTEXT=Path('work/analysis/lil_Stockholm_context_audit_v1855/original_Stockholm36_branch_and_three_fixture_audit.json')

if __name__=='__main__':
    assert not ROOT.exists()
    research=read(RELOC);spec=research['blocks'][0];loader=read(LOADER);actual=read(CONTEXT)
    assert spec['block']==27 and len(spec['text_records'])==51 and len(spec['relative_skip_fixups'])==24
    assert len(spec['target_native_skip_cases'])==120 and spec['inverse_restoration_recovers_every_original_logical_byte']
    assert loader['all336_whole_blocks_and672_modes_each_pass']
    assert loader['original_EV2_actions_select_by_block_index_without_interior_byte_offset']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    assert sha(PARENT.read_bytes())==research['candidate_sha256']==actual['candidate_sha256']
    for version in loader['versions']:
        for k in('load','parent'):assert sha(Path(version[k+'_proof']).read_bytes())==version[k+'_sha256']
    clean,current,target=NdsImage.open('work/clean.nds'),NdsImage.open(PARENT),NdsImage.open(ROM)
    arm=current.read_file('/__arm9__.bin');assert arm==target.read_file('/__arm9__.bin')
    code={label:census(im)for label,im in [('clean',clean),('current',current),('research',target)]}
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in(clean,current,target)]
    assert all(len(bs)==336 for bs in blocks)
    assert all(a==b for i,(a,b)in enumerate(zip(blocks[1],blocks[2],strict=True))if i!=27)
    assert sha(blocks[1][27])==spec['source_block_sha256']and sha(blocks[2][27])==spec['research_block_sha256']
    walks=[inventory(im.read_file('/__arm9__.bin'),bs[27])[0]for im,bs in zip((clean,current,target),blocks,strict=True)]
    assert all(len(w)==102 for w in walks)
    patches=sorted([{'start':r['old_offset'],'end':r['old_offset']+r['old_length'],
        'delta':r['new_length']-r['old_length']}for r in spec['text_records']],key=lambda p:p['start'])
    def mapped(offset):
        delta=0
        for p in patches:
            if offset<p['start']:break
            assert not p['start']<offset<p['end']
            if offset==p['start']:return offset+delta
            delta+=p['delta']
        return offset+delta
    commands=[]
    for jp,old,new in zip(*walks,strict=True):
        assert jp['word']==old['word']==new['word']and jp['offset']==old['offset']
        assert jp['native_extent']==old['native_extent']
        assert new['offset']==mapped(old['offset'])
        assert new['native_extent']==mapped(old['offset']+old['native_extent'])-new['offset']
        assert new['ancestor_0100_offsets']==[mapped(a)for a in old['ancestor_0100_offsets']]
        if old['word']==0x4000:
            assert blocks[1][27][old['offset']:old['offset']+6]==blocks[2][27][new['offset']:new['offset']+6]
        elif old['word']not in(0x100,0x200,0x300):assert old['whole_command_hex']==new['whole_command_hex']
        commands.append({'word':old['word'],'old_offset':old['offset'],'new_offset':new['offset'],
            'old_native_extent':old['native_extent'],'new_native_extent':new['native_extent'],
            'original_0100_ancestors':old['ancestor_0100_offsets'],'relocated_0100_ancestors':new['ancestor_0100_offsets']})
    observed_types={r['word']for r in actual['original_command_pairs']}
    assert{r['word']for r in commands}<=observed_types
    ROOT.mkdir(parents=True)
    save(ROOT/'all102_commands24_relative_sites_and_shipped_entry_census.json',{
        'parent':str(PARENT),'parent_sha256':sha(PARENT.read_bytes()),'research_ROM':str(ROM),
        'research_ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),'block':27,
        'native_call_census':code,'native_walks':dict(zip(('clean','current','research'),walks,strict=True)),
        'mapped_commands':commands,'all102_commands_reexecuted_clean_current_and_target':True,
        'all24_typed_span_sites_and120_target_native_cases_preserve_destinations':True,
        'all_original_opaque_commands_and_complete_speech_preambles_preserved':True,
        'every_original_command_type_has_actual_current_scene_evidence':True,
        'all335_other_blocks_preserved':True,'entry_point_offset':8,
        'original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes':True,
        'only_original24070_interpreter_call_no_literal_alias':True,
        'structural_walk_bridges_opaque_effects_not_a_claim_all_conditional_paths_were_played':True,
        'actual_revised_scene_and_final_reference_approval_pending':True,
        'registered_ROM_patch_or_completion_credit_not_yet_created':True,
        'evidence':{str(p):sha(p.read_bytes())for p in(RELOC,LOADER,CONTEXT)},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'native_entry_censuses':3,'native_commands_each':102,'relative_sites':24,
        'target_native_skip_cases':120,'every_command_type_observed_in_original_scene':True},flush=True)
