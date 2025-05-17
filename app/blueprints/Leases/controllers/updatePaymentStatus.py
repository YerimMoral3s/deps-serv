from flask import request
from app.extensions.db import db
from app.models.Payment import Payment
from app.extensions.responses import success_response, error_response


def updatePaymentStatus(payment_id, new_status):
  try:
    if not new_status:
      return error_response(message="Missing 'status' in request body", status_code=400)

    valid_statuses = ["pendiente", "pagado", "vencido", "cancelado"]
    if new_status not in valid_statuses:
      return error_response(message="Invalid status value", status_code=400)

    payment = Payment.query.get(payment_id)
    if not payment:
      return error_response(message="Payment not found", status_code=404)

    payment.status = new_status
    db.session.commit()

    return success_response(
      data={"id": payment.id, "status": payment.status},
      message="Payment status updated successfully",
      status_code=200
    )

  except Exception as e:
    db.session.rollback()
    return error_response(message="Internal error", errors=[str(e)], status_code=500)