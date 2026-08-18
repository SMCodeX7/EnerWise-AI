from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentUpdate,
)
from app.schemas.auth import CurrentUser
from app.services.assessments import (
    create_assessment,
    delete_assessment,
    get_user_assessment,
    list_user_assessments,
    update_assessment,
)


router = APIRouter(prefix="/assessments")


@router.post(
    "",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_assessment(
    payload: AssessmentCreate,
    current_user: Annotated[
        CurrentUser,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> AssessmentResponse:
    return create_assessment(
        db=db,
        user_id=current_user.id,
        payload=payload,
    )


@router.get(
    "",
    response_model=list[AssessmentResponse],
)
def read_user_assessments(
    current_user: Annotated[
        CurrentUser,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> list[AssessmentResponse]:
    return list_user_assessments(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
)
def read_user_assessment(
    assessment_id: UUID,
    current_user: Annotated[
        CurrentUser,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> AssessmentResponse:
    assessment = get_user_assessment(
        db=db,
        user_id=current_user.id,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    return assessment


@router.patch(
    "/{assessment_id}",
    response_model=AssessmentResponse,
)
def update_user_assessment(
    assessment_id: UUID,
    payload: AssessmentUpdate,
    current_user: Annotated[
        CurrentUser,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> AssessmentResponse:
    assessment = get_user_assessment(
        db=db,
        user_id=current_user.id,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    return update_assessment(
        db=db,
        assessment=assessment,
        payload=payload,
    )


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_assessment(
    assessment_id: UUID,
    current_user: Annotated[
        CurrentUser,
        Depends(get_current_user),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ],
) -> Response:
    assessment = get_user_assessment(
        db=db,
        user_id=current_user.id,
        assessment_id=assessment_id,
    )

    if assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    delete_assessment(
        db=db,
        assessment=assessment,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)