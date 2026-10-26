print(f"[hello.py] top-level code running, __name__ = {__name__}")
def greet(name: str) -> str:
    return f"Hello, {name}!"


def main() -> None:
    print(greet("arcade"))


if __name__ == "__main__":
    main()