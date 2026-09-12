from pathlib import Path
import os
import sys
import unittest

API_DIR = Path(__file__).resolve().parents[1]
os.chdir(API_DIR)
sys.path.insert(0, str(API_DIR))

import tests.test_geo as module

suite = unittest.defaultTestLoader.loadTestsFromModule(module)
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
