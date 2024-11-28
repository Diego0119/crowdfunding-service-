from litestar import post, get, put, delete
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from dtos import UserCreate, UserUpdate, UserOut
from repositories import UserRepository  

class UserController:
    def __init__(self, session_provider: Provide[AsyncSession]):
        self.session_provider = session_provider

    @post("/users", response_model=UserOut)
    async def create_user(self, request, data: UserCreate):
        async with self.session_provider() as session:
            user_repo = UserRepository(session)
            try:
                user = await user_repo.create_user(data)
                return user
            except ValueError:
                # raise HTTPException(status_code=400, detail="Username or Email already exists")
                return

    @get("/users/{user_id}", response_model=UserOut)
    async def get_user(self, request, user_id: int):
        async with self.session_provider() as session:
            user_repo = UserRepository(session)
            user = await user_repo.get_user_by_id(user_id)
            if not user:
                # raise HTTPException(status_code=404, detail="User not found")
                return
            return user

    @put("/users/{user_id}", response_model=UserOut)
    async def update_user(self, request, user_id: int, data: UserUpdate):
        async with self.session_provider() as session:
            user_repo = UserRepository(session)
            try:
                user = await user_repo.update_user(user_id, data)
                return user
            except ValueError:
                # raise HTTPException(status_code=404, detail="User not found")
                return

    @delete("/users/{user_id}", response_description="User deleted successfully")
    async def delete_user(self, request, user_id: int):
        async with self.session_provider() as session:
            user_repo = UserRepository(session)
            try:
                await user_repo.delete_user(user_id)
                return {"message": "User deleted successfully"}
            except ValueError:
                # raise HTTPException(status_code=404, detail="User not found")
                return
