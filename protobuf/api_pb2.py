# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/api.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12protobuf/api.proto\"X\n\rrequest_frame\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05width\x18\x02 \x01(\x05\x12\x0e\n\x06height\x18\x03 \x01(\x05\x12\r\n\x05\x64\x65pth\x18\x04 \x01(\x05\x12\r\n\x05\x66rame\x18\x05 \x01(\x0c\"g\n\x0eresponse_frame\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05width\x18\x02 \x01(\x05\x12\x0e\n\x06height\x18\x03 \x01(\x05\x12\r\n\x05\x64\x65pth\x18\x04 \x01(\x05\x12\r\n\x05\x66rame\x18\x05 \x01(\x0c\x12\x0c\n\x04json\x18\x06 \x01(\t29\n\x03\x41PI\x12\x32\n\rprocess_frame\x12\x0e.request_frame\x1a\x0f.response_frame\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protobuf.api_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REQUEST_FRAME']._serialized_start=22
  _globals['_REQUEST_FRAME']._serialized_end=110
  _globals['_RESPONSE_FRAME']._serialized_start=112
  _globals['_RESPONSE_FRAME']._serialized_end=215
  _globals['_API']._serialized_start=217
  _globals['_API']._serialized_end=274
# @@protoc_insertion_point(module_scope)
