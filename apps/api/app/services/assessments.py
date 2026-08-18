from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate


def create_assessment(
    db: Session,
    user_id: UUID,
    payload: AssessmentCreate,
) -> Assessment:
    assessment = Assessment(
        user_id=user_id,
        title=payload.title,
        input_text=payload.input_text,
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


def list_user_assessments(
    db: Session,
    user_id: UUID,
) -> list[Assessment]:
    statement = (
        select(Assessment)
        .where(Assessment.user_id == user_id)
        .order_by(Assessment.created_at.desc())
    )

    return list(db.scalars(statement).all())


def get_user_assessment(
    db: Session,
    user_id: UUID,
    assessment_id: UUID,
) -> Assessment | None:
    statement = select(Assessment).where(
        Assessment.id == assessment_id,
        Assessment.user_id == user_id,
    )

    return db.scalars(statement).first()


def update_assessment(
    db: Session,
    assessment: Assessment,
    payload: AssessmentUpdate,
) -> Assessment:
    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if field == "input_text" and value is None:
            continue

        setattr(assessment, field, value)

    db.commit()
    db.refresh(assessment)

    return assessment


def delete_assessment(
    db: Session,
    assessment: Assessment,
) -> None:
    db.delete(assessment)
    db.commit()