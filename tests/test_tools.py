from app.tools import book_appointment, get_medication_info, search_symptoms


def test_symptom_tool():
    result = search_symptoms.invoke({"symptoms": "headache"})
    assert "headache" in result.lower()


def test_medication_tool():
    result = get_medication_info.invoke({"medication": "paracetamol"})
    assert "paracetamol" in result.lower()


def test_booking_tool_is_mocked():
    result = book_appointment.invoke({
        "patient_name": "Demo Patient",
        "date": "2026-10-15",
        "doctor": "Sharma",
    })
    assert "simulated booking" in result.lower()
