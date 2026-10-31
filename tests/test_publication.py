import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOADS = (
    "counters.svg",
    "counters-mobile.svg",
    "calendar.svg",
    "calendar-mobile.svg",
    "cadence.svg",
    "cadence-mobile.svg",
    "pulse.svg",
    "pulse-mobile.svg",
    "activity.svg",
    "snapshot.json",
    "README.md",
)


def git(directory, *args):
    return subprocess.check_output(
        ["git", "-C", str(directory), *args], text=True, stderr=subprocess.DEVNULL
    ).strip()


class PublicationTests(unittest.TestCase):
    def publish(self, omitted=None):
        workflow = (ROOT / ".github/workflows/profile.yml").read_text()
        script = workflow.split("      - name: Publish generated assets only\n")[
            1
        ].split("        run: |\n")[1]
        script = "\n".join(line[10:] for line in script.splitlines())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            checkout.mkdir()
            remote = root / "remote.git"
            git(root, "init", "--bare", "--initial-branch=profile-data", str(remote))
            git(checkout, "init", "--initial-branch=main")
            git(checkout, "config", "user.name", "Fixture")
            git(checkout, "config", "user.email", "fixture@example.invalid")
            for name in (*PAYLOADS, "openclaw.svg"):
                (checkout / name).write_text("previous")
            (checkout / "unrelated.txt").write_text("preserve")
            git(checkout, "add", ".")
            git(checkout, "commit", "-m", "Previous snapshot")
            git(checkout, "remote", "add", "origin", str(remote))
            git(checkout, "push", "origin", "HEAD:profile-data")
            git(checkout, "fetch", "origin")
            before = git(remote, "rev-parse", "refs/heads/profile-data")
            output = root / "generated"
            output.mkdir()
            for name in PAYLOADS:
                if name != omitted:
                    (output / name).write_text("current " + name)
            result = subprocess.run(
                ["bash", "-e", "-c", script],
                cwd=checkout,
                env={"PATH": "/usr/bin:/bin", "GENERATED": str(output)},
                capture_output=True,
                text=True,
                check=False,
            )
            after = git(remote, "rev-parse", "refs/heads/profile-data")
            if omitted:
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(omitted, result.stderr)
                self.assertEqual(before, after)
            else:
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotEqual(before, after)
                for name in PAYLOADS:
                    self.assertEqual(
                        git(remote, "show", f"profile-data:{name}"), "current " + name
                    )
                self.assertEqual(
                    git(remote, "show", "profile-data:unrelated.txt"), "preserve"
                )
                self.assertNotIn(
                    "openclaw.svg",
                    git(remote, "ls-tree", "--name-only", "profile-data").splitlines(),
                )
                self.assertEqual(
                    git(remote, "rev-list", "--count", f"{before}..{after}"), "1"
                )

    def test_missing_current_payload_retains_remote_snapshot(self):
        for name in PAYLOADS:
            with self.subTest(name=name):
                self.publish(omitted=name)

    def test_complete_snapshot_migrates_the_legacy_card_in_one_commit(self):
        self.publish()


if __name__ == "__main__":
    unittest.main()
