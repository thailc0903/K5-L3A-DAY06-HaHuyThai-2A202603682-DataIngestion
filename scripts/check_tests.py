"""Run meaningful pipeline/review checks and save actual unittest output/counts."""
import io
import json
import time
import unittest
from datetime import datetime,timezone
from starter_import import ROOT

started=time.perf_counter()
stream=io.StringIO()
suite=unittest.defaultTestLoader.discover(str(ROOT/"tests"),pattern="test_*.py")
result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
(ROOT/"results/unit_test_run.txt").write_text(stream.getvalue(),encoding="utf-8")
summary={"run_at_utc":datetime.now(timezone.utc).isoformat(),"tests_run":result.testsRun,
    "failures":len(result.failures),"errors":len(result.errors),"skipped":len(result.skipped),
    "successful":result.wasSuccessful(),"elapsed_seconds":time.perf_counter()-started}
(ROOT/"results/unit_test_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
print(stream.getvalue())
print(json.dumps(summary,indent=2))
if not result.wasSuccessful():
    raise SystemExit(1)
