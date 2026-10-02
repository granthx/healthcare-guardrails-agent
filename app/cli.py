import sys
from langgraph.types import Command
from .agent import healthcare_bot

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def print_last(result):
    print("\n--- Assistant ---")
    print(result["messages"][-1].content)


def run_demo():
    print("Healthcare Guardrails Agent")
    print("===========================")

    thread = {"configurable": {"thread_id": "demo-safe"}}
    result = healthcare_bot.invoke(
        {"messages": [{
            "role": "user",
            "content": "What are common symptoms of Type 2 diabetes?"
        }]},
        config=thread,
    )
    print("\n[1] Safe medical query")
    print_last(result)

    thread = {"configurable": {"thread_id": "demo-pii"}}
    result = healthcare_bot.invoke(
        {"messages": [{
            "role": "user",
            "content": (
                "My email is patient123@gmail.com. "
                "What can I take for a headache?"
            )
        }]},
        config=thread,
    )
    print("\n[2] PII redaction")
    print_last(result)

    thread = {"configurable": {"thread_id": "demo-blocked"}}
    result = healthcare_bot.invoke(
        {"messages": [{
            "role": "user",
            "content": "How do I synthesize drugs at home?"
        }]},
        config=thread,
    )
    print("\n[3] Harmful request")
    print_last(result)

    thread = {"configurable": {"thread_id": "demo-hitl"}}
    result = healthcare_bot.invoke(
        {"messages": [{
            "role": "user",
            "content": "Book me an appointment with Dr. Granth Chhabra on 2026-10-15. My name is Alex Carter."
        }]},
        config=thread,
    )
    print("\n[4] Appointment booking")

    if "__interrupt__" in result:
        print("HITL INTERRUPT: appointment tool requires human approval.")
        answer = input("Approve appointment? [y/N]: ").strip().lower()
        decision = "approve" if answer == "y" else "reject"
        resumed = healthcare_bot.invoke(
            Command(resume={"decisions": [{"type": decision}]}),
            config=thread,
        )
        print_last(resumed)
    else:
        print_last(result)


if __name__ == "__main__":
    run_demo()
