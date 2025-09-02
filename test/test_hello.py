
import pytest
from pytest_logger import log

@pytest.fixture
def setup():
    log.info('This is info from the setup')
    log.warning('This is warning from the setup')

@pytest.mark.hello
def test_hello(setup):
    log.info("✋ Hello from a test!")
    log.warning("⚠️  Warning from a test!")