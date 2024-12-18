from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.services.accounts.models import User
from app.services.accounts.dtos import UserCreateDTO, UserUpdateDTO
from sqlalchemy.orm import sessionmaker
from typing import Optional

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: UserCreateDTO) -> User:
        user = User(**user_data.dict())
        self.session.add(user)
        try:
            self.session.commit()
            self.session.refresh(user)
        except IntegrityError:
            raise ValueError("Username or Email already exists")
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).filter_by(id=user_id))
        return result.scalar_one_or_none()


    async def update_user(self, user_id: int, user_data: UserUpdateDTO) -> User:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        await self.session.delete(user)
        await self.session.commit()


    async def username_or_email_exists(self, username: str, email: str) -> bool:
        result = self.session.execute(
            select(User).filter_by(username=username, email=email)
        )
        return result.scalar_one_or_none() is not None
