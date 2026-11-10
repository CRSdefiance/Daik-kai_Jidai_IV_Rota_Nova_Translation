"""Join exact native handoff cases from disjoint checked batches without reexecution."""
import argparse
from pathlib import Path
from ndspy.code import MainCodeFile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parent',type=Path,required=True)
    p.add_argument('--proof',type=Path,action='append',required=True)
    p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();assert not args.out.exists()
    image=NdsImage.open(args.parent);blocks=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    arm=image.read_file('/__arm9__.bin');sections=MainCodeFile(arm,BASE).sections
    spans=[(s.ramAddress,bytes(s.data)) for s in sections]+[(POOL,bytes(sections[3].data[:-48]))]
    candidates=[];evidence={str(args.parent):sha(args.parent.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for path in args.proof:
        proof=load(path);modepath=Path(proof['modes']);assert sha(modepath.read_bytes())==proof['modes_sha256']
        modes=load(modepath);candidates.append((path,modepath,modes));evidence.update({str(path):sha(path.read_bytes()),str(modepath):sha(modepath.read_bytes())})
    cases=[];origins=[];words={};used=set()
    for index,block in enumerate(blocks):
        matching=[]
        for path,modepath,modes in candidates:
            rows=[r for r in modes['native_handoff_and_first_read_cases'] if r['route']==0 and r['block']==index]
            assert len(rows)==2 and {r['mode'] for r in rows}=={0,1}
            if all(r['source_block_sha256']==sha(block) for r in rows):matching.append((path,modepath,modes,rows))
        assert matching,('No exact prior native parent cases',index)
        path,modepath,modes,rows=matching[0];cases.extend(rows);used.add(path)
        origins.append(dict(block=index,source_block_sha256=sha(block),proof=str(path),modes=str(modepath)))
        for word in modes['executed_source_words']:
            pc=word['PC'];value=bytes.fromhex(word['hex'])
            matches=[data[pc-base:pc-base+len(value)] for base,data in spans if base<=pc and pc+len(value)<=base+len(data)]
            assert matches and all(v==value for v in matches)
            assert pc not in words or words[pc]==word
            words[pc]=word
    assert len(cases)==2*len(blocks) and len(used)==len(args.proof)
    args.out.mkdir(parents=True);modepath=args.out/'exact_joined_parent_modes.json'
    save(modepath,dict(native_handoff_and_first_read_cases=cases,executed_source_words=[words[k] for k in sorted(words)],
        origins=origins,all_case_source_blocks_andexecuted_code_exact=True,no_new_native_execution=True,actual_gameplay=False,new_credit=0,evidence=evidence))
    save(args.out/'qualification.json',dict(parent=str(args.parent),parent_sha256=sha(args.parent.read_bytes()),modes=str(modepath),modes_sha256=sha(modepath.read_bytes()),
        exact_joined_cases=len(cases),source_proofs=[str(x) for x in args.proof],no_new_native_execution=True,actual_gameplay=False,new_credit=0,evidence=evidence))
    print(dict(exact_joined_cases=len(cases),native_execution_repeated=False,source_proofs=len(used)))
