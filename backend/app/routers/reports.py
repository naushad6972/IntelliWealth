from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import User
from app.core.deps import get_current_user
from app.services.report_service import generate_pdf_report, generate_csv_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/download/pdf")
def download_pdf_report(
    report_type: str = "monthly",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pdf_bytes = generate_pdf_report(db, current_user, report_type)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=intelliwealth_{report_type}_report.pdf"}
    )

@router.get("/download/csv")
def download_csv_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    csv_str = generate_csv_report(db, current_user)
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=intelliwealth_transactions.csv"}
    )
