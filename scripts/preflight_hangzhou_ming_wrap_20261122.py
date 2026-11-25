"""Preflight the observed Hangzhou country briefing's phrase wrap."""

from pathlib import Path
from types import FunctionType

from scripts import stage_square_country_briefings_20261115 as town
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts import register_maria_opening_hodram_wraps_20261122 as parent


base,native=parent.base,parent.native
ROOT=Path("work/analysis/hangzhou_early_actual_20261122/ming_phrase_followup")
OBSERVED=ROOT.parent/"observed_dialogue_and_roles.json"
OUT=ROOT/"native_preflight.json"
KEY=704
REVISED=("The Ming dynasty once flourished. Now the eunuchs do as they please. "
         "The government's falling apart. It's dreadful.")


def main():
    assert not OUT.exists()
    release,observation=map(base.load,(parent.RELEASE,OBSERVED))
    assert release["candidate_sha256"]==base.digest(parent.ROM)==observation["bound_current_candidate_sha256"]
    hold,=[h for h in observation["ordinary_city_dialogue_holds"] if h["message_ID"]==KEY]
    assert base.digest(hold["capture"]["path"])==hold["capture"]["PNG_sha256"]
    runtime=town.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    clean=base.NdsImage.open(town.CLEAN)
    clean_arm=clean.read_file(town.ARM)
    arm,common=runtime.arm,runtime.common
    assert all(clean_arm[a:b]==arm[a:b] for a,b in town.SOURCE_RANGES)
    assert town.selectors(clean_arm)==town.selectors(arm)
    directory=native.digest(arm[town.DIRECTORY_OFFSET:town.TABLE_OFFSET])
    sources=town.common_message_entries(clean.read_file(town.COMMON),clean_arm)
    installed=town.owned_entries(common,arm,directory)
    source,old=sources[KEY],installed[KEY]
    assert source.text.hex()==hold["source_hex"] and old.text.hex()==hold["current_hex"]
    words=" ".join(old.text.decode("ascii").split())
    row=dict(id="COMMON_MESSAGE_704",message_ID=KEY,file_path=town.COMMON,speaker="Shopkeeper",
        context="After Maria asks at the Hangzhou Luxury Shop, the shopkeeper contrasts past Ming prosperity and growing disorder.",
        source_meaning="The once-prosperous Ming dynasty faces growing disorder as eunuchs act arbitrarily. The shopkeeper ends in dismay.",
        localization_note="The shopkeeper speaks plainly about past prosperity, arbitrary rule, growing disorder, and personal dismay. Each sentence carries one of those thoughts.",
        source_reference=town.reference(source),current_reference=town.reference(old),
        source_hex=source.text.hex(),current_hex=old.text.hex(),clean_Japanese=source.text.decode("cp932"),
        previous_English=words,english=REVISED,protected_phrases=[],decision="revision",change_class="wording",
        review=dict.fromkeys(town.GATES,True)|{"formatting":False})
    storage={KEY:town.compile_paragraph(REVISED)}
    resize=FunctionType(relocate.__code__,relocate.__globals__|{"DIRECTORY":directory})
    target_common,target_arm,after,allocation=resize(common,arm,{KEY:row},storage)
    assert allocation["changed_visible_templates"]==[KEY] and allocation["complete_COMMON_and_ARM9_table_inverse"]
    changed=town.with_components(runtime,target_arm,target_common)
    cpu,get,provider=changed.machine(target_arm,target_common,changed.raw,changed.plan)
    final=after[KEY].text
    ptr=get(0x5528C,KEY)
    assert bytes(cpu.mem_read(ptr,len(final)+1))==final+b"\0" and provider.reads
    painter,_,_=town.font_tools(runtime.image)
    font=runtime.image.read_file("/GRP/KANJI.FNT")
    pictures,visible=[],{}
    for label,stored in (("observed wording",old.text),("proposed wrap",final)):
        body,lines=town.native_layout(cpu,stored,KEY,())
        assert " ".join(lines)==(words if label=="observed wording" else REVISED) and len(lines)==4
        plane,glyphs=town.render_portrait(painter,target_arm,font,body)
        assert [glyph["code"] for glyph in glyphs]==town.glyph_codes(body)
        visible[label]=dict(lines=lines,native_display_hex=body.hex(),plane_sha256=native.digest(plane))
        pictures.append((f"{KEY} {label}",plane))
    assert visible["observed wording"]["lines"]==hold["observed_lines"]
    assert visible["proposed wrap"]["lines"]!=hold["observed_lines"]
    assert visible["proposed wrap"]["lines"][1]=="Now the eunuchs do as they please."
    ROOT.mkdir(exist_ok=True)
    sheets=town.portrait_sheets(ROOT,pictures)
    base.save(OUT,dict(candidate_sha256=release["candidate_sha256"],observed_source=str(OBSERVED),
        observed_sha256=base.digest(OBSERVED),record=row,staged_text_hex=final.hex(),storage=allocation,
        visible=visible,sheets=sheets,preflight_only=True,new_gameplay=False))
    print(visible["proposed wrap"]["lines"])


if __name__=="__main__":
    main()

