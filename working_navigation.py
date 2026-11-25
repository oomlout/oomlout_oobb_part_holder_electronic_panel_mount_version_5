"""Publish directory-based discovery, illustrated instructions and printable leaf STLs."""
import filecmp
import os
from pathlib import Path
import re
import shutil
from urllib.parse import quote

import yaml

from working_oomp_populate import ELECTRONICS_CATALOG, PROJECT_DESCRIPTION, PROJECT_TITLE, REAR_PLATES
from working_presentation import CATALOG, NAMES, NOTICE

ORIGIN = ("This is an entirely AI-generated coding project. The source code is largely unreadable by humans. "
          "The generated files are included so others can use and modify the designs with their own AI tools.")
DESCRIPTIONS = dict(panel="A panel with OOBB mounting holes around all four edges.",
                    panel_width_only="A panel with one mounting row on each side of the device.",
                    box_width_only="An open-backed box with three interchangeable rear plates.",
                    cutout_only="A positive CAD tool for cutting a clip-in pocket into a solid block.")


def relative(target, page):
    path = os.path.relpath(target, page.parent).replace(os.sep, "/")
    return quote(path, safe="/.") + ("/" if target.is_dir() else "")


def write_page(page, lines):
    start, end = "<!-- oobb-presentation:start -->", "<!-- oobb-presentation:end -->"
    old = page.read_text(encoding="utf-8") if page.exists() else ""
    text = start + "\n" + "\n".join(lines).strip() + "\n" + end
    if start in old or end in old:
        if old.count(start) != 1 or old.count(end) != 1 or old.index(end) < old.index(start):
            raise ValueError(f"Unpaired generated README markers in {page}")
        text = old.split(start)[0] + text + old.split(end)[1]
    else:
        text += "\n" + old
    page.write_text(text.rstrip() + "\n", encoding="utf-8")


def assembly_lines(record, folder, page, **kwargs):
    illustrated = kwargs.get("illustrated", True)
    assembly = folder / "assembly"
    cutter = record["taxonomy_5"] == "cutout_only"
    lines = []
    for number, step in enumerate(record["assembly_steps"], 1):
        lines.extend([f"{number}. {step['action']}", ""])
        if illustrated and not cutter:
            img = relative(assembly / "cards" / f"step_{number:02d}.png", page)
            lines.extend([f'   <a href="{img}"><img src="{img}" width="310" alt="Installation step {number}"></a>', ""])
    if not cutter:
        lines.extend(["The gray shape represents the catalog device envelope. Clip travel and physical fit still need a sample print.", "",
                      f"[Offline HTML viewer]({relative(assembly / 'assembly_instructions.html', page)}) · "
                      f"[Printable PDF]({relative(assembly / 'assembly_instructions.pdf', page)})"])
    return lines


