"""Materialize the current parts_source selections with the shared OOMP library."""
from pathlib import Path

import oomp
import yaml


def main(**kwargs):
    source = Path(kwargs.get("source_dir", "parts_source"))
    part_ids = kwargs.get("part_ids")
    if part_ids is None:
        part_ids = sorted(path.parent.name for path in source.glob("*/working.yaml"))
    parts = []
    for part_id in part_ids:
        path = source / part_id / "working.yaml"
        parts.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    oomp.add_parts(parts, wait_for_completion=True)
    # The shared OOMP materializer supplies old central-catalog URLs for every
    # record. These parts are published in this project, under their local IDs.
    for part_id in part_ids:
        dest = Path("parts") / part_id / "working.yaml"
        record = yaml.safe_load(dest.read_text(encoding="utf-8"))
        for key in ("link_github", "link_main", "link_redirect"):
            if "oomlout_oomp_version_1_messy" in record.get(key, ""):
                del record[key]
        record["source_device_url"] = ("https://github.com/oomlout/oomp_electronic_panel_mount_version_5"
                                       f"/tree/main/parts/{record['source_oomp_id']}")
        dest.write_text(yaml.safe_dump(record, allow_unicode=True), encoding="utf-8")


if __name__ == "__main__":
    main()
