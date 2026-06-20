def validation_limit_offset(limit: int, offset: int) -> bool:
    is_valid: bool = False
    if isinstance(limit, int) and isinstance(offset, int):
        if 0 <= limit <= 10 and offset >= 0:
            is_valid = True
    return is_valid

def validation_create_review(reservation_id, description: str, stars) -> bool:
    is_valid: bool = False
    if reservation_id is not None and description is not None and stars is not None:
        if isinstance(description, str) and description.strip() != '':
            if 1 <= int(stars) <= 5:
                is_valid = True
    return is_valid

def validation_update_review(description: str, stars) -> bool:
    is_valid: bool = False
    if description is not None and stars is not None:
        if isinstance(description, str) and description.strip() != '':
            if 1 <= int(stars) <= 5:
                is_valid = True
    return is_valid
