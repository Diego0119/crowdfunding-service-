from litestar import post, get, Controller, Router, Request
from litestar.di import Provide
from litestar.response import Response
from sqlalchemy.orm import Session
from typing import Union
from app.services.funding.dtos import ProjectCreate, ProjectOut, ContributionBase
from app.services.funding.repositories import ProjectRepository, provide_project_repository
from app.services.funding.models import Project
from app.database import sqlalchemy_plugin  
from typing import List


class ProjectController(Controller):
    path = "/"

    dependencies = {"project_repo": Provide(provide_project_repository)}

    @post("/create")
    async def create_project(self, project_repo: ProjectRepository, data: ProjectCreate, request: Request) -> Response:
        creator_id = 1 
        project_data = data.dict()
        project = project_repo.create_project(project_data, creator_id)
        return Response(content={"detail": "Project created successfully", "project_id": project.id},status_code=200)

    @get("/")
    async def get_projects(self, project_repo: ProjectRepository) -> List[ProjectOut]:
        projects = project_repo.get_projects()
        return [ProjectOut.from_orm(project) for project in projects]

    @get("/{project_id:int}")
    async def get_project(self, project_id: int, project_repo: ProjectRepository) -> Union[ProjectOut, Response]:
        project = project_repo.get_project_by_id(project_id)
        if not project:
            return Response({"detail": "Project not found"}, status_code=404)
        
        return ProjectOut.from_orm(project)

    @post("/{project_id:int}/contribute")
    async def contribute_to_project(self, project_repo: ProjectRepository, project_id: int, request: Request, data: ContributionBase):
        user_id = request.user.id
        contribution = project_repo.contribute_to_project(user_id, project_id, data.amount, data.payment_method)
        return {"detail": "Contribución exitosa", "amount": contribution.amount, "project_id": project_id}

funding_router = Router(route_handlers=[ProjectController], path="/projects")
