from sqlalchemy.orm import Session
from app.services.funding.models import Project, Contribution, Evaluation
from app.services.accounts.models import User
from sqlalchemy.exc import IntegrityError
from advanced_alchemy.repository import SQLAlchemySyncRepository
from datetime import datetime, timezone
from typing import Any, Dict
from typing import Optional

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
    
    def get_project_by_id(self, project_id: int) -> Optional[Project]:
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

    def contribute_to_project(self, project_id: int, amount: float, payment_method: str):
        project = self.db_session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found.")

        contribution = Contribution(
        project_id=project_id,
        user_id=1, 
        amount=amount,
        contributed_at=datetime.utcnow(),
        payment_method=payment_method,
        )
        
        project.current_amount += amount
        self.check_and_start_project(project)
        self.db_session.add(project)
        self.db_session.add(contribution)
        self.db_session.add(contribution)
        self.db_session.commit()

        return contribution


    def cancel_proyects(self):
        """Marca proyectos como cancelados si no alcanzaron el objetivo después de la fecha límite."""
        now = datetime.now(timezone.utc)
        projects_to_cancel = self.db_session.query(Project).filter(
            Project.status == "active",
            Project.end_date < now,
            Project.current_amount < Project.goal_amount
        ).all()

        for project in projects_to_cancel:
            project.status = "cancelled"

        self.db_session.commit()
    
    def check_and_start_project(self, project: Project) -> None:
        if project.current_amount >= project.goal_amount and project.status == "active":
            project.status = "completed"
            self.db_session.add(project)
            self.db_session.commit()
            self.db_session.refresh(project)    

    def add_evaluation(self, user_id: int, project_id: int, rating: int, comment: Optional[str]) -> Evaluation:
        """Permite a un usuario calificar un proyecto."""
        project = self.db_session.query(Project).filter(Project.id == project_id).first()

        if not project or project.status != "finalized":
            raise ValueError("Project not found.")

        #verifica q el usuario haya contribuido al proyecto
        contribution = self.db_session.query(Contribution).filter(Contribution.project_id == project_id, Contribution.user_id == user_id).first()
        if not contribution:
            raise ValueError("User not contribute to this project.")

        evaluation = Evaluation(
            project_id=project_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
            created_at=datetime.now(timezone.utc)
        )

        self.db_session.add(evaluation)
        self.db_session.commit()
        self.db_session.refresh(evaluation)
        return evaluation

    def get_evaluations(self, project_id: int):
        return self.db_session.query(Evaluation).filter(Evaluation.project_id == project_id).all()

    def finalize_project(self, project_id: int):
        project = self.db_session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found.")
        
        if project.status != "completed":
            raise ValueError("Only completed projects can be finalized.")
        
        project.status = "finalized"
        self.db_session.add(project)
        self.db_session.commit()
        self.db_session.refresh(project)
        
        return project

    def delete_project(self, project_id: int) -> None:
        project = self.db_session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found.")
        if project.status != "finalized":
            raise ValueError("Only finalized projects can be eliminated.")
        
        project = self.db_session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError("Project not found.")
        self.db_session.query(Contribution).filter(Contribution.project_id == project_id).delete()
        self.db_session.query(Evaluation).filter(Evaluation.project_id == project_id).delete()
        self.db_session.delete(project)
        self.db_session.commit()

async def provide_project_repository(db_session: Session) -> ProjectRepository:
    return ProjectRepository(db_session=db_session)
