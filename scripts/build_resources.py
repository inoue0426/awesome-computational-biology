#!/usr/bin/env python3
"""Build enriched resource artifacts.

This stable entrypoint delegates to the schema-v2 builder so existing workflows
continue to call scripts/build_resources.py while preserving enrichment metadata.
"""

from build_resources_v2 import main


if __name__ == "__main__":
    main()
