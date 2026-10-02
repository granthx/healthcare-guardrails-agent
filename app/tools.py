from langchain_core.tools import tool


@tool
def search_symptoms(symptoms: str) -> str:
    """Return general educational information about supplied symptoms."""
    return (
        f"Educational symptom information for: {symptoms}. "
        "Possible causes vary widely. This tool does not diagnose disease "
        "and a qualified clinician should evaluate concerning symptoms."
    )


@tool
def get_medication_info(medication: str) -> str:
    """Return general educational information about a medication."""
    return (
        f"General medication information for: {medication}. "
        "Follow the prescription or official instructions and ask a "
        "qualified healthcare professional about personal dosing or interactions."
    )


@tool
def book_appointment(patient_name: str, date: str, doctor: str) -> str:
    """Simulate booking a medical appointment.

    This is intentionally a mock side-effecting tool for demonstrating HITL.
    """
    doc_name = doctor if doctor.strip().lower().startswith("dr.") else f"Dr. {doctor}"
    return (
        f"Appointment booked for {patient_name} with {doc_name} on {date}. "
        "This is a simulated booking for the demo."
    )