def part_lines(record, folder, leaf, page):
    d = record["oobb_details"]
    variant = d["variant"]
    name = record["device_label"].replace("_", "-").upper()
    title = f"{name} · {NAMES[variant]}"
    source = f"{CATALOG}/tree/main/parts/{record['source_oomp_id']}"
    image = relative(folder / "3dpr_presentation.png", page)
    part_url = relative(folder, page)
    lines = [f"# {title}", "", NOTICE, "", "## Summary", "", DESCRIPTIONS[variant], "", ORIGIN, "",
             f"[![{title} in two CAD views]({image})]({part_url})", "", "## Details", "",
             f"**Full OOMP ID** `{record['id']}`", "",
             f"[Part folder]({part_url}) · [OOBB navigation]({relative(leaf, page)}) · [Source device]({source})", "",
             "| Dimension | Value |", "| --- | --- |",
             f"| OOBB width × height | {d['width']} × {d['height']} grid units |",
             f"| Depth | {d['depth']:g} mm |",
             f"| Front opening | {d['width_cutout_mm']:g} × {d['height_cutout_mm']:g} mm |",
             f"| Clip shoulder | {d['depth_cutout_mm']:g} mm |", ""]
    if variant == "cutout_only":
        lines.extend([f"The grid dimensions describe its bounding envelope. The cutter measures "
                      f"{d['cavity_width_mm']:g} × {d['cavity_height_mm']:g} × {d['depth']:g} mm.", ""])
    if variant == "box_width_only":
        lines.extend([f"The assembled depth includes a {d['body_depth_mm']:g} mm open body and a "
                      f"{d['back_plate_depth_mm']:g} mm rear plate. The [print layout]({relative(folder/'3dpr.stl',page)}) "
                      f"contains the body and bottom-opening plate side by side. Use the "
                      f"[body-only STL]({relative(folder/'body_3dpr.stl',page)}) with either alternate plate.", "",
                      "The flat faces mate together, with a 1.5 mm edge radius on the front of the box and the outside of the rear plate. "
                      "The two rear screws occupy one M3 through-bore on each side when fitted.", "",
                      "### Rear plate options", "",
                      "| Plate | Opening | Optional M3 nuts | Files |",
                      "| --- | --- | --- | --- |"])
        for prefix, plate in REAR_PLATES.items():
            openings = []
            nuts = 0
            if plate["bottom"]:
                openings.append(f"{d['wire_width_mm']:g} × {d['wire_height_mm']:g} mm bottom wire exit")
                nuts += 4
            if plate["electronics"]:
                window = d["electronics_window_mm"]
                openings.append(f"{window:g} × {window:g} mm electronics window at the top right, viewed from the rear")
                nuts += 2
            stl = relative(folder / f"{prefix}3dpr.stl", page)
            preview = relative(folder / f"{prefix}3dpr_presentation.png", page)
            lines.append(f"| {plate['label']} | {' and '.join(openings)} | {nuts} | [Print STL]({stl}) · [Both faces]({preview}) |")
        lines.extend(["", "Drop accessory nuts into the hex pockets from the rear. Fit the accessory and start its screws from the inside before installing the rear plate. "
                      "The two nuts that secure the rear plate slide into the box rails from the sides.", "",
                      "The electronics window and its two M3 mounting points use the lower pair of side pins from the "
                      f"3 × 3 little spacer. [OOBB Electronics source]({ELECTRONICS_CATALOG}/blob/main/working_scad.py)", "",
                      f"![Both faces of the dual-opening plate]({relative(folder/'back_plate_both_3dpr_presentation.png',page)})", ""])
    metadata = yaml.safe_dump(record, allow_unicode=True, sort_keys=False).rstrip()
    fence = "`" * max([3] + [len(t) + 1 for t in re.findall(r"`+", metadata)])
    inventory = ("Use the nominal cutter mesh for a CAD subtraction." if variant == "cutout_only" else
                 f"One printed holder and one [{name} panel-mount device]({source}). Choose chassis screws to suit the receiving structure.")
    if variant == "box_width_only":
        inventory = (f"One printed body, one rear plate, one [{name}]({source}), two M3 × 12 mm countersunk screws "
                     "and two M3 hex nuts. Add four M3 nuts for a bottom patch panel or two for an OOBB Electronics plate. "
                     "Use six if fitting both accessories.")
    lines.extend(["<details>", "<summary>Complete OOMP metadata</summary>", "", fence + "yaml", metadata,
                  fence, "", "</details>", "", "## Parts", "", inventory, "", "## Assembly", ""])
    lines.extend(assembly_lines(record, folder, page))
    return lines


