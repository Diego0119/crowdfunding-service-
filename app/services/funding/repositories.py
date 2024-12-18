from sqlalchemy.orm import Session
from app.services.funding.models import Project, Contribution
from app.services.accounts.models import User
from sqlalchemy.exc import IntegrityError
from advanced_alchemy.repository import SQLAlchemySyncRepository
from datetime import datetime
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

    def contribute_to_project(self, user_id: int, project_id: int, amount: float, payment_method: str) -> Contribution:
        """Permite a un usuario contribuir a un proyecto."""
        user = self.db_session.query(User).filter(User.id == user_id).first()
        project = self.db_session.query(Project).filter(Project.id == project_id).first()
        
        if not user or not project:
            raise ValueError("Usuer or project not found.")
        
        if user.money is None or user.money < amount:
            raise ValueError("Insufficient money in the users account.")
        
        new_balance = user.money - amount
        user.money = new_balance
        project.current_amount = project.current_amount + amount
        project.contributions_count = project.contributions_count + 1

        contribution = Contribution(
            user_id=user_id,
            project_id=project_id,
            amount=amount,
            payment_method=payment_method,
            contributed_at=datetime.utcnow()
        )
        
        self.db_session.add(contribution)
        self.db_session.commit()
        self.db_session.refresh(project)
        self.db_session.refresh(user)
        return contribution

async def provide_project_repository(db_session: Session) -> ProjectRepository:
    return ProjectRepository(db_session=db_session)
