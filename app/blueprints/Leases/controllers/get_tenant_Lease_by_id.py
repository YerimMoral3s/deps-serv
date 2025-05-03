from app.models.Lease import Lease
from app.extensions.db import db
from app.extensions.responses import success_response, error_response
from sqlalchemy.exc import SQLAlchemyError
from app.models.Department import Department


def get_tenant_Lease_by_id(tenant_id):
  try:
    lease = (
      db.session.query(Lease)
      .filter(Lease.tenant_id == tenant_id)
      .first()
    )

    if not lease:
      return error_response(message="lease not found", status_code=404)

    lease_data = {
      "id": lease.id,
      "type": lease.type,
      "start_date": lease.start_date.isoformat() if lease.start_date else None,
      "end_date": lease.end_date.isoformat(),
      "payment_day": lease.payment_day,
      "monthly_rent": float(lease.monthly_rent),
      "upfront_payment": float(lease.upfront_payment),
      "status": lease.status,
    }

    return success_response(data=lease_data, message="Lease fetched successfully")
  
  except Exception as e:
    return error_response(message="Error fetching lease", errors=[str(e)], status_code=500)