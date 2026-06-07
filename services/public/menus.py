def validation_limit_offset(limit: int, offset: int):
    is_validate: bool = False
    if limit <= 10 and limit >= 0 and offset >= 0:
        is_validate = True

    return is_validate
            