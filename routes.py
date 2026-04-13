from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import (
    ConsumptionCreate,
    ConsumptionResponse,
    ConsumptionUpdate,
    LoadResponse,
)

router = APIRouter(prefix="/api/v1", tags=["consumption"])


@router.post("/load", response_model=LoadResponse)
def load_dataset(db: Session = Depends(get_db)):
    """Bulk-load the household power consumption dataset from source file."""
    # TODO: implement dataset load logic
    return LoadResponse(records_loaded=0, status="not_implemented")


@router.get("/consumption", response_model=List[ConsumptionResponse])
def list_consumption(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List consumption records with pagination."""
    # TODO: implement list logic
    return []


@router.get("/consumption/{record_id}", response_model=ConsumptionResponse)
def get_consumption(record_id: int, db: Session = Depends(get_db)):
    """Retrieve a single consumption record by ID."""
    # TODO: implement retrieval logic
    return ConsumptionResponse(
        ID=record_id,
        Date="",
        Time="",
    )


@router.post("/consumption", response_model=ConsumptionResponse, status_code=201)
def create_consumption(payload: ConsumptionCreate, db: Session = Depends(get_db)):
    """Create a new consumption record."""
    # TODO: implement create logic
    return ConsumptionResponse(ID=0, **payload.model_dump())


@router.put("/consumption/{record_id}", response_model=ConsumptionResponse)
def update_consumption(
    record_id: int,
    payload: ConsumptionUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing consumption record."""
    # TODO: implement update logic
    return ConsumptionResponse(
        ID=record_id,
        Date=payload.Date or "",
        Time=payload.Time or "",
        Global_active_power=payload.Global_active_power,
        Global_reactive_power=payload.Global_reactive_power,
        Voltage=payload.Voltage,
        Global_intensity=payload.Global_intensity,
        Sub_metering_1=payload.Sub_metering_1,
        Sub_metering_2=payload.Sub_metering_2,
        Sub_metering_3=payload.Sub_metering_3,
    )


@router.delete("/consumption/{record_id}", status_code=204)
def delete_consumption(record_id: int, db: Session = Depends(get_db)):
    """Delete a consumption record by ID."""
    # TODO: implement delete logic
    return None
