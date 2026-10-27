"""Town font tools at screenshot-calibrated 16-pixel row pitch; no ROM edits."""
import inspect
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font as original_independent
from dk4tool.patch.grand_race_menu_release import sha

def font_tools(rom):
 class CurrentFont:
  @staticmethod
  def open(path):return rom
 source=inspect.getsource(original_raster);assert source.count('struct.pack("<2I", 6, 16)')==1
 env={**original_raster.__globals__,'NdsImage':CurrentFont};exec(compile(source,__file__,'exec'),env)
 independent_source=inspect.getsource(original_independent);assert independent_source.count('228 * 64')==1 and independent_source.count('row * 16')==2
 independent_source=independent_source.replace('228 * 64','228 * 48');other=dict(original_independent.__globals__);exec(compile(independent_source,__file__,'exec'),other)
 return env['raster'],other['independent_font'],dict(native_raster_sha256=sha(source.encode()),independent_font_sha256=sha(independent_source.encode()),ink_glyph_height=12,native_row_step=16,paper=[228,48],screenshot_calibration='work/analysis/town_services_pixel_anchor_v2101e/original49_exact_native_ink_anchor.json')

def glyph_codes(raw):
 result=[];i=0
 while i<len(raw):
  b=raw[i];wide=0x81<=b<=0x9F or 0xE0<=b<=0xFC;size=2 if wide else 1;code=int.from_bytes(raw[i:i+size],'big');i+=size
  if code not in(10,32):result.append(code)
 return result
