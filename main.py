import os
import sys
from case.xdclass_test import ApiTestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    app = ApiTestCase()
    app.run_all_case("ErgoSportive")
