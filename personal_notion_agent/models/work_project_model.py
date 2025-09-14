from pydantic import BaseModel, model_validator
from typing import Optional, Literal
from datetime import datetime, date

from skills.utils.datetime_utils import ensure_sp_aware, isoformat_sp


class WorkProject(BaseModel):
    name: str
    priority: Optional[Literal["High", "Medium", "Low"]] = None
    tag: Optional[Literal["Consultant", "College", "Personal", "Agilize"]] = None
    status: Optional[
        Literal[
            "Not started",
            "Planning",
            "Paused",
            "Waiting",
            "In progress",
            "Discontinued",
            "Done",
        ]
    ] = None
    start: Optional[str | date | datetime] = None
    end: Optional[str | date | datetime] = None

    @model_validator(mode="after")
    def validate_date_order(self):
        start_dt = ensure_sp_aware(self.start)
        end_dt = ensure_sp_aware(self.end)
        if start_dt is not None and end_dt is not None and end_dt < start_dt:
            raise ValueError("End date/time cannot be before start date/time.")
        return self

    def to_create_payload(self, database_id: str) -> dict:
        props: dict = {
            "Name": {"title": [{"text": {"content": self.name}}]},
        }
        if self.priority:
            props["Priority"] = {"select": {"name": self.priority}}
        if self.tags:
            props["Tags"] = {"select": [{"name": self.tag}]}
        if self.status:
            props["Status"] = {"status": {"name": self.status}}
        if self.start or self.end:
            props["Deadline"] = {
                "date": {
                    "start": isoformat_sp(self.start),
                    "end": isoformat_sp(self.end),
                }
            }
        return {"parent": {"database_id": database_id}, "properties": props}
