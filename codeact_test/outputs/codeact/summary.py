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
        basename = os.path.splitext(os.path.basename(filepath))[0]
        # Strip _success suffix if present to get the task_id
        task_id = basename.removesuffix("_success")
        with open(filepath, "r") as f:
            content = f.read()

        passed = re.findall(r"Num Passed Tests\s*:\s*\x1b\[[\d;]*m(\d+)", content)
        failed = re.findall(r"Num Failed Tests\s*:\s*\x1b\[[\d;]*m(\d+)", content)
        total = re.findall(r"Num Total\s+Tests\s*:\s*\x1b\[[\d;]*m(\d+)", content)

        p = passed[-1] if passed else "0"
        f_ = failed[-1] if failed else "0"
        t = total[-1] if total else "0"

        # STEP: 1 may appear 1~3 times (rounds). Sum the max step of each round.
        all_steps = re.findall(r"============= STEP: (\d+) ===========", content)
        if all_steps:
            step_nums = [int(x) for x in all_steps]
            # Split into rounds: each round starts at step 1
            rounds = []
            current_round = []
            for s in step_nums:
                if s == 1 and current_round:
                    rounds.append(current_round)
                    current_round = [s]
                else:
                    current_round.append(s)
            if current_round:
                rounds.append(current_round)
            total_steps = sum(max(r) for r in rounds)
            s = str(total_steps)
        else:
            s = "0"

        lines.append(f"{task_id}\t{p}\t{f_}\t{t}\t{s}")

    output = "\n".join(lines) + "\n"
    print(output, end="")
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "summary.txt")
    with open(out_path, "w") as f:
        f.write(output)


if __name__ == "__main__":
    summarize()
