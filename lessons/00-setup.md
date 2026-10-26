# Lesson 0: The toolbox (interpreters, venv, uv, modules)

Time: 1 to 2 sessions. You type every command yourself. When you see **PREDICT**, write your
guess in `LOG.md` before you press Enter. Answers are in the collapsed sections; open them only
after you have run the command.

---

## Part A: What actually runs your code? (15 min)

In C++, `g++` turns your source into a machine-code binary, and the binary runs without g++.
In Python, the **interpreter** (a program called `python3`, itself written in C) reads your `.py`
file, compiles it to **bytecode** (instructions for a virtual machine, a bit like Java's), and
executes that bytecode immediately. No separate binary. That is why:
- errors only appear when the bad line actually **runs** (a typo inside an `if` that never runs
  goes unnoticed),
- you sometimes see `__pycache__/` folders: cached bytecode (`.pyc`), safe to delete.

Run:
```bash
which -a python3
python3 --version
/usr/bin/python3 --version
/usr/local/bin/python3 --version
```
**PREDICT** first: how many Pythons are on your Mac, and which one does plain `python3` run?

<details><summary>What you will see and why</summary>

Three interpreters:
- `/usr/bin/python3` → **3.9**, Apple's, for macOS's own use. Never install things into it.
- `/usr/local/bin/python3` → **3.14**, installed by Homebrew.
- `~/.pyenv/shims/python3` → **3.12**, managed by pyenv. It is first in your `$PATH`, so plain
  `python3` runs this one.

The shell walks `$PATH` left to right and runs the first match, exactly like it does for any C++
binary. This mess is normal, and it is the first reason virtual environments exist: a project
should not care which `python3` happens to be first in your PATH today.
</details>

Now the REPL (Read-Eval-Print Loop), your new best friend for experiments:
```bash
python3
>>> 2 ** 100
>>> 7 / 2
>>> 7 // 2
>>> -7 // 2
>>> type(7), type(7 / 2), type("7")
>>> exit()
```
**PREDICT** each line. The `-7 // 2` one is a trap for C++ people.

<details><summary>Answers</summary>

`1267650600228229401496703205376` (ints never overflow, they grow as needed) · `3.5` (`/` is always
float division) · `3` · `-4` (Python floors toward minus infinity; C++ truncates toward zero and
gives `-3`) · `(<class 'int'>, <class 'float'>, <class 'str'>)` (every value knows its type at run time).
</details>

---

## Part B: Where do libraries live? (15 min)

In C++, libraries are headers and `.a`/`.so` files you point at with `-I` and `-L`. In Python, a
library is just a folder of `.py` files (plus sometimes compiled C), and the interpreter looks for
it in a list of folders called `sys.path`. Third-party libraries go into a folder called
**`site-packages`**.

```bash
python3 -c "import sys; print(sys.executable); print(sys.prefix)"
python3 -c "import sys; print('\n'.join(sys.path))"
```
`python3 -c "..."` runs one line of code. Look at the `sys.path` list: your own folder first, then
the standard library, then `site-packages`.

**The problem:** each interpreter has **one** `site-packages`. If project A needs `pandas 1.5` and
project B needs `pandas 2.2`, and both use the same interpreter, one of them breaks. Installing
everything globally is like every C++ project on your machine sharing one `/usr/local/include`
with whatever versions happen to be there.

**The fix: a virtual environment (venv)** = a folder containing
1. a link to an existing interpreter, and
2. its **own empty `site-packages`**.

That is all. No VM, no container, no copy of Python.

---

## Part C: Build a venv by hand, so it stops being magic (25 min)

Do this in a throwaway folder:
```bash
mkdir -p ~/Desktop/switch/venv-playground && cd ~/Desktop/switch/venv-playground
python3 -m venv .venv          # "-m venv" = run the standard-library module named venv
ls .venv
ls -l .venv/bin/
cat .venv/pyvenv.cfg
```
**PREDICT** before `ls -l`: is `.venv/bin/python` a full copy of Python, or something else?

<details><summary>Answer</summary>

It is a **symlink** (`python -> python3 -> python3.12`), and the last link points at the interpreter
that created the venv (`pyvenv.cfg` records which one under `home =`).
`.venv/lib/python3.12/site-packages/` is the private library folder. `.venv/bin/activate` is a
shell script.
</details>

Now see what "activate" really does:
```bash
echo $PATH
source .venv/bin/activate
echo $PATH
which python
python -c "import sys; print(sys.prefix); print(sys.base_prefix)"
```
**PREDICT:** what changed in `$PATH`?

<details><summary>Answer</summary>

`activate` only **puts `.venv/bin` at the front of `$PATH`** (and changes your prompt). So `python`
now finds `.venv/bin/python` first. `sys.prefix` is the venv; `sys.base_prefix` is the real
interpreter. Activation is a convenience: running `.venv/bin/python` directly works the same
without activating anything.
</details>

Install a library into the venv and prove it is isolated:
```bash
pip install cowsay
python -c "import cowsay; print(cowsay.__file__)"
python -c "import cowsay; cowsay.cow('hello from inside the venv')"
deactivate
python3 -c "import cowsay"
```
**PREDICT** the last line.

<details><summary>Answer</summary>

`ModuleNotFoundError: No module named 'cowsay'`. The library lives only in `.venv/.../site-packages`.
Outside the venv, Python cannot see it.

Careful: this only works because `cowsay` was never installed globally. Try the same thing with
`rich` and it still imports after `deactivate`, because your global pyenv 3.12 already had its own
copy of `rich` (installed back in August). Compare the two `__file__` paths: they are different
copies in different `site-packages` folders. Isolation means the venv has **its own** folder. It
does not delete what is already in the global one.
</details>

Finally, venvs are disposable. Never commit them to git; rebuild them from a list of dependencies.
```bash
cd .. && rm -rf venv-playground
```

---

## Part D: uv, the modern way (20 min)

Doing Part C by hand gets tedious: you must remember to activate, remember what you installed, and
your teammate has no idea which versions you used. **uv** is a single tool that does all of it
(it plays the role that CMake + a package manager play in C++ land). You already have it
installed.

| Command | What it does |
|---|---|
| `uv init` | creates `pyproject.toml` (project name, Python version, dependency list), `.python-version`, `main.py`, `.gitignore`, and a git repo |
| `uv add rich` | adds `rich` to `pyproject.toml`, creates `.venv` if missing, installs it, and writes exact versions to `uv.lock` |
| `uv run <cmd>` | makes sure `.venv` matches the lock file, then runs `<cmd>` **inside** the venv (no `activate` needed) |
| `uv sync` | rebuilds `.venv` from `uv.lock` (what a teammate runs after cloning) |
| `uv remove rich` | the reverse of `uv add` |

`pyproject.toml` = what you *want* (`rich>=14`). `uv.lock` = what you *got* (exact versions and
hashes), so everyone gets the same install. Both go in git. `.venv` does not.

Set up the arcade project (you are in the folder that holds this lesson's `ROADMAP.md`):
```bash
cd ~/Desktop/switch/python-arcade
uv init --python 3.12
ls -a
cat pyproject.toml
uv run main.py
ls -a
uv add rich
cat pyproject.toml
head -20 uv.lock
```
**PREDICT:** after `uv run main.py`, which new folder appears and why?

<details><summary>Answer</summary>

`.venv/`. `uv run` saw there was no environment yet, created one, synced it (empty, no
dependencies), and ran `main.py` with `.venv/bin/python`. Check `cat .gitignore`: `.venv` is listed.
</details>

---

## Part E: Modules, packages, and the three "init"s (30 min)

**`import` is not `#include`.** `#include` pastes text at compile time. `import x` at run time:
1. finds `x.py` by searching `sys.path`,
2. **runs the whole file** top to bottom, once,
3. stores the result as a **module object** in a cache (`sys.modules`) and binds the name `x`.

A second `import x` anywhere finds it in the cache and does not rerun the file.

- **module** = one `.py` file.
- **package** = a folder of modules with an `__init__.py` file in it. `__init__.py` runs when the
  package is first imported. It is usually empty; it can also expose a nicer public API.

Create this (yes, type it yourself):
```
python-arcade/
└── arcade/
    ├── __init__.py      →  print(f"[__init__.py] package loading, __name__ = {__name__}")
    └── hello.py         →  see below
```
`arcade/hello.py`:
```python
print(f"[hello.py] top-level code running, __name__ = {__name__}")


def greet(name: str) -> str:
    return f"Hello, {name}!"


def main() -> None:
    print(greet("arcade"))


if __name__ == "__main__":
    main()
```

Now run each of these. **PREDICT** for each one: which lines print, and what is `__name__`?
```bash
uv run python -c "import arcade.hello"
uv run python -c "import arcade.hello; import arcade.hello; print(arcade.hello.greet('Kaustubh'))"
uv run python -m arcade.hello
uv run python arcade/hello.py
```

<details><summary>Answers</summary>

1. `__init__.py` prints with `__name__ = arcade`, then `hello.py` prints with `__name__ = arcade.hello`. `main()` does **not** run.
2. Same two lines **once only** (cached), then `Hello, Kaustubh!`.
3. `-m arcade.hello` = "run this module as the program". The package `__init__.py` runs first, then `hello.py` runs with `__name__ = "__main__"`, so `main()` runs.
4. Running the file by path treats it as a loose script: `__init__.py` does **not** run, `__name__` is `"__main__"`. This is why we prefer `-m` once code lives in packages: imports between your own modules work reliably.
</details>

**So, `if __name__ == "__main__":`** means "only do this when I am the program being run, not when
someone imports me". It is Python's `int main()`. Every game you write will end with it.

### The three different "init"s (people mix them up constantly)
| Name | What it is | You will meet it |
|---|---|---|
| `uv init` | a **shell command** that creates a new project | today |
| `__init__.py` | a **file** that makes a folder a package; runs on first import | today |
| `def __init__(self, ...)` | a **method** inside a class; the constructor | Game 6 (classes) |

Clean up: delete the `print` line from `arcade/__init__.py` (leave the file, empty) and delete
`main.py` (`uv init` created it as a sample). Keep `hello.py` if you like.

---

## Part F: Commit (5 min)
```bash
git status            # .venv and __pycache__ should NOT appear (thanks to .gitignore)
git add -A && git commit -m "Lesson 0: uv project and arcade package"
```

---

## Explain-it-back (write the answers in `LOG.md` from memory, no peeking)
1. What physically is a venv, and what does `source .venv/bin/activate` change?
2. Why do `pyproject.toml` and `uv.lock` both exist? Which one goes in git? Does `.venv`?
3. What does `uv run` do that plain `python` does not?
4. What happens, step by step, the first time Python executes `import arcade.hello`? And the second time?
5. What is `__name__` when a file is imported vs run with `-m`? Why does that matter?
6. Name the three "init"s and what each one is.

When you are done, tell Claude "lesson 0 done" and paste your answers for review. Then on to
[Lesson 1: Guess the Number](01-guess-the-number.md).
