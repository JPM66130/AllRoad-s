from pathlib import Path

HTML = (Path(__file__).parents[1] / 'frontend' / 'index.html').read_text(encoding='utf-8')


def test_driving_refresh_keeps_drive_layer_authority():
    assert "if(arE7DrivingStates.has(state) && (!demoMode||window.__allroadsRouteSimulationMode)){" in HTML
    assert "enableDrivingBaseLayer();\n        return;" in HTML


def test_clearing_bearing_does_not_restore_layer_by_default():
    assert "function clearDrivingBearing(restoreBase=false)" in HTML
    assert "if(restoreBase)restoreDrivingBaseLayer();" in HTML


def test_only_real_exit_from_driving_restores_previous_layer():
    assert "if(wasDriving&&!drivingState){\n      try{clearDrivingBearing()}catch(_){}\n      try{restoreDrivingBaseLayer()}catch(_){}" in HTML
    assert "try{clearDrivingBearing()}catch(_){}\n    try{restoreDrivingBaseLayer()}catch(_){}\n    try{\n      if(mobileDriveMarker" in HTML


def test_transient_camera_losses_do_not_change_background_layer():
    assert "if(!rawPos||pts.length<2){" in HTML
    assert "holding-camera-no-fresh-gps" in HTML
    assert "arE7LastDrivingCamera" in HTML
    assert "if(Math.hypot(headingDx,headingDy)<=1){clearDrivingBearing();return;}" in HTML
