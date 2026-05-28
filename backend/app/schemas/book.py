from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# 1. The Base Schema
# Contains fields that are common to reading, creating, and updating.
class BookBase(BaseModel):
    # Field(...) means this field is strictly required.
    # min_length=1 ensures the user cannot send an empty string ("").
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)

    # ge=1 (greater/equal), le=5 (less/equal).
    # default=None makes it optional.
    rating: int | None = Field(default=None, ge=1, le=5)
    note: str | None = None

# 2. The Create Schema
# Used when a user sends a POST request.
# It inherits everything from BookBase. We don't want users sending an 'id'.
class BookCreate(BookBase):
    pass

# 3. The Update Schema
# Used for PUT/PATCH requests. Every field must be optional because
# the user might only want to update the title, but leave the author alone.
class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    author: str | None = Field(default=None, min_length=1)
    rating: int | None = Field(default=None, ge=1, le=5)
    note: str | None = Field(default=None, max_length=2000)

# 4. The Read Schema
# Used for the API response. It inherits from BookBase but adds the system-generated fields that the user is allowed to be.
class BookRead(BookBase):
    id: int
    user_id: int
    created_at: datetime

    # This is a critical configuration for SQLAlchemy
    # By default, Pydantic expects a dictionary. SQLAlchemy returns class objects.
    # from_attributes=True tells Pydantic to read object attributes (e.g., book.title)
    # and automatically convert them into JSON.
    model_config = ConfigDict(from_attributes=True)