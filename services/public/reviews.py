def validation_create_review(user_id: int, reservation_id: int, description: str, stars: int) -> bool:
    is_valid: bool = False
    if user_id is not None and reservation_id is not None and description is not None and stars is not None:
        if isinstance(description, str) and description.strip() != '':
            if isinstance(stars, int) and 1 <= stars <= 5:
                is_valid = True
    return is_valid

def validation_update_review(description: str, stars: int) -> bool:
    is_valid: bool = False
    if description is not None and stars is not None:
        if isinstance(description, str) and description.strip() != '':
            if isinstance(stars, int) and 1 <= stars <= 5:
                is_valid = True
    return is_valid
