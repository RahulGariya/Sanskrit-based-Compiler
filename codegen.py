def generate_target(tac):
    target = []

    for line in tac:
        parts = line.split()

        if "=" in line:
            target.append(f"LOAD {parts[2]}")
            target.append(f"STORE {parts[0]}")

        elif parts[0] == "PRINT":
            target.append(f"PRINT {parts[1]}")

    return target