def catalog_rows(records, page):
    devices = {}
    for folder, record in records:
        source_id = record["source_oomp_id"]
        devices.setdefault(source_id, {})[record["taxonomy_5"]] = (folder, record)

    headers = ["OOMP item", *NAMES.values()]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for source_id, variants in sorted(devices.items()):
        _, device = next(iter(variants.values()))
        label = device["device_label"].replace("_", "-").upper()
        cells = [f"[{label}]({CATALOG}/tree/main/parts/{source_id})"]
        for variant in NAMES:
            if variant not in variants:
                cells.append("—")
                continue
            folder, record = variants[variant]
            details = record["oobb_details"]
            size = f"{details['width']} × {details['height']} × {details['depth']:g} mm"
            mesh = "true.stl" if variant == "cutout_only" else "3dpr.stl"
            cells.append(f"[{size}]({relative(folder, page)}) · [STL]({relative(folder / mesh, page)})")
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def main(**kwargs):
    root = Path(kwargs.get("root", ".")).resolve()
    part_ids = kwargs.get("part_ids")
    parts = root / "parts"
    if part_ids is None:
        part_ids = sorted(path.parent.name for path in parts.glob("*/working.yaml"))
    nav = root / "navigation_oobb"
    children = {}
    leaves = {}
    records = []
    for part_id in part_ids:
        folder = parts / part_id
        record = yaml.safe_load((folder / "working.yaml").read_text(encoding="utf-8"))
        records.append((folder, record))
        branch = nav
        for level in range(1, 16):
            segment = record.get(f"taxonomy_{level}")
            if not segment:
                continue
            if not re.fullmatch(r"[\w-]+", segment):
                raise ValueError(f"Invalid taxonomy directory {segment!r}")
            child = branch / segment
            children.setdefault(branch, set()).add(child)
            branch = child
        branch.mkdir(parents=True, exist_ok=True)
        leaves[branch] = folder
        (branch / "oomp_id.txt").write_text(part_id + "\n", encoding="utf-8")
        source = folder / ("true.stl" if record["taxonomy_5"] == "cutout_only" else "3dpr.stl")
        shutil.copyfile(source, branch / source.name)
        if record["taxonomy_5"] == "box_width_only":
            for prefix in ("body_", *REAR_PLATES):
                name = f"{prefix}3dpr.stl"
                shutil.copyfile(folder / name, branch / name)
        if not filecmp.cmp(source, branch / source.name, shallow=False):
            raise IOError(f"Navigation mesh differs from {source}")
        for page in (folder / "README.md", branch / "README.md"):
            write_page(page, part_lines(record, folder, branch, page))
    for branch, options in children.items():
        page = branch / "README.md"
        lines = [f"# {branch.name.replace('_', ' ')}", "", "[Up one level](../)", ""]
        for child in sorted(options, key=lambda p: [int(v) if v.isdigit() else v for v in re.split(r"(\d+)", p.name)]):
            lines.append(f"- [{child.name.replace('_', ' ')}]({relative(leaves.get(child, child), page)})")
        write_page(page, lines)
    discovery = nav
    while len(children.get(discovery, ())) == 1:
        discovery = next(iter(children[discovery]))
    page = root / "README.md"
    folder, record = next(pair for pair in records if pair[1]["taxonomy_5"] == "panel")
    name = record["device_label"].replace("_", "-").upper() + " four-sided panel"
    part_url = relative(folder, page)
    lines = [f"# {PROJECT_TITLE}", "", NOTICE, "", "## Summary", "", PROJECT_DESCRIPTION, "",
             f"Device dimensions come from the [OOMP panel-mount catalog]({CATALOG}) maintained by [Oom Lout](https://github.com/oomlout).",
             "", ORIGIN, "", f"[![{name}]({relative(folder / '3dpr_presentation.png', page)})]({part_url})", "",
             f"[{name}]({part_url})", "", "## Details", "",
             f"[Browse the {len(records)} entries by taxonomy]({relative(leaves.get(discovery, discovery), page)}). "
             "After the style, width and height count 15 mm OOBB grid units. Depth is in millimetres. "
             "The cutter uses the smallest OOBB envelope that contains its pocket.", "",
             "Run `python make_all.py` to rebuild the catalog, CAD, illustrations and instructions. [Build guide](BUILD.md)",
             "", "## Parts", "",
             "Choose a panel for an existing enclosure or an open-backed box with a removable cable plate. The width-only styles leave the top "
             "and bottom edges free of front mounting rows. Choose the positive cutter to design your own enclosure.", "",
             "Sizes are shown as grid width × grid height × depth in millimetres.", ""]
    lines.extend(catalog_rows(records, page))
    lines.extend(["", "## Assembly", "", "### Four-sided panel", ""])
    lines.extend(assembly_lines(record, folder, page))
    box = next((pair for pair in records if pair[1]["taxonomy_5"] == "box_width_only"
                and pair[1]["source_oomp_id"] == record["source_oomp_id"]), None)
    if box:
        box_folder, box_record = box
        plate_options = relative(box_folder, page) + "#rear-plate-options"
        lines.extend(["", "### Side-mount box with rear plate", "",
                      f"Choose a bottom wire opening, a top-right electronics window, or both. [Rear plate options and print files]({plate_options})", ""])
        lines.extend(assembly_lines(box_record, box_folder, page))
    write_page(page, lines)


if __name__ == "__main__":
    main()
