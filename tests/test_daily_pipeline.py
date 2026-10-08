"""Daily study-pack pipeline: content checks, deterministic figures and rendering, archive tags."""
import copy, json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "daily"))
from engine import schema, render, archive, paths, plan  # noqa: E402

REF = "2026-10-07"


def load(date=REF):
    return json.loads((ROOT / "daily/days" / date / "content.json").read_text(encoding="utf-8"))


class DailyPipeline(unittest.TestCase):
    def test_reference_day_is_valid(self):
        self.assertEqual(schema.validate(load()), [])

    def test_every_committed_day_is_valid(self):
        for f in sorted((ROOT / "daily/days").glob("*/content.json")):
            with self.subTest(day=f.parent.name):
                self.assertEqual(schema.validate(json.loads(f.read_text(encoding="utf-8"))), [])

    def test_checks_catch_missing_and_banned_content(self):
        c = copy.deepcopy(load())
        del c["muscles"][0]["n"]
        c["acupoints"][0]["pinyin"] = "Zhongfu"
        c["chapters"][0]["blocks"][0]["zh"] = "public health"
        errs = " | ".join(schema.validate(c))
        self.assertIn("missing n", errs)
        self.assertIn("tone marks", errs)
        self.assertIn("banned framing", errs)

    def test_plan_mismatch_is_reported(self):
        c = copy.deepcopy(load())
        c["acupoints"] = c["acupoints"][::-1]
        self.assertTrue(any("plan" in e for e in schema.validate(c)))

    def test_figures_are_deterministic_and_match_the_record(self):
        for f in sorted((ROOT / "daily/days").glob("*/figures.py")):
            with self.subTest(day=f.parent.name), tempfile.TemporaryDirectory() as tmp:
                subprocess.run([sys.executable, str(f), tmp], check=True, cwd=f.parent, capture_output=True)
                made = {p.name: p.read_bytes() for p in Path(tmp).glob("*.svg")}
                kept = {p.name: p.read_bytes() for p in (f.parent / "build/资源").glob("*.svg")}
                self.assertEqual(made, kept)

    def test_sections_render_identically(self):
        for f in sorted((ROOT / "daily/days").glob("*/content.json")):
            date = f.parent.name
            B = paths.build_dir(date)
            if not (B / "sections").exists():
                continue
            with self.subTest(day=date), tempfile.TemporaryDirectory() as tmp:
                c = json.loads(f.read_text(encoding="utf-8"))
                figs = {p.name[:2]: p.name for p in (B / "资源").glob("*.svg")}
                render.render_sections(c, figs, tmp)
                for p in Path(tmp).iterdir():
                    self.assertEqual(p.read_text(encoding="utf-8"), (B / "sections" / p.name).read_text(encoding="utf-8"), p.name)

    def test_archive_items_use_the_fixed_top_levels(self):
        for it in archive.items(load()):
            self.assertTrue(any(it["vertical"].startswith(t) for t in archive.TOP_LEVELS), it["vertical"])
            self.assertEqual(len(it["review_schedule"]), 5)

    def test_plan_covers_all_points(self):
        S = plan.schedule()
        names = [a["name"] for d in S["learning_days"] for a in d["acupoints"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(names), S["counts"]["acupoints"])


if __name__ == "__main__":
    unittest.main()
