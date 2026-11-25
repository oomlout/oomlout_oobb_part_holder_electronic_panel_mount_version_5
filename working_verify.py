"""Check the local links, navigation copies and manuals before upload."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

import fitz
import yaml


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_readme(page):
    body = page.read_text(encoding="utf-8")
    # Only prose contributes links. An embedded YAML record can contain arbitrary text.
    body = re.sub(r"^(`{3,})yaml\n.*?^\1$", "", body, flags=re.MULTILINE | re.DOTALL)
    urls = re.findall(r"\]\(([^)]+)\)", body) + re.findall(r'(?:src|href)="([^"]+)"', body)
    for url in urls:
        target = urlsplit(url)
        if target.scheme or not target.path:
            continue
        path = page.parent / unquote(target.path)
        if not path.exists():
            raise FileNotFoundError(f"Broken link in {page}: {url}")
        if target.fragment == "assembly":
            destination = path / "README.md" if path.is_dir() else path
            if "## Assembly" not in destination.read_text(encoding="utf-8"):
                raise ValueError(f"Missing Assembly heading at {destination}")


def main(**kwargs):
    root = Path(kwargs.get("root", ".")).resolve()
    nav = root / "navigation_oobb"
    leaves = {}
    for marker in nav.rglob("oomp_id.txt"):
        part_id = marker.read_text(encoding="utf-8").strip()
        if part_id in leaves:
            raise ValueError(f"Repeated navigation leaf for {part_id}")
        leaves[part_id] = marker.parent
    source_ids = {p.parent.name for p in (root / "parts_source").glob("*/working.yaml")}
    records = sorted((root / "parts").glob("*/working.yaml"))
    if source_ids != set(leaves) or source_ids != {p.parent.name for p in records}:
        raise ValueError("Source, canonical and navigation ID sets differ")
    for path in records:
        record = yaml.safe_load(path.read_text(encoding="utf-8"))
        folder = path.parent
        taxonomy_id = "_".join(record[f"taxonomy_{i}"] for i in range(1, 16) if record.get(f"taxonomy_{i}"))
        if taxonomy_id != record["id"] or taxonomy_id != folder.name:
            raise ValueError(f"Taxonomy and folder disagree at {folder}")
        for mode in ("true", "3dpr"):
            for name in (f"{mode}.scad", f"{mode}.stl", f"{mode}_presentation.png"):
                if (folder / name).stat().st_size == 0:
                    raise ValueError(f"Empty production file: {folder / name}")
        cutter = record["taxonomy_5"] == "cutout_only"
        mesh = "true.stl" if cutter else "3dpr.stl"
        if sha256(folder / mesh) != sha256(leaves[taxonomy_id] / mesh):
            raise ValueError(f"Stale leaf mesh: {taxonomy_id}")
        if record["taxonomy_5"] == "box_width_only":
            for mode in ("true", "3dpr"):
                for extension in ("scad", "stl"):
                    for piece in ("body", "back_plate"):
                        if not (folder / f"{piece}_{mode}.{extension}").stat().st_size:
                            raise ValueError(f"Empty {piece} CAD")
            for name in ("body_3dpr.stl", "back_plate_3dpr.stl"):
                if sha256(folder / name) != sha256(leaves[taxonomy_id] / name):
                    raise ValueError(f"Stale navigation mesh {name}")
        if not cutter:
            assembly = folder / "assembly"
            manifest = json.loads((assembly / "assembly_manifest.json").read_text(encoding="utf-8"))
            if manifest["production_stl_sha256"] != sha256(folder / "3dpr.stl"):
                raise ValueError(f"Stale illustrated geometry: {taxonomy_id}")
            if record["taxonomy_5"] == "box_width_only":
                if manifest["body_stl_sha256"] != sha256(folder / "body_3dpr.stl"):
                    raise ValueError("Stale body in box booklet")
                if manifest["back_plate_stl_sha256"] != sha256(folder / "back_plate_3dpr.stl"):
                    raise ValueError("Stale rear plate in box booklet")
            report = json.loads((assembly / "validation.json").read_text(encoding="utf-8"))
            for ext in ("pdf", "html"):
                if sha256(assembly / f"assembly_instructions.{ext}") != report[f"{ext}_sha256"]:
                    raise ValueError(f"Stale assembly {ext}: {taxonomy_id}")
            with fitz.open(assembly / "assembly_instructions.pdf") as book:
                links = [link.get("uri") for page in book for link in page.get_links()]
                if record["source_device_url"] not in links:
                    raise ValueError(f"Missing device catalog link in {assembly}")
                if manifest["book"]["project_url"] not in [item.get("uri") for item in book[0].get_links()]:
                    raise ValueError(f"Missing project link on the cover of {assembly}")
        check_readme(folder / "README.md")
    for page in nav.rglob("README.md"):
        check_readme(page)
    check_readme(root / "README.md")
    check_readme(root / "BUILD.md")
    print(f"Verified {len(records)} catalog entries, navigation meshes, README links and installation books.")


if __name__ == "__main__":
    main()
