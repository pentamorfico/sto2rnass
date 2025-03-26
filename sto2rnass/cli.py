import sys

def parse_stockholm_project_sequence(sto_file, target_seq_id):
    sequences = {}
    ss_cons_lines = []

    with open(sto_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            if not line.startswith("#"):
                parts = line.split()
                if len(parts) >= 2:
                    seq_id, seq_data = parts[0], parts[1]
                    sequences[seq_id] = sequences.get(seq_id, "") + seq_data
            elif line.startswith("#=GC SS_cons"):
                parts = line.split()
                if len(parts) >= 3:
                    ss_cons_lines.append(parts[2])

    ss_cons = ''.join(ss_cons_lines)

    if target_seq_id not in sequences:
        print(f"Error: Sequence ID '{target_seq_id}' not found in the file.")
        sys.exit(1)

    aligned_seq = sequences[target_seq_id]
    ungapped_seq = ""
    projected_structure = ""

    for base, ss in zip(aligned_seq, ss_cons):
        if base != '-':
            ungapped_seq += base
            projected_structure += ss

    projected_structure = projected_structure.replace('<', '(').replace('>', ')')

    print(f">{target_seq_id}")
    print(ungapped_seq)
    print(projected_structure)

def main():
    if len(sys.argv) != 3:
        print("Usage: extract-rna-structure <file.sto> <sequence_id>")
        sys.exit(1)

    sto_file = sys.argv[1]
    sequence_id = sys.argv[2]
    parse_stockholm_project_sequence(sto_file, sequence_id)

