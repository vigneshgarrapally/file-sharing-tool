from app.models import User
from app import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
