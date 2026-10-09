import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageChecks(unittest.TestCase):
    def test_complete_original_license_preserved(self):
        digest = hashlib.sha256((ROOT / "LICENSE").read_bytes()).hexdigest()
        self.assertEqual(digest, "f4e7f373b9b996950337e8d41a4a2939c2d90b7725e9baf3d5084a22717ad328")

    def test_manifest_identifies_one_local_skill_package(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "codex-cost-aware-orchestrator")
        self.assertEqual(manifest["license"], "CC0-1.0")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        skill_root = (ROOT / manifest["skills"]).resolve()
        self.assertTrue(skill_root.is_relative_to(ROOT))
        self.assertEqual([p.parent.name for p in skill_root.glob("*/SKILL.md")], ["orchestrate"])
        for unused in ("mcpServers", "apps", "hooks"):
            self.assertNotIn(unused, manifest)

    def test_explicit_invocation_and_codex_scope(self):
        metadata = (ROOT / "skills/orchestrate/agents/openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(metadata, r"(?m)^  allow_implicit_invocation: false$")
        self.assertRegex(metadata, r'(?m)^  products: \["CODEX"\]$')
        match = re.search(r'(?m)^  short_description: "([^"]+)"$', metadata)
        self.assertIsNotNone(match)
        self.assertTrue(25 <= len(match.group(1)) <= 64)

    def test_relative_markdown_links_resolve_inside_package(self):
        for source in ROOT.rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", source.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                destination = (source.parent / target.split("#")[0]).resolve()
                self.assertTrue(destination.is_relative_to(ROOT), (source, target))
                self.assertTrue(destination.exists(), (source, target))

    def test_one_runtime_helper_and_no_service_registration(self):
        helpers = list((ROOT / "skills").rglob("scripts/*.py"))
        self.assertEqual([p.name for p in helpers], ["validate_run.py"])
        for relative in (".mcp.json", ".app.json", "hooks", ".agents/plugins/marketplace.json"):
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_public_source_has_no_personal_paths_or_native_uuid(self):
        for source in ROOT.rglob("*"):
            if not source.is_file() or ".git" in source.parts or source.suffix == ".pyc":
                continue
            content = source.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[A-Za-z]:[\\/]Users[\\/]", content), source)
            self.assertIsNone(re.search(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", content), source)


if __name__ == "__main__":
    unittest.main()
