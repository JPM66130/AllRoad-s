from pathlib import Path
import inspect
from utils import geo
HTML=(Path(__file__).parents[1]/'frontend'/'index.html').read_text(encoding='utf-8')
def test_geocoder_accepts_focus_point_for_ambiguous_names():
    src=inspect.getsource(geo.geocoder); assert 'focus.point.lat' in src and 'focus.point.lon' in src
def test_destination_is_resolved_after_start_with_start_as_focus():
    a=HTML.index('async function previewExisting()'); block=HTML[a:HTML.index('// V52.8.1',a)]; assert 'const startPlace=await arE7ResolveRoutePoint(from,0);' in block; assert 'const endPlace=await arE7ResolveRoutePoint(dest,1,startPlace);' in block; assert 'Promise.all([arE7ResolveRoutePoint' not in block
def test_mobile_geocoder_sends_focus_coordinates():
    a=HTML.index('async function arE7ResolveRoutePoint'); block=HTML[a:HTML.index('async function previewExisting()',a)]; assert 'focus_lat=' in block and 'focus_lon=' in block
