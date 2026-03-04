"""NEXUS Sandbox — Process-level isolation for executing untrusted skills."""
import subprocess
import os
import sys
import json
from utils.logger import get_logger

logger = get_logger("NexusSandbox")


class SandboxManager:
    """Executes skills in a restricted subprocess environment.

    Security measures:
    - Strips sensitive environment variables (API keys, tokens)
    - Passes payload via stdin (not CLI args — prevents shell injection)
    - Enforces strict timeout (prevents infinite loops)
    - Uses sys.executable (not hardcoded 'python')
    - Preserves SYSTEMROOT/TEMP/TMP for Windows compatibility
    """

    # Environment variables to explicitly block
    BLOCKED_ENV_VARS = [
        "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY", "AZURE_API_KEY", "GOOGLE_API_KEY",
        "HF_TOKEN", "HUGGINGFACE_TOKEN", "GITHUB_TOKEN",
        "DATABASE_URL", "SECRET_KEY", "JWT_SECRET",
    ]

    def __init__(self, timeout_seconds: int = 30):
        self.timeout = timeout_seconds

    def _build_safe_env(self, script_path: str) -> dict:
        """Build a sanitized environment dict."""
        safe_env = {
            "PATH": os.environ.get("PATH", ""),
            "PYTHONPATH": os.path.dirname(script_path),
            "NEXUS_SANDBOX_MODE": "1",
            # Windows requires these to function at all
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
            "TEMP": os.environ.get("TEMP", ""),
            "TMP": os.environ.get("TMP", ""),
            # Preserve locale settings
            "LANG": os.environ.get("LANG", ""),
            "LC_ALL": os.environ.get("LC_ALL", ""),
        }
        # Explicitly blank out all known sensitive vars
        for var in self.BLOCKED_ENV_VARS:
            safe_env[var] = ""
        return safe_env

    def execute_safely(self, script_path: str, payload: dict) -> dict:
        """Execute a skill script in a restricted subprocess.

        Args:
            script_path: Path to the Python script to execute
            payload: Dict to pass as JSON via stdin

        Returns:
            Dict with 'status' ('success' or 'error') and 'data' or 'message'
        """
        logger.info(f"Sandbox: executing {os.path.basename(script_path)}")

        safe_env = self._build_safe_env(script_path)
        payload_str = json.dumps(payload)

        try:
            # Use sys.executable, pass payload via stdin (not CLI args)
            process = subprocess.run(
                [sys.executable, script_path],
                input=payload_str + "\n",
                env=safe_env,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if process.returncode != 0:
                logger.error(f"Sandbox error (exit {process.returncode}): {process.stderr[:500]}")
                return {"status": "error", "message": process.stderr[:1000]}

            # Try to parse as JSON, fall back to raw text
            output = process.stdout.strip()
            try:
                result = json.loads(output.split("\n")[0])  # First line only (match MCP pattern)
                return {"status": "success", "data": result}
            except (json.JSONDecodeError, IndexError):
                return {"status": "success", "data": output}

        except subprocess.TimeoutExpired:
            logger.critical(
                f"Sandbox TIMEOUT: {script_path} exceeded {self.timeout}s — process killed"
            )
            return {
                "status": "error",
                "message": f"Timeout: skill exceeded {self.timeout}s limit. Process terminated."
            }
        except FileNotFoundError:
            logger.error(f"Script not found: {script_path}")
            return {"status": "error", "message": f"Script not found: {script_path}"}
        except Exception as e:
            logger.error(f"Sandbox unexpected error: {e}")
            return {"status": "error", "message": str(e)}
