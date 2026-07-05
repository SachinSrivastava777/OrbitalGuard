from pydantic import BaseModel, Field

class ConjunctionRequest(BaseModel):
    semi_major_axis: float = Field(..., description="Orbit radius in km", ge=6000)
    eccentricity: float = Field(..., description="Orbit shape", ge=0.0, le=1.0)
    inclination: float = Field(..., description="Angle in degrees", ge=0.0, le=180.0)
    relative_distance: float = Field(..., description="Distance between objects in km", ge=0.0)
    relative_velocity: float = Field(..., description="Speed in km/s", ge=0.0)