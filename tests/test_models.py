import pytest
from app import db
from app.models import GeneratedText


def test_user_password_hashing(client, user_with_generated_text):
    """Ensure password is hashed and validation works"""

    valid_user, _ = user_with_generated_text

    db.session.add(valid_user)
    db.session.commit()

    assert valid_user.hash_password != "testpassword"  # Should be hashed
    assert valid_user.check_password("testpassword") is True
    assert valid_user.check_password("wrongpassword") is False


    # Assert that accessing password raises AttributeError
    with pytest.raises(AttributeError, match="password is not a readable attribute"):
        _ = valid_user.password


def test_generated_text_model(client, user_with_generated_text):
    """Ensure a GeneratedText object can be created"""
    
    valid_user, gen_text = user_with_generated_text

    retrieved_text = GeneratedText.query.first()
    assert retrieved_text is not None
    assert retrieved_text.prompt == "Test Prompt"
    assert retrieved_text.response == "Generated response"
    assert retrieved_text.user_id == valid_user.id
