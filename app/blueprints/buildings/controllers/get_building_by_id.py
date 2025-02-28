from app.extensions.db import db
from app.models.Building import Building
from app.extensions.responses import success_response, error_response

def get_building_by_id(building_id):
    """
    Retrieves a building by its ID.
    """
    try:
        building = Building.query.get(building_id)

        if not building:
            return error_response(
                message="Building not found",
                status_code=404,
                error_code=3003
            )

        return success_response(
            message="Building retrieved successfully",
            data={
                "id": building.id,
                "name": building.name,
                "total_units": building.total_units,
                "created_at": building.created_at
            },
            status_code=200
        )

    except Exception as e:
        return error_response(
            message="Error retrieving building",
            errors=[str(e)],
            status_code=500,
            error_code=3004
        )