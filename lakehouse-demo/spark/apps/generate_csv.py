import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = Path("/data/input_wide.csv")
N_ROWS = 1000
N_COLS = 50  # можно увеличить

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["id"] + [f"col_{i:02d}" for i in range(1, N_COLS)]
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        start_date = datetime(2020, 1, 1)

        for i in range(1, N_ROWS + 1):
            row = {"id": i}
            for j in range(1, N_COLS):
                if j % 5 == 0:
                    # дата
                    row[f"col_{j:02d}"] = (start_date + timedelta(days=i + j)).strftime("%Y-%m-%d")
                elif j % 5 == 1:
                    # целое
                    row[f"col_{j:02d}"] = random.randint(0, 100000)
                elif j % 5 == 2:
                    # float
                    row[f"col_{j:02d}"] = round(random.random() * 1000, 3)
                elif j % 5 == 3:
                    # строка
                    row[f"col_{j:02d}"] = f"text_{i}_{j}"
                else:
                    # булево
                    row[f"col_{j:02d}"] = random.choice([0, 1])
            writer.writerow(row)

    print(f"Generated {N_ROWS} rows into {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
