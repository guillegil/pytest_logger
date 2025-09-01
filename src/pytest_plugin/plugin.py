import pytest
from pytest import Item, CallInfo, TestReport, Config, Session
from _pytest.fixtures import FixtureDef
from _pytest.terminal import TerminalReporter
from _pytest.python import Metafunc
from _pytest.nodes import Collector
from _pytest.config.argparsing import Parser
from pathlib import Path
from typing import Any, List, Optional, Union
import warnings

from .mytool.mytool import MyTool

class PytestHooksPlugin:
    """Pytest plugin with commonly available hooks."""
    
    def __init__(self):
        self.allow_hook_verbose = False
    
        self.mytool = MyTool()

    # ========== CONFIGURATION HOOKS ==========
    
    def pytest_addoption(self, parser: Parser) -> None:
        """Add command-line options."""
        parser.addoption(
            "--myoption", 
            action="store", 
            default="myoption_default",
            help="Specify an argument for the plugin"
        )
    
    def pytest_configure(self, config: Config) -> None:
        """Called after command line options have been parsed."""
        if self.allow_hook_verbose: print(f"🔧 Plugin configured")
    
    def pytest_unconfigure(self, config: Config) -> None:
        """Called before test process is exited."""
        if self.allow_hook_verbose: print(f"🔧 Plugin unconfigured")
    
    # ========== SESSION HOOKS ==========
    
    def pytest_sessionstart(self, session: Session) -> None:
        """Called after Session object has been created."""
        if self.allow_hook_verbose: print(f"🚀 Session started")    
        self.session = session
    
    def pytest_sessionfinish(self, session: Session, exitstatus: int) -> None:
        """Called after whole test run finished."""
        if self.allow_hook_verbose: print(f"🏁 Session finished with exit status: {exitstatus}")
    
    # ========== COLLECTION HOOKS ==========
    
    def pytest_collect_file(self, file_path: Path, parent: Collector) -> Optional[Collector]:
        """Create collector for the given path."""
        # Only collect .py files to reduce noise
        if file_path.suffix == '.py':
            if self.allow_hook_verbose: print(f"📁 Collecting file: {file_path}")
        return None
    
    def pytest_generate_tests(self, metafunc: Metafunc) -> None:
        """Generate parametrized tests."""
        if self.allow_hook_verbose: print(f"⚙️ Generating tests for: {metafunc.function.__name__}")
    
    def pytest_collection_modifyitems(self, session: Session, config: Config, items: List[Item]) -> None:
        """Modify collected test items."""
        if self.allow_hook_verbose: print(f"📝 Modifying {len(items)} collected items")
    
    def pytest_collection_finish(self, session: Session) -> None:
        """Called after collection is completed."""
        if self.allow_hook_verbose: print(f"✅ Collection finished")
    
    def pytest_itemcollected(self, item: Item) -> None:
        """Called when test item is collected."""
        if self.allow_hook_verbose: print(f"📋 Item collected: {item.nodeid}")
    
    # ========== TEST EXECUTION HOOKS ==========
    
    def pytest_runtest_protocol(self, item: Item, nextitem: Optional[Item]) -> Optional[bool]:
        """Perform the runtest protocol for a single test item."""
        if self.allow_hook_verbose: print(f"🔄 Running test protocol: {item.nodeid}")
        return None
    
    def pytest_runtest_logstart(self, nodeid: str, location: tuple) -> None:
        """Called at the start of running the runtest protocol."""
        if self.allow_hook_verbose: print(f"📍 Test log start: {nodeid} - {location}")
    
    def pytest_runtest_logfinish(self, nodeid: str, location: tuple) -> None:
        """Called at the end of running the runtest protocol."""
        if self.allow_hook_verbose: print(f"🏁 Test log finish: {nodeid}")
    
    def pytest_runtest_setup(self, item: Item) -> None:
        """Called to execute the test item setup."""
        if self.allow_hook_verbose: print(f"🔧 Test setup: {item.nodeid}")
    
    def pytest_runtest_call(self, item: Item) -> None:
        """Called to run the test."""
        if self.allow_hook_verbose: print(f"▶️ Test call: {item.nodeid}")
    
    def pytest_runtest_teardown(self, item: Item, nextitem: Optional[Item]) -> None:
        """Called to execute the test item teardown."""
        if self.allow_hook_verbose: print(f"🧹 Test teardown: {item.nodeid}")
    
    def pytest_runtest_makereport(self, item: Item, call: CallInfo) -> Optional[TestReport]:
        """Create test report for the given item and call."""
        if self.allow_hook_verbose: print(f"📊 Making report: {item.nodeid} - {call.when}")
        return None 
    
    # ========== FIXTURE HOOKS ==========
    
    def pytest_fixture_setup(self, fixturedef: FixtureDef, request) -> None:
        """Called before fixture setup."""
        if self.allow_hook_verbose: print(f"🔧 Fixture setup: {fixturedef.argname}")
    
    def pytest_fixture_post_finalizer(self, fixturedef: FixtureDef, request) -> None:
        """Called after fixture finalizer."""
        if self.allow_hook_verbose: print(f"🧹 Fixture post finalizer: {fixturedef.argname}")
    
    # ========== REPORTING HOOKS ==========
    
    def pytest_report_header(self, config: Config, start_path: Path) -> Union[str, List[str]]:
        """Add information to test report header."""
        return None
    
    def pytest_report_collectionfinish(self, config: Config, start_path: Path, items: List[Item]) -> Union[str, List[str]]:
        """Add information after collection finished."""
        pass
    
    def pytest_report_teststatus(self, report: TestReport, config: Config) -> Optional[tuple]:
        """Return result-category, shortletter and verbose word."""
        if self.allow_hook_verbose: print(f"📈 Test status: {report.nodeid} - {report.outcome}")
        return None
    
    def pytest_terminal_summary(self, terminalreporter: TerminalReporter, exitstatus: int, config: Config) -> None:
        """Add section to terminal summary reporting."""
        if self.allow_hook_verbose: print(f"📋 Pytest Terminal Summary")
    
    def pytest_runtest_logreport(self, report: TestReport) -> None:
        """Process test setup/call/teardown report."""
        if self.allow_hook_verbose: print(f"📋 Log report: {report.nodeid} - {report.when} - {report.outcome}")
    
    # ========== ERROR/WARNING HOOKS ==========
    
    def pytest_warning_recorded(self, warning_message: warnings.WarningMessage, when: str, nodeid: str, location: tuple) -> None:
        """Called when warning is recorded."""
        if self.allow_hook_verbose: print(f"⚠️ Warning recorded: {warning_message.message}")
    
    def pytest_exception_interact(self, node, call: CallInfo, report: TestReport) -> None:
        """Called when exception occurred and can be interacted with."""
        if self.allow_hook_verbose: print(f"💥 Exception interact: {node.nodeid}")
    
    def pytest_internalerror(self, excrepr, excinfo) -> Optional[bool]:
        """Called for internal errors."""
        if self.allow_hook_verbose: print(f"🚨 Internal error: {excrepr}")
        return None


