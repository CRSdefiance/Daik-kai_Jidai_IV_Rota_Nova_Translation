"""Fresh current-ROM original long-menu caption/view/backing observation,with read-only callbacks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read
source=Path('scripts/run_lil_B166_menu_owner_trace_v4086.py')
if __name__=='__main__':
    text=checked_text(source.read_text('utf-8'),{
      'import pefile\n':'',
      "pe=pefile.PE(str(CORE),fast_load=True);file_at=":"pebytes=CORE.read_bytes();nt=struct.unpack_from('<I',pebytes,0x3C)[0];assert pebytes[nt:nt+4]==b'PE\\0\\0' and struct.unpack_from('<H',pebytes,nt+24)[0]==0x20B;image_base=struct.unpack_from('<Q',pebytes,nt+48)[0];file_at=",
      'pe.OPTIONAL_HEADER.ImageBase':'image_base',
      'lil_B166_menu_owner_trace_v4086':'lil_B206_menu_owner_v6284','lil_B166_menu_owner_v4086':'lil_B206_menu_owner_v6284',
      "text.startswith(b'Please do') or text.startswith(b'Decline')":"text in [b\"I'll take them!\",b\"That's expensive...\"]",
      'work/analysis/lil_B166_menu_fixture_v4076/focused_typed_menu_constructor_fixtures.json':'work/analysis/lil_B206_long_menu_fixture_v6283/focused_typed_menu_constructor_fixture.json',
      'work/analysis/lil_B166_menu_run_v4077/reviewed_inputs.json':'work/analysis/lil_B206_long_menu_fixture_v6283/inputs.json',
      'source_B166_menu_only_not_story_activation':'source_B206_menu_only_not_story_activation',
    })
    exec(compile(text,str(source)+'::current-B206-long-menu-original-owner','exec'),dict(__name__='__main__',__file__=__file__))
