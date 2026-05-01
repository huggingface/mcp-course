"""
This script automates the process of updating the titles in the `_toctree.yml` file for a specific locale.
It reads each `.mdx` file referenced in the table of contents, extracts the main H1 title,
and updates the `title` field in the `_toctree.yml` accordingly.

This helps to keep the navigation titles consistent with the content of the documentation pages.

Usage:
    python scripts/update_toc.py <locale>

Example:
    python scripts/update_toc.py zh-CN
"""
import argparse
from pathlib import Path
from ruamel.yaml import YAML

def get_mdx_title(mdx_path: Path) -> str | None:
    """Reads and extracts the H1 title from an mdx file."""
    if not mdx_path.exists():
        print(f"Warning: File not found: {mdx_path}")
        return None
    try:
        with open(mdx_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    # Strip the '# ' prefix, and any surrounding quotes and whitespace
                    return line.lstrip('# ').strip().strip("'\"")
    except Exception as e:
        print(f"Error reading file {mdx_path}: {e}")
        return None
    print(f"Warning: H1 title not found in {mdx_path}")
    return None

def update_toc_for_locale(locale: str, project_root: Path):
    """Updates the _toctree.yml file for a given locale."""
    print(f"Starting update for locale: {locale}")
    toc_path = project_root / 'units' / locale / '_toctree.yml'
    units_dir = project_root / 'units' / locale

    if not toc_path.exists():
        print(f"Error: TOC file not found at {toc_path}")
        return

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)  # Maintain consistent formatting

    try:
        with open(toc_path, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
    except Exception as e:
        print(f"Error parsing YAML file {toc_path}: {e}")
        return

    updated_count = 0
    if isinstance(data, list):
        for part in data:
            if 'sections' in part and isinstance(part['sections'], list):
                for section in part['sections']:
                    if 'local' in section and isinstance(section['local'], str):
                        local_path = section['local']
                        mdx_file_path = units_dir / f"{local_path}.mdx"
                        
                        new_title = get_mdx_title(mdx_file_path)
                        
                        if new_title:
                            if 'title' not in section or section['title'] != new_title:
                                print(f"  - Updating '{local_path}':")
                                print(f"    Old title: {section.get('title', 'N/A')}")
                                print(f"    New title: {new_title}")
                                section['title'] = new_title
                                updated_count += 1

    if updated_count > 0:
        try:
            with open(toc_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f)
            print(f"\n[✔︎] Successfully updated {updated_count} titles in {toc_path}")
        except Exception as e:
            print(f"Error writing YAML file {toc_path}: {e}")
    else:
        print("\n[✔︎] All titles are already up-to-date.")


def main():
    """Parses command-line arguments and starts the TOC update process."""
    parser = argparse.ArgumentParser(
        description="Updates titles in a locale's _toctree.yml based on the H1 titles of the corresponding mdx files."
    )
    parser.add_argument(
        "locale", 
        type=str, 
        help="The locale to update (e.g., 'zh-CN', 'vi')"
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    update_toc_for_locale(args.locale, project_root)

if __name__ == "__main__":
    main()
