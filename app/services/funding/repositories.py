from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.project import Project
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

class ProjectRepository:
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_project(self, project_data: dict, creator_id: int) -> Project:
        new_project = Project(**project_data, creator_id=creator_id)
        self.db_session.add(new_project)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(new_project)
            return new_project
        except IntegrityError:
            await self.db_session.rollback()
            raise Exception("Error creating project")
    
    async def get_projects(self):
        result = await self.db_session.execute(select(Project))
        return result.scalars().all()
    
    async def get_project_by_id(self, project_id: int) -> Project:
        result = await self.db_session.execute(select(Project).filter(Project.id == project_id))
        return result.scalar_one_or_none()
    
    async def update_project(self, project: Project, updated_data: dict) -> Project:
        for key, value in updated_data.items():
            setattr(project, key, value)
        self.db_session.add(project)
        await self.db_session.commit()
        await self.db_session.refresh(project)
        return project
