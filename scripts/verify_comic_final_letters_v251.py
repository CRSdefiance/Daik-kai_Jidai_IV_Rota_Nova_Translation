"""Check stored five-bit comic letters against the same restored backing plane."""

import argparse
import json
import struct
from pathlib import Path
from unittest.mock import patch

from PIL import Image, ImageDraw

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_bgr555_art import FRAME_BYTES, render_region_payload
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.maria_gallery_v180 import region_bytes

ROOT=Path("work/analysis/comic_fidelity_v251")
BATCH=Path("translations/gallery_reveal_comic_raw_art_v7.json")
ROM=Path("out/all_routes_combined_v247_candidate.nds")


def backing_and_payload(row,region,batch,block):
    # Record the actual renderer's draw canvases without changing its output.
    factory=Image.new;drawing=ImageDraw.ImageDraw.text;made=[];events=[]
    def record_image(*args,**kwargs):
        image=factory(*args,**kwargs);made.append(image);return image
    def record_text(self,xy,text,*args,**kwargs):
        font=kwargs.get("font")
        events.append({"canvas":next(n for n,im in enumerate(made) if im is self._image),
                       "text":text,"font_size":getattr(font,"size",None)})
        return drawing(self,xy,text,*args,**kwargs)
    with patch.object(Image,"new",side_effect=record_image),patch.object(ImageDraw.ImageDraw,"text",new=record_text):
        payload,proof=render_region_payload(row,region,batch,block)
    targets=set()
    if proof.get("segments"):
        for part in proof["segments"]:
            targets.add(next(e["canvas"] for e in events if e["text"]==part["text"] and e["font_size"]==part["font_size"]))
    else:
        lines=set(proof["automatic_lines"])
        targets={e["canvas"] for e in events if e["text"] in lines}
    if not targets:
        raise ValueError("No full English draw canvases identified")
    if "full_mask_sha256" in proof:
        matched=any(sha(image.tobytes())==proof["full_mask_sha256"] for image in made)
        if row.get("rotation")==-90:
            matched=matched or any(sha(made[n].transpose(Image.Transpose.ROTATE_270).tobytes())==proof["full_mask_sha256"] for n in targets)
        assert matched,row["id"]
    sequence=[0]
    def image_without_letters(*args,**kwargs):
        image=factory(*args,**kwargs);image.info["letter_audit_canvas"]=sequence[0];sequence[0]+=1;return image
    def text_without_letters(self,xy,text,*args,**kwargs):
        if self._image.info.get("letter_audit_canvas") in targets:
            return None
        return drawing(self,xy,text,*args,**kwargs)
    # Only full-line/segment English paint is suppressed. Individual glyph
    # measurement and the original source restoration/protection still execute.
    with patch.object(Image,"new",side_effect=image_without_letters),patch.object(ImageDraw.ImageDraw,"text",new=text_without_letters):
        backing,_=render_region_payload(row,region,batch,block)
    assert sequence[0]==len(made)
    return payload,backing,proof,sorted(targets)


def glyph_pixels(words,backing,width,box):
    x0,y0,x1,y1=box
    return [(x,y) for y in range(y0,y1) for x in range(x0,x1)
            if (words[y*width+x]&32767)!=(backing[y*width+x]&32767)]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--rom",type=Path,default=ROM)
    parser.add_argument("--batch",type=Path,default=BATCH)
    parser.add_argument("--out",type=Path,default=ROOT)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    batch=json.loads(args.batch.read_text(encoding="utf-8"));base=NdsImage.open("out/raphael_natural_v2_accepted_base.nds");candidate=NdsImage.open(args.rom)
    manifest=json.loads(args.rom.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert sha(args.rom.read_bytes())==manifest["candidate_sha256"]
    assert str(args.batch).replace("\\","/") in [s.replace("\\","/") for s in manifest["batches"]]
    source=base.read_file(batch["file_path"]);assert sha(source)==batch["source_file_sha256"]
    block=IlnkContainer.parse(source).blocks[19];saved=IlnkContainer.parse(candidate.read_file(batch["file_path"])).blocks[19]
    cases=[]
    for row in batch["records"]:
        f=row["image_index"];x0,y0,x1,y1=row["box"];width=x1-x0;height=y1-y0
        region=region_bytes(block[f*FRAME_BYTES:(f+1)*FRAME_BYTES],row["box"])
        actual=region_bytes(saved[f*FRAME_BYTES:(f+1)*FRAME_BYTES],row["box"])
        payload,backing,proof,targets=backing_and_payload(row,region,batch,block)
        assert actual==payload and sha(payload)==row["words_sha256"]
        assert len(payload)==len(backing)==width*height*2
        words=list(struct.unpack(f"<{width*height}H",actual));blank=list(struct.unpack(f"<{width*height}H",backing))
        glyphs=[]
        for g in proof["visible_characters"]:
            box=list(g["bbox"])
            if row["background_rule"]=="source-reveal-comic-v7":box=[box[0]-x0,box[1]-y0,box[2]-x0,box[3]-y0]
            assert 0<=box[0]<box[2]<=width and 0<=box[1]<box[3]<=height
            visible=glyph_pixels(words,blank,width,box)
            if not visible:
                raise ValueError("No final five-bit English contrast for "+row["id"]+":"+g["character"])
            glyphs.append({"character":g["character"],"complete_record_relative_bounds":box,
                           "final_Bgr555_changed_pixels_in_glyph_bounds":len(visible)})
        assert "".join(g["character"] for g in glyphs)=="".join(row["english"].split())
        negatives=[]
        for index in sorted({0,len(glyphs)-1}):
            damaged=words[:];box=glyphs[index]["complete_record_relative_bounds"]
            for y in range(box[1],box[3]):
                for x in range(box[0],box[2]):damaged[y*width+x]=blank[y*width+x]
            assert not glyph_pixels(damaged,blank,width,box)
            assert struct.pack(f"<{len(damaged)}H",*damaged)!=payload
            negatives.append({"character_position":index,"character":glyphs[index]["character"],"erased_letter_detected":True})
        cases.append({"id":row["id"],"image_index":f,"source_text":row["source_text"],"english":row["english"],
                      "font_size":proof.get("font_size"),"automatic_lines":proof.get("automatic_lines"),
                      "word_payload_sha256":sha(payload),"reconstructed_backing_sha256":sha(backing),
                      "captured_English_draw_canvases":targets,"characters":glyphs,
                      "first_and_final_quantized_letters_present":True,"erased_letter_negative_cases":negatives,
                      "background_reconstruction_still_approximate_where_declared":True,
                      "actual_native_gallery_display_not_proved":True})
    result={"format":"dk4-comic-final-letters-v251","candidate_sha256":sha(args.rom.read_bytes()),"batch_sha256":sha(args.batch.read_bytes()),
            "records_checked":len(cases),"final_quantized_character_bounds_checked":sum(len(c["characters"]) for c in cases),
            "first_final_erasure_negative_cases":sum(len(c["erased_letter_negative_cases"]) for c in cases),"cases":cases,
            "all_saved_word_planes_reproduce_exactly":True,"checks_are_stored_art_not_native_GPU_or_readability_proof":True,
            "existing_English_unchanged":True,"ROM_modified":False,"all18_plaque_hint_entries_remain_incomplete":True,"full_goal_complete":False}
    (args.out/"proof.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"records":len(cases),"final_pixel_character_bounds":result["final_quantized_character_bounds_checked"],"first_last_negative_cases":result["first_final_erasure_negative_cases"],"ROM_modified":False}))


if __name__=="__main__":
    main()
