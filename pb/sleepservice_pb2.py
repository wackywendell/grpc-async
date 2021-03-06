# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pb/sleepservice.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='pb/sleepservice.proto',
  package='sleepservice',
  syntax='proto3',
  serialized_pb=_b('\n\x15pb/sleepservice.proto\x12\x0csleepservice\"/\n\tSleepTask\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0csleepSeconds\x18\x02 \x01(\x02\"?\n\nSleepTasks\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0csleepSeconds\x18\x02 \x01(\x02\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\",\n\rSleepResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t2\x98\x01\n\x0bSleepTasker\x12?\n\x05Sleep\x12\x17.sleepservice.SleepTask\x1a\x1b.sleepservice.SleepResponse\"\x00\x12H\n\x0bSleepStream\x12\x18.sleepservice.SleepTasks\x1a\x1b.sleepservice.SleepResponse\"\x00\x30\x01\x62\x06proto3')
)




_SLEEPTASK = _descriptor.Descriptor(
  name='SleepTask',
  full_name='sleepservice.SleepTask',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='sleepservice.SleepTask.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sleepSeconds', full_name='sleepservice.SleepTask.sleepSeconds', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=39,
  serialized_end=86,
)


_SLEEPTASKS = _descriptor.Descriptor(
  name='SleepTasks',
  full_name='sleepservice.SleepTasks',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='sleepservice.SleepTasks.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sleepSeconds', full_name='sleepservice.SleepTasks.sleepSeconds', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='sleepservice.SleepTasks.count', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=88,
  serialized_end=151,
)


_SLEEPRESPONSE = _descriptor.Descriptor(
  name='SleepResponse',
  full_name='sleepservice.SleepResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='sleepservice.SleepResponse.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='sleepservice.SleepResponse.message', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=153,
  serialized_end=197,
)

DESCRIPTOR.message_types_by_name['SleepTask'] = _SLEEPTASK
DESCRIPTOR.message_types_by_name['SleepTasks'] = _SLEEPTASKS
DESCRIPTOR.message_types_by_name['SleepResponse'] = _SLEEPRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SleepTask = _reflection.GeneratedProtocolMessageType('SleepTask', (_message.Message,), dict(
  DESCRIPTOR = _SLEEPTASK,
  __module__ = 'pb.sleepservice_pb2'
  # @@protoc_insertion_point(class_scope:sleepservice.SleepTask)
  ))
_sym_db.RegisterMessage(SleepTask)

SleepTasks = _reflection.GeneratedProtocolMessageType('SleepTasks', (_message.Message,), dict(
  DESCRIPTOR = _SLEEPTASKS,
  __module__ = 'pb.sleepservice_pb2'
  # @@protoc_insertion_point(class_scope:sleepservice.SleepTasks)
  ))
_sym_db.RegisterMessage(SleepTasks)

SleepResponse = _reflection.GeneratedProtocolMessageType('SleepResponse', (_message.Message,), dict(
  DESCRIPTOR = _SLEEPRESPONSE,
  __module__ = 'pb.sleepservice_pb2'
  # @@protoc_insertion_point(class_scope:sleepservice.SleepResponse)
  ))
_sym_db.RegisterMessage(SleepResponse)



_SLEEPTASKER = _descriptor.ServiceDescriptor(
  name='SleepTasker',
  full_name='sleepservice.SleepTasker',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=200,
  serialized_end=352,
  methods=[
  _descriptor.MethodDescriptor(
    name='Sleep',
    full_name='sleepservice.SleepTasker.Sleep',
    index=0,
    containing_service=None,
    input_type=_SLEEPTASK,
    output_type=_SLEEPRESPONSE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SleepStream',
    full_name='sleepservice.SleepTasker.SleepStream',
    index=1,
    containing_service=None,
    input_type=_SLEEPTASKS,
    output_type=_SLEEPRESPONSE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SLEEPTASKER)

DESCRIPTOR.services_by_name['SleepTasker'] = _SLEEPTASKER

# @@protoc_insertion_point(module_scope)
