"""Prepare paired original-code recommendation fixtures and pin the one-message reference."""
from pathlib import Path
import json,os
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/recommendation_focus_tools_v4983')
ROM=Path('out/recommendation775_reference_v4983_RESEARCH_ONLY.nds')
CURRENT=Path('out/all_routes_combined_v4966_candidate.nds')
QUALIFY="""    if pc==0x020BBCA4:
     assert not self.fixtures,'Only one declared reward-input fixture is permitted'
     assert v[8]==2,'The genuine sale still contains two cargo holds'
     before={k:ct.string_at(ptr,length) for k,ptr,length in [('CPU',self.cpu,128),('WRAM',self.wram,0x400000),('DTCM',self.dtcm,0x4000),('ITCM',self.itcm,0x8000)]}
     sp=v[17];address=sp+0x10;db=struct.unpack('<I',self.image.read(self.dtcm_base,4))[0]
     if 0x02000000<=address<=0x023FFFFC:host=self.wram+address-0x02000000;kind='WRAM';offset=address-0x02000000
     else:
      assert db<=address<=db+0x3FFC,(hex(address),hex(db))
      host=self.dtcm+address-db;kind='DTCM';offset=address-db
     old_flag=ct.c_uint32.from_address(host).value;assert old_flag in [0,1]
     ct.c_uint32.from_address(self.cpu+4*4).value=2
     ct.c_uint32.from_address(self.cpu+8*4).value=16
     ct.c_uint32.from_address(host).value=1
     after={k:ct.string_at(ptr,length) for k,ptr,length in [('CPU',self.cpu,128),('WRAM',self.wram,0x400000),('DTCM',self.dtcm,0x4000),('ITCM',self.itcm,0x8000)]}
     diffs={k:[i for i,(a,b) in enumerate(zip(before[k],after[k],strict=True)) if a!=b] for k in before}
     assert set(diffs['CPU'])<=set(range(16,20))|set(range(32,36))
     assert all(set(diffs[k])<=(set(range(offset,offset+4)) if k==kind else set()) for k in ['WRAM','DTCM','ITCM'])
     files={}
     for version,data in [('before',before),('after',after)]:
      for k,value in data.items():
       path=self.folder/f'qualification_{version}_{k}.bin';path.write_bytes(value);files[version+'_'+k]=dict(path=str(path),bytes=len(value),sha256=sha(value))
     self.fixtures.append(dict(frame=frame,PC=pc,original_instruction_word=v[1],original_qualification_result=v[4],supplied_qualification_result=2,
      original_sale_hold_total=v[8],supplied_reward_quantity_input=16,original_bonus_flag=old_flag,supplied_bonus_flag=1,
      stack_field_address=address,stack_memory_kind=kind,stack_memory_offset=offset,exact_changed_offsets=diffs,snapshots=files,
      all_other_CPU_WRAM_DTCM_ITCM_bytes_exact=True,no_PC_code_RNG_cash_or_cargo_quantity_write=True,
      counterfactual_qualification_and_quantity_inputs_not_an_earned_letter_or_large_real_sale=True))
     return
"""

if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();tools=[]
    tools.append(derive('scripts/native_market_stock_edge_fixture_v756.py','scripts/native_recommendation_stock_fixture_v4983.py',{
        "assert sha(arm) in (config['source_arm9_sha256'], config['target_arm9_sha256'])":"assert sha(arm)=='39b11636e9b9904f96e18691154c813ebcad6e61647db412fa60b7344221b4a1'",
        "bytes((company, 1))":"bytes((company, 80))", "== 1\n":"== 80\n",
        "'previously unused company/share pair'":"'declared counterfactual company/share80 pair for the original reward branch'",
        'one-percent share':'80-percent share',
    }))
    tools.append(derive('scripts/run_market_stock_edge_capture_v756.py','scripts/recommendation_harness_v4983.py',{
        'scripts.native_market_stock_edge_fixture_v756':'scripts.native_recommendation_stock_fixture_v4983',
        'bounded stock/share':'bounded cargo/share80',
    }))
    tools.append(derive('scripts/observe_shop657_v4768b.py','scripts/observe_recommendation_v4984.py',{
        'Read-only market source/body observation; accepts native alignment continuation.':'Market observation with a single disclosed source-bound reward-input fixture.',
        "ROOT=Path('work/analysis/shop657_actual_v4768b')":"ROOT=Path('work/analysis/recommendation_actual_v4984_unconfigured')\ndef configure(case,rom):\n global ROOT,ROM\n ROOT=Path('work/analysis/recommendation_actual_v4984_'+case);ROM=Path(rom)",
        "for pc in(REQUEST,FONT):":"for pc in(REQUEST,FONT,0x020BBCA4):",
        'self.closed=False;self.last=None':'self.closed=False;self.last=None;self.fixtures=[]',
        '    if pc==REQUEST:':QUALIFY+'    if pc==REQUEST:',
        "dict(rows=self.rows,source_requests=self.requests,errors=self.errors,callbacks=":"dict(rows=self.rows,source_requests=self.requests,synthetic_recommendation_reward_input_fixtures=self.fixtures,errors=self.errors,callbacks=",
    }))
    a=read('work/analysis/earlier_common_wraps_approval_v4979/four_retentions_one_reflow_source_native_approval.json')
    target=Path(a['target_COMMON']).read_bytes();assert sha(target)==a['target_COMMON_sha256']
    parent=NdsImage.open(CURRENT);image=NdsImage.open(CURRENT)
    assert sha(CURRENT.read_bytes())==read('work/analysis/editorial_handoff_verification_v4982/verified_handoff.json')['candidate_sha256']
    assert sha(parent.read_file('/COMMON/MESFILE.DK4'))==a['source_COMMON_sha256']
    image.replace_file('/COMMON/MESFILE.DK4',target);image.save(ROM);result=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if result.read_file(p)!=v]==['/COMMON/MESFILE.DK4']
    assert all(result.read_file(p)==v for p,v in parent.iter_components())
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    data=(json.dumps(values+[dict(path=str(ROM.resolve()),reason='One-message775 native reference and paired disclosed reward-input capture;preserve every ROM. SHA256 '+sha(ROM.read_bytes()))],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    (ROOT/'pins.before.json').write_bytes(before)
    with pins.open('r+b') as stream:stream.write(data);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'prepared_reference_and_fixture_tools.json',dict(tools=tools,parent=str(CURRENT),parent_sha256=sha(CURRENT.read_bytes()),
        research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),only_COMMON775_bytes_change=True,all_other_files_components_exact=True,
        reference_pinned=True,all_prior_pins_and_ROMs_preserved=True,declared_stock_share80_qualification_and_reward_quantity_inputs_not_earned=True,
        original_code_portraits_COMMON775_780_766_sequence_and_effect_bodies_retained=True,new_editorial_credit=0,full_goal_complete=False))
    print('Prepared and pinned775 reference plus bounded stock/share and source-bound qualification-input fixtures;no earned reward claim.')
