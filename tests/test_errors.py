
import pytest
from app.models import GeneratedText, User

def test_unauthenticated_resources_creation(client, invalid_auth_header, new_generated_text):

    
    # attempt resousrce creation
    response = client.post('/api/generated-text', json=new_generated_text,
                           headers=invalid_auth_header)
    assert response.status_code == 401
    assert GeneratedText.query.count() == 0

    
def test_unauthenticated_resources_mutation(client, invalid_auth_header, new_generated_text, user_with_generated_text):

    _, generated_text = user_with_generated_text
    
    #"Attempt Resource deletion"
    response = client.delete(f'/api/generated-text/{generated_text.id}', headers=invalid_auth_header)
    
    print(response.json)
    assert response.status_code == 401
    assert GeneratedText.query.count() == 1
    deleted_text = GeneratedText.query.get(generated_text.id)
    assert deleted_text is not None
    
    # test unauthorised mutations
    updated_text = {'prompt': 'Updated promt'}
    response = client.put(f'/api/generated-text/{generated_text.id}',
                          json=updated_text, headers=invalid_auth_header)
        
        
    assert response.status_code == 401

    db_text_updated = GeneratedText.query.get(generated_text.id)
    assert db_text_updated.prompt != updated_text['prompt']
    assert db_text_updated.response != 'Generated response update'




    



