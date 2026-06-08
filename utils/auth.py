from flask_jwt_extended import get_jwt_identity
from database.public.users import db_get_user

def get_current_user() -> dict:
    user_id = int(get_jwt_identity())
    return db_get_user(id=user_id)

def is_admin() -> bool:
    user = get_current_user()
    return user["category"] in ("admin", "root")
