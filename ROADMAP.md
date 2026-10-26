# Python Arcade: from C++ to Data Engineering + Agentic AI, one game at a time

**Goal:** write Python the way data engineers and AI engineers write it, and be able to explain
every line in an interview. Each game teaches a set of language features, and every game after
the first few also teaches a career skill (testing, files, SQL, pipelines, APIs, LLM tools).

**Rules**
1. **You write the code. Claude explains, sets the spec, and reviews.** Reading is not learning.
2. Every lesson follows **PREDICT → RUN → BREAK → BUILD → EXPLAIN-BACK**. Before running a line,
   write down what you think it will print. Being wrong is where you learn the most.
3. One game = one folder of work + one git commit (or more). Log what you learned in `LOG.md`.
4. If something feels like magic (`venv`, `__init__`, `self`, `import`), stop and ask. Nothing in
   Python is magic; it is a bit of code someone wrote that we can read.

**Pace:** about 1 to 2 hours a day. Each game takes 2 to 5 sessions. Full track: about 8 to 10 weeks.
Do not skip ahead. Slower and solid beats faster and shaky.

---

## Phase 0: The toolbox (1 to 2 sessions)
| # | Lesson | You will understand |
|---|---|---|
| 0 | [Setup: interpreters, venv, uv, modules](lessons/00-setup.md) | Why your Mac has three `python3`s, what a venv physically is, what `uv init` / `uv add` / `uv run` do, how `import` differs from `#include`, the three different "init"s, `if __name__ == "__main__"` |

