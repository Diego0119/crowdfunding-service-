from litestar import post, get, Controller, Router, Request
from litestar.di import Provide
from sqlalchemy.orm import Session
from app.services.funding.dtos import ProjectCreate, ProjectOut
from app.services.funding.repositories import ProjectRepository, provide_project_repository
from app.services.funding.models import Project
from app.database import sqlalchemy_plugin  
from typing import List


class ProjectController(Controller):
    path = "/"

    dependencies = {"project_repo": Provide(provide_project_repository)}

    @post("/create")
    async def create_project(self, project_repo: ProjectRepository, data: ProjectCreate, request: Request) -> dict:
        creator_id = 1 
        project_data = data.dict()
        project = project_repo.create_project(project_data, creator_id)
        return {"detail": "Project created successfully", "project_id": project.id}, 200

    @get("/")
    async def get_projects(self, project_repo: ProjectRepository) -> List[ProjectOut]:
        projects = project_repo.get_projects()
        return [ProjectOut.from_orm(project) for project in projects]


funding_router = Router(route_handlers=[ProjectController], path="/projects")
