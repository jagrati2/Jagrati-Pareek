"""
main.py

Entry point for the Chat-with-Documents agent.

Usage:
  # First-time setup: ingest documents
  python main.py --ingest

  # Ask a question
  python main.py --ask "What is gradient descent?"

  # Interactive chat mode
  python main.py
"""

import argparse
import sys


def run_ingest():
    print("=" * 60)
    print("Running ingestion pipeline...")
    print("=" * 60)
    from ingest.ingest import run_ingestion
    run_ingestion()
    print("\nIngestion complete. You can now ask questions.")


def ask_question(question: str):
    print(f"\nQuestion: {question}")
    print("-" * 60)
    from agent.graph import run_agent
    answer = run_agent(question)
    print(f"Answer:\n{answer}")
    print("-" * 60)


def interactive_mode():
    print("=" * 60)
    print("Chat with Documents Agent")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 60)
    from agent.graph import run_agent
    while True:
        try:
            question = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        print("\nAgent: ", end="", flush=True)
        answer = run_agent(question)
        print(answer)


def main():
    parser = argparse.ArgumentParser(description="Chat with Documents Agent")
    parser.add_argument(
        "--ingest",
        action="store_true",
        help="Run the ingestion pipeline to index documents",
    )
    parser.add_argument(
        "--ask",
        type=str,
        help="Ask a single question and exit",
    )
    args = parser.parse_args()

    if args.ingest:
        run_ingest()
    elif args.ask:
        ask_question(args.ask)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()