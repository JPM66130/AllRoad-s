from pathlib import Path


def test_launcher_uses_fresh_geocoding_build_token():
    text=(Path(__file__).parents[2]/"AA_LANCER_JEPALYS.bat").read_text(encoding="utf-8-sig")
    assert "v=52.9.199" in text
    assert "build=e3gpsmarker1" not in text
