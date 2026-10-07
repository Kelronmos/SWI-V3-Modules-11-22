"""SWI CLI entry — platform inspection only; no authorization."""
from __future__ import annotations

import json

from swi_v3.platform.capabilities import detect_platform


def main() -> int:
    info = detect_platform()
    print(
        json.dumps(
            {
                "architecture": info.architecture,
                "capabilities": sorted(info.capabilities),
                "platform": info.name,
                "version": info.version,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
