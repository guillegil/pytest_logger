import pytest
from pytest import Item, CallInfo, TestReport, Config, Session, OptionGroup
from _pytest.fixtures import FixtureDef
from _pytest.terminal import TerminalReporter
from _pytest.python import Metafunc
from _pytest.nodes import Collector
from _pytest.config.argparsing import Parser
from pathlib import Path
from typing import Any, List, Optional, Union
import warnings

from .logger.logger import log, levels

from pytest_meta import meta


def __map_correct_level(level_name: str) -> int:
    level_name = level_name.lower().replace(' ', '').replace('-', '').replace('_', '')
    
    for key, _ in levels.items():
        if level_name in key:
            level_name = key
            break

    return levels.get(level_name, {}).get('level', levels['info']['level'])   

# ========== CONFIGURATION HOOKS ==========

@pytest.hookimpl
def pytest_addoption(parser: Parser) -> None:
    """Add command-line options."""
    parser.addoption(
        "--term-config-loglevel", 
        action="store", 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Defines the log level for the terminal logs at config time."
    )

    parser.addoption(
        "--term-setup-loglevel", 
        action="store", 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Defines the log level for the terminal logs at setup time."
    )

    parser.addoption(
        "--term-call-loglevel", 
        action="store", 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Defines the log level for the terminal logs at call time."
    )

@pytest.hookimpl
def pytest_configure(config: Config) -> None:
    """Called after command line options have been parsed."""    
    options : OptionGroup = config.option

    term_config_loglevel =  getattr(options, 'term_config_loglevel', 'info') 
    term_setup_loglevel  =  getattr(options, 'term_setup_loglevel', 'info') 
    term_call_loglevel   =  getattr(options, 'term_call_loglevel', 'info') 

    # logger = TestLogger(
    #     logger_name="pytest_logger",
    #     # term_format=__map_correct_level('info'),
    #     # setup_format=__map_correct_level('info'),
    #     term_config_loglevel = __map_correct_level( term_config_loglevel ),
    #     term_setup_loglevel  = __map_correct_level( term_setup_loglevel  ),
    #     term_call_loglevel   = __map_correct_level( term_call_loglevel   )
    # )

    log.init_term_handler()


@pytest.hookimpl
def pytest_unconfigure(config: Config) -> None:
    """Called before test process is exited."""
    pass

# ========== SESSION HOOKS ==========

@pytest.hookimpl
def pytest_sessionstart(session: Session) -> None:
    """Called after Session object has been created."""
    pass  

@pytest.hookimpl
def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """Called after whole test run finished."""
    pass

# ========== COLLECTION HOOKS ==========

@pytest.hookimpl
def pytest_collect_file(file_path: Path, parent: Collector) -> Optional[Collector]:
    """Create collector for the given path."""
    # Only collect .py files to reduce noise
    if file_path.suffix == '.py':
        pass
    return None

@pytest.hookimpl
def pytest_generate_tests(metafunc: Metafunc) -> None:
    """Generate parametrized tests."""
    pass

@pytest.hookimpl
def pytest_collection_modifyitems(session: Session, config: Config, items: List[Item]) -> None:
    """Modify collected test items."""
    pass

@pytest.hookimpl
def pytest_collection_finish(session: Session) -> None:
    """Called after collection is completed."""
    pass

@pytest.hookimpl
def pytest_itemcollected(item: Item) -> None:
    """Called when test item is collected."""
    pass

# ========== TEST EXECUTION HOOKS ==========

@pytest.hookimpl
def pytest_runtest_protocol(item: Item, nextitem: Optional[Item]) -> Optional[bool]:
    """Perform the runtest protocol for a single test item."""
    return None

@pytest.hookimpl
def pytest_runtest_logstart(nodeid: str, location: tuple) -> None:
    """Called at the start of running the runtest protocol."""
    pass

@pytest.hookimpl
def pytest_runtest_logfinish(nodeid: str, location: tuple) -> None:
    """Called at the end of running the runtest protocol."""
    pass

@pytest.hookimpl(trylast=False)
def pytest_runtest_setup(item: Item) -> None:
    """Called to execute the test item setup."""
    print(meta.testcase)
    print(meta.stage)
    print(meta)
    log.configure_term_logger_setup()
    log.init_setup_logger(f'./reports/{meta.testcase}_setup.log')

@pytest.hookimpl
def pytest_runtest_call(item: Item) -> None:
    """Called to run the test."""
    log.configure_term_logger_call()

@pytest.hookimpl
def pytest_runtest_teardown(item: Item, nextitem: Optional[Item]) -> None:
    """Called to execute the test item teardown."""
    pass

@pytest.hookimpl
def pytest_runtest_makereport(item: Item, call: CallInfo) -> Optional[TestReport]:
    """Create test report for the given item and call."""
    return None 

# ========== FIXTURE HOOKS ==========

@pytest.hookimpl
def pytest_fixture_setup(fixturedef: FixtureDef, request) -> None:
    """Called before fixture setup."""
    pass

@pytest.hookimpl
def pytest_fixture_post_finalizer(fixturedef: FixtureDef, request) -> None:
    """Called after fixture finalizer."""
    pass

# ========== REPORTING HOOKS ==========

@pytest.hookimpl
def pytest_report_header(config: Config, start_path: Path) -> Union[str, List[str]]:
    """Add information to test report header."""
    return None

@pytest.hookimpl
def pytest_report_collectionfinish(config: Config, start_path: Path, items: List[Item]) -> Union[str, List[str]]:
    """Add information after collection finished."""
    pass

@pytest.hookimpl
def pytest_report_teststatus(report: TestReport, config: Config) -> Optional[tuple]:
    """Return result-category, shortletter and verbose word."""
pass

@pytest.hookimpl
def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: int, config: Config) -> None:
    """Add section to terminal summary reporting."""
    pass

@pytest.hookimpl
def pytest_runtest_logreport(report: TestReport) -> None:
    """Process test setup/call/teardown report."""
    pass

# ========== ERROR/WARNING HOOKS ==========

@pytest.hookimpl
def pytest_warning_recorded(warning_message: warnings.WarningMessage, when: str, nodeid: str, location: tuple) -> None:
    """Called when warning is recorded."""
    pass

@pytest.hookimpl
def pytest_exception_interact(node, call: CallInfo, report: TestReport) -> None:
    """Called when exception occurred and can be interacted with."""
    pass

@pytest.hookimpl
def pytest_internalerror(excrepr, excinfo) -> Optional[bool]:
    """Called for internal errors."""
    return None
