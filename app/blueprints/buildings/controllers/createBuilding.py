
from flask import  request
from app.extensions.db import db
from app.models.Building import Building
from app.extensions.responses import success_response, error_response


def create_building(name):
    """
    Creates a new building.
    Expects JSON: { "name": "Building A", "total_units": 10 }
    """
    try:
        print(name)

        if not name:
            return error_response(
                message="Missing required fields",
                errors=["name and total_units are required"],
                status_code=400,
                error_code=3001
            )


        if Building.query.filter_by(name=name).first():
            return error_response(message="El nombre ya existe", status_code=409)

        new_building = Building(name=name, total_units=0)
        db.session.add(new_building)
        db.session.commit()

        return success_response(
            message="Building created successfully",
            data={
                "id": new_building.id,
                "name": new_building.name,
                "total_units": new_building.total_units,
                "created_at": new_building.created_at
            },
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(
            message="Error creating building",
            errors=[str(e)],
            status_code=500,
            error_code=3002
        )