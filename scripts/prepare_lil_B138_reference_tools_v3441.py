"""Prepare44-speech relocation, final-storage rendering, loader and entry proofs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_reference_tools_v3441');assert not root.exists();pairs=[]
    def make(old,new,changes):
        a,b=Path(old),Path(new);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append((a,b))
    common=[('B137','B138'),('v3401b','v3441'),('v3402','v3442'),('v3403','v3443'),('v3404','v3444'),('v3372','v3416'),('V3372','V3416')]
    make('scripts/research_lil_B137_relocation_v3401b.py','scripts/research_lil_B138_relocation_v3441.py',[
        ('lil_B137_editorial_manuscript_v7','lil_B137_editorial_manuscript_v6'),("sum(len(r['relative_skip_fixups']) for r in results)==48","sum(len(r['relative_skip_fixups']) for r in results)==45"),('all48speech_and48_relative_operands_preserved','all44speech_and45_relative_operands_preserved'),('all240_','all225_'),('==240','==225'),("sum(len(r['text_records']) for r in results)==48","sum(len(r['text_records']) for r in results)==44"),('==117','==111'),('[137]','[138]'),('117commands/48speech/48spans/240targetskipcases','111commands/44speech/45spans/225targetskipcases')]+[p for p in common if p[0] in ['B137','v3401b','v3372']])
    make('scripts/prepare_lil_B137_research_v3402.py','scripts/prepare_lil_B138_research_v3442.py',[
        ('lil_B137_native_approval_v3398b','lil_B137_native_approval_v3438'),('lil_B137_fonts_v3397c','lil_B137_fonts_v3437'),('all48speech_and48_relative_operands_preserved','all44speech_and45_relative_operands_preserved'),('all240_','all225_'),('all48','all44'),('and192_','and176_'),('==48','==44'),('==192','==176'),('cases=192','cases=176'),('[137]','[138]'),('48final nativeplanes/192macro','44final nativeplanes/176macro')]+[p for p in common if p[0] in ['B137','v3401b','v3402','v3372','V3372']])
    make('scripts/verify_lil_B137_loader_v3403.py','scripts/verify_lil_B138_loader_v3443.py',[p for p in common if p[0] in ['B137','v3402','v3403']])
    make('scripts/verify_lil_B137_references_v3404.py','scripts/verify_lil_B138_references_v3444.py',[
        ('[137]','[138]'),('==117','==111'),('==48','==45'),('==240','==225'),('all117_commands48_relative_sites','all111_commands45_relative_sites'),('all117_clean_current_target_commands_and48_relative_sites','all111_clean_current_target_commands_and45_relative_sites'),('native_commands_each=117','native_commands_each=111'),('relative_sites=48','relative_sites=45'),('target_native_skip_cases=240','target_native_skip_cases=225')]+[p for p in common if p[0] in ['B137','v3402','v3403','v3404']])
    root.mkdir(parents=True);save(root/'provenance.json',dict(producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],producer_sha256=sha(Path(__file__).read_bytes()),all_prior_producers_ROMs_and_translations_preserved=True,full_goal_complete=False))
