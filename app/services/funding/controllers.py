from litestar import post, get, Router, Controller
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.funding.dtos import ProjectCreate, ProjectOut
from app.services.funding.repositories import ProjectRepository
from app.services.accounts.repositories import UserRepository

class ProjectController(Controller):
    path = "/"  

    @post("/create")
    async def create_project(self) -> dict:
        # aca debe ir la logica
        return {"detail": "OK"}, 200
    

    @get("/")
    async def get_projects(self, db: AsyncSession) -> None:
        project_repo = ProjectRepository(db)
        projects = project_repo.get_projects()
        
        return [ProjectOut.from_orm(project) for project in projects]

funding_router = Router(
    route_handlers=[ProjectController],
    path="/projects", 
)
