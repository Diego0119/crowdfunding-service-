from litestar import post, get, put, delete, Router, Response
from app.services.accounts.dtos import UserCreateDTO, UserUpdateDTO, UserDTO
from app.services.accounts.repositories import UserRepository, provide_user_repository
from litestar import Controller
from litestar.di import Provide
from typing import Any, Dict

class UserController(Controller):
    path = "/"

    dependencies = {"user_repo": Provide(provide_user_repository)}

    # @get("/{user_id:int}", response_model=UserDTO)
    # async def get_user(self, user_id: int, user_repo: UserRepository) -> Any:
    #     user = user_repo.get_user_by_id(user_id)
    #     if not user:
    #         return Response({"detail": "User not found"}, status_code=404)
    #     return UserDTO.from_orm(user)

    # @put("/{user_id:int}", response_model=UserDTO)
    # async def update_user(self, user_id: int, data: UserUpdateDTO, user_repo: UserRepository) -> Any:
    #     user = user_repo.update_user(user_id, data)
    #     if not user:
    #         return Response({"detail": "User not found or could not be updated"}, status_code=404)
    #     return UserDTO.from_orm(user)

    # @delete("/{user_id:int}", status_code=204)
    # async def delete_user(self, user_id: int, user_repo: UserRepository) -> Response:
    #     success = user_repo.delete_user(user_id)
    #     if not success:
    #         return Response({"detail": "User not found or could not be deleted"}, status_code=404)
    #     # 204 No Content: No devuelve un cuerpo
    #     return Response(status_code=204)

accounts_router = Router(route_handlers=[UserController], path="/users")