# Plugin instance
pytest_hooks_plugin = PytestHooksPlugin()

# Register only the commonly available hooks
def pytest_addoption(parser): return pytest_hooks_plugin.pytest_addoption(parser)
def pytest_configure(config): return pytest_hooks_plugin.pytest_configure(config)
def pytest_unconfigure(config): return pytest_hooks_plugin.pytest_unconfigure(config)
def pytest_sessionstart(session): return pytest_hooks_plugin.pytest_sessionstart(session)
def pytest_sessionfinish(session, exitstatus): return pytest_hooks_plugin.pytest_sessionfinish(session, exitstatus)
def pytest_collect_file(file_path, parent): return pytest_hooks_plugin.pytest_collect_file(file_path, parent)
def pytest_generate_tests(metafunc): return pytest_hooks_plugin.pytest_generate_tests(metafunc)
def pytest_collection_modifyitems(session, config, items): return pytest_hooks_plugin.pytest_collection_modifyitems(session, config, items)
def pytest_collection_finish(session): return pytest_hooks_plugin.pytest_collection_finish(session)
def pytest_itemcollected(item): return pytest_hooks_plugin.pytest_itemcollected(item)
def pytest_runtest_protocol(item, nextitem): return pytest_hooks_plugin.pytest_runtest_protocol(item, nextitem)
def pytest_runtest_logstart(nodeid, location): return pytest_hooks_plugin.pytest_runtest_logstart(nodeid, location)
def pytest_runtest_logfinish(nodeid, location): return pytest_hooks_plugin.pytest_runtest_logfinish(nodeid, location)
def pytest_runtest_setup(item): return pytest_hooks_plugin.pytest_runtest_setup(item)
def pytest_runtest_call(item): return pytest_hooks_plugin.pytest_runtest_call(item)
def pytest_runtest_teardown(item, nextitem): return pytest_hooks_plugin.pytest_runtest_teardown(item, nextitem)
def pytest_runtest_makereport(item, call): return pytest_hooks_plugin.pytest_runtest_makereport(item, call)
def pytest_fixture_setup(fixturedef, request): return pytest_hooks_plugin.pytest_fixture_setup(fixturedef, request)
def pytest_fixture_post_finalizer(fixturedef, request): return pytest_hooks_plugin.pytest_fixture_post_finalizer(fixturedef, request)
def pytest_report_header(config, start_path): return pytest_hooks_plugin.pytest_report_header(config, start_path)
def pytest_report_collectionfinish(config, start_path, items): return pytest_hooks_plugin.pytest_report_collectionfinish(config, start_path, items)
def pytest_report_teststatus(report, config): return pytest_hooks_plugin.pytest_report_teststatus(report, config)
def pytest_terminal_summary(terminalreporter, exitstatus, config): return pytest_hooks_plugin.pytest_terminal_summary(terminalreporter, exitstatus, config)
def pytest_runtest_logreport(report): return pytest_hooks_plugin.pytest_runtest_logreport(report)
def pytest_warning_recorded(warning_message, when, nodeid, location): return pytest_hooks_plugin.pytest_warning_recorded(warning_message, when, nodeid, location)
def pytest_exception_interact(node, call, report): return pytest_hooks_plugin.pytest_exception_interact(node, call, report)
def pytest_internalerror(excrepr, excinfo): return pytest_hooks_plugin.pytest_internalerror(excrepr, excinfo)