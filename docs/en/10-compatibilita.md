# Compatibility and testing

🌐 [Italiano](../10-compatibilita.md) · **English** · [中文](../zh/10-compatibilita.md)

This page states what has been verified against the real program and what has not. It is not a list of promises.

**Version tested:** nuclei v3.11.1, official release binary, macOS arm64.

## What has been verified

1. **The profile flags exist.** Every flag used by a profile was checked against the `nuclei -h` output of the tested version: none unknown.
2. **The forbidden flags exist.** The forbidden list was also checked against the real help, so as not to forbid made-up names and to look for dangerous flags that were missing. Some were found and added.
3. **A real run works.** `nuclei-cli lancia ... --esegui` with the real binary, and `rapporto` reading the result.
4. **Stdin closed.** Some tools also read targets from stdin, and those bypass the scope. The program closes the child process's stdin; there is a test that proves it with a fake executable, and the check with the real binaries is below.
5. **Result formats.** The parsers read real outputs, kept in `tests/fixtures/` (see the README in there).
6. **The right binary.** `doctor` and `--esegui` check that the executable in the PATH really is nuclei and not a program with the same name. Tested with the real binary (accepted) and with a fake one (refused, code 5).
7. **Python and installation.** Tests pass with Python 3.11.18 and 3.13 on macOS and with 3.12.3 on Linux. Clean install with `pip install .` in a fresh venv, command on the PATH included.
8. **Types.** `mypy --strict` finds no errors in `src/`. It is not proof of correctness, but an extra check on what a parameter or return value can actually be; it runs in CI, so it cannot break without a test flagging it.
9. **How much the tests actually cover.** `coverage` measures coverage: CI fails below 85%, the real figure is higher. A number stated without ever being measured means nothing.



## What has NOT been verified

`prudente` was tested with 3992 official templates (downloaded on 22/11/2026) against the local target: no results, as expected for a plain server. A positive result was parsed from a test template run directly, because the wrapper forbids `-t`.

## If you use a different version

Output formats and flags change between versions. If `nuclei-cli doctor` shows a different version, the tests do not know that. Run `make check` and, above all, a test run against a target of your own before trusting it. If you find a flag that bypasses the scope and is not on the forbidden list, it is a vulnerability: see [SECURITY.md](../../SECURITY.md).
