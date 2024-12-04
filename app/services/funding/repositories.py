from sqlalchemy.orm import Session
from app.services.funding.models import Project
from sqlalchemy.exc import IntegrityError
from advanced_alchemy.repository import SQLAlchemySyncRepository

class ProjectRepository(SQLAlchemySyncRepository[Project]):
    
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_project(self, project_data: dict, creator_id: int) -> Project:
        """Crea un proyecto con los datos proporcionados."""
        new_project = Project(**project_data, creator_id=creator_id)
        self.db_session.add(new_project)
        try:
            self.db_session.commit()
            self.db_session.refresh(new_project)
            return new_project
        except IntegrityError:
            self.db_session.rollback()
            raise Exception("Error creating project")
    
    def get_projects(self):
        """Obtiene todos los proyectos."""
        result = self.db_session.query(Project).all()
        return result
    
    def get_project_by_id(self, project_id: int) -> Project:
        """Obtiene un proyecto por su ID."""
        result = self.db_session.query(Project).filter(Project.id == project_id).first()
        return result
    
    def update_project(self, project: Project, updated_data: dict) -> Project:
        """Actualiza un proyecto con nuevos datos."""
        for key, value in updated_data.items():
            setattr(project, key, value)
        self.db_session.add(project)
        self.db_session.commit()
        self.db_session.refresh(project)
        return project


async def provide_project_repository(db_session: Session) -> ProjectRepository:
        return ProjectRepository(session=db_session)

