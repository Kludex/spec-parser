"""
The OpenAPI Specification (OAS) defines a standard, language-agnostic interface to
RESTful APIs which allows both humans and computers to discover and understand the
capabilities of the service without access to source code, documentation, or through
network traffic inspection. When properly defined, a consumer can understand and
interact with the remote service with a minimal amount of implementation logic.

An OpenAPI definition can then be used by documentation generation tools to display the
API, code generation tools to generate servers and clients in various programming
languages, testing tools, and many other use cases.

Reference: https://swagger.io/specification/
"""

from enum import Enum
from textwrap import dedent
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic.class_validators import root_validator


class Contact(BaseModel):
    name: Optional[str] = Field(
        None, description="The identifying name of the contact person/organization."
    )
    url: Optional[str] = Field(
        None,
        description="The URL pointing to the contact information. MUST be in the format of a URL.",
    )
    email: Optional[str] = Field(
        None,
        description=(
            "The email address of the contact person/organization. "
            "MUST be in the format of an email address."
        ),
    )


class License(BaseModel):
    name: str = Field(..., description="The license name used for the API.")
    url: Optional[str] = Field(
        None,
        description="A URL to the license used for the API. MUST be in the format of a URL.",
    )


class Info(BaseModel):
    title: str = Field(..., description="The title of the API.")
    description: Optional[str] = Field(
        None,
        description=(
            "A short description of the API. CommonMark syntax MAY be used for rich "
            "text representation."
        ),
    )
    terms_of_service: Optional[str] = Field(
        None,
        alias="termsOfService",
        description="A URL to the Terms of Service for the API. MUST be in the format of a URL.",
    )
    contact: Optional[Contact] = Field(
        None, description="The contact information for the exposed API."
    )
    license: Optional[License] = Field(
        None, description="The license information for the exposed API."
    )


class ServerVariable(BaseModel):
    enum: List[str] = Field(
        [],
        description=(
            "An enumeration of string values to be used if the substitution options "
            "are from a limited set. The array SHOULD NOT be empty."
        ),
    )
    default: str = Field(
        ...,
        description=(
            "The default value to use for substitution, which SHALL be sent if an "
            "alternate value is not supplied. Note this behavior is different than the "
            "Schema Object's treatment of default values, because in those cases "
            "parameter values are optional. If the enum is defined, the value SHOULD "
            "exist in the enum's values."
        ),
    )
    description: Optional[str] = Field(
        None,
        description=(
            "An optional description for the server variable. "
            "CommonMark syntax MAY be used for rich text representation."
        ),
    )


class ServerVariables(BaseModel):
    __root__ = Dict[str, ServerVariable]


class Server(BaseModel):
    url: str = Field(
        ...,
        description=(
            "A URL to the target host. This URL supports Server Variables and MAY be "
            "relative, to indicate that the host location is relative to the location "
            "where the OpenAPI document is being served. Variable substitutions will "
            "be made when a variable is named in {brackets}."
        ),
    )
    description: Optional[str] = Field(
        None,
        description=(
            "An optional string describing the host designated by the URL. "
            "CommonMark syntax MAY be used for rich text representation."
        ),
    )
    variables: ServerVariables = Field(
        {},
        description=(
            "A map between a variable name and its value. "
            "The value is used for substitution in the server's URL template."
        ),
    )


class Servers(BaseModel):
    __root__ = List[Server]


class ExternalDocumentation(BaseModel):
    description: Optional[str] = Field(
        None,
        description="A short description of the target documentation. CommonMark syntax MAY be used for rich text representation.",
    )
    url: str = Field(
        ...,
        description="The URL for the target documentation. Value MUST be in the format of a URL.",
    )


class Tag(BaseModel):
    name: str = Field(..., description="The name of the tag.")
    description: Optional[str] = Field(
        None,
        description="A short description for the tag. CommonMark syntax MAY be used for rich text representation.",
    )
    external_docs: Optional[ExternalDocumentation] = Field(
        None,
        alias="externalDocs",
        description="Additional external documentation for this tag.",
    )


class Tags(BaseModel):
    __root__ = List[Tag]


class ParameterLocation(str, Enum):
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"


