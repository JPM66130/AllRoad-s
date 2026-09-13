from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def text(): return (ROOT/'api/frontend/index.html').read_text(encoding='utf-8')
def test_j243_boot_reconciles_empty_two_view_state():
 s=text()
 assert 'jepalys-j243-boot-state-authority' in s
 assert 'body:not(.vs-driving-visible) #allroads-mobile-home' in s
 assert "b.classList.remove('ar-mobile-nav-open','vsflat-route-pending','ar52-vehicle-open')" in s
 assert "b.classList.add('ar-mobile-home-open')" in s
def test_j243_mirrors_and_cache():
 assert (ROOT/'api/frontend/index.html').read_bytes()==(ROOT/'frontend/index.html').read_bytes()
 sw=(ROOT/'api/frontend/sw.js').read_text(encoding='utf-8')
 assert "VERSION='52.9.243'" in sw and 'jepalys-v52-9-243-final' in sw
 assert (ROOT/'api/frontend/sw.js').read_bytes()==(ROOT/'frontend/sw.js').read_bytes()
