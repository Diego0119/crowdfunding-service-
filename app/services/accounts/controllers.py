from litestar import post, get, put, delete, Router
from app.services.accounts.dtos import UserCreateDTO, UserUpdateDTO, UserDTO
from app.services.accounts.repositories import UserRepository
from litestar import Controller
from typing import Any

class UserController(Controller):
    path = "/users"  

    @get("/{user_id:int}", response_model=UserDTO)
    async def get_user(self, request: Any, user_id: int) -> None:
            async with self.session_provider() as session:
                user_repo = UserRepository(session)
                user = user_repo.get_user_by_id(user_id)
                if not user:
                    return
                return user

    @put("/{user_id:int}", response_model=UserDTO)
    async def update_user(self, request: Any, user_id: int, data: UserUpdateDTO) -> None:
            async with self.session_provider() as session:
                user_repo = UserRepository(session)
                try:
                    user = user_repo.update_user(user_id, data)
                    return user
                except ValueError:
                    return

    @delete("/{user_id:int}", response_description="User deleted successfully")
    async def delete_user(self, request: Any, user_id: int) -> None:
            async with self.session_provider() as session:
                user_repo = UserRepository(session)
                try:
                    user_repo.delete_user(user_id)
                    return {"message": "User deleted successfully"}
                except ValueError:
                    return

accounts_router = Router(
    route_handlers=[UserController], 
    path="/accounts",
)