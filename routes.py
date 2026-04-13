import os
from typing import List

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import HouseholdPowerConsumption
from schemas import (
    ConsumptionCreate,
    ConsumptionResponse,
    ConsumptionUpdate,
    LoadResponse,
)

router = APIRouter(prefix="/api/v1", tags=["consumption"])

DEFAULT_CSV_PATH = "household_power_consumption.csv"
BATCH_SIZE = 5000

NUMERIC_COLUMNS = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
]
EXPECTED_COLUMNS = ["Date", "Time", *NUMERIC_COLUMNS]


@router.post(
    "/load",
    response_model=LoadResponse,
    status_code=status.HTTP_201_CREATED,
)
def load_dataset(
    csv_path: str = DEFAULT_CSV_PATH,
    db: Session = Depends(get_db),
):
    """Bulk-load the household power consumption CSV into the database.

    Idempotent: clears existing rows before inserting. Missing values ("?")
    become NULL. Dates are stored verbatim as VARCHAR (no format coercion).
    """
    if not os.path.isfile(csv_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CSV file not found: {csv_path}",
        )

    try:
        # Read CSV — treat "?" as NaN so numeric columns parse as float.
        df = pd.read_csv(csv_path, na_values=["?"])

        # Drop the "index" column if present (case-insensitive match).
        index_cols = [c for c in df.columns if c.lower() == "index"]
        if index_cols:
            df = df.drop(columns=index_cols)

        missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"CSV missing required columns: {missing}",
            )

        # Keep only expected columns, in order.
        df = df[EXPECTED_COLUMNS]

        # Ensure numeric columns are float (NaN for missing).
        for col in NUMERIC_COLUMNS:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Dates/Times stored verbatim as strings.
        df["Date"] = df["Date"].astype(str)
        df["Time"] = df["Time"].astype(str)

        # Replace NaN with None for SQLAlchemy (NULL in DB).
        df = df.replace({np.nan: None})

        # Idempotency: wipe existing rows.
        db.query(HouseholdPowerConsumption).delete()
        db.commit()

        total = 0
        records = df.to_dict(orient="records")
        for start in range(0, len(records), BATCH_SIZE):
            batch = records[start : start + BATCH_SIZE]
            db.bulk_insert_mappings(HouseholdPowerConsumption, batch)
            db.commit()
            total += len(batch)

        return LoadResponse(records_loaded=total, status="success")

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load dataset: {exc}",
        )


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
