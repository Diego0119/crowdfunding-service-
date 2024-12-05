from sqlalchemy.orm import Session
from app.services.funding.models import Project
from sqlalchemy.exc import IntegrityError
from advanced_alchemy.repository import SQLAlchemySyncRepository
from datetime import datetime
from typing import Any, Dict

class ProjectRepository(SQLAlchemySyncRepository[Project]):
    
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _convert_dates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convierte cadenas de fechas a objetos datetime si es necesario."""
        date_fields = ['start_date', 'end_date']
        for field in date_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = datetime.fromisoformat(data[field].replace("Z", "+00:00"))
                except ValueError:
                    raise ValueError(f"Invalid date format for field '{field}': {data[field]}")
        return data

    def create_project(self, project_data: dict, creator_id: int) -> Project:
        """Crea un proyecto con los datos proporcionados."""
        project_data = self._convert_dates(project_data)
        new_project = Project(**project_data, creator_id=creator_id)
        self.db_session.add(new_project)
        try:
            self.db_session.commit()
            self.db_session.refresh(new_project)
            return new_project
        except IntegrityError as e:
            self.db_session.rollback()
            raise Exception(f"Error creating project: {str(e)}")
    
    def get_projects(self):
        """Obtiene todos los proyectos."""
        return self.db_session.query(Project).all()
    
    def get_project_by_id(self, project_id: int) -> Project:
        """Obtiene un proyecto por su ID."""
        return self.db_session.query(Project).filter(Project.id == project_id).first()
    
    def update_project(self, project: Project, updated_data: dict) -> Project:
        """Actualiza un proyecto con nuevos datos."""
        updated_data = self._convert_dates(updated_data)
        for key, value in updated_data.items():
            setattr(project, key, value)
        self.db_session.add(project)
        self.db_session.commit()
        self.db_session.refresh(project)
        return project


async def provide_project_repository(db_session: Session) -> ProjectRepository:
    return ProjectRepository(db_session=db_session)
