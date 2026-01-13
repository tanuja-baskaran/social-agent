def mock_lead_capture(name: str, email: str, platform: str):
    print(f"Lead captured successfully: {name}, {email}, {platform}")
    return {"status": "ok", "name": name, "email": email, "platform": platform}
