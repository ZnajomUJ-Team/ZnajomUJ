from pathlib import Path
import pandas as pd

def write_results_to_excel(output_path: str | Path, rows_by_sheet: dict[str, list]) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, rows in rows_by_sheet.items():
            df = pd.DataFrame(rows)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        