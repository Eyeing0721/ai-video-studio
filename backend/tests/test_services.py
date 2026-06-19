"""Basic service smoke tests — verify imports, config, and core functions work."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config, DEFAULTS
from services.templates import list_templates, get_template, PRESETS
from services.bgm_library import search_bgm, recommend_for_template, BGM_CATALOG
from services.workflow_manager import validate_workflow, sanitize_workflow


class TestConfig:
    def test_defaults_loaded(self):
        assert config["comfyui_url"] == "http://127.0.0.1:8188"
        assert "z_image_width" in config["generation"]

    def test_models_defined(self):
        models = config["models"]
        assert models["z_image"] == "z_image_turbo_bf16.safetensors"
        assert "sulphur_fp8" in models


class TestTemplates:
    def test_five_presets(self):
        assert len(PRESETS) == 5  # micro_drama, documentary, vlog, cinematic_trailer, slideshow

    def test_get_existing_template(self):
        t = get_template("micro_drama")
        assert t is not None
        assert t["name"] == "微短剧"
        assert "hook" in [s["segment"] for s in t["timing"]["structure"]]

    def test_all_templates_listable(self):
        tl = list_templates()
        assert len(tl) == 5
        ids = {t["id"] for t in tl}
        assert "micro_drama" in ids
        assert "documentary" in ids


class TestBGM:
    def test_catalog_not_empty(self):
        assert len(BGM_CATALOG) > 0

    def test_search_by_genre(self):
        results = search_bgm(genre="piano")
        assert len(results) >= 1
        assert all(b["genre"] == "piano" for b in results)

    def test_search_by_mood(self):
        results = search_bgm(mood="epic")
        assert len(results) >= 1
        moods = [m.lower() for b in results for m in b["mood"]]
        assert "epic" in moods

    def test_recommend_for_template(self):
        results = recommend_for_template("micro_drama")
        assert len(results) >= 1


class TestWorkflowManager:
    def test_validate_valid_workflow(self):
        wf = {
            "1": {"class_type": "KSampler", "inputs": {"seed": 1}},
            "2": {"class_type": "SaveImage", "inputs": {}},
        }
        valid, msg, info = validate_workflow(wf)
        assert valid
        assert info["node_count"] == 2

    def test_validate_empty(self):
        valid, msg, info = validate_workflow({})
        assert not valid

    def test_sanitize_removes_prompt_enhance(self):
        wf = {
            "1": {"class_type": "PromptEnhance", "inputs": {"text": "test"}},
            "2": {"class_type": "KSampler", "inputs": {}},
        }
        sanitized = sanitize_workflow(wf)
        assert sanitized["1"].get("_bypassed") is True
        assert sanitized["2"].get("_bypassed") is not True

    def test_sanitize_keeps_normal_nodes(self):
        wf = {
            "1": {"class_type": "KSampler", "inputs": {"seed": 42}},
        }
        sanitized = sanitize_workflow(wf)
        assert "_bypassed" not in sanitized["1"]


class TestMoodDetection:
    def test_mood_transition_map(self):
        """Verify AI transition recommendation maps mood keywords correctly."""
        from services.templates import merge_template_with_ai, get_template
        template = get_template("micro_drama")
        moods = ["紧张", "压抑", "热血"]
        recipe = merge_template_with_ai(template, moods, 60)
        assert "ai_selected_transition" in recipe
        # "紧张" maps to hard_cut, "压抑" to dip_to_black, "热血" to flash_white
        # Most frequent wins
        assert recipe["ai_selected_transition"] in ["hard_cut", "dip_to_black"]
