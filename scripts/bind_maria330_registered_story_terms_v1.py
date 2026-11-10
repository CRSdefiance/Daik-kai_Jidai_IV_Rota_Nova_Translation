"""Bind the existing full Proof term and epithet to exact unchanged registered story anchors."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

def main():
    out=ROOT/'registered_story_terms_reference_v1.json';assert not out.exists()
    current_path=ROOT/'current_v1/current_effective.json';current=load(current_path);runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    blocks=IlnkContainer.parse(ctx.image.read_file('/data/SC3.DK4')).blocks;anchors=[]
    paths=[Path('translations/maria301_integrated_final_review_v1.json'),Path('translations/maria310_integrated_final_review_v1.json')]
    for path,ident,term in [(paths[0],'DK4_MES_B28_R0005','Soaring Scarlet Orca'),(paths[1],'DK4_MES_B53_R0006','Proofs of Conquest')]:
        prior=load(path);assert digest(prior['target_ROM'])==prior['target_ROM_sha256']
        image=NdsImage.open(prior['target_ROM']);assert image.read_file('/__arm9__.bin')==ctx.arm and image.read_file('/COMMON/MESFILE.DK4')==ctx.common
        row=next(r for r in prior['records'] if r['id']==ident);assert all(row['review'].values()) and term in row['english']
        block=row['block'];assert IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks[block]==blocks[block]
        ref=row['planned_integrated_reference'];body=bytes.fromhex(ref['exact_stored_hex'])
        assert blocks[block][ref['offset']:ref['offset']+len(body)+1]==body+b'\0'
        anchors.append(dict(term=term,path=str(path),path_sha256=digest(path),id=ident,english=row['english'],source_reference=row['source_reference'],
            source_hex=row['source_hex'],current_stored_reference=ref,review=row['review'],exact_current_complete_block_sha256=sha(blocks[block])))
    save(out,dict(runtime=runtime,anchors=anchors,full_Proof_term=dict(singular='Proof of Conquest',plural='Proofs of Conquest'),
        epithet=dict(source='翔緋鯱',english='Soaring Scarlet Orca',scope='Existing source-qualified naval-context localization inference, not an official English-name claim; distinct from the Shachihoko item.'),
        source_review='translations/maria_epithet_source_review_v294.json',source_review_sha256=digest('translations/maria_epithet_source_review_v294.json'),
        exact_unchanged_registered_anchors_reused_not_new_dictionary_research=True,no_new_font_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [current_path,*paths,Path(__file__)]}))
    print('Bound both exact registered story anchors: full Proof term and Soaring Scarlet Orca; no new font/gameplay approval.')

if __name__=='__main__':main()
