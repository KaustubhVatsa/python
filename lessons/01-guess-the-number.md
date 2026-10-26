# Game 1: Guess the Number

You will write `arcade/guess.py` from an empty file. No libraries beyond the standard library.
Run it with `uv run python -m arcade.guess`.

## Step 1: Warm-up in the REPL (20 min)
Open `uv run python`. **PREDICT** each line in `LOG.md`, then run it.
```python
x = 5
x = "five"            # allowed? (C++ would refuse)
"3" + 3               # allowed?
"3" * 3
int("42") + 1
int(" 42 \n")
int("4.2")
float("4.2")
0.1 + 0.2 == 0.3
1 < 5 < 10            # what does C++ do with this?
bool(""), bool("0"), bool([]), bool(0), bool(None)
name = "Ada"; f"Hi {name}, 2+2={2+2}, upper={name.upper()}"
import random; random.randint(1, 3)   # run it 10 times: can it return 3?
```
<details><summary>What to take away</summary>

- **Dynamic typing:** names have no type, values do. `x` can point to an int, then a str.
- **Strong typing:** Python will not silently convert. `"3" + 3` is a `TypeError`. `"3" * 3` is `"333"` (repetition is defined for str × int).
- `int()` strips whitespace but refuses `"4.2"` with a `ValueError`. You will catch exactly that error in your game.
- Floats are IEEE doubles, same pitfalls as C++.
- Chained comparisons work like math: `1 < 5 < 10` means `1 < 5 and 5 < 10`. In C++ it compares a bool to 10.
- Empty things (`""`, `[]`, `0`, `None`) are falsy. `"0"` is a non-empty string, so it is truthy.
- `random.randint(a, b)` includes **both** ends.
</details>

## Step 2: The spec
```
=== Guess the Number ===
Choose difficulty: (e)asy 1-50 / 10 tries, (m)edium 1-100 / 7 tries, (h)ard 1-1000 / 10 tries
> m
I'm thinking of a number between 1 and 100. You have 7 tries.
Guess #1: 50
Too high!
Guess #2: abc
That's not a whole number. Try again.        <- does NOT cost a try
Guess #2: 500
Please guess between 1 and 100.              <- does NOT cost a try
Guess #2: 25
Too low!
...
Correct! You got it in 4 tries.
Play again? (y/n) n
Thanks for playing. You won 1 of 1 games.
```
Requirements:
1. Invalid input (not a number, out of range) is rejected with a message and **does not** use up a try.
2. Out of tries → reveal the number.
3. Play-again loop; print wins/games at the end.
4. Pressing Ctrl+C or Ctrl+D quits politely instead of dumping a stack trace. (Hint: which exceptions does `input()` raise for these? Find out by trying it in the REPL.)

## Step 3: Shape of the code (write it in this shape)
```python
import random

DIFFICULTIES = ...   # how will you store (name -> low, high, tries)? A dict? Tuples inside?


def ask_int(prompt: str, low: int, high: int) -> int:
    """Keep asking until the user types a whole number in [low, high]. Return it."""


def play_round(low: int, high: int, max_tries: int) -> bool:
    """Play one game. Return True if the player won."""


def main() -> None:
    """Difficulty menu, play-again loop, final score."""


if __name__ == "__main__":
    main()
```
Type hints like `-> bool` are **documentation only**; Python does not enforce them at run time.
(Later a tool called `mypy` will check them for you, like a compiler would.)

## Hints (read only when stuck)
<details><summary>Hint 1: looping until valid input</summary>

`while True:` with `return` inside when the input is good. `try: n = int(text) except ValueError: ...`
</details>
<details><summary>Hint 2: Python has no do-while or ++</summary>

`count += 1`. And `for attempt in range(1, max_tries + 1):` is often cleaner than a `while` with a counter.
</details>
<details><summary>Hint 3: for/else</summary>

A `for` loop can have an `else:` block that runs only if the loop finished **without** `break`.
Perfect for "ran out of tries". Look it up, it is unusual but idiomatic.
</details>

## Stretch goals (pick at least one)
1. **Reverse mode:** *you* think of a number and the computer guesses, using your answers "h/l/c". You know the best strategy from C++ days. How many guesses does it need for 1-1000, worst case? Make it detect when you lie.
2. **Testable randomness:** make `play_round` take an optional `rng: random.Random | None = None` and use `rng.randint(...)`. Then `random.Random(42)` always produces the same secret. Why is that useful? (This idea returns in Game 7 and in data pipelines.)
3. **Pretty output:** use `rich` (you added it in Lesson 0) for colours.

## Done when
- [ ] Every requirement in Step 2 works (try to break your own game: empty input, `-5`, `1e3`, `   7  `, Ctrl+D)
- [ ] `git commit -m "Game 1: guess the number"`
- [ ] Tell Claude "game 1 ready for review". You will get a review like a real code review: bugs first, then "more Pythonic" suggestions.

## Explain-it-back
1. Dynamic typing vs strong typing: one sentence each, plus an example.
2. Why does `int("4.2")` fail while `int(float("4.2"))` works?
3. What does `for ... else` do?
4. Why does `-7 // 2` give `-4` in Python?
