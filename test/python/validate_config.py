#!/usr/bin/env python
from __future__ import print_function

import re
import sys


def extract_datasets_and_blocks(source):
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

            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith('for dataset in DATASETS'):
                if re.match(r'^DATASETS\s*=\s*\[', lines[j]) or re.match(r'^##+', lines[j]):
                    break
                j += 1

            if j < len(lines) and lines[j].strip().startswith('for dataset in DATASETS'):
                k = j + 1
                while k < len(lines) and not lines[k].strip().startswith('addDataset('):
                    k += 1

                if k < len(lines):
                    call_text = lines[k]
                    paren_depth = 0
                    for ch in call_text:
                        if ch == '(':
                            paren_depth += 1
                        elif ch == ')':
                            paren_depth -= 1
                    while paren_depth > 0 and k + 1 < len(lines):
                        k += 1
                        call_text += '\n' + lines[k]
                        for ch in lines[k]:
                            if ch == '(':
                                paren_depth += 1
                            elif ch == ')':
                                paren_depth -= 1

                    kwargs = parse_addDataset_kwargs(call_text)
                    for name in dataset_names:
                        results.append((name, kwargs))

        direct_match = re.match(r'^addDataset\(tier0Config,\s*"([^"]+)"', line)
        if direct_match:
            name = direct_match.group(1)
            call_text = line
            paren_depth = 0
            for ch in call_text:
                if ch == '(':
                    paren_depth += 1
                elif ch == ')':
                    paren_depth -= 1
            while paren_depth > 0 and i + 1 < len(lines):
                i += 1
                call_text += '\n' + lines[i]
                for ch in lines[i]:
                    if ch == '(':
                        paren_depth += 1
                    elif ch == ')':
                        paren_depth -= 1

            kwargs = parse_addDataset_kwargs(call_text)
            results.append((name, kwargs))

        i += 1

    return results


def parse_addDataset_kwargs(call_text):
    kwargs = {}
    for match in re.finditer(r'(\w+)\s*=\s*', call_text):
        param = match.group(1)
        start = match.end()
        value = extract_value(call_text, start)
        if value is not None:
            kwargs[param] = value.strip()
    return kwargs


def extract_value(text, start):
    rest = text[start:].strip()
    if not rest:
        return None

    depth = 0
    in_string = False
    string_char = None
    i = 0
    for i, ch in enumerate(rest):
        if in_string:
            if ch == string_char and (i == 0 or rest[i - 1] != '\\'):
                in_string = False
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
            elif ch in ('(', '[', '{'):
                depth += 1
            elif ch in (')', ']', '}'):
                if depth == 0:
                    return rest[:i]
                depth -= 1
            elif ch == ',' and depth == 0:
                return rest[:i]
    return rest[:i + 1]


def group_by_family(dataset_entries):
    families = {}
    has_zero_padded = set()
    for name, kwargs in dataset_entries:
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
            families[base][index] = (name, kwargs)

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


def check_sibling_consistency(families):
    issues = []
    error_params = ["do_reco", "scenario"]
    warning_params = ["physics_skims", "dqm_sequences"]

    for family, members in sorted(families.items()):
        if len(members) < 2:
            continue

        member_list = sorted(members.values(), key=lambda x: x[0])

        for param in error_params + warning_params:
            values = {}
            for name, kwargs in member_list:
                val = kwargs.get(param, "<default>")
                if val not in values:
                    values[val] = []
                values[val].append(name)

            if len(values) > 1:
                level = "ERROR" if param in error_params else "WARNING"
                detail_parts = []
                for val, names in sorted(values.items(), key=lambda x: x[1][0]):
                    detail_parts.append(
                        "%s have %s=%s" % (", ".join(names), param, val)
                    )
                issues.append((
                    level,
                    family,
                    "Inconsistent '%s': %s" % (param, "; ".join(detail_parts))
                ))

    return issues


def validate_file(filepath):
    with open(filepath, 'r') as f:
        source = f.read()

    entries = extract_datasets_and_blocks(source)
    families = group_by_family(entries)

    all_issues = []
    all_issues.extend(check_gaps(families))
    all_issues.extend(check_sibling_consistency(families))

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
