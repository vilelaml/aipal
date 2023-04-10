import coverage
import unittest

cov = coverage.Coverage(source=["src"])
cov.start()

loader = unittest.TestLoader()
test_suite = loader.discover(start_dir="tests", pattern="test_*.py")
test_runner = unittest.TextTestRunner(verbosity=2)
test_runner.run(test_suite)

cov.stop()
cov.save()
cov.report()
