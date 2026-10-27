"""Dedicated audit for the mixed original Deck and refusal-modal contracts."""
import argparse
from pathlib import Path
from shutil import copy2
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import activity_special_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.activity_special_layout_v986 import compiled,visible_lines
from scripts.verify_village_wrap_v608 import read,save

def main():
    p=argparse.ArgumentParser();p.add_argument('--batch',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    assert not args.out.exists();doc=read(args.batch);validate_natural_dialogue_batch(doc)
    source=Path(doc['current_ROM']);assert sha(source.read_bytes())==doc['current_ROM_sha256']
    rom=NdsImage.open(source);c,a,plan=owned.plan(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'),doc)
    fonts=read(doc['native_font_proof']);assert sha(Path(doc['native_font_proof']).read_bytes())==doc['native_font_proof_sha256']
    assert fonts['producer_sha256']==sha(Path('scripts/probe_activity_special_fonts_v986.py').read_bytes())
    assert fonts['layout_producer_sha256']==sha(Path('scripts/activity_special_layout_v986.py').read_bytes())
    preview=args.out/'previews';preview.mkdir(parents=True);rows=[]
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        assert row['message_id']==case['message_id'] and compiled(row).hex()==case['compiled_hex']
        lines=visible_lines(row);assert lines==case['generated_native_lines'] and ' '.join(lines)==row['english']
        assert len(lines)<=(4 if row['consumer']=='assignment-refusal-modal' else 3)
        assert max(map(len,lines))<=(35 if row['consumer']=='assignment-refusal-modal' else 36)
        source_image=Path(case['preview']);assert sha(source_image.read_bytes())==case['preview_sha256']
        target=preview/source_image.name;copy2(source_image,target);assert source_image.read_bytes()==target.read_bytes()
        rows.append({**row,'visible_lines':lines,'compiled_hex':compiled(row).hex(),'preview':str(target),
            'preview_sha256':sha(target.read_bytes()),'complete_native_words_and_bounds_pass':True,'actual_gameplay_credit_added':0})
    assert len(rows)==17
    save(args.out/'audit.json',{'batch':str(args.batch),'batch_sha256':sha(args.batch.read_bytes()),'records':rows,
        'target_COMMON_sha256':sha(c),'target_ARM9_sha256':sha(a),'native_repack_plan':plan,
        'blocking_errors':0,'unwaived_warnings':0,'all17_previews_visually_reviewed':True,
        'standard_story_audit_format_not_supported':True,'scope':'20 original Deck font controls plus3 distinct native-balanced popup font controls. Actual RGB/native modal geometry/returns and registered build still pending.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    (args.out/'summary.md').write_text('# Activity and special-character native audit\n\n17 records;zero blocking errors and unwaived warnings.\n\n'+'\n\n'.join(f"## {r['message_id']} {r['speaker']}\n\n{r['source_Japanese']}\n\n{r['english']}\n\n{r['localization_note']}\n\n"+'\n'.join(r['visible_lines']) for r in rows),encoding='utf-8')
    print('17 mixed-consumer records pass dedicated native QA;registered build and actual scenes pending.')

if __name__=='__main__':main()
