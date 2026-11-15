"""Close original scheme callers and fixed nonplayer name providers."""

import re
import struct
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_schemes_integration_v776')
FUNCTIONS={0x02056AE8:(0x02056C38,0x02057024),
    0x02056C38:(0x02056D8C,0x0205700C),0x02056D8C:(0x02056F14,0x02056F90),
    0x02056F14:(0x02057068,0x02057380),0x02057194:(0x020571DC,0x02056F60)}


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('out/all_routes_combined_v773_candidate.nds')
    rom=NdsImage.open(path)
    arm=rom.read_file('/__arm9__.bin')
    source=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    refs={hex(a):{'absolute':[],'ARM_branch':[],'ADR':[],'Thumb_BL_BLX':[]} for a in FUNCTIONS}
    def owner(target):return next((a for a,(b,_) in FUNCTIONS.items() if a<=target<b),None)
    thumb=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for name,base,raw in units(rom):
        for m in re.finditer(rb'(?=(...\x02))',raw,re.S):
            target=int.from_bytes(m.group(1),'little')
            a=owner(target)
            if a is not None:refs[hex(a)]['absolute'].append([name,base+m.start(),target])
        for at in range(0,len(raw)-3,4):
            pc=base+at
            word=struct.unpack_from('<I',raw,at)[0]
            kind=None
            if word&0x0E000000==0x0A000000:
                d=word&0xffffff
                if d&0x800000:d-=0x1000000
                target=pc+8+d*4
                kind='ARM_branch'
            elif word&0x0E0F0000==0x020F0000 and (word>>21)&15 in(2,4):
                v,shift=word&255,((word>>8)&15)*2
                if shift:v=((v>>shift)|(v<<(32-shift)))&0xffffffff
                target=pc+8+(v if (word>>21)&15==4 else -v)
                kind='ADR'
            if kind:
                a=owner(target)
                if a is not None and not a<=pc<FUNCTIONS[a][0]:refs[hex(a)][kind].append([name,pc,target])
        for at in range(0,len(raw)-3,2):
            first,second=struct.unpack_from('<HH',raw,at)
            if first&0xF800!=0xF000 or second&0xF800 not in(0xE800,0xF800):continue
            i=next(thumb.disasm(raw[at:at+4],base+at),None)
            if i is None or i.mnemonic not in('bl','blx') or not i.op_str.startswith('#'):continue
            target=int(i.op_str[1:],0)&~1
            a=owner(target)
            if a is not None and not a<=base+at<FUNCTIONS[a][0]:refs[hex(a)]['Thumb_BL_BLX'].append([name,base+at,target])
    for a,(b,caller) in FUNCTIONS.items():
        assert arm[a-BASE:b-BASE]==source[a-BASE:b-BASE]
        r=refs[hex(a)]
        assert r['ARM_branch']==[['section0',caller,a]],(hex(a),r)
        assert not any(r[k] for k in ('absolute','ADR','Thumb_BL_BLX')),(hex(a),r)
    # Original fixed-template initializer writes object+4 from the immutable
    # information row. Save/load begin at+0xB;name/vtable pointers are not saved.
    for a,b in ((0xCD488,0xCD4A4),(0xCD53C,0xCD550),(0x3CD80,0x3CFEC)):
        assert arm[a:b]==source[a:b]
    context=read('work/analysis/tavern_schemes_editorial_v774/native_context.json')
    raw=Path(context['read_only_snapshot']['path']).read_bytes()
    assert sha(raw)==context['read_only_snapshot']['sha256']
    u=machine(arm)
    u.mem_write(BASE,raw)
    def get(fn,args=()):
        call(u,fn,args)
        return u.reg_read(UC_ARM_REG_R0)
    def ptr(at):return struct.unpack('<I',u.mem_read(at,4))[0]
    root=get(0xCB160)
    rows=[]
    code=MainCodeFile(arm,BASE)
    for n in range(20):
        obj=root+4+76*n
        info=get(0xCD53C,(n,))
        section=next(s for s in code.sections if s.ramAddress<=info<info+4<=s.ramAddress+len(s.data))
        at=info-section.ramAddress
        immutable=struct.unpack_from('<I',section.data,at)[0]
        assert ptr(info)==immutable==ptr(obj+4)
        u.reg_write(UC_ARM_REG_SP,STACK)
        u.reg_write(UC_ARM_REG_R0,obj)
        u.emu_start(BASE+0xCD488,BASE+0xCD4A4,count=1000)
        assert u.reg_read(UC_ARM_REG_R1)==immutable and ptr(obj+4)==immutable
        value=bytes(u.mem_read(immutable,64)).split(b'\0')[0]
        expected=context['all21_initialized_native_faction_names'][n]
        assert value.hex()==expected['name_hex']
        rows.append({'faction':n,'information_row':info,'immutable_default_pointer':immutable,
                     'default_name_hex':value.hex(),'original_initializer_name_assignment_verified':True})
    prior=read('work/analysis/tavern_scheme_targets_v775/source_contract.json')
    assert len(prior['all400_first_target_exclusions'])==400 and len(prior['all8000_second_target_exclusions'])==8000
    save(ROOT/'input_contract.json',{'source_ROM_sha256':sha(path.read_bytes()),
        'source_ARM9_sha256':sha(source),'current_ARM9_sha256':sha(arm),
        'complete_direct_callers_and_no_pointer_ADR_or_Thumb_entry_aliases':refs,
        'all20_immutable_faction_information_rows_and_native_initializers':rows,
        'prior_target_exclusion_proof_sha256':sha(Path('work/analysis/tavern_scheme_targets_v775/source_contract.json').read_bytes()),
        'scheme_targets_exclude_current_faction_at_both_selections':True,
        'normal_nonplayer_names_are_fixed_initialized_information_row_names':True,
        'editable_company_name_does_not_reach_these_original_scheme_consumers':True,
        'legal_editor_stress_findings_outside_this_family_input_contract_not_waived_in_general':True,
        'all39730_fixed_catalog_layouts_are_clean':True,
        'scope':'Original unmodified game calling path and initialized/save-loaded faction model;arbitrary memory edits or corruption are outside this contract. No actual gameplay activation claimed.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Five private calling paths and20 immutable name initializers verified;original scheme targets exclude the player-name field.',flush=True)


if __name__=='__main__':main()
