from app.extensions.db import db
from app.extensions.responses import success_response, error_response
from app.models.Lease import Lease
from app.models.Payment import Payment


def get_payments_tenant_id(tenant_id):
  try:
    leases = Lease.query.filter_by(tenant_id=tenant_id).all()

    if not leases:
        return error_response(message="No leases found for tenant")

    lease_ids = [lease.id for lease in leases]
    print(lease_ids)

    payments = (
        Payment.query.filter(Payment.lease_id.in_(lease_ids))
        .order_by(Payment.due_date.asc())
        .all()
    )

    payments_data = [
        {
            "id": payment.id,
            "amount": payment.amount,
            "payment_day": payment.payment_date,
            "lease_id": payment.lease_id,
            "status": payment.status,
            "payment_method": payment.payment_method,
            "due_date": payment.due_date,
            "type": payment.type,
        }
        for payment in payments
    ]

    return success_response(
        data=payments_data,
        message="Payments retrieved successfully",
        status_code=200
    )
  except Exception as e:
    print(str(e))
    return error_response(message="Error fetching tenant", errors=[str(e)], status_code=500)