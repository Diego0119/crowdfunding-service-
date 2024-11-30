from litestar import post, get, Router, Controller
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.funding.dtos import ProjectCreate, ProjectOut
from app.services.funding.repositories import ProjectRepository
from app.services.accounts.repositories import UserRepository

class ProjectController(Controller):
    path = "/projects"  

    @post("/")
    async def create_project(self, project_data: ProjectCreate, db: AsyncSession) -> None:
        project_repo = ProjectRepository(db)
        user_repo = UserRepository(db)
        
        creator = user_repo.get_user_by_id(project_data.creator_id)
        if not creator:
            return {"detail": "Creator not found"}, 404 
        
        project_dict = project_data.dict(exclude={"creator_id"})
        new_project = project_repo.create_project(project_dict, project_data.creator_id)
        
        return ProjectOut.from_orm(new_project)

    @get("/")
    async def get_projects(self, db: AsyncSession) -> None:
        project_repo = ProjectRepository(db)
        projects = project_repo.get_projects()
        
        return [ProjectOut.from_orm(project) for project in projects]

funding_router = Router(
    route_handlers=[ProjectController],
    path="/projects", 
)
