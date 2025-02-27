from flask import request
from app.models.Department import Department
from app.extensions.responses import success_response, error_response

def get_departments(building_id, page, per_page):
    try:
      pagination = Department.query.filter_by(building_id=building_id).paginate(page=page, per_page=per_page, error_out=False)
      departments = [dept.to_dict() for dept in pagination.items]
      pagination_data = {
          "page": page,
          "per_page": per_page,
          "total_pages": pagination.pages,
          "total_items": pagination.total,
          "has_next": pagination.has_next
      }

      return success_response(data={"departments": departments, "pagination": pagination_data}, message="Departments retrieved successfully", status_code=200)

    except Exception as e:
        return error_response(message="Failed to fetch departments", errors=[str(e)])
