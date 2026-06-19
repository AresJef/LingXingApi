# -*- coding: utf-8 -*-
import datetime
from typing import Any, Optional
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator
from lingxingapi import errors
from lingxingapi.fields import StrOrNone2Blank


# Token 令牌 --------------------------------------------------------------------------------------------------------------------
class Token(BaseModel):
    # 接口的访问令牌
    access_token: str
    # 用于续约 access_token 的更新令牌
    refresh_token: str
    # 访问令牌的有效时间 (单位: 秒)
    expires_in: int


# 公用 Schema -------------------------------------------------------------------------------------------------------------------
class TagInfo(BaseModel):
    """商品的标签信息."""

    # 领星标签ID (GlobalTag.tag_id) [原字段 'global_tag_id']
    tag_id: int = Field(validation_alias="global_tag_id")
    # 领星标签名称 (GlobalTag.tag_name) [原字段 'tag_name']
    tag_name: str = Field(validation_alias="tag_name")
    # 领星标签颜色 (如: "#FF0000") [原字段 'color']
    tag_color: str = Field(validation_alias="color")


class AttachmentFile(BaseModel):
    """附件信息"""

    # 文件ID
    file_id: int
    # 文件名称
    file_name: str
    # 文件类型 (0: 未知, 1: 图片, 2: 压缩包)
    file_type: int = 0
    # 文件链接
    file_url: str = ""


class SpuProductAttribute(BaseModel):
    """SPU 商品属性"""

    # 属性ID
    attr_id: int
    # 属性名称
    attr_name: str
    # 属性值
    attr_value: str


class CustomField(BaseModel):
    """自定义字段"""

    # 自定义字段ID
    field_id: int = Field(validation_alias="id")
    # 自定义字段名称
    field_name: str = Field(validation_alias="name")
    # 自定义字段值
    field_value: str = Field(validation_alias="val_text")


class BaseResponse(BaseModel):
    """基础响应数据"""

    # 状态码
    code: int = 0
    # 提示信息
    message: Optional[StrOrNone2Blank] = None
    # 错误信息
    errors: Optional[list] = Field(None, validation_alias="error_details")
    # 请求链路id
    request_id: Optional[str] = None
    # 响应时间
    response_time: Optional[str] = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="after")
    def _adjustments(self) -> Self:
        # 设置默认数值
        if self.message is None:
            self.message = "success"
        if self.errors is None:
            self.errors = []
        if self.request_id is None:
            self.request_id = ""
        if self.response_time is None:
            # fmt: off
            dt = datetime.datetime.now()
            self.response_time = "%04d-%02d-%02d %02d:%02d:%02d" % (
                dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
            )
            # fmt: on

        # 返回
        return self


class ResponseV1(BaseResponse):
    """响应数据 - 下划线命名"""

    # 响应数据量
    response_count: int = 0
    # 总数据量
    total_count: int = Field(0, validation_alias="total")
    # 响应数据
    data: Any = None

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="after")
    def _set_count(self) -> Self:
        # 计算响应数据量
        if isinstance(self.data, list):
            self.response_count = len(self.data)
        elif isinstance(self.data, (dict, BaseModel)):
            self.response_count = 1
        else:
            return self

        # 调整总数据量
        if self.response_count > 0:
            self.total_count = max(self.total_count, self.response_count)
        return self


class ResponseV1Token(ResponseV1):
    """响应数据 - 下划线命名 + 分页游标 (next_token)"""

    # 分页游标
    next_token: StrOrNone2Blank


class ResponseV1TraceId(ResponseV1):
    """响应数据 - request_id 替换为 traceId"""

    # 请求链路id
    request_id: Optional[str] = Field(None, validation_alias="traceId")


class ResponseV2(ResponseV1):
    """响应数据 - 驼峰命名"""

    # 错误信息
    errors: Optional[list] = Field(None, validation_alias="errorDetails")
    # 请求链路id
    request_id: Optional[str] = Field(None, validation_alias="requestId")
    # 响应时间
    response_time: Optional[str] = Field(None, validation_alias="responseTime")


class ResponseResult(BaseResponse):
    """响应结果"""

    # 响应结果
    data: Any = None


# 特殊 Schema -------------------------------------------------------------------------------------------------------------------
class FlattenDataRecords(BaseModel):
    """从嵌套数据中提取列表数据 (records)

    - 1. 从 data 字段中, 提取 total 并赋值至基础层
    - 2. 从 data 字段中, 提取 records 并覆盖 data 字段
    """

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["total"] = max(inner.get("total", 0), data.get("total", 0))
            data["data"] = inner.get("records", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data


class FlattenDataList(BaseModel):
    """从嵌套数据中提取列表数据 (list)

    - 1. 从 data 字段中, 提取 total 并赋值至基础层
    - 2. 从 data 字段中, 提取 list 并覆盖 data 字段
    """

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    @model_validator(mode="before")
    def _flatten_data(cls, data: dict) -> dict:
        try:
            inner: dict = data.pop("data", {})
            data["total"] = max(inner.get("total", 0), data.get("total", 0))
            data["data"] = inner.get("list", [])
        except Exception:
            raise errors.ResponseDataError(cls.__name__, data=data)
        return data
