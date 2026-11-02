import subprocess
import tempfile
import unittest
from pathlib import Path


def git(path, *args, check=True):
    return subprocess.run(
        ["git", "-C", str(path), *args], capture_output=True, text=True, check=check
    )


class StalePushTests(unittest.TestCase):
    def test_non_force_push_rejects_stale_parent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            remote = root / "remote.git"
            root.joinpath("seed").mkdir()
            seed = root / "seed"
            git(root, "init", "--bare", str(remote))
            git(seed, "init", "--initial-branch=profile-data")
            git(seed, "config", "user.name", "Fixture")
            git(seed, "config", "user.email", "fixture@example.invalid")
            (seed / "snapshot").write_text("old")
            git(seed, "add", "snapshot")
            git(seed, "commit", "-m", "old")
            git(seed, "remote", "add", "origin", str(remote))
            git(seed, "push", "origin", "HEAD:profile-data")
            for name in ("first", "stale"):
                checkout = root / name
                git(
                    root,
                    "clone",
                    "--branch",
                    "profile-data",
                    str(remote),
                    str(checkout),
                )
                git(checkout, "config", "user.name", "Fixture")
                git(checkout, "config", "user.email", "fixture@example.invalid")
                (checkout / "snapshot").write_text(name)
                git(checkout, "add", "snapshot")
                git(checkout, "commit", "-m", name)
            git(root / "first", "push", "origin", "HEAD:profile-data")
            before = git(remote, "rev-parse", "refs/heads/profile-data").stdout.strip()
            result = git(
                root / "stale", "push", "origin", "HEAD:profile-data", check=False
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("rejected", result.stderr)
            self.assertEqual(
                before,
                git(remote, "rev-parse", "refs/heads/profile-data").stdout.strip(),
            )
            self.assertEqual(
                "first", git(remote, "show", "profile-data:snapshot").stdout
            )


if __name__ == "__main__":
    unittest.main()
