import pytest
from unittest.mock import patch
# from your_app.openai_service import generate_openai_response
from app.models import GeneratedText


def test_create_generated_text(client, auth_header, new_generated_text):
    # Mocking OpenAI API response
    
    with patch('app.resources.main.generate_openai_response', return_value="Generated response"):
        response = client.post('/api/generated-text', json=new_generated_text, headers=auth_header)
        
        assert response.status_code == 201
        assert response.json['prompt'] == new_generated_text['prompt']
        assert response.json['response'] == "Generated response"

        db_text = GeneratedText.query.get(response.json['id'])
        assert db_text.prompt == new_generated_text['prompt']
        assert db_text.response == "Generated response"
        "assert table count"
        assert GeneratedText.query.count() == 1



def test_get_generated_text(client, auth_header, user_with_generated_text):
    
    user, generated_text = user_with_generated_text
    response = client.get(f'/api/generated-text/{generated_text.id}', headers=auth_header)
    
    assert response.status_code == 200
    assert response.json['id'] == generated_text.id
    assert response.json['response'] == "Generated response"


def test_update_generated_text(client, auth_header, user_with_generated_text):
    with patch('app.resources.main.generate_openai_response', return_value="Generated response update"):
        user, generated_text = user_with_generated_text
        updated_text = {'prompt': 'Updated promt'}
        response = client.put(f'/api/generated-text/{generated_text.id}', json=updated_text, headers=auth_header)
        
        assert response.status_code == 200
        assert response.json['response'] == 'Generated response update'
        assert response.json['prompt'] == updated_text['prompt']
        assert response.json['id'] == generated_text.id
        

        db_text_updated = GeneratedText.query.get(generated_text.id)
        assert db_text_updated.prompt == updated_text['prompt']
        assert db_text_updated.response == 'Generated response update'



def test_delete_generated_text(client, auth_header, user_with_generated_text):
    user, generated_text = user_with_generated_text
    response = client.delete(f'/api/generated-text/{generated_text.id}', headers=auth_header)

    print("response.status_code for test_delete_generated_text: ", response.status_code)
    
    print(response.status_code)
    assert response.status_code == 204
    deleted_text = GeneratedText.query.get(generated_text.id)
    assert deleted_text is None


def test_resource_acccess_by_non_owner(client, user_with_generated_text, user_without_generated_text, auth_header_2):
    _, generated_text = user_with_generated_text
    user, _ = user_without_generated_text
    
    #"Test authorised deletion"
    response = client.delete(f'/api/generated-text/{generated_text.id}', headers=auth_header_2)
    assert response.status_code == 404
    deleted_text = GeneratedText.query.get(generated_text.id)
    assert deleted_text is not None
    
    # test unauthorised mutations
    updated_text = {'prompt': 'Updated promt'}
    response = client.put(f'/api/generated-text/{generated_text.id}',
                          json=updated_text, headers=auth_header_2)
        
    print(response.json)
    assert response.status_code == 404
    

    db_text_updated = GeneratedText.query.get(generated_text.id)
    assert db_text_updated.prompt != updated_text['prompt']
    assert db_text_updated.response != 'Generated response update'


