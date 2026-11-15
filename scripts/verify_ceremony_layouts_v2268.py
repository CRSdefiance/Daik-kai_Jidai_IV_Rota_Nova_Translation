"""Current51 progressive/modal payloads plus distinct unindented retained64."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from scripts.verify_arrival_native_v792 import prepared,run
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts import probe_tavern_continuation_layout_v768 as paragraphs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/ceremony_layouts_v2268');DOC=Path('translations/ceremony_contextual_editorial_manuscript_v1.json')
MATRIX=Path('work/analysis/ceremony_integration_v809/production_layout.json')
MODAL=(289,290,291,293,294,295)
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);doc=read(DOC);rows={r['message_id']:r for r in doc['records']};rom=NdsImage.open(doc['current_ROM']);arm,common=[rom.read_file(p)for p in('/__arm9__.bin','/COMMON/MESFILE.DK4')];entries=current_entries(common,arm)
    for n,r in rows.items():assert entries[n].text==(b''if n==64 else b' ')+r['english'].removesuffix('{PAD}').encode('ascii')
    _,modal,ordinary_source,modal_source=production_functions()
    old="    raw = b' ' + row['english'].removesuffix('{PAD}').encode('ascii')";new="    raw = (b'' if row['message_id']==64 else b' ') + row['english'].removesuffix('{PAD}').encode('ascii')";assert ordinary_source.count(old)==1;ordinary_source=ordinary_source.replace(old,new)
    marker="    call(u,0x01FFCF3C-BASE,(wrapped,output,0),instruction_limit=2000000)";assert ordinary_source.count(marker)==1
    ordinary_source=ordinary_source.replace(marker,marker+"\n    for p,value in zip(pointers,values):assert bytes(u.mem_read(p,len(value)+1))==value+bytes(1)")
    env=dict(paragraphs.__dict__);from scripts.context_ceremony_v806 import TABLES
    env['TABLES']=TABLES;exec(compile(ordinary_source,__file__,'exec'),env);ordinary=env['format_case'];(ROOT/'ordinary_formatter.py').write_text(ordinary_source);(ROOT/'modal_formatter.py').write_text(modal_source)
    oldcases=read(MATRIX)['cases'];assert len(oldcases)==201;cases=[]
    for i,c in enumerate(oldcases):
        n=c['id'];r=rows[n];values=tuple(bytes.fromhex(v)for v in c['source_values_hex']);u=prepared(arm);result=(modal if n in MODAL else ordinary)(u,r,values)
        assert result['formatted_hex']==c['formatted_hex']and not result['findings']
        if n in MODAL:assert bytes(u.mem_read(0x02426800,len(values[0])+1))==values[0]+bytes(1)if values else True
        result.update(index=i,message_ID=n,values_hex=[v.hex()for v in values],template_hex=entries[n].text.hex(),native_binding=r['native_binding']);cases.append(result)
    bare=ordinary(prepared(arm),rows[64],());assert bare['formatted_hex']==entries[64].text.hex()and not bare['findings']and len(bare['lines'])==1;bare.update(index=201,message_ID=64,values_hex=[],template_hex=entries[64].text.hex(),native_binding=rows[64]['native_binding']);cases.append(bare)
    hero_cases=[];context=read('work/analysis/ceremony_context_v2264c/native_context.json')
    for selected in context['hero_table_selections']:
        n=selected['selected_message'];r={**rows[n],'_selector_table':selected['table']};result=ordinary(prepared(arm),r,());assert result['formatted_hex']==next(c['formatted_hex']for c in cases if c['message_ID']==n)and not result['findings'];hero_cases.append(dict(**selected,formatted_hex=result['formatted_hex'],original_53C14_pointer_scope_and_complete_output=True))
    priorarm=NdsImage.open('out/all_routes_combined_v829_candidate.nds').read_file('/__arm9__.bin');controls=[];text=b' Complete ceremony words preserve every leading and final character.'
    for parent in(0x0205469C,0x02054014):
        for n in MODAL:
            before,after=run(prepared(priorarm),parent,n,text),run(prepared(arm),parent,n,text);assert before==after;controls.append(dict(parent=parent,ID=n,current_matches_registered_prior=True))
    assert len(cases)==202 and {r['message_ID']for r in cases}==set(rows)
    save(ROOT/'all52_current_native_layouts.json',dict(ARM9_sha256=sha(arm),COMMON_sha256=sha(common),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),historical_matrix=str(MATRIX),historical_matrix_sha256=sha(MATRIX.read_bytes()),case_count=202,cases=cases,findings=[],representative_full_font_indices=list(range(202)),all51_relocated_paragraphs_and_bare64_actual_parent_bindings=True,all201_production_formatted_bytes_identical_historical=True,source64_unindented_bare_payload_preserved=True,complete_printf_words_argument_copies_canaries_bounds_and_ABI=True,current32_hero_pointer_contracts=hero_cases,current12_wrong_parent_modal_controls=controls,source_aliases_and_23byte_names_are_supplied_stress_not_earned_player_names=True,all202_native_full_fonts_visual_historical_actual_and_reconciliation_pending=True,no_ROM_runtime_or_registry_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(layouts=202,IDs=52,hero_contracts=32,wrong_parent_modal_controls=12,findings=0))