class Parameter(BaseModel):
    name: str = Field(
        ...,
        description=dedent(
            """
            The name of the parameter. Parameter names are case sensitive.
            - If in is "path", the name field MUST correspond to a template expression occurring within the path field in the Paths Object. See Path Templating for further information.
            - If in is "header" and the name field is "Accept", "Content-Type" or "Authorization", the parameter definition SHALL be ignored.
            - For all other cases, the name corresponds to the parameter name used by the in property.
            """
        ),
    )
    in_: ParameterLocation = Field(
        ...,
        alias="in",
        description='The location of the parameter. Possible values are "query", "header", "path" or "cookie".',
    )
    description: Optional[str] = Field(
        None,
        description="A brief description of the parameter. This could contain examples of use. CommonMark syntax MAY be used for rich text representation.",
    )
    required: bool = Field(
        False,
        description='Determines whether this parameter is mandatory. If the parameter location is "path", this property is REQUIRED and its value MUST be true. Otherwise, the property MAY be included and its default value is false.',
    )
    deprecated: bool = Field(
        False,
        description="Specifies that a parameter is deprecated and SHOULD be transitioned out of usage. Default value is false.",
    )
    allow_empty_value: bool = Field(
        False,
        alias="allowEmptyValue",
        description="Sets the ability to pass empty-valued parameters. This is valid only for query parameters and allows sending a parameter with an empty value. Default value is false. If style is used, and if behavior is n/a (cannot be serialized), the value of allowEmptyValue SHALL be ignored. Use of this property is NOT RECOMMENDED, as it is likely to be removed in a later revision.",
    )

    @validator("required")
    def validate_required(cls, v: bool, values: Dict[str, Any]) -> bool:
        if values.get("in_") == ParameterLocation.path and v is False:
            raise ValueError(
                "Field required must be assigned and its value MUST be true."
            )
        return v


class Reference(BaseModel):
    ref: str = Field(..., alias="$ref", description="The reference string.")


class Example(BaseModel):
    summary: Optional[str] = Field(
        None, description="Short description for the example."
    )
    description: Optional[str] = Field(
        None,
        description="Long description for the example. CommonMark syntax MAY be used for rich text representation.",
    )
    value: Optional[Any] = Field(
        None,
        description="Embedded literal example. The value field and externalValue field are mutually exclusive. To represent examples of media types that cannot naturally represented in JSON or YAML, use a string value to contain the example, escaping where necessary.",
    )
    external_value: Optional[str] = Field(
        None,
        alias="externalValue",
        description="A URL that points to the literal example. This provides the capability to reference examples that cannot easily be included in JSON or YAML documents. The value field and externalValue field are mutually exclusive.",
    )


class Examples(BaseModel):
    __root__ = Dict[str, Union[Example, Reference]]


class Schema(BaseModel):
    ...


class Encoding(BaseModel):
    content_type: Optional[str] = Field(
        None,
        alias="contentType",
        description="The Content-Type for encoding a specific property. Default value depends on the property type: for string with format being binary – application/octet-stream; for other primitive types – text/plain; for object - application/json; for array – the default is defined based on the inner type. The value can be a specific media type (e.g. application/json), a wildcard media type (e.g. image/*), or a comma-separated list of the two types.",
    )
    # headers
    # style
    # explode
    # allow_reserved


class MediaType(BaseModel):
    schema_: Optional[Union[Schema, Reference]] = Field(
        None,
        alias="schema",
        description="The schema defining the content of the request, response, or parameter.",
    )
    example: Optional[Any] = Field(
        None,
        description="Example of the media type. The example object SHOULD be in the correct format as specified by the media type. The example field is mutually exclusive of the examples field. Furthermore, if referencing a schema which contains an example, the example value SHALL override the example provided by the schema.",
    )
    examples: Optional[Examples] = Field(
        None,
        description="Examples of the media type. Each example object SHOULD match the media type and specified schema if present. The examples field is mutually exclusive of the example field. Furthermore, if referencing a schema which contains an example, the examples value SHALL override the example provided by the schema.",
    )
    encoding: Optional[Encoding] = Field(
        None,
        description="A map between a property name and its encoding information. The key, being the property name, MUST exist in the schema as a property. The encoding object SHALL only apply to requestBody objects when the media type is multipart or application/x-www-form-urlencoded.",
    )

    @root_validator()
    def validate_examples(cls, values):
        ...


class Content(BaseModel):
    __root__ = Dict[str, MediaType]


class RequestBody(BaseModel):
    description: Optional[str] = Field(
        None,
        description="A brief description of the request body. This could contain examples of use. CommonMark syntax MAY be used for rich text representation.",
    )
    content: Content = Field(
        ...,
        description="The content of the request body. The key is a media type or media type range and the value describes it. For requests that match multiple keys, only the most specific key is applicable. e.g. text/plain overrides text/*",
    )
    required: bool = Field(
        False,
        description="Determines if the request body is required in the request. Defaults to false.",
    )


class Operation(BaseModel):
    tags: List[str] = Field(
        [],
        description=(
            "A list of tags for API documentation control. Tags can be used for "
            "logical grouping of operations by resources or any other qualifier."
        ),
    )
    summary: Optional[str] = Field(
        None, description="A short summary of what the operation does."
    )
    description: Optional[str] = Field(
        None,
        description="A verbose explanation of the operation behavior. CommonMark syntax MAY be used for rich text representation.",
    )
    external_docs: Optional[ExternalDocumentation] = Field(
        None, description="Additional external documentation for this operation."
    )
    operation_id: Optional[str] = Field(
        None,
        description="Unique string used to identify the operation. The id MUST be unique among all operations described in the API. The operationId value is case-sensitive. Tools and libraries MAY use the operationId to uniquely identify an operation, therefore, it is RECOMMENDED to follow common programming naming conventions.",
    )
    # parameters:
    request_body: Optional[Union[RequestBody, Reference]] = Field(
        None,
        alias="requestBody",
        description="The request body applicable for this operation. The requestBody is only supported in HTTP methods where the HTTP 1.1 specification RFC7231 has explicitly defined semantics for request bodies. In other cases where the HTTP spec is vague, requestBody SHALL be ignored by consumers.",
    )
    responses: Responses = Field(
        ...,
        description="The list of possible responses as they are returned from executing this operation.",
    )
    # callbacks: = Field({}, description="A map of possible out-of band callbacks related to the parent operation. The key is a unique identifier for the Callback Object. Each value in the map is a Callback Object that describes a request that may be initiated by the API provider and the expected responses.")
    deprecated: bool = Field(
        False,
        description="Declares this operation to be deprecated. Consumers SHOULD refrain from usage of the declared operation. Default value is false.",
    )
    # security:
    servers: Servers = Field(
        [],
        description="An alternative server array to service this operation. If an alternative server object is specified at the Path Item Object or Root level, it will be overridden by this value.",
    )


