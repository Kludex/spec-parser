"""
AsyncAPI is an open source initiative that seeks to improve the current state of
Event-Driven Architectures (EDA). Our long-term goal is to make working with EDAs as
easy as it is to work with REST APIs. That goes from documentation to code generation,
from discovery to event management. Most of the processes you apply to your REST APIs
nowadays would be applicable to your event-driven/asynchronous APIs too.

To make this happen, the first step has been to create a specification that allows
developers, architects, and product managers to define the interfaces of an async API.
Much like OpenAPI (fka Swagger) does for REST APIs.

The AsyncAPI specification settles the base for a greater and better tooling ecosystem
for EDA's. We recently launched AsyncAPI specification 2.0.0 —the strongest version to
date— that will sustain the event-driven architectures of tomorrow.

Reference: https://www.asyncapi.com/docs/getting-started
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Info(BaseModel):
    ...


class Identifier(BaseModel):
    __root__ = str


class AsyncAPI(BaseModel):
    asyncapi: Literal["2.0.0"] = Field(
        ...,
        description="Specifies the AsyncAPI Specification version being used. It can be used by tooling Specifications and clients to interpret the version. The structure shall be major.minor.patch, where patch versions must be compatible with the existing major.minor tooling. Typically patch versions will be introduced to address errors in the documentation, and tooling should typically be compatible with the corresponding major.minor (1.0.*). Patch versions will correspond to patches of this document.",
    )
    id_: Optional[Identifier] = Field(
        None,
        alias="id",
        description="Identifier of the application the AsyncAPI document is defining.",
    )
    info: Info = Field(
        ...,
        description="Provides metadata about the API. The metadata can be used by the clients if needed.",
    )