## Phase 1: Core Python through terminal games (stdlib only, about 2 weeks)
| # | Game | New Python | C++ habit to unlearn |
|---|---|---|---|
| 1 | [**Guess the Number**](lessons/01-guess-the-number.md) | variables, dynamic vs strong typing, `input`, `int()`, `while`/`if`/`elif`, f-strings, functions, `try/except`, `random` | `-7 // 2` is `-4`, ints never overflow, no `{}` or `;` |
| 2 | **Hangman** | strings (immutable, slicing), lists, sets, `for x in ...`, `in`, string methods, constants | indexing loops (`for i in range(len(x))`) instead of iterating directly |
| 3 | **Tic-Tac-Toe + unbeatable AI** | lists of lists, tuples, unpacking, `enumerate`, `zip`, recursion (minimax), **names are references** | `[[" "]*3]*3` aliasing bug; assignment never copies |
| 4 | **Blackjack** | dicts, comprehensions, splitting code into modules, packages, `__init__.py`, first **pytest** tests | header/implementation split; Python has no headers |
| 5 | **Text Adventure (data-driven)** | world loaded from JSON, `pathlib`, `with open(...)`, validating input data, `dict.get` | hard-coding data in code (the #1 data-engineering lesson: data lives outside code) |

## Phase 2: Real Python (classes, packages, tooling, about 2 weeks)
| # | Game | New Python | Career link |
|---|---|---|---|
| 6 | **Snake** (`pygame-ce`) | classes, `self`, `__init__`, dunder methods, a game loop, third-party deps via `uv add` | event loops (agents and schedulers are loops too) |
| 7 | **Dungeon Forge: dice + combat RPG** (resumes `agentic-ai-month/dungeon-forge`) | `@dataclass`, `Enum`, type hints + `mypy`, inheritance vs composition, `Protocol`, regex, seeded RNG for testable randomness | these game functions become **LLM tools** in Phase 4 |
| 8 | **Save system + leaderboard** | JSON vs SQLite (`sqlite3`), context managers, decorators (timing/logging), generators (event stream), `logging` | you are now writing a tiny database-backed app |

## Phase 3: Data Engineering with game data (about 2 to 3 weeks)
| # | Project | New Python | Career link |
|---|---|---|---|
| 9 | **Casino Simulator**: bots play 100k Blackjack hands, emit JSONL events | generators for streaming, batching, `itertools`, `multiprocessing` vs threads (the GIL) | producing event data like real product telemetry |
| 10 | **Telemetry pipeline**: raw events → validated → warehouse → analytics | Pydantic schemas, bad-row quarantine, idempotent/incremental loads, Parquet, DuckDB, pandas/polars, charts | ETL/ELT, data quality, partitions, "what happens if the job runs twice?" |
| 11 | **Pokémon Battle**: data pulled live from PokeAPI | `asyncio` + `httpx`, retries with backoff, rate limits, caching, config/env vars, a CLI, Docker basics, CI | API ingestion, orchestration-ready jobs (we will schedule it with Prefect or Airflow) |

## Phase 4: Agentic AI with the games you built (about 2 to 3 weeks)
| # | Project | New Python | Career link |
|---|---|---|---|
| 12 | **LLM Dungeon Master**: your Dungeon Forge functions become tools | raw LLM API calls, JSON Schema tool definitions, the agent loop by hand, max-iteration guards, cost tracking | "How does tool calling actually work?" asked in every agent interview |
| 13 | **An agent that plays your games** (Hangman / Text Adventure) + **evals** | structured output with Pydantic, run N games and measure win rate, LLM-as-judge vs deterministic checks, tracing | evals are what separate demos from production agents |
| 14 | **Capstone: "Ask your game warehouse"** agent: questions in English → safe SQL over the Phase 3 DuckDB warehouse → answer + chart | LangGraph (state, routing, human approval), guardrails (read-only SQL, row limits), prompt-injection awareness | combines data engineering and agentic AI in one portfolio project |

After Phase 4 you are ready to go back to `agentic-ai-month/ROADMAP.md` Phase 3 (the pipeline-triage
agent) and to Verity's reasoning tasks with a solid Python base.

---

## C++ → Python cheat sheet (fill in more as you learn)
| C++ | Python | Watch out |
|---|---|---|
| `g++ main.cpp && ./a.out` | `python3 main.py` (compiled to bytecode on the fly, in `__pycache__/`) | errors appear at **run time**, only when that line runs |
| `#include "x.h"` | `import x` | import **runs** `x.py` once and hands you a module object |
| `int main()` | `if __name__ == "__main__": main()` | top-level code runs on import too |
| `int x = 5;` | `x = 5` | a name is a label stuck on an object, not a box of memory |
| `std::vector<int>` | `list` | holds any type; `a = b` does **not** copy |
| `std::unordered_map` | `dict` | insertion order is preserved |
| `std::set` | `set` | |
| `std::tuple` / `std::pair` | `tuple` | immutable |
| `nullptr` | `None` | compare with `is None`, not `== None` |
| `this->x` | `self.x` | `self` is written explicitly as the first parameter |
| constructor `Foo()` | `def __init__(self):` | |
| `operator==`, `operator<<` | `__eq__`, `__repr__` / `__str__` | "dunder" = double underscore |
| `for (int i=0;i<n;i++)` | `for item in items:` (or `enumerate(items)` if you need `i`) | |
| `&&` `\|\|` `!` | `and` `or` `not` | |
| `x / y` (ints) | `x // y` | `/` always gives a float; `//` floors (`-7 // 2 == -4`) |
| CMakeLists.txt | `pyproject.toml` | |
| system libs in `/usr/lib` | `site-packages/` inside a venv | |

## Progress
- [ ] 0 Setup
- [ ] 1 Guess the Number
- [ ] 2 Hangman
- [ ] 3 Tic-Tac-Toe
- [ ] 4 Blackjack
- [ ] 5 Text Adventure
- [ ] 6 Snake
- [ ] 7 Dungeon Forge
- [ ] 8 Save system + leaderboard
- [ ] 9 Casino Simulator
- [ ] 10 Telemetry pipeline
- [ ] 11 Pokémon Battle
- [ ] 12 LLM Dungeon Master
- [ ] 13 Game-playing agent + evals
- [ ] 14 Capstone: Ask your game warehouse
