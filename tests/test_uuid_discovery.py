"""Execute only a synthetic helper copy with inert query/flash/service spies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "klipper_config" / "setup_canbus_ebb.sh"
BASH = shutil.which("bash")
assert BASH is not None
SPY = r'''
import json, os, sys
from pathlib import Path
root = Path(os.environ["HELPER_SPY_ROOT"]).resolve()
command = Path(sys.argv[0]).name
args = sys.argv[1:]
assert os.environ["PATH"] == str(root / "bin")
with (root / "calls.jsonl").open("a") as f:
    f.write(json.dumps({"command": command, "argv": args}) + "\n")
if command in ("python", "python3"):
    assert Path(args[0]).resolve().is_relative_to(root)
    if "-q" in args or args[-1] == "can0":
        print(os.environ["HELPER_SPY_QUERY"])
        sys.exit(int(os.environ["HELPER_SPY_QUERY_EXIT"]))
    if "-f" in args:
        assert Path(args[args.index("-f") + 1]).resolve().is_relative_to(root)
        sys.exit(0)  # Inert flash receipt, no firmware or device is opened.
if command == "sudo":
    assert args == ["systemctl", "restart", "klipper"]
    sys.exit(0)  # Never invoke sudo/systemctl.
raise AssertionError("forbidden helper command: " + command + repr(args))
'''


class UUIDDiscoveryTests(unittest.TestCase):
    def invoke(self, option, output, query_exit=0, manual=""):
        with tempfile.TemporaryDirectory(prefix="can-helper-spy-") as temp:
            root = Path(temp).resolve()
            app, tools = root / "app", root / "bin"
            app.mkdir()
            tools.mkdir()
            script = app / SCRIPT.name
            shutil.copyfile(SCRIPT, script)
            cfg = app / "printer_data" / "config" / "ebb-sb2209.cfg"
            cfg.parent.mkdir(parents=True)
            before = b"[mcu EBBCan]\ncanbus_uuid: aaaaaaaaaaaa\n# synthetic canary\n"
            cfg.write_bytes(before)
            for name in ("dirname", "grep", "sort", "head", "sed"):
                real = shutil.which(name)
                assert real is not None
                (tools / name).symlink_to(real)
            for path in [tools / name for name in ("python3", "sudo", "make", "ip", "tee", "systemctl")] + [
                    app / "klippy-env" / "bin" / "python"]:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"#!{sys.executable}\n" + SPY)
                path.chmod(0o700)
            env = {"PATH": str(tools), "HOME": str(root), "TMPDIR": str(root), "LC_ALL": "C",
                   "HELPER_SPY_ROOT": str(root), "HELPER_SPY_QUERY": output,
                   "HELPER_SPY_QUERY_EXIT": str(query_exit)}
            result = subprocess.run([BASH, str(script)], input=f"{option}\n{manual}\n".encode(),
                                    cwd=root, env=env, capture_output=True, timeout=10)
            calls = [json.loads(line) for line in (root / "calls.jsonl").read_text().splitlines()]
            self.assertEqual(script.read_bytes(), SCRIPT.read_bytes())
            receipts = os.environ.get("CAN_HELPER_TEST_RECEIPTS")
            if receipts:
                suffix = hashlib.sha256((str(option) + output + str(query_exit) + manual).encode()).hexdigest()[:16]
                target = Path(receipts) / self._testMethodName / suffix
                target.mkdir(parents=True, exist_ok=False)
                (target / "stdout.bin").write_bytes(result.stdout)
                (target / "stderr.bin").write_bytes(result.stderr)
                (target / "calls.jsonl").write_bytes((root / "calls.jsonl").read_bytes())
                (target / "config-after.bin").write_bytes(cfg.read_bytes())
                (target / "receipt.json").write_text(json.dumps({"argv": result.args, "cwd": str(root),
                    "environment": env, "exit": result.returncode,
                    "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest()}, indent=2) + "\n")
            return result, calls, before, cfg.read_bytes()

    def test_ambiguous_scans_do_not_flash_update_config_or_restart(self):
        for option in (4, 6):
            with self.subTest(option=option):
                output = "Found canbus_uuid=111111111111\nFound canbus_uuid=222222222222"
                result, calls, before, after = self.invoke(option, output)
                self.assertNotEqual(result.returncode, 0, "multiple UUIDs must require deliberate board selection")
                self.assertEqual(after, before, "ambiguous scans must not rewrite even the synthetic config")
                self.assertEqual(len(calls), 1, "only the query spy may be invoked")
                self.assertIn(b"multiple", result.stdout.lower() + result.stderr.lower())

    def test_failed_queries_do_not_use_partial_output(self):
        for option in (4, 6):
            with self.subTest(option=option):
                result, calls, before, after = self.invoke(option, "Found canbus_uuid=111111111111", query_exit=9)
                self.assertNotEqual(result.returncode, 0, "failed queries must not authorize configuration or flashing")
                self.assertEqual(after, before)
                self.assertEqual(len(calls), 1)

    def test_single_unique_uuid_keeps_existing_success_paths(self):
        for option in (4, 6):
            with self.subTest(option=option):
                result, calls, before, after = self.invoke(option, "Found canbus_uuid=111111111111")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(len(calls), 2)
                if option == 4:
                    self.assertIn("-f", calls[1]["argv"])
                    self.assertEqual(calls[1]["argv"][calls[1]["argv"].index("-u") + 1], "111111111111")
                    self.assertEqual(after, before)
                else:
                    self.assertEqual(calls[1]["command"], "sudo")
                    self.assertEqual(after, before.replace(b"aaaaaaaaaaaa", b"111111111111"))

    def test_duplicate_uuid_lines_still_identify_one_board(self):
        for option in (4, 6):
            with self.subTest(option=option):
                result, calls, before, after = self.invoke(
                    option, "Found canbus_uuid=111111111111\nFound canbus_uuid=111111111111")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(len(calls), 2)
                if option == 4:
                    self.assertEqual(after, before)
                else:
                    self.assertEqual(after, before.replace(b"aaaaaaaaaaaa", b"111111111111"))

    def test_empty_katapult_scan_still_allows_explicit_manual_uuid(self):
        result, calls, before, after = self.invoke(4, "No devices", manual="111111111111")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 2)
        self.assertIn("111111111111", calls[1]["argv"])
        self.assertEqual(after, before)


if __name__ == "__main__":
    unittest.main()
