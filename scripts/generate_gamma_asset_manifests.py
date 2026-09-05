import argparse
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OWNER = "jd-SearchEngines"
REPO = "image-repair-agent-lab"
BRANCH = "main"

SPECS = {
    "ep01": {
        "source": "/Users/jingdong/Downloads/EP01SkillAI.zip",
        "files": [
            ("1_AI.png", "封面 / 总问题 / AI 局部修复主题"),
            ("2_.png", "错误文字、问题定位或 Before 视觉证据"),
            ("3_.png", "修复结果 / After / 局部结果"),
            ("4_Prompt-Skill.png", "Prompt → Skill / Skill 规则 / Codex 工程价值"),
            ("5_.png", "真实运行记录 / 工程执行证据"),
            ("6_.png", "结论 / Before-After / 最终可用性证据"),
        ],
    },
    "ep02": {
        "source": "/Users/jingdong/Downloads/EP02Agent.pptx; exported with native Keynote to PDF, then rendered at 220 DPI",
        "files": [
            ("1_verify_hook.png", "Agent Done 与外部验证失败的矛盾"),
            ("2_pytest_fail.png", "第一次 Patch / pytest FAIL / verifier failure"),
            ("3_replan_flow.png", "FAIL → Replan → PASS 流程"),
            ("4_pytest_pass.png", "第二次 Patch / pytest PASS / false_finish=false"),
            ("5_five_cases.png", "5 Cases / 5 Recovery / 5/5 Final Pass"),
            ("6_verifier_conclusion.png", "Verifier 结论：FAIL 必须阻断 Done"),
        ],
    },
    "ep03": {
        "source": "/Users/jingdong/Downloads/EP03Demo.zip",
        "files": [
            ("1_Demo.png", "单次 Demo 证据"),
            ("2_Demo.png", "Demo 过程 / 结果证据"),
            ("3_5-Cases-5.png", "5 Cases 可重复实验"),
            ("4_False-Finish5-0.png", "false_finish 5 → 0 对比"),
            ("5_Case.png", "固定 Case 对比"),
            ("6_.png", "Benchmark / regression 证据"),
        ],
    },
    "ep04": {
        "source": "/Users/jingdong/Downloads/EP04Pipeline.zip",
        "files": [
            ("1_Pipeline.png", "Pipeline 总览"),
            ("2_Compose.png", "Compose 阶段证据"),
            ("3_Assets.png", "Assets 阶段证据"),
            ("4_Compose-Assets.png", "Compose 与 Assets 对比"),
            ("5_.png", "Fail Fast / Fail Local 证据"),
            ("6_Workflow.png", "Pipeline Workflow"),
        ],
    },
    "ep05": {
        "source": "/Users/jingdong/Downloads/EP05.zip",
        "files": [
            ("1_.png", "失败证据"),
            ("2_Skill-Push.png", "Skill 更新与 Push"),
            ("3_.png", "规则缺口定位"),
            ("4_.png", "Regression 验证"),
            ("5_Skill.png", "Skill 沉淀"),
            ("6_Loop-Engineering.png", "Loop Engineering 闭环"),
        ],
    },
}


def urls(ep, filename):
    path = f"gamma-assets/{ep}/{filename}"
    return (
        f"https://github.com/{OWNER}/{REPO}/blob/{BRANCH}/{path}",
        f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{path}",
    )


def verify(raw_url):
    request = Request(raw_url, headers={"User-Agent": "image-repair-agent-lab-asset-verifier/1.0"})
    try:
        with urlopen(request, timeout=30) as response:
            content_type = response.headers.get_content_type()
            response.read(32)
            status = response.status
            return {"http_status": status, "content_type": content_type, "verified": status == 200 and content_type.startswith("image/")}
    except Exception as exc:
        return {"http_status": None, "content_type": None, "verified": False, "error": f"{type(exc).__name__}: {exc}"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verification = {}
    total = []
    for ep, spec in SPECS.items():
        rows = []
        for filename, purpose in spec["files"]:
            path = ROOT / "gamma-assets" / ep / filename
            if not path.exists() or path.stat().st_size <= 0:
                raise FileNotFoundError(path)
            with Image.open(path) as image:
                width, height = image.size
                image.verify()
            blob_url, raw_url = urls(ep, filename)
            result = verify(raw_url) if args.verify else {"http_status": "PENDING", "content_type": "PENDING", "verified": False}
            verification[raw_url] = result
            row = {
                "episode": ep.upper(), "file": filename, "purpose": purpose, "source_file": spec["source"],
                "github_blob_url": blob_url, "raw_url": raw_url, "http_status": result["http_status"],
                "content_type": result["content_type"], "width": width, "height": height, "verified": result["verified"],
            }
            rows.append(row)
            total.append(row)
        lines = [f"# {ep.upper()} Gamma Asset Manifest", "", f"- Episode: `{ep.upper()}`", f"- Source: `{spec['source']}`", "", "| File | Purpose | Source file | GitHub Blob URL | Raw URL | HTTP Status | Content-Type | Width | Height | Verified |", "|---|---|---|---|---|---:|---|---:|---:|---|"]
        for row in rows:
            lines.append(f"| `{row['file']}` | {row['purpose']} | `{row['source_file']}` | [{row['file']}]({row['github_blob_url']}) | [{row['file']} raw]({row['raw_url']}) | `{row['http_status']}` | `{row['content_type']}` | {row['width']} | {row['height']} | `{('YES' if row['verified'] else 'NO')}` |")
        (ROOT / "gamma-assets" / ep / "asset_manifest.md").write_text("\n".join(lines) + "\n")
    all_lines = ["# Gamma Asset Manifest - EP01 to EP05", "", "All files are real experiment assets. Raw URLs are intended for Gamma image insertion.", ""]
    for ep in SPECS:
        all_lines.extend([f"## {ep.upper()}", "", "| File | Purpose | Raw URL | HTTP Status | Content-Type | Width | Height | Verified |", "|---|---|---|---:|---|---:|---:|---|"])
        for row in [x for x in total if x["episode"].lower() == ep]:
            all_lines.append(f"| `{row['file']}` | {row['purpose']} | [{row['file']} raw]({row['raw_url']}) | `{row['http_status']}` | `{row['content_type']}` | {row['width']} | {row['height']} | `{('YES' if row['verified'] else 'NO')}` |")
        all_lines.append("")
    (ROOT / "gamma-assets" / "asset_manifest_all.md").write_text("\n".join(all_lines))
    (ROOT / "gamma-assets" / "verification.json").write_text(json.dumps({"asset_count": len(total), "verification": verification}, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"asset_count": len(total), "verified_count": sum(1 for x in total if x["verified"]), "verify": args.verify}, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
