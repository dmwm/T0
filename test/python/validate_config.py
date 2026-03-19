#!/usr/bin/env python
from __future__ import print_function

import re
import sys


def extract_dataset_names(source):
    results = []
    lines = source.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        match = re.match(r'^DATASETS\s*=\s*\[', line)
        if match:
            bracket_line = line
            while bracket_line.count('[') > bracket_line.count(']'):
                i += 1
                if i < len(lines):
                    bracket_line += '\n' + lines[i]

            dataset_names = re.findall(r'"([^"]+)"', bracket_line)

            peek = i + 1
            while peek < len(lines):
                peek_line = lines[peek].strip()
                if not peek_line or peek_line.startswith('#') or peek_line.startswith('PARKING_PDS'):
                    peek += 1
                    continue
                extend_match = re.match(r'^DATASETS\s*\+=\s*\[', lines[peek])
                if extend_match:
                    bracket_line = lines[peek]
                    while bracket_line.count('[') > bracket_line.count(']'):
                        peek += 1
                        if peek < len(lines):
                            bracket_line += '\n' + lines[peek]
                    dataset_names.extend(re.findall(r'"([^"]+)"', bracket_line))
                    i = peek
                    peek += 1
                else:
                    break

            results.extend(dataset_names)

        direct_match = re.match(r'^addDataset\(tier0Config,\s*"([^"]+)"', line)
        if direct_match:
            results.append(direct_match.group(1))

        i += 1

    return results


def group_by_family(dataset_names):
    families = {}
    has_zero_padded = set()
    for name in dataset_names:
        if name == "Default":
            continue

        match = re.match(r'^(.+?)(\d+)$', name)
        if match:
            base = match.group(1)
            num_str = match.group(2)
            if len(base) < 2:
                continue
            if len(num_str) > 1 and num_str[0] == '0':
                has_zero_padded.add(base)
                continue
            index = int(num_str)
            if base not in families:
                families[base] = {}
            families[base][index] = name

    return {k: v for k, v in families.items()
            if len(v) >= 2 and k not in has_zero_padded}


def check_gaps(families):
    issues = []
    for family, members in sorted(families.items()):
        indices = sorted(members.keys())
        min_idx = indices[0]
        max_idx = indices[-1]

        if min_idx != 0:
            issues.append((
                "WARNING",
                family,
                "Family starts at index %d instead of 0 (members: %s)"
                % (min_idx, ", ".join(str(i) for i in indices))
            ))

        expected = set(range(min_idx, max_idx + 1))
        actual = set(indices)
        missing = sorted(expected - actual)
        if missing:
            issues.append((
                "ERROR",
                family,
                "Gap detected: missing index %s (found: %s)"
                % (", ".join(str(i) for i in missing),
                   ", ".join(str(i) for i in indices))
            ))

    return issues


CHECKS = [
    check_gaps,
]


def validate_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    names = extract_dataset_names(source)
    families = group_by_family(names)

    all_issues = []
    for check in CHECKS:
        all_issues.extend(check(families))

    errors = [(fam, msg) for level, fam, msg in all_issues if level == "ERROR"]
    warnings = [(fam, msg) for level, fam, msg in all_issues if level == "WARNING"]

    return families, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: %s <config_file> [<config_file> ...]" % sys.argv[0])
        sys.exit(2)

    total_errors = 0
    total_warnings = 0
    total_families = 0

    for filepath in sys.argv[1:]:
        print("=" * 60)
        print("Validating: %s" % filepath)
        print("=" * 60)

        try:
            families, errors, warnings = validate_file(filepath)
        except Exception as e:
            print("  FATAL: Could not parse file: %s" % e)
            total_errors += 1
            continue

        total_families += len(families)

        if not errors and not warnings:
            print("  OK: %d dataset families checked, all passed" % len(families))
        else:
            for family, msg in errors:
                print("  ERROR [%s]: %s" % (family, msg))
                total_errors += 1

            for family, msg in warnings:
                print("  WARNING [%s]: %s" % (family, msg))
                total_warnings += 1

        print()

    print("=" * 60)
    print("SUMMARY: %d families checked, %d errors, %d warnings"
          % (total_families, total_errors, total_warnings))
    print("=" * 60)

    if total_errors > 0:
        print("FAILED")
        sys.exit(1)
    else:
        if total_warnings > 0:
            print("PASSED (with warnings)")
        else:
            print("PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
