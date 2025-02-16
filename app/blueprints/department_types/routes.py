from flask import Blueprint, request
from app.extensions.db import db
from app.models.DepartmentType import DepartmentType
from app.extensions.responses import success_response, error_response
from app.extensions.require_api_key import require_api_key
from app.extensions.require_access_token import require_access_token

department_types_bp = Blueprint("departments", __name__, url_prefix="/departments")


# ✅ Create a new department type
@department_types_bp.route("", methods=["POST"])
@require_api_key
@require_access_token
def create_department_type():
    try:
        data = request.json

        required_fields = ["type_name", "bedrooms", "bathrooms"]
        if not all(field in data for field in required_fields):
            return error_response("Missing required fields", 400)

        new_department = DepartmentType(
            type_name=data["type_name"],
            bedrooms=data["bedrooms"],
            bathrooms=data["bathrooms"],
            size_sqm=data.get("size_sqm"),
            base_rent_price=data.get("base_rent_price"),
            description=data.get("description"),
        )

        db.session.add(new_department)
        db.session.commit()

        return success_response(
            message="Department type created successfully", data=new_department.id, status_code=201
        )
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to create department type", 500, [str(e)])


# ✅ Get all department types
@department_types_bp.route("", methods=["GET"])
@require_api_key
@require_access_token
def get_all_department_types():
    try:
        departments = DepartmentType.query.all()
        return success_response(
            data=[{
                "id": dept.id,
                "bedrooms": dept.bedrooms,
                "bathrooms": dept.bathrooms,
                "base_rent_price": float(dept.base_rent_price) if dept.base_rent_price else None,
                "description": dept.description,
                "created_at": dept.created_at.isoformat(),
                "updated_at": dept.updated_at.isoformat(),
            } for dept in departments],
            message="List of department types"
        )
    except Exception as e:
        return error_response("Failed to retrieve department types", 500, [str(e)])


# ✅ Get a single department type by ID
@department_types_bp.route("/<int:id>", methods=["GET"])
@require_api_key
@require_access_token
def get_department_type(id):
    try:
        dept = DepartmentType.query.get(id)
        if not dept:
            return error_response("Department type not found", 404)

        return success_response(
            data={
                "id": dept.id,
                "type_name": dept.type_name,
                "bedrooms": dept.bedrooms,
                "bathrooms": dept.bathrooms,
                "size_sqm": float(dept.size_sqm) if dept.size_sqm else None,
                "base_rent_price": float(dept.base_rent_price) if dept.base_rent_price else None,
                "description": dept.description,
                "created_at": dept.created_at.isoformat(),
                "updated_at": dept.updated_at.isoformat(),
            }
        )
    except Exception as e:
        return error_response("Failed to retrieve department type", 500, [str(e)])


# ✅ Update a department type
@department_types_bp.route("/<int:id>", methods=["PUT"])
@require_api_key
@require_access_token
def update_department_type(id):
    try:
        dept = DepartmentType.query.get(id)
        if not dept:
            return error_response("Department type not found", 404)

        data = request.json
        dept.type_name = data.get("type_name", dept.type_name)
        dept.bedrooms = data.get("bedrooms", dept.bedrooms)
        dept.bathrooms = data.get("bathrooms", dept.bathrooms)
        dept.size_sqm = data.get("size_sqm", dept.size_sqm)
        dept.base_rent_price = data.get("base_rent_price", dept.base_rent_price)
        dept.description = data.get("description", dept.description)

        db.session.commit()

        return success_response(
            message="Department type updated successfully"
        )
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to update department type", 500, [str(e)])


# ✅ Delete a department type
@department_types_bp.route("/<int:id>", methods=["DELETE"])
@require_api_key
@require_access_token
def delete_department_type(id):
    try:
        dept = DepartmentType.query.get(id)
        if not dept:
            return error_response("Department type not found", 404)

        db.session.delete(dept)
        db.session.commit()

        return success_response(
            message="Department type deleted successfully"
        )
    except Exception as e:
        db.session.rollback()
        return error_response("Failed to delete department type", 500, [str(e)])