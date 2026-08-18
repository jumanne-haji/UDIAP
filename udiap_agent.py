import os
import subprocess
from pathlib import Path

from google import genai
from google.genai import types


PROJECT = Path.home() / "udiap-complete-fixed"

if not PROJECT.exists():
    raise SystemExit(f"❌ UDIAP project haipo: {PROJECT}")

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise SystemExit("❌ GEMINI_API_KEY haijawekwa.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


def safe_path(path: str) -> Path:
    p = (PROJECT / path).resolve()

    if p != PROJECT and PROJECT not in p.parents:
        raise ValueError("❌ Path iko nje ya UDIAP project.")

    return p


def git_status() -> str:
    result = subprocess.run(
        ["git", "status", "--short", "--branch"],
        cwd=PROJECT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout + result.stderr


def git_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "--stat"],
        cwd=PROJECT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout + result.stderr


def read_file(path: str) -> str:
    p = safe_path(path)

    if not p.is_file():
        return f"File haipo: {path}"

    if p.stat().st_size > 500_000:
        return "File ni kubwa sana."

    return p.read_text(encoding="utf-8", errors="replace")


def write_file(path: str, content: str) -> str:
    p = safe_path(path)

    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

    return f"✅ File imeandikwa: {p.relative_to(PROJECT)}"


def list_files(path: str = ".") -> str:
    p = safe_path(path)

    if not p.is_dir():
        return f"Directory haipo: {path}"

    entries = []

    for item in sorted(p.iterdir()):
        if item.name in {
            ".git",
            ".venv",
            "venv",
            "__pycache__",
            "node_modules",
        }:
            continue

        prefix = "DIR " if item.is_dir() else "FILE"
        entries.append(f"{prefix} {item.name}")

    return "\n".join(entries[:200])


def run_tests() -> str:
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        cwd=PROJECT,
        capture_output=True,
        text=True,
        timeout=120,
    )

    return (
        f"exit_code={result.returncode}\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )


def search_code(query: str, path: str = ".") -> str:
    """Search text/code locally ndani ya UDIAP bila kutumia Gemini."""
    root = safe_path(path)

    if not root.exists():
        return f"Path haipo: {path}"

    results = []

    skip_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".next",
    }

    extensions = {
        ".py", ".ts", ".tsx", ".js", ".jsx",
        ".json", ".yaml", ".yml", ".md",
        ".txt", ".sql", ".env.example"
    }

    if root.is_file():
        files = [root]
    else:
        files = []

        for f in root.rglob("*"):
            if not f.is_file():
                continue

            if any(part in skip_dirs for part in f.parts):
                continue

            if f.suffix.lower() in extensions:
                files.append(f)

    for f in files:
        try:
            text = f.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        for line_no, line in enumerate(
            text.splitlines(),
            start=1
        ):
            if query.lower() in line.lower():
                relative = f.relative_to(PROJECT)

                results.append(
                    f"{relative}:{line_no}: {line.strip()}"
                )

                if len(results) >= 100:
                    return "\n".join(results)

    if not results:
        return f'No matches found for "{query}"'

    return "\n".join(results)


def file_info(path: str) -> str:
    """Pata metadata ya file/directory ndani ya UDIAP."""
    p = safe_path(path)

    if not p.exists():
        return f"Haipo: {path}"

    stat = p.stat()

    if p.is_dir():
        kind = "directory"
    else:
        try:
            import mimetypes
            kind = mimetypes.guess_type(p.name)[0] or "file"
        except Exception:
            kind = "file"

    return (
        f"Path: {p.relative_to(PROJECT)}\n"
        f"Type: {kind}\n"
        f"Size: {stat.st_size} bytes\n"
        f"Modified: {stat.st_mtime}\n"
        f"Permissions: {oct(stat.st_mode & 0o777)}"
    )


TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="git_status",
                description="Angalia Git branch na modified files za UDIAP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={},
                ),
            ),
            types.FunctionDeclaration(
                name="git_diff",
                description="Angalia summary ya Git changes.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={},
                ),
            ),
            types.FunctionDeclaration(
                name="read_file",
                description="Soma file ndani ya UDIAP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "path": types.Schema(type=types.Type.STRING)
                    },
                    required=["path"],
                ),
            ),
            types.FunctionDeclaration(
                name="write_file",
                description="Andika au rekebisha file ndani ya UDIAP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "path": types.Schema(type=types.Type.STRING),
                        "content": types.Schema(type=types.Type.STRING),
                    },
                    required=["path", "content"],
                ),
            ),
            types.FunctionDeclaration(
                name="list_files",
                description="Orodhesha files ndani ya UDIAP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "path": types.Schema(type=types.Type.STRING)
                    },
                ),
            ),
            types.FunctionDeclaration(
                name="search_code",
                description="Search locally ndani ya UDIAP source code bila kutumia API.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(type=types.Type.STRING),
                        "path": types.Schema(type=types.Type.STRING),
                    },
                    required=["query"],
                ),
            ),
            types.FunctionDeclaration(
                name="file_info",
                description="Pata type, size, modification time na permissions za file ndani ya UDIAP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "path": types.Schema(type=types.Type.STRING)
                    },
                    required=["path"],
                ),
            ),
            types.FunctionDeclaration(
                name="run_tests",
                description="Endesha pytest ndani ya UDIAP.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={},
                ),
            ),
        ]
    )
]


def execute_tool(name, args):
    if name == "git_status":
        return git_status()

    if name == "git_diff":
        return git_diff()

    if name == "read_file":
        return read_file(args["path"])

    if name == "write_file":
        return write_file(
            args["path"],
            args["content"],
        )

    if name == "list_files":
        return list_files(args.get("path", "."))

    if name == "search_code":
        return search_code(
            args["query"],
            args.get("path", ".")
        )

    if name == "file_info":
        return file_info(args["path"])

    if name == "run_tests":
        return run_tests()

    return f"Unknown tool: {name}"


SYSTEM = """
Wewe ni UDIAP Local Engineering Agent.

Unafanya kazi ndani ya repository hii tu:

~/udiap-complete-fixed

Majukumu:
- Kuchambua UDIAP.
- Kuangalia Git status/diff.
- Kusoma files.
- Kuandika/kurekebisha files.
- Kuendesha pytest.
- Kutoa diagnosis kabla ya mabadiliko.

USIFANYE:
- git reset --hard
- git push
- rm -rf
- kufuta repository
- kubadilisha secrets
- kusoma files zilizo nje ya UDIAP.

Ukifanya mabadiliko ya code, eleza ulichobadilisha
na run tests inapowezekana.
"""


def ask_agent(user_message: str):

    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)],
        )
    ]

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            tools=TOOLS,
            temperature=0.2,
        ),
    )

    while True:

        function_calls = []

        for candidate in response.candidates or []:
            for part in candidate.content.parts or []:
                if part.function_call:
                    function_calls.append(part.function_call)

        if not function_calls:
            return response.text

        tool_parts = []

        for call in function_calls:

            print(f"\n🔧 Tool: {call.name}")
            print(f"   Args: {call.args}")

            try:
                result = execute_tool(
                    call.name,
                    dict(call.args or {}),
                )
            except Exception as e:
                result = f"ERROR: {type(e).__name__}: {e}"

            print(f"   → {str(result)[:500]}")

            tool_parts.append(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

        contents.append(response.candidates[0].content)

        contents.append(
            types.Content(
                role="user",
                parts=tool_parts,
            )
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM,
                tools=TOOLS,
                temperature=0.2,
            ),
        )


def main():

    print()
    print("╔══════════════════════════════════════╗")
    print("║       🤖 UDIAP LOCAL AGENT           ║")
    print("╚══════════════════════════════════════╝")
    print()
    print(f"📁 Project: {PROJECT}")
    print(f"🧠 Model:   {MODEL}")
    print()
    print("Andika 'exit' kuacha.")
    print()

    while True:

        try:

            user = input("UDIAP> ").strip()

            if not user:
                continue

            if user.lower() in {"exit", "quit"}:
                print("👋 Agent stopped.")
                break

            answer = ask_agent(user)

            print("\n🤖", answer)
            print()

        except KeyboardInterrupt:
            print("\n👋 Agent stopped.")
            break

        except Exception as e:
            print(f"\n❌ ERROR: {type(e).__name__}: {e}\n")


if __name__ == "__main__":
    main()
