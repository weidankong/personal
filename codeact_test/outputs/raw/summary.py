import os
import re
import glob


def summarize():
    raw_dir = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(raw_dir, "*.txt")))
    files = [f for f in files if os.path.basename(f) != "summary.txt"]

    lines = []
    lines.append("task_id\tpass\tfail\ttotal\tstep")

    for filepath in files:
        task_id = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, "r") as f:
            content = f.read()

        passed = re.findall(r"Num Passed Tests\s*:\s*\x1b\[[\d;]*m(\d+)", content)
        failed = re.findall(r"Num Failed Tests\s*:\s*\x1b\[[\d;]*m(\d+)", content)
        total = re.findall(r"Num Total\s+Tests\s*:\s*\x1b\[[\d;]*m(\d+)", content)
        steps = re.findall(r"--- Step (\d+) ---", content)

        p = passed[-1] if passed else "0"
        f_ = failed[-1] if failed else "0"
        t = total[-1] if total else "0"
        s = str(max(int(x) for x in steps)) if steps else "0"

        lines.append(f"{task_id}\t{p}\t{f_}\t{t}\t{s}")

    output = "\n".join(lines) + "\n"
    print(output, end="")
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.txt")
    with open(out_path, "w") as f:
        f.write(output)


if __name__ == "__main__":
    summarize()