class PathItem(BaseModel):
    ref: Optional[str] = Field(
        None,
        alias="$ref",
        description="Allows for an external definition of this path item. The referenced structure MUST be in the format of a Path Item Object. In case a Path Item Object field appears both in the defined object and the referenced object, the behavior is undefined.",
    )
    summary: Optional[str] = Field(
        None,
        description="An optional, string summary, intended to apply to all operations in this path.",
    )
    description: Optional[str] = Field(
        None,
        description="An optional, string description, intended to apply to all operations in this path. CommonMark syntax MAY be used for rich text representation.",
    )
    get: Optional[Operation] = Field(
        None, description="A definition of a GET operation on this path."
    )
    put: Optional[Operation] = Field(
        None, description="A definition of a PUT operation on this path."
    )
    post: Optional[Operation] = Field(
        None, description="A definition of a POST operation on this path."
    )
    delete: Optional[Operation] = Field(
        None, description="A definition of a DELETE operation on this path."
    )
    options: Optional[Operation] = Field(
        None, description="A definition of a OPTIONS operation on this path."
    )
    head: Optional[Operation] = Field(
        None, description="A definition of a HEAD operation on this path."
    )
    patch: Optional[Operation] = Field(
        None, "A definition of a PATCH operation on this path."
    )
    trace: Optional[Operation] = Field(
        None, description="A definition of a TRACE operation on this path."
    )
    servers: Servers = Field(
        [],
        description="An alternative server array to service all operations in this path.",
    )
    parameters: Optional[List[Union[Parameter, Reference]]] = Field(
        None,
        description="A list of parameters that are applicable for all the operations described under this path. These parameters can be overridden at the operation level, but cannot be removed there. The list MUST NOT include duplicated parameters. A unique parameter is defined by a combination of a name and location. The list can use the Reference Object to link to parameters that are defined at the OpenAPI Object's components/parameters.",
    )


class Paths(BaseModel):
    __root__ = Dict[str, PathItem]


class Security(BaseModel):
    __root__ = Dict[str, List[str]]


class Schemas(BaseModel):
    __root__ = Dict[str, Union[Schema, Reference]]


class Components(BaseModel):
    schemas: Optional[Schemas] = Field(
        None, description="An object to hold reusable Schema Objects."
    )


class OpenAPI(BaseModel):
    openapi: Literal["3.0.3"] = Field(
        ...,
        description=(
            "This string MUST be the semantic version number of the OpenAPI "
            "Specification version that the OpenAPI document uses. The openapi "
            "field SHOULD be used by tooling specifications and clients to interpret "
            "the OpenAPI document. This is not related to the API info.version string."
        ),
    )
    info: Info = Field(
        ...,
        description=(
            "Provides metadata about the API. "
            "The metadata MAY be used by tooling as required."
        ),
    )
    servers: Servers = Field(
        [],
        description=(
            "An array of Server Objects, which provide connectivity information to "
            "a target server. If the servers property is not provided, or is an empty "
            "array, the default value would be a Server Object with a url value of /."
        ),
    )
    paths: Paths = Field(
        ..., description="The available paths and operations for the API."
    )
    components: Optional[Components] = Field(
        None, description="An element to hold various schemas for the specification."
    )
    security: Optional[List[Security]] = Field(
        None,
        description=(
            "A declaration of which security mechanisms can be used across the API. "
            "The list of values includes alternative security requirement objects that "
            "can be used. Only one of the security requirement objects need to be "
            "satisfied to authorize a request. Individual operations can override this "
            "definition. To make security optional, an empty security requirement ({}) "
            "can be included in the array."
        ),
    )
    tags: Optional[Tags] = Field(
        None,
        description=(
            "A list of tags used by the specification with additional metadata. "
            "The order of the tags can be used to reflect on their order by the "
            "parsing tools. Not all tags that are used by the Operation Object must be "
            "declared. The tags that are not declared MAY be organized randomly or "
            "based on the tools' logic. Each tag name in the list MUST be unique."
        ),
    )
    external_docs: Optional[ExternalDocumentation] = Field(
        None, alias="externalDocs", description="Additional external documentation."
    )
