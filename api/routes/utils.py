from fastapi import APIRouter, Depends # type: ignore
from pydantic.networks import EmailStr # type: ignore

from app.api.deps import get_current_active_superuser # type: ignore
from app.models import Message # type: ignore
from app.utils import generate_test_email, send_email # type: ignore

router = APIRouter()

@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")

@router.get("/health-check/")
async def health_check() -> bool:
    return True
