def validation_creation(name: str, email: str, password: str)-> bool:
    
    is_validate: bool = False
    if name is not None and email is not None and password is not None:
        name = name.strip().lower()
        email = email.strip().lower()
        password = password.strip()
        if name != '' and email != '' and password != '':
            if '@' in email and email.count('@') == 1:
                if len(email[email.index('@'):]) >=2:
                    if password.isalnum():
                        is_validate = True

    return is_validate

def validation_id_user(id: int)-> bool:
    
    is_validate: bool = False
    
    if isinstance(id, (int)):
        if id > 0:
            is_validate = True
    
    return is_validate
