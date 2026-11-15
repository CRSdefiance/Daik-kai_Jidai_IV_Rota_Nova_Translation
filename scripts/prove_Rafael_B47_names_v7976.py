"""Bind own-captain0 static names/voices and measured defaults; FE remains a separate consumer."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.audit_native_given_name_table import string
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_names_v7976')
GLOSS=Path('work/analysis/Rafael_B47_clean_gloss_v7973/15_fresh_clean_glosses_complete_B37_context_before_current_English.json')
INPUT=Path('work/analysis/current_V7964_Rafael_native_v7967/current_native_input.json')
START=Path('work/analysis/Rafael_B46_context_binding_v7967/own_Rafael_startup_andstrict_captain0_context.json')
if __name__=='__main__':
    assert not ROOT.exists();gloss,inp,start=map(read,[GLOSS,INPUT,START]);source=read('work/analysis/Rafael_next_clean_v7971/complete_clean_SC0_B47_EV0_andcoverage_before_current_English.json')
    assert gloss['all15_glosses_fresh_before_current_English_exposure'] and all(r['current_English_body_unread'] for r in gloss['records'])
    chosen=sorted({r['source_selector'] for r in gloss['records'] if r['source_selector']!=254});assert chosen==[0,4,5,6]
    excluded=[r['id'] for r in gloss['records'] if r['source_selector']==254];assert excluded==[]
    current,clean=[NdsImage.open(x) for x in [inp['current_ROM'],source['source_ROM']]]
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    name_adapter=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in SELECTED_ACTORS:',
        'actor = root+4+32*ident':'actor = root+0x19E4 if ident==0 else root+4+32*ident',
        'all_ten_original_consumers':'all_eight_original_consumers'})
    env={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(name_adapter,__file__+'::four-source-static-speakers','exec'),env)
    native=ctx.execute(env['names']);ctx.machines.pop()
    voice_adapter=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert captain==0'})
    env=dict(selectors.__globals__);exec(compile(voice_adapter,__file__+'::own-captain0-voices','exec'),env)
    voices=ctx.execute(env['selectors'],chosen);ctx.machines.pop()
    expected={0:'Rafael Castor',4:'Janus Pasar',5:'Claudio Manaus',6:'Julio Erneco'}
    assert len(native['rows'])==8 and all(r['text']==expected[r['actor_ID']] for r in native['rows'])
    fields=[]
    for ident in chosen:
        versions=[]
        for label,image in [('clean-Japanese',clean),('current-English-names-only',current)]:
            arm=image.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000;assert table==0x120B80
            values=[]
            for col,kind in [(0,'given-name'),(4,'surname'),(8,'middle-name')]:
                at=table+32*ident+col
                values.append(dict(kind=kind,table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,struct.unpack_from('<I',arm,at)[0])))
            versions.append(dict(version=label,ARM9_sha256=sha(arm),fields=values))
        fields.append(dict(actor_ID=ident,versions=versions))
    source_values={r['actor_ID']:[v.get('text') for v in r['versions'][0]['fields']] for r in fields}
    assert source_values=={0:['ラファエル','カストール',None],4:['ジェナス','パサー',None],5:['クラウディオ','マナウス',None],6:['フリオ','エルネコ',None]}
    macro_adapter=checked_text(inspect.getsource(expand),{
        'captain==3':'captain==0',"b'Maria'":"b'Rafael'","b'Li'":"b'Castor'","b'Li Clan'":"b'Castor Co.'"})
    env=dict(expand.__globals__);exec(compile(macro_adapter,__file__+'::measured-own-Rafael-defaults','exec'),env)
    defaults=[]
    for ident in chosen:
        result=ctx.execute(env['expand'],b'FI FA FO',ident);ctx.machines.pop();defaults.append(result)
        assert all(bytes.fromhex(c['output_hex'])==b'Rafael Castor Castor Co.' for c in result['cases'])
    assert not ctx.machines
    assert start['actual_original_captain_ID']==0 and start['all_whole_RGB_actor_andcaptain_controls_equal']
    assert sha(Path(start['review_sheet']['path']).read_bytes())==start['review_sheet']['sha256']
    save(ROOT/'four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_ROM=source['source_ROM'],source_ROM_sha256=source['source_ROM_sha256'],
        current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        actual_original_captain_ID=0,selected_source_static_actors=chosen,
        native_eight_progressive_andfull_getters=native,native_static_selector_andvoice_resolution=voices,
        complete_clean_andcurrent_name_fields=fields,
        naming_retentions=[
            dict(actor_ID=0,name='Rafael Castor',reason='Approved Rafael andsource カストール/Castor bind the original player character;no new rank or relationship.'),
            dict(actor_ID=4,name='Janus Pasar',reason='Clean ジェナス/パサー and both native getters support retaining the established Janus Pasar identity. パサー is distinct from パシャ in the force references; do not rename him Pasha or infer an affiliation. Full catalogue UI andwider207 consumers remain unreviewed.'),
            dict(actor_ID=5,name='Claudio Manaus',reason='Clean クラウディオ/マナウス and both original getters support Claudio Manaus. Retain the existing spelling without adding rank or kinship.'),
            dict(actor_ID=6,name='Julio Erneco',reason='Clean フリオ/エルネコ supports the current Julio/Erneco fields andboth actual getters;retain the existing source-compatible spelling. The dialogue uses the given name politely without establishing kinship.')],
        excluded_FE_system_panel_IDs=excluded,FE_is_not_static_actor254=True,
        synthetic_default_probes_not_added_to_source=defaults,macro_default_alignment_cases=16,
        measured_default_macro_values=dict(FI='Rafael',FA='Castor',FO='Castor Co.'),
        measured_default_macro_ASCII_lengths=dict(FI=6,FA=6,FO=10),
        original_source_macro_counts=dict(FI=0,FA=0,FO=0),
        all15_progressive_body_nameplate_source_predicates_andactual_display_pending=True,
        source_owned_name_adapter=name_adapter,source_owned_voice_adapter=voice_adapter,source_owned_macro_adapter=macro_adapter,
        all_original_owned_scratch_orreadonly_paths_restore_all4MiB=True,
        startup_sheet_viewed=start['review_sheet'],startup_sheet_directly_viewed=True,
        current_English_B47_bodies_still_unread=True,
        no_actual_B47_header_orwhole_catalogue_UI_orcustom_player_name_coverage=True,
        full207_names_branches_controls_progressive_fonts_actual_andrelease_still_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,INPUT,START,Path(__file__)]},full_goal_complete=False))
    print('B47 names:',[(r['actor_ID'],r['consumer'],r['text']) for r in native['rows']])
    print('Voices',[(r['source_selector'],r['original_voice_class']) for r in voices['rows']])
    print('Synthetic default macros FI6/FA6/FO10,sixteen guarded alignments;none added to source.All15 B47 progressive displays andbranches pending;current English unread.')
