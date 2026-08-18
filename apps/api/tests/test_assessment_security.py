from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas.assessment import AssessmentCreate


def test_valid_assessment_request_is_allowed() -> None:
    assessment = AssessmentCreate(
        title="Solar Assessment",
        input_text="I want to assess rooftop solar for my house.",
    )

    assert assessment.title == "Solar Assessment"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("user_id", str(uuid4())),
        ("status", "COMPLETED"),
        ("energy_profile", {"system_size": 10}),
    ],
)
def test_server_controlled_fields_are_rejected(
    field: str,
    value: object,
) -> None:
    payload = {
        "title": "Solar Assessment",
        "input_text": "I want to assess rooftop solar.",
        field: value,
    }

    with pytest.raises(ValidationError):
        AssessmentCreate(**payload)


def test_empty_input_text_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AssessmentCreate(
            title="Solar Assessment",
            input_text="   ",
        )