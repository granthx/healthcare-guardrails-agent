def test_project_imports():
    from app.agent import healthcare_bot
    assert healthcare_bot is not None
