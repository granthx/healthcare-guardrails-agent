from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage
from langgraph.runtime import Runtime


class HealthcareSafetyFilter(AgentMiddleware):
    """Deterministic safety/domain gate executed before agent reasoning."""

    BLOCKED_TOPICS = (
        "drug synthesis",
        "synthesize drug",
        "synthesizing drug",
        "synthesise drug",
        "how to synthesize",
        "make drugs",
        "manufacture drugs",
        "self-harm",
        "suicide method",
        "how to commit suicide",
        "weapon construction",
        "how to make a weapon",
        "hack into",
        "steal passwords",
    )

    HEALTHCARE_HINTS = (
        "symptom", "medicine", "medication", "doctor", "hospital",
        "appointment", "pain", "headache", "fever", "diabetes",
        "blood pressure", "prescription", "health", "medical",
        "disease", "treatment", "dose", "diagnosis", "clinic",
    )

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        if not state["messages"]:
            return None

        human_messages = []
        for m in state["messages"]:
            msg_type = m.get("type") if isinstance(m, dict) else getattr(m, "type", None)
            if msg_type in ("human", "user"):
                human_messages.append(m)

        if not human_messages:
            return None

        last_msg = human_messages[-1]
        msg_content = (
            last_msg.get("content")
            if isinstance(last_msg, dict)
            else getattr(last_msg, "content", "")
        )
        content = str(msg_content).lower()

        for topic in self.BLOCKED_TOPICS:
            if topic in content:
                return {
                    "messages": [{
                        "role": "assistant",
                        "content": (
                            "I can't help with harmful instructions. "
                            "I'm designed for healthcare information and "
                            "appointment support. If someone is in immediate "
                            "danger, contact local emergency services."
                        ),
                    }],
                    "jump_to": "end",
                }

        if len(content.split()) >= 3:
            looks_medical = any(term in content for term in self.HEALTHCARE_HINTS)
            if not looks_medical:
                return {
                    "messages": [{
                        "role": "assistant",
                        "content": (
                            "I'm a healthcare assistant. Please ask a "
                            "healthcare, medication, symptom, or appointment "
                            "related question."
                        ),
                    }],
                    "jump_to": "end",
                }

        return None


class MedicalOutputValidator(AgentMiddleware):
    """Ensure final AI responses contain a general medical disclaimer."""

    DISCLAIMER = (
        "\n\nThis is general health information, not medical advice. "
        "Please consult a qualified healthcare professional."
    )

    NON_DISCLAIMER_SIGNALS = (
        "can't help with harmful",
        "healthcare assistant. please ask",
        "has been cancelled",
        "request has been cancelled",
        "cancelled and will not be",
    )

    @hook_config(can_jump_to=["end"])
    def after_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        if not state["messages"]:
            return None

        last_message = state["messages"][-1]
        content = (
            last_message.content
            if isinstance(last_message, AIMessage)
            else last_message.get("content", "")
            if isinstance(last_message, dict)
            else ""
        )
        content_str = str(content)

        if any(signal in content_str.lower() for signal in self.NON_DISCLAIMER_SIGNALS):
            return None

        if "not medical advice" not in content_str.lower():
            if isinstance(last_message, AIMessage):
                last_message.content = content_str + self.DISCLAIMER
            elif isinstance(last_message, dict):
                last_message["content"] = content_str + self.DISCLAIMER

        return None
