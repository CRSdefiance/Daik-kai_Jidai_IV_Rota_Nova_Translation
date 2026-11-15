"""Exact next22 clean/current records;no consumer mapping or editorial credit yet."""
import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.activity_special_editorial_v987b import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_declaration_v990')
ROM=Path('out/all_routes_combined_v987_candidate.nds')
IDS=tuple(range(1889,1911))

def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1174 and ledger['records_with_source_and_prose_pass']==1177
    rom,clean,canonical=map(NdsImage.open,(ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    assert sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    arm=rom.read_file('/__arm9__.bin');jp_arm=clean.read_file('/__arm9__.bin')
    current=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),jp_arm)
    accepted=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'),clean=False)
    completed={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not completed.intersection(IDS)
    rows=[]
    for n in range(1888,1912):
        literals=[];offset=jp_arm.find(struct.pack('<I',n))
        while offset>=0:
            if offset%4==0:literals.append(offset)
            offset=jp_arm.find(struct.pack('<I',n),offset+1)
        source,english=jp[n].text.decode('cp932'),current[n].text.decode('cp932')
        rows.append({'message_id':n,'selected_next_inventory':n in IDS,'source_Japanese':source,'source_hex':jp[n].text.hex(),
            'source_reference':reference(jp[n]),'current_English':english,'current_text_hex':current[n].text.hex(),
            'current_reference':reference(current[n]),'canonical_text_hex':accepted[n].text.hex(),
            'source_percent_s_count':jp[n].text.count(b'%s'),'current_full_width_I': 'Ｉ' in english,
            'current_explicit_LF_count':english.count('\n'),'clean_aligned_scalar_literals_as_leads_only':literals,
            'original_callers_speakers_argument_meaning_confirmation_and_rendering_not_mapped':True,
            'source_prose_native_or_actual_review_credit':False})
    selected=[r for r in rows if r['selected_next_inventory']]
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'COMMON_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),
        'ARM9_sha256':sha(arm),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'native_message_IDs':list(IDS),
        'records_and_neighbors':rows,'source_argument_s_IDs':[r['message_id'] for r in selected if r['source_percent_s_count']],
        'current_full_width_I_IDs':[r['message_id'] for r in selected if r['current_full_width_I']],
        'current_explicit_LF_IDs':[r['message_id'] for r in selected if r['current_explicit_LF_count']],
        'source_inventory_only_no_consecutive_scene_or_table_ownership_assumption':True,
        'next_required_work':'Trace original callers,voice variants,known/unknown faction selection,%s owner and display name semantics,confirmation cancellation,then review natural English and test runtime name expansion/leading letters.',
        'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False,'producer_sha256':sha(Path(__file__).read_bytes())}
    path=ROOT/'source_inventory.json';save(path,proof)
    ledger['next_battle_declaration_v990_inventory']={'native_message_IDs':list(IDS),'proof':str(path),
        'status':'22-raw-source-and-current-inventoried-original-callers-and-all-editorial-gates-pending',
        'completed_entries_added':0,'source_prose_reviews_added':0}
    ledger['research_checkpoints'].append({'id':'V990-next22-battle-declaration-inventory','proof':str(path),
        'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    save(ledger_path,ledger)
    doc=Path('docs/battle_declaration_v990_inventory.md');assert not doc.exists()
    with doc.open('x',encoding='utf-8') as f:f.write('# V990: next battle/declaration source inventory\n\nExact clean Japanese,current V987 and canonical bytes/references are preserved for1889-1910 with immediate neighbors1888/1911. These22 are unreviewed;original callers,voice tables,faction-name argument meaning,confirmation cancellation and consumers still need mapping. The inventory does not assume neighboring strings are a conversation.\n\nCurrent full-width I findings:'+repr(proof['current_full_width_I_IDs'])+'. Current explicit LF findings:'+repr(proof['current_explicit_LF_IDs'])+'. Japanese percent-s argument entries:'+repr(proof['source_argument_s_IDs'])+'. These are leads for source/context and complete native glyph/expansion testing,not automatic replacement instructions.\n\nV987 remains current;1174 entries complete and1177 source/prose reviewed. No new credit. Older750-752,all wider shared/route/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;goal active.\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V990: next22 battle/declaration source inventory\n\nExact source/current records1889-1910 are inventoried,including percent-s names,full-width I and old explicit line breaks. Original callers/arguments and all editorial/native/actual gates remain pending;no new review credit. V987 current,1174 complete,1177 source/prose;goal active. See [V990 inventory](battle_declaration_v990_inventory.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V990 Battle declaration source inventory');assert not archive.exists();copied=[]
    for source in (path,Path(__file__),doc,ledger_path):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert source.read_bytes()==target.read_bytes();copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_ROM_or_save_duplicated':True})
    print('Next22 exact records inventoried;full-width I:',proof['current_full_width_I_IDs'],'LF:',proof['current_explicit_LF_IDs'],'source-prose credit0. Goal active.')

if __name__=='__main__':main()
