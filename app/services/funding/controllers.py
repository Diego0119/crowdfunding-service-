from litestar import post, get, Router, Controller
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.funding.dtos import ProjectCreate, ProjectOut
from app.services.funding.repositories import ProjectRepository
from app.services.accounts.repositories import UserRepository
from sqlalchemy.orm import Session

class ProjectController(Controller):
    path = "/"  

    @post("/create")
    def create_project(self, data: ProjectCreate, db: Session) -> dict:
        project_repo = ProjectRepository(db)

        creator_id = 1  

        project = project_repo.create_project(data.dict(), creator_id)

        return {"detail": "Project created successfully", "project_id": project.id}, 200

    @get("/")
    async def get_projects(self, db: AsyncSession) -> None:
        project_repo = ProjectRepository(db)
        projects = project_repo.get_projects()
        
        return [ProjectOut.from_orm(project) for project in projects]

funding_router = Router(
    route_handlers=[ProjectController],
    path="/projects", 
)
