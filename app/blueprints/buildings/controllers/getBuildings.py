from app.extensions.db import db
from app.models.Building import Building
from app.extensions.responses import success_response, error_response

def get_all_buildings():
    """
    Fetch all buildings from the database.
    Returns:
        JSON response with a list of buildings.
    """
    try:
        buildings = Building.query.all()
        buildings_data = [
            {
                "id": building.id,
                "name": building.name,
                "total_units": building.total_units,
                "created_at": building.created_at.isoformat(),
                "updated_at": building.updated_at.isoformat(),
            }
            for building in buildings
        ]
        return success_response(data=buildings_data, message="Buildings fetched successfully")

    except Exception as e:
        return error_response(message="Error fetching buildings", errors=[str(e)], status_code=500)