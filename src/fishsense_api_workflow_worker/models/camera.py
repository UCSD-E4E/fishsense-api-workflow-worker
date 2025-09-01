from sqlmodel import Field, SQLModel


class Camera(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    serial_number: str = Field(unique=True, index=True)
    name: str = Field(unique=True, index=True)
