from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.services.accounts.models import User
from app.services.accounts.dtos import UserCreateDTO, UserUpdateDTO
from advanced_alchemy.repository import SQLAlchemySyncRepository

class UserRepository(SQLAlchemySyncRepository[User]):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, user_data: UserCreateDTO) -> User:
        user = User(**user_data.dict())
        self.db_session.add(user)
        try:
            self.db_session.commit()
            self.db_session.refresh(user)
        except IntegrityError:
            raise ValueError("Username or Email already exists")
        return user

    async def get_user_by_id(self, user_id: int) -> User:
        result = self.db_session.execute(select(User).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        return user

    async def update_user(self, user_id: int, user_data: UserUpdateDTO) -> User:
        user = åself.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)

        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        self.db_session.delete(user)
        self.db_session.commit()

    async def username_or_email_exists(self, username: str, email: str) -> bool:
        result = self.db_session.execute(
            select(User).filter_by(username=username, email=email)
        )
        return result.scalar_one_or_none() is not None

    async def get_user_profile(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id) 
        return UserDTO.from_model(user)



def provide_user_repository(db_session: Session) -> UserRepository:
    return UserRepository(db_session=db_session)
