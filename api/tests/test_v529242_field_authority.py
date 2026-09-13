from pathlib import Path

HTML = Path(__file__).parents[1] / 'frontend' / 'index.html'

def text():
    return HTML.read_text(encoding='utf-8')

def test_j242_version_and_final_authority():
    s=text()
    assert any(v in s for v in ('J242 · Virage Serré · WP35','J243 · Virage Serré · WP35','J244 · Virage Serré · WP35'))
    assert 'jepalys-j242-field-authority' in s
    assert 'grid-template-rows:repeat(2,82px)' in s
    assert 'height:42px!important;min-height:42px' in s

def test_j242_french_is_upstream_of_voice_and_visual():
    s=text()
    assert 'function jepalysInstructionFr' in s
    assert 'message = jepalysInstructionFr(message);' in s
    assert 'const nextText=jepalysInstructionFr(next.text);' in s
    assert 'mobileInstruction.textContent=nextText' in s
    assert 'maneuverVoiceStage(nextText' in s

def test_j242_landscape_maneuver_and_trip_windows():
    s=text()
    assert 'height:104px!important;min-height:104px' in s
    assert 'white-space:normal!important' in s
    assert 'height:64px!important;min-height:64px' in s

def test_j242_route_total_width_kept_white_thinner():
    s=text()
    assert "weight:Math.max(3,weight+2),color:'#FFFFFF'" in s
    assert "weight:Math.min(48,weight+1.0),color:'#0A7BFF'" in s
