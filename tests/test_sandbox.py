"""Tests for NEXUS Sandbox isolation."""
import os
import tempfile
from core.sandbox import SandboxManager


class TestSandboxEnv:
    """Test environment sanitization."""

    def setup_method(self):
        self.sandbox = SandboxManager(timeout_seconds=10)

    def test_safe_env_strips_api_keys(self):
        env = self.sandbox._build_safe_env("/fake/script.py")
        for key in self.sandbox.BLOCKED_ENV_VARS:
            assert env[key] == "", f"{key} should be blanked"

    def test_safe_env_preserves_path(self):
        env = self.sandbox._build_safe_env("/fake/script.py")
        assert env["PATH"] == os.environ.get("PATH", "")

    def test_safe_env_has_sandbox_flag(self):
        env = self.sandbox._build_safe_env("/fake/script.py")
        assert env["NEXUS_SANDBOX_MODE"] == "1"

    def test_safe_env_preserves_windows_vars(self):
        env = self.sandbox._build_safe_env("/fake/script.py")
        assert "SYSTEMROOT" in env
        assert "TEMP" in env
        assert "TMP" in env


class TestSandboxExecution:
    """Test subprocess execution."""

    def setup_method(self):
        self.sandbox = SandboxManager(timeout_seconds=5)

    def test_execute_valid_script(self):
        # Create a temp script that outputs JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('import sys, json\n')
            f.write('data = json.loads(sys.stdin.readline())\n')
            f.write('print(json.dumps({"result": "ok", "echo": data.get("prompt", "")}))\n')
            script_path = f.name
        try:
            result = self.sandbox.execute_safely(script_path, {"prompt": "hello"})
            assert result["status"] == "success"
        finally:
            os.unlink(script_path)

    def test_timeout_kills_process(self):
        sandbox = SandboxManager(timeout_seconds=2)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('import time\ntime.sleep(60)\n')
            script_path = f.name
        try:
            result = sandbox.execute_safely(script_path, {"prompt": "test"})
            assert result["status"] == "error"
            assert "Timeout" in result["message"] or "timeout" in result["message"].lower()
        finally:
            os.unlink(script_path)

    def test_missing_script(self):
        result = self.sandbox.execute_safely("/nonexistent/script.py", {"prompt": "test"})
        assert result["status"] == "error"

    def test_script_with_nonzero_exit(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('import sys\nsys.exit(1)\n')
            script_path = f.name
        try:
            result = self.sandbox.execute_safely(script_path, {"prompt": "test"})
            assert result["status"] == "error"
        finally:
            os.unlink(script_path)

    def test_plain_text_output(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("just plain text")\n')
            script_path = f.name
        try:
            result = self.sandbox.execute_safely(script_path, {"prompt": "test"})
            assert result["status"] == "success"
            assert result["data"] == "just plain text"
        finally:
            os.unlink(script_path)

    def test_sandbox_env_blocks_api_key_access(self):
        """Verify that a sandboxed script cannot read sensitive env vars."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('import os, json\n')
            f.write('key = os.environ.get("OPENAI_API_KEY", "EMPTY")\n')
            f.write('print(json.dumps({"key": key}))\n')
            script_path = f.name
        try:
            # Set a fake API key in current env
            os.environ["OPENAI_API_KEY"] = "sk-secret-test-key-12345"
            result = self.sandbox.execute_safely(script_path, {"prompt": "test"})
            assert result["status"] == "success"
            assert result["data"]["key"] == "" or result["data"]["key"] == "EMPTY"
        finally:
            os.environ.pop("OPENAI_API_KEY", None)
            os.unlink(script_path)


class TestSandboxManager:
    def test_custom_timeout(self):
        s = SandboxManager(timeout_seconds=60)
        assert s.timeout == 60

    def test_default_timeout(self):
        s = SandboxManager()
        assert s.timeout == 30
