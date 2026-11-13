# Hồ sơ đọc và đánh giá mẫu

Direct reading by Codex in this session; not an undeclared LLM judge or a claim of student/human review. Coherence read without numeric retrieval scores; grounding read after selection/test. No labels inferred from hit flags.

**Chưa có xác nhận của học viên:** Pending student verification; do not describe these as human-confirmed labels.

## Coherence — cùng 10 vị trí nguồn, 30 nhãn

0: không hiểu do mất ý/chủ thể; 1: hiểu một phần, thiếu ngữ cảnh; 2: tự hiểu và giữ ý. Không lấy Hit@3 làm nhãn.

### A · array · 1/2

Anchor 247; span [0, 500); chunk `15052533de8826817a7183aa2cbe6a736cccf87b7188a883bfb8cab58f5089fa`.

Giữ được định nghĩa array và type code nhưng kết thúc giữa nhãn 'Minimum size in by'; bảng thiếu cấu trúc/tiêu đề đầy đủ.

~~~text
# array — Efficient arrays of numeric values

This module defines an object type which can compactly represent an array of
basic values: characters, integers, floating-point numbers. Arrays are mutable sequence types and behave very much like lists, except that the type of objects stored in
them is constrained. The type is specified at object creation time by using a type code , which is a single character. The following type codes are
defined:

Type code

C Type

Python Type

Minimum size in by
~~~

### A · bisect · 1/2

Anchor 193; span [0, 500); chunk `07e2c69d985a11e0df1d1b210f8d467f4c440c77403e54fd926fc6e17a47ab85`.

Mục đích duy trì danh sách có thứ tự rõ, nhưng phần giải thích insertion point bị cắt ở 'this modul'.

~~~text
# bisect — Array bisection algorithm

Source code: Lib/bisect.py

This module provides support for maintaining a list in sorted order without
having to sort the list after each insertion. For long lists of items with
expensive comparison operations, this can be an improvement over
linear searches or frequent resorting.

The module is called bisect because it uses a basic bisection
algorithm to do its work. Unlike other bisection tools that search for a
specific value, the functions in this modul
~~~

### A · codecs · 1/2

Anchor 353; span [0, 500); chunk `45e1c428477548140c88ed9ecfbc09d3d5d9060ce1295cec242d22743288520d`.

Có chủ thể module và chuyển đổi text/bytes, nhưng câu về custom codecs bị cắt ở 'arbi', thiếu giới hạn áp dụng.

~~~text
# codecs — Codec registry and base classes

Source code: Lib/codecs.py

This module defines base classes for standard Python codecs (encoders and
decoders) and provides access to the internal Python codec registry, which
manages the codec and error handling lookup process. Most standard codecs
are text encodings , which encode text to bytes (and
decode bytes to text), but there are also codecs provided that encode text to
text, and bytes to bytes. Custom codecs may encode and decode between arbi
~~~

### A · collections · 1/2

Anchor 158; span [0, 500); chunk `e9e86fb0d712b27bd63e019a0dc265202faddbf6b8ae7bc148fa11d9bb39a190`.

Định nghĩa module rõ, nhưng bảng container bị cắt ngay phần Counter ('counting h'), khiến mục danh sách dang dở.

~~~text
# collections — Container datatypes

Source code: Lib/collections/__init__.py

This module implements specialized container datatypes providing alternatives to
Python’s general purpose built-in containers, dict , list , set , and tuple .

namedtuple()

factory function for creating tuple subclasses with named fields

deque

list-like container with fast appends and pops on either end

ChainMap

dict-like class for creating a single view of multiple mappings

Counter

dict subclass for counting h
~~~

### A · collections.abc · 1/2

Anchor 267; span [0, 500); chunk `bf3fa0b62924651f86ff5849347117e076b5769d1c0ab68ccd4085875bf4cd4e`.

Giới thiệu kiểm tra interface còn đủ, nhưng hướng dẫn kế thừa ABC bị cắt giữa từ ở 'one of th'.

~~~text
# collections.abc — Abstract Base Classes for Containers

Added in version 3.3: Formerly, this module was part of the collections module.

Source code: Lib/_collections_abc.py

This module provides abstract base classes that
can be used to test whether a class provides a particular interface; for
example, whether it is hashable or whether it is a mapping .

An issubclass() or isinstance() test for an interface works in one
of three ways.

A newly written class can inherit directly from one of th
~~~

### A · configparser · 2/2

Anchor 208; span [0, 498); chunk `870708c7deb8fc6c50b99988eb0c5d911f94a7841295d4ffd79926cde55e137e`.

Đủ mục đích ConfigParser/INI và ngoại lệ value-type prefix; Module tomllib là tên tham chiếu, không làm sai hay cắt ý chính.

~~~text
# configparser — Configuration file parser

Source code: Lib/configparser.py

This module provides the ConfigParser class which implements a basic
configuration language which provides a structure similar to what’s found in
Microsoft Windows INI files. You can use this to write Python programs which
can be customized by end users easily.

Note

This library does not interpret or write the value-type prefixes used in
the Windows Registry extended version of INI syntax.

See also

Module tomllib
~~~

### A · copy · 1/2

Anchor 232; span [0, 499); chunk `f358b89e16ca75420e2edb97c04fbd2fb8c56de3342b3ecb28f7166131406454`.

Phân biệt assignment và copying rõ nhưng signature deepcopy bị cắt ngay '[, memo', chưa dùng được độc lập.

~~~text
# copy — Shallow and deep copy operations

Source code: Lib/copy.py

Assignment statements in Python do not copy objects, they create bindings
between a target and an object. For collections that are mutable or contain
mutable items, a copy is sometimes needed so one can change one copy without
changing the other. This module provides generic shallow and deep copy
operations (explained below).

Interface summary:

copy. copy ( obj )

Return a shallow copy of obj .

copy. deepcopy ( obj [ , memo
~~~

### A · csv · 1/2

Anchor 420; span [0, 499); chunk `b7d13ad985b55c069490d68ec8abc5f65f79cf0c03e3ed5468a6e482b0f6c819`.

Có chủ thể CSV và lý do khác biệt định dạng, nhưng đoạn bị cắt trước lời giải thích vai trò module thống nhất I/O.

~~~text
# csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases. CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 . The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications. These
differences can make it annoying to process CSV files
~~~

### A · datetime · 1/2

Anchor 218; span [0, 500); chunk `3a404e972d772eb4b787a1f07a4e0265c253a9ba887b2f2d64f848f326bb2596`.

Mục đích datetime hoàn chỉnh, nhưng phần tham chiếu zoneinfo bị cắt ở 'IANA time', thiếu nội dung kết.

~~~text
# datetime — Basic date and time types

Source code: Lib/datetime.py

The datetime module supplies classes for manipulating dates and times.

While date and time arithmetic is supported, the focus of the implementation is
on efficient attribute extraction for output formatting and manipulation.

Tip

Skip to the format codes .

See also

Module calendar

General calendar related functions.

Module time

Time access and conversions.

Module zoneinfo

Concrete time zones representing the IANA time
~~~

### A · decimal · 1/2

Anchor 167; span [0, 500); chunk `54bf497bc68e800fe245a4f44d8ecd87b6c95b6e865808579d1b0645d6a077e4`.

Giới thiệu số thập phân rõ nhưng trích dẫn lý do thiết kế dừng giữa từ 'excer', thiếu kết câu và ví dụ.

~~~text
# decimal — Decimal fixed-point and floating-point arithmetic

Source code: Lib/decimal.py

The decimal module provides support for fast correctly rounded
decimal floating-point arithmetic. It offers several advantages over the float datatype:

Decimal “is based on a floating-point model which was designed
with people in mind, and necessarily has a paramount guiding principle –
computers must provide an arithmetic that works in the same way as the
arithmetic that people learn at school.” – excer
~~~

### B · array · 1/2

Anchor 247; span [0, 982); chunk `e65c6f2b958239c47b376da8f105914bef2dee8794780d67211013bef4c3d1e7`.

Đoạn mở đầu và các type code đọc được, nhưng bảng đã trải phẳng và ghi chú 'It can be 16 bits or 32 bits' thiếu đối tượng/ghi chú kế tiếp; chưa tự đủ ngữ cảnh.

~~~text
# array — Efficient arrays of numeric values

This module defines an object type which can compactly represent an array of
basic values: characters, integers, floating-point numbers. Arrays are mutable sequence types and behave very much like lists, except that the type of objects stored in
them is constrained. The type is specified at object creation time by using a type code , which is a single character. The following type codes are
defined:

Type code

C Type

Python Type

Minimum size in bytes

Notes

'b'

signed char

int

1

'B'

unsigned char

int

1

'u'

wchar_t

Unicode character

2

(1)

'w'

Py_UCS4

Unicode character

4

(2)

'h'

signed short

int

2

'H'

unsigned short

int

2

'i'

signed int

int

2

'I'

unsigned int

int

2

'l'

signed long

int

4

'L'

unsigned long

int

4

'q'

signed long long

int

8

'Q'

unsigned long long

int

8

'f'

float

float

4

'd'

double

float

8

Notes:

It can be 16 bits or 32 bits depending on the platform.
~~~

### B · bisect · 2/2

Anchor 193; span [0, 768); chunk `cdde81c371dc111aa0fdb2905b3b9f5c78002eaa2c2594a66eb20771fee8d742`.

Giữ trọn mục đích module và giải thích insertion point, so sánh __lt__ thay __eq__; nhãn Note ở cuối không làm mất ý chính.

~~~text
# bisect — Array bisection algorithm

Source code: Lib/bisect.py

This module provides support for maintaining a list in sorted order without
having to sort the list after each insertion. For long lists of items with
expensive comparison operations, this can be an improvement over
linear searches or frequent resorting.

The module is called bisect because it uses a basic bisection
algorithm to do its work. Unlike other bisection tools that search for a
specific value, the functions in this module are designed to locate an
insertion point. Accordingly, the functions never call an __eq__() method to determine whether a value has been found. Instead, the
functions only call the __lt__() method and will return an insertion
point between values in an array.

Note
~~~

### B · codecs · 2/2

Anchor 353; span [0, 840); chunk `db5673893a82256d8f7256fae058fd223d8f58abc773c97e00d72fba8199598c`.

Đủ định nghĩa registry, các kiểu chuyển đổi, giới hạn text encoding và mô tả encode; câu kết hoàn chỉnh.

~~~text
# codecs — Codec registry and base classes

Source code: Lib/codecs.py

This module defines base classes for standard Python codecs (encoders and
decoders) and provides access to the internal Python codec registry, which
manages the codec and error handling lookup process. Most standard codecs
are text encodings , which encode text to bytes (and
decode bytes to text), but there are also codecs provided that encode text to
text, and bytes to bytes. Custom codecs may encode and decode between arbitrary
types, but some module features are restricted to be used specifically with text encodings or with codecs that encode to bytes .

The module defines the following functions for encoding and decoding with
any codec:

codecs. encode ( obj , encoding = 'utf-8' , errors = 'strict' )

Encodes obj using the codec registered for encoding .
~~~

### B · collections · 2/2

Anchor 158; span [0, 883); chunk `16322302be919f27776cebaebc82883b0b6a199206e6c1ec4ed05aa7c036d713`.

Có tiêu đề, mục đích và đầy đủ tên/mô tả các container trong bảng mở đầu; có thể hiểu độc lập.

~~~text
# collections — Container datatypes

Source code: Lib/collections/__init__.py

This module implements specialized container datatypes providing alternatives to
Python’s general purpose built-in containers, dict , list , set , and tuple .

namedtuple()

factory function for creating tuple subclasses with named fields

deque

list-like container with fast appends and pops on either end

ChainMap

dict-like class for creating a single view of multiple mappings

Counter

dict subclass for counting hashable objects

OrderedDict

dict subclass that remembers the order entries were added

defaultdict

dict subclass that calls a factory function to supply missing values

UserDict

wrapper around dictionary objects for easier dict subclassing

UserList

wrapper around list objects for easier list subclassing

UserString

wrapper around string objects for easier string subclassing
~~~

### B · collections.abc · 1/2

Anchor 267; span [0, 996); chunk `48d3521bc51d9560bf55cd0551981dcbff1f11282f71dc45cd6e7147b998feaa`.

Định nghĩa interface rõ và có ví dụ kế thừa trực tiếp, nhưng câu báo có ba cách rồi chỉ trình bày cách đầu; ngữ cảnh hướng dẫn chưa đầy đủ.

~~~text
# collections.abc — Abstract Base Classes for Containers

Added in version 3.3: Formerly, this module was part of the collections module.

Source code: Lib/_collections_abc.py

This module provides abstract base classes that
can be used to test whether a class provides a particular interface; for
example, whether it is hashable or whether it is a mapping .

An issubclass() or isinstance() test for an interface works in one
of three ways.

A newly written class can inherit directly from one of the
abstract base classes. The class must supply the required abstract
methods. The remaining mixin methods come from inheritance and can be
overridden if desired. Other methods may be added as needed:

class C ( Sequence ): # Direct inheritance def __init__ ( self ): ... # Extra method not required by the ABC def __getitem__ ( self , index ): ... # Required abstract method def __len__ ( self ): ... # Required abstract method def count ( self , value ): ... # Optionally override a mixin method
~~~

### B · configparser · 2/2

Anchor 208; span [0, 902); chunk `5344c55f0a6ea8772e6a924937f3c970e6e44dbf60192976f05c9819708a4b41`.

Giữ trọn mô tả, giới hạn INI và ba lựa chọn TOML/shlex/JSON cùng giải thích; không cắt giữa câu.

~~~text
# configparser — Configuration file parser

Source code: Lib/configparser.py

This module provides the ConfigParser class which implements a basic
configuration language which provides a structure similar to what’s found in
Microsoft Windows INI files. You can use this to write Python programs which
can be customized by end users easily.

Note

This library does not interpret or write the value-type prefixes used in
the Windows Registry extended version of INI syntax.

See also

Module tomllib

TOML is a well-specified format for application configuration files.
It is specifically designed to be an improved version of INI.

Module shlex

Support for creating Unix shell-like mini-languages which can also
be used for application configuration files.

Module json

The json module implements a subset of JavaScript syntax which is
sometimes used for configuration, but does not support comments.
~~~

### B · copy · 1/2

Anchor 232; span [0, 903); chunk `5a6f3f9e2939f3986d6b25f1e4e0c3aa9f23ec4eee0b3c8b81f755d47fd2858c`.

Có interface copy/deepcopy/replace/Error đầy đủ, nhưng câu cuối mở ra khác biệt shallow/deep với dấu hai chấm mà thiếu giải thích tiếp theo.

~~~text
# copy — Shallow and deep copy operations

Source code: Lib/copy.py

Assignment statements in Python do not copy objects, they create bindings
between a target and an object. For collections that are mutable or contain
mutable items, a copy is sometimes needed so one can change one copy without
changing the other. This module provides generic shallow and deep copy
operations (explained below).

Interface summary:

copy. copy ( obj )

Return a shallow copy of obj .

copy. deepcopy ( obj [ , memo ] )

Return a deep copy of obj .

copy. replace ( obj , / , ** changes )

Creates a new object of the same type as obj , replacing fields with values
from changes .

Added in version 3.13.

exception copy. Error

Raised for module specific errors.

The difference between shallow and deep copying is only relevant for compound
objects (objects that contain other objects, like lists or class instances):
~~~

### B · csv · 2/2

Anchor 420; span [0, 777); chunk `3f4a6efa0dcad9c278feca6cc96288a0562646ebb2d586d7b46e09a124993601`.

Trọn đoạn mở đầu: vấn đề thiếu chuẩn chung, khác delimiters/quoting và vai trò module che chi tiết đọc/ghi.

~~~text
# csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases. CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 . The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications. These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiters and quoting characters vary, the overall format is
similar enough that it is possible to write a single module which can
efficiently manipulate such data, hiding the details of reading and writing the
data from the programmer.
~~~

### B · datetime · 2/2

Anchor 218; span [0, 763); chunk `a69e4c365ad79552680d393f1d1396d40b5f2a8aca16cc7bdb51ecaa3f42214d`.

Mục đích, ưu tiên triển khai và các module/package tham chiếu đều được giữ trọn; không cần đoạn bên cạnh để hiểu.

~~~text
# datetime — Basic date and time types

Source code: Lib/datetime.py

The datetime module supplies classes for manipulating dates and times.

While date and time arithmetic is supported, the focus of the implementation is
on efficient attribute extraction for output formatting and manipulation.

Tip

Skip to the format codes .

See also

Module calendar

General calendar related functions.

Module time

Time access and conversions.

Module zoneinfo

Concrete time zones representing the IANA time zone database.

Package dateutil

Third-party library with expanded time zone and parsing support.

Package DateType

Third-party library that introduces distinct static types to e.g. allow static type checkers to differentiate between naive and aware datetimes.
~~~

### B · decimal · 2/2

Anchor 167; span [0, 807); chunk `66c005cd3c2ffbe9f9af8766d621b3af43523392c9a4791f97fb83e708ec14b6`.

Giới thiệu, trích dẫn có nguồn và ví dụ 1.1+2.2 về sai số binary đều hoàn chỉnh; giữ mạch ý.

~~~text
# decimal — Decimal fixed-point and floating-point arithmetic

Source code: Lib/decimal.py

The decimal module provides support for fast correctly rounded
decimal floating-point arithmetic. It offers several advantages over the float datatype:

Decimal “is based on a floating-point model which was designed
with people in mind, and necessarily has a paramount guiding principle –
computers must provide an arithmetic that works in the same way as the
arithmetic that people learn at school.” – excerpt from the decimal
arithmetic specification.

Decimal numbers can be represented exactly. In contrast, numbers like 1.1 and 2.2 do not have exact representations in binary
floating point. End users typically would not expect 1.1 + 2.2 to display
as 3.3000000000000003 as it does with binary floating point.
~~~

### C · array · 1/2

Anchor 247; span [0, 982); chunk `e65c6f2b958239c47b376da8f105914bef2dee8794780d67211013bef4c3d1e7`.

Đoạn mở đầu và các type code đọc được, nhưng bảng đã trải phẳng và ghi chú 'It can be 16 bits or 32 bits' thiếu đối tượng/ghi chú kế tiếp; chưa tự đủ ngữ cảnh.

~~~text
# array — Efficient arrays of numeric values

This module defines an object type which can compactly represent an array of
basic values: characters, integers, floating-point numbers. Arrays are mutable sequence types and behave very much like lists, except that the type of objects stored in
them is constrained. The type is specified at object creation time by using a type code , which is a single character. The following type codes are
defined:

Type code

C Type

Python Type

Minimum size in bytes

Notes

'b'

signed char

int

1

'B'

unsigned char

int

1

'u'

wchar_t

Unicode character

2

(1)

'w'

Py_UCS4

Unicode character

4

(2)

'h'

signed short

int

2

'H'

unsigned short

int

2

'i'

signed int

int

2

'I'

unsigned int

int

2

'l'

signed long

int

4

'L'

unsigned long

int

4

'q'

signed long long

int

8

'Q'

unsigned long long

int

8

'f'

float

float

4

'd'

double

float

8

Notes:

It can be 16 bits or 32 bits depending on the platform.
~~~

### C · bisect · 2/2

Anchor 193; span [0, 768); chunk `cdde81c371dc111aa0fdb2905b3b9f5c78002eaa2c2594a66eb20771fee8d742`.

Giữ trọn mục đích module và giải thích insertion point, so sánh __lt__ thay __eq__; nhãn Note ở cuối không làm mất ý chính.

~~~text
# bisect — Array bisection algorithm

Source code: Lib/bisect.py

This module provides support for maintaining a list in sorted order without
having to sort the list after each insertion. For long lists of items with
expensive comparison operations, this can be an improvement over
linear searches or frequent resorting.

The module is called bisect because it uses a basic bisection
algorithm to do its work. Unlike other bisection tools that search for a
specific value, the functions in this module are designed to locate an
insertion point. Accordingly, the functions never call an __eq__() method to determine whether a value has been found. Instead, the
functions only call the __lt__() method and will return an insertion
point between values in an array.

Note
~~~

### C · codecs · 2/2

Anchor 353; span [0, 840); chunk `db5673893a82256d8f7256fae058fd223d8f58abc773c97e00d72fba8199598c`.

Đủ định nghĩa registry, các kiểu chuyển đổi, giới hạn text encoding và mô tả encode; câu kết hoàn chỉnh.

~~~text
# codecs — Codec registry and base classes

Source code: Lib/codecs.py

This module defines base classes for standard Python codecs (encoders and
decoders) and provides access to the internal Python codec registry, which
manages the codec and error handling lookup process. Most standard codecs
are text encodings , which encode text to bytes (and
decode bytes to text), but there are also codecs provided that encode text to
text, and bytes to bytes. Custom codecs may encode and decode between arbitrary
types, but some module features are restricted to be used specifically with text encodings or with codecs that encode to bytes .

The module defines the following functions for encoding and decoding with
any codec:

codecs. encode ( obj , encoding = 'utf-8' , errors = 'strict' )

Encodes obj using the codec registered for encoding .
~~~

### C · collections · 2/2

Anchor 158; span [0, 883); chunk `16322302be919f27776cebaebc82883b0b6a199206e6c1ec4ed05aa7c036d713`.

Có tiêu đề, mục đích và đầy đủ tên/mô tả các container trong bảng mở đầu; có thể hiểu độc lập.

~~~text
# collections — Container datatypes

Source code: Lib/collections/__init__.py

This module implements specialized container datatypes providing alternatives to
Python’s general purpose built-in containers, dict , list , set , and tuple .

namedtuple()

factory function for creating tuple subclasses with named fields

deque

list-like container with fast appends and pops on either end

ChainMap

dict-like class for creating a single view of multiple mappings

Counter

dict subclass for counting hashable objects

OrderedDict

dict subclass that remembers the order entries were added

defaultdict

dict subclass that calls a factory function to supply missing values

UserDict

wrapper around dictionary objects for easier dict subclassing

UserList

wrapper around list objects for easier list subclassing

UserString

wrapper around string objects for easier string subclassing
~~~

### C · collections.abc · 1/2

Anchor 267; span [0, 996); chunk `48d3521bc51d9560bf55cd0551981dcbff1f11282f71dc45cd6e7147b998feaa`.

Định nghĩa interface rõ và có ví dụ kế thừa trực tiếp, nhưng câu báo có ba cách rồi chỉ trình bày cách đầu; ngữ cảnh hướng dẫn chưa đầy đủ.

~~~text
# collections.abc — Abstract Base Classes for Containers

Added in version 3.3: Formerly, this module was part of the collections module.

Source code: Lib/_collections_abc.py

This module provides abstract base classes that
can be used to test whether a class provides a particular interface; for
example, whether it is hashable or whether it is a mapping .

An issubclass() or isinstance() test for an interface works in one
of three ways.

A newly written class can inherit directly from one of the
abstract base classes. The class must supply the required abstract
methods. The remaining mixin methods come from inheritance and can be
overridden if desired. Other methods may be added as needed:

class C ( Sequence ): # Direct inheritance def __init__ ( self ): ... # Extra method not required by the ABC def __getitem__ ( self , index ): ... # Required abstract method def __len__ ( self ): ... # Required abstract method def count ( self , value ): ... # Optionally override a mixin method
~~~

### C · configparser · 2/2

Anchor 208; span [0, 902); chunk `5344c55f0a6ea8772e6a924937f3c970e6e44dbf60192976f05c9819708a4b41`.

Giữ trọn mô tả, giới hạn INI và ba lựa chọn TOML/shlex/JSON cùng giải thích; không cắt giữa câu.

~~~text
# configparser — Configuration file parser

Source code: Lib/configparser.py

This module provides the ConfigParser class which implements a basic
configuration language which provides a structure similar to what’s found in
Microsoft Windows INI files. You can use this to write Python programs which
can be customized by end users easily.

Note

This library does not interpret or write the value-type prefixes used in
the Windows Registry extended version of INI syntax.

See also

Module tomllib

TOML is a well-specified format for application configuration files.
It is specifically designed to be an improved version of INI.

Module shlex

Support for creating Unix shell-like mini-languages which can also
be used for application configuration files.

Module json

The json module implements a subset of JavaScript syntax which is
sometimes used for configuration, but does not support comments.
~~~

### C · copy · 1/2

Anchor 232; span [0, 903); chunk `5a6f3f9e2939f3986d6b25f1e4e0c3aa9f23ec4eee0b3c8b81f755d47fd2858c`.

Có interface copy/deepcopy/replace/Error đầy đủ, nhưng câu cuối mở ra khác biệt shallow/deep với dấu hai chấm mà thiếu giải thích tiếp theo.

~~~text
# copy — Shallow and deep copy operations

Source code: Lib/copy.py

Assignment statements in Python do not copy objects, they create bindings
between a target and an object. For collections that are mutable or contain
mutable items, a copy is sometimes needed so one can change one copy without
changing the other. This module provides generic shallow and deep copy
operations (explained below).

Interface summary:

copy. copy ( obj )

Return a shallow copy of obj .

copy. deepcopy ( obj [ , memo ] )

Return a deep copy of obj .

copy. replace ( obj , / , ** changes )

Creates a new object of the same type as obj , replacing fields with values
from changes .

Added in version 3.13.

exception copy. Error

Raised for module specific errors.

The difference between shallow and deep copying is only relevant for compound
objects (objects that contain other objects, like lists or class instances):
~~~

### C · csv · 2/2

Anchor 420; span [0, 777); chunk `3f4a6efa0dcad9c278feca6cc96288a0562646ebb2d586d7b46e09a124993601`.

Trọn đoạn mở đầu: vấn đề thiếu chuẩn chung, khác delimiters/quoting và vai trò module che chi tiết đọc/ghi.

~~~text
# csv — CSV File Reading and Writing

Source code: Lib/csv.py

The so-called CSV (Comma Separated Values) format is the most common import and
export format for spreadsheets and databases. CSV format was used for many
years prior to attempts to describe the format in a standardized way in RFC 4180 . The lack of a well-defined standard means that subtle differences
often exist in the data produced and consumed by different applications. These
differences can make it annoying to process CSV files from multiple sources.
Still, while the delimiters and quoting characters vary, the overall format is
similar enough that it is possible to write a single module which can
efficiently manipulate such data, hiding the details of reading and writing the
data from the programmer.
~~~

### C · datetime · 2/2

Anchor 218; span [0, 763); chunk `a69e4c365ad79552680d393f1d1396d40b5f2a8aca16cc7bdb51ecaa3f42214d`.

Mục đích, ưu tiên triển khai và các module/package tham chiếu đều được giữ trọn; không cần đoạn bên cạnh để hiểu.

~~~text
# datetime — Basic date and time types

Source code: Lib/datetime.py

The datetime module supplies classes for manipulating dates and times.

While date and time arithmetic is supported, the focus of the implementation is
on efficient attribute extraction for output formatting and manipulation.

Tip

Skip to the format codes .

See also

Module calendar

General calendar related functions.

Module time

Time access and conversions.

Module zoneinfo

Concrete time zones representing the IANA time zone database.

Package dateutil

Third-party library with expanded time zone and parsing support.

Package DateType

Third-party library that introduces distinct static types to e.g. allow static type checkers to differentiate between naive and aware datetimes.
~~~

### C · decimal · 2/2

Anchor 167; span [0, 807); chunk `66c005cd3c2ffbe9f9af8766d621b3af43523392c9a4791f97fb83e708ec14b6`.

Giới thiệu, trích dẫn có nguồn và ví dụ 1.1+2.2 về sai số binary đều hoàn chỉnh; giữ mạch ý.

~~~text
# decimal — Decimal fixed-point and floating-point arithmetic

Source code: Lib/decimal.py

The decimal module provides support for fast correctly rounded
decimal floating-point arithmetic. It offers several advantages over the float datatype:

Decimal “is based on a floating-point model which was designed
with people in mind, and necessarily has a paramount guiding principle –
computers must provide an arithmetic that works in the same way as the
arithmetic that people learn at school.” – excerpt from the decimal
arithmetic specification.

Decimal numbers can be represented exactly. In contrast, numbers like 1.1 and 2.2 do not have exact representations in binary
floating point. End users typically would not expect 1.1 + 2.2 to display
as 3.3000000000000003 as it does with binary floating point.
~~~

## Grounding — 5 test × 3 chiến lược

Đọc toàn bộ top-3; đánh giá đủ bằng chứng và điều kiện, có thể dùng nhiều chunk. Không phải độ chính xác câu trả lời LLM. Điểm 2 không có nghĩa literal Evidence Hit@3 phải bằng 1.

### A · q16 · 2/2

User context: restrict retrieval to the official chapter 'File and Directory Access'. In Python 3.13, how does Path.resolve handle a nonexistent path or symlink loop with strict=True versus strict=False?

Đáp án cần hỗ trợ: Strict mode raises OSError. Non-strict mode resolves as far as possible and appends the remainder without existence checks; symlink loops follow the same strict/non-strict error policy in 3.13.

Rank 1 giữ trọn đoạn nói nonexistent path/symlink loop, strict=True gây OSError và strict=False nối phần chưa kiểm tra; metadata xác nhận Python 3.13. Note đổi phiên bản bị cắt nên strict quote-hit thất bại, nhưng đoạn chính đủ trả lời hành vi hiện tại.

Rank 1: [pathlib](https://docs.python.org/3.13/library/pathlib.html), category `File and Directory Access`, span [24750, 25250); chunk `b7468508c4584052aaead7e6e2691e86a1572ef30ce79968a9ae31d45b3c7b3c`.

~~~text
is the only method to do so):

>>> p = Path ( 'docs/../setup.py' ) >>> p . resolve () PosixPath('/home/antoine/pathlib/setup.py')

If a path doesn’t exist or a symlink loop is encountered, and strict is True , OSError is raised. If strict is False , the path is
resolved as far as possible and any remainder is appended without checking
whether it exists.

Changed in version 3.6: The strict parameter was added (pre-3.6 behavior is strict).

Changed in version 3.13: Symlink loops are treated like o
~~~

Rank 2: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [13501, 14000); chunk `7e7ab87960a73b1839bf69d796bb50bacadb14421865d24f1f503455d1e2375d`.

~~~text
can differ from the case of path ,
in particular the drive letter is capitalized.

By default, the path is evaluated up to the first component that does not
exist, is a symlink loop, or whose evaluation raises OSError .
All such components are appended unchanged to the existing part of the path.

Some errors that are handled this way include “access denied”, “not a
directory”, or “bad argument to internal function”. Thus, the
resulting path may be missing or inaccessible, may still contain
link
~~~

Rank 3: [pathlib](https://docs.python.org/3.13/library/pathlib.html), category `File and Directory Access`, span [10350, 10849); chunk `99266e0b2904a16daa941bab3c4e30213a6bd0a8672ad83f05d1384f1a0b21e2`.

~~~text
it is
recommended to first call Path.resolve() so as to resolve
symlinks and eliminate ".." components.

PurePath. name

A string representing the final path component, excluding the drive and
root, if any:

>>> PurePosixPath ( 'my/library/setup.py' ) . name 'setup.py'

UNC drive names are not considered:

>>> PureWindowsPath ( '//some/share/setup.py' ) . name 'setup.py' >>> PureWindowsPath ( '//some/share' ) . name ''

PurePath. suffix

The last dot-separated portion of the final component, if
~~~

### A · q17 · 2/2

Why can commonprefix return an invalid filesystem path, and which function should be used to find a common path prefix?

Đáp án cần hỗ trợ: It works character by character and can return invalid paths; use commonpath for a common path prefix.

Rank 3 có toàn bộ cảnh báo commonprefix xử lý từng ký tự và khuyên dùng commonpath; rank 1 thêm ví dụ /usr/l đối lập /usr. Đủ nguyên nhân và cách thay thế.

Rank 1: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [3601, 4100); chunk `e37a82642670b9ccb5548347ebcf5f0d7b9bb54d04f18ad9a57ea0cc7ab86b28`.

~~~text
prefix.

>>> os . path . commonprefix ([ '/usr/lib' , '/usr/local/lib' ]) '/usr/l' >>> os . path . commonpath ([ '/usr/lib' , '/usr/local/lib' ]) '/usr'

Changed in version 3.6: Accepts a path-like object .

os.path. dirname ( path , / )

Return the directory name of pathname path . This is the first element of
the pair returned by passing path to the function split() .

Changed in version 3.6: Accepts a path-like object .

os.path. exists ( path )

Return True if path refers to an existing pat
~~~

Rank 2: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [2700, 3200); chunk `75553d26cb15c82eefc308dbd1c8bf2bf834c50e0bbdde8d3eafcb72c404dcf9`.

~~~text
-like object .

os.path. commonpath ( paths )

Return the longest common sub-path of each pathname in the iterable paths . Raise ValueError if paths contain both absolute
and relative pathnames, if paths are on different drives, or
if paths is empty. Unlike commonprefix() , this returns a
valid path.

Added in version 3.5.

Changed in version 3.6: Accepts a sequence of path-like objects .

Changed in version 3.13: Any iterable can now be passed, rather than just sequences.

os.path. commonprefix
~~~

Rank 3: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [3150, 3650); chunk `af9fbb39dfde9e99992820b2ea3b610d72bb746e4c0ec1015e9b81fd5f20f70c`.

~~~text
rather than just sequences.

os.path. commonprefix ( list , / )

Return the longest string prefix (taken character-by-character) that is a
prefix of all strings in list . If list is empty, return the empty string
( '' ).

Warning

This function may return invalid paths because it works a
character at a time.
If you need a common path prefix , then the algorithm
implemented in this function is not secure. Use commonpath() for finding a common path prefix.

>>> os . path . commonprefix ([ '/usr/li
~~~

### A · q18 · 2/2

On Windows, when reopening a NamedTemporaryFile with delete=True and delete_on_close=False through builtin open, what must happen before context-manager exit?

Đáp án cần hỗ trợ: Additional opens that do not share delete access must be closed before exiting; otherwise os.unlink on exit raises PermissionError.

Given the Windows/delete flags already supplied in the question, rank 1 contains the obligation to close additional opens without delete sharing before context exit and the PermissionError consequence. Rank 2 adds explicit broader Windows context. The complete answer can be supported by rank 1 despite the longer literal gold being split.

Rank 1: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [4950, 5450); chunk `8ab589cfff5575e92c4c0169013834c9cd9d0cb02076df8eb350fd2dcfef67bf`.

~~~text
true but delete_on_close is false. Note, that in this
case the additional opens that do not share delete access (e.g.
created via builtin open() ) must be closed before exiting the
context manager, else the os.unlink() call on context manager
exit will fail with a PermissionError .

On Windows, if delete_on_close is false, and the file is created in a
directory for which the user lacks delete access, then the os.unlink() call on exit of the context manager will fail with a PermissionError .
This
~~~

Rank 2: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [4500, 5000); chunk `6893069c18f521f7152d47fe0f6086f2bba8d86324f6cd2037deea430b926836`.

~~~text
commended as it provides assistance in automatic
cleaning of the temporary file upon the context manager exit.

Opening the temporary file again by its name while it is still open works as
follows:

On POSIX the file can always be opened again.

On Windows, make sure that at least one of the following conditions are
fulfilled:

delete is false

additional open shares delete access (e.g. by calling os.open() with the flag O_TEMPORARY )

delete is true but delete_on_close is false. Note, that in t
~~~

Rank 3: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [5400, 5900); chunk `03252c4a9ac84dc9e8268e42fde4e9368c82bb3b52ba91ad26219fe2f26ba6b6`.

~~~text
xt manager will fail with a PermissionError .
This cannot happen when delete_on_close is true because delete access is
requested by the open, which fails immediately if the requested access is not
granted.

On POSIX (only), a process that is terminated abruptly with SIGKILL
cannot automatically delete any NamedTemporaryFiles it created.

Raises an auditing event tempfile.mkstemp with argument fullpath .

Changed in version 3.8: Added errors parameter.

Changed in version 3.12: Added delete_on_cl
~~~

### A · q19 · 2/2

User context: restrict retrieval to the official chapter 'File Formats'. Why should CSV files be opened with newline='' when fields can contain newlines or a platform writes CRLF?

Đáp án cần hỗ trợ: Without it, embedded newlines in quoted fields are not interpreted correctly and CRLF platforms may add an extra carriage return on write; csv handles newline translation itself.

Rank 2 chứa trọn footnote về quoted newline, CRLF thêm carriage return và csv tự xử lý newline. Rank 3 difflib không liên quan và sai phạm vi filter yêu cầu, nhưng hai điều kiện trả lời vẫn đủ trong rank 2.

Rank 1: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [20250, 20750); chunk `cb5ae87d82f4fb2090b1d29cea13b04f4cea3b45508f9ae4e2c556463958bf09`.

~~~text
sv' , newline = '' , encoding = 'utf-8' ) as f : reader = csv . reader ( f ) for row in reader : print ( row )

The same applies to writing in something other than the system default
encoding: specify the encoding argument when opening the output file.

Registering a new dialect:

import csv csv . register_dialect ( 'unixpwd' , delimiter = ':' , quoting = csv . QUOTE_NONE ) with open ( 'passwd' , newline = '' ) as f : reader = csv . reader ( f , 'unixpwd' )

A slightly more advanced use of the r
~~~

Rank 2: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [21150, 21515); chunk `117563ceb34118278ea81da2841977b8196eec29a4a746d261ad588c7082a68d`.

~~~text
in csv . reader ([ 'one,two,three' ]): print ( row )

Footnotes

If newline='' is not specified, newlines embedded inside quoted fields
will not be interpreted correctly, and on platforms that use \r\n line endings
on write an extra \r will be added. It should always be safe to specify newline='' , since the csv module does its own
( universal ) newline handling.
~~~

Rank 3: [difflib](https://docs.python.org/3.13/library/difflib.html), category `Text Processing Services`, span [13051, 13550); chunk `68548ceb1f013e165c13a1651785e7681dbdb0529eb3d4184b4f485b9c670456`.

~~~text
default, the diff control lines (those with --- , +++ , or @@ ) are
created with a trailing newline. This is helpful so that inputs created from io.IOBase.readlines() result in diffs that are suitable for use with io.IOBase.writelines() since both the inputs and outputs have trailing
newlines.

For inputs that do not have trailing newlines, set the lineterm argument to "" so that the output will be uniformly newline free.

The unified diff format normally has a header for filenames and modifica
~~~

### A · q20 · 2/2

How should Python values be bound into sqlite3 SQL statements to avoid SQL injection?

Đáp án cần hỗ trợ: Use placeholders, such as ?, to bind values instead of string formatting.

Rank 1 cảnh báo ghép SQL bằng string operations gây injection và có heading dùng placeholders; rank 2 mô tả execute(sql, parameters) bind values bằng placeholders, rank 3 có ví dụ VALUES(?). Đây là evidence tương đương trên cùng trang, không trùng quote gold ban đầu.

Rank 1: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [53550, 54050); chunk `9d3e1c72a5fefe9555c00e1bf0ef881bdd32f197b3884b4c03fc6df2d664aec5`.

~~~text
e .quit or CTRL-D to exit the shell.

-h , --help

Print CLI help.

-v , --version

Print underlying SQLite library version.

Added in version 3.12.

## How-to guides

### How to use placeholders to bind values in SQL queries

SQL operations usually need to use values from Python variables. However,
beware of using Python’s string operations to assemble queries, as they
are vulnerable to SQL injection attacks . For example, an attacker can simply
close the single quote and inject OR TRUE to sele
~~~

Rank 2: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [39600, 40100); chunk `f448b74ed3e46e88bbbb842615cf4a67f738bbaf889037fa1425222df6cb0874`.

~~~text
LECT t FROM data" ): print ( row )

class sqlite3. Cursor

A Cursor instance has the following attributes and methods.

execute ( sql , parameters = () , / )

Execute a single SQL statement,
optionally binding Python values using placeholders .

Parameters :

sql ( str ) – A single SQL statement.

parameters ( dict | sequence ) – Python values to bind to placeholders in sql .
A dict if named placeholders are used.
A sequence if unnamed placeholders are used.
See How to use placeholders to bind v
~~~

Rank 3: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [59400, 59900); chunk `8537cb8fb7b53f00e6ae62ae6e6e4b7b2df7102023838d0ece2973b5b29272e0`.

~~~text
3 . PARSE_DECLTYPES ) cur = con . execute ( "CREATE TABLE test(p point)" ) cur . execute ( "INSERT INTO test(p) VALUES(?)" , ( p ,)) cur . execute ( "SELECT p FROM test" ) print ( "with declared types:" , cur . fetchone ()[ 0 ]) cur . close () con . close () # 2) Parse using column names con = sqlite3 . connect ( ":memory:" , detect_types = sqlite3 . PARSE_COLNAMES ) cur = con . execute ( "CREATE TABLE test(p)" ) cur . execute ( "INSERT INTO test(p) VALUES(?)" , ( p ,)) cur . execute ( 'SELECT p
~~~

### B · q16 · 2/2

User context: restrict retrieval to the official chapter 'File and Directory Access'. In Python 3.13, how does Path.resolve handle a nonexistent path or symlink loop with strict=True versus strict=False?

Đáp án cần hỗ trợ: Strict mode raises OSError. Non-strict mode resolves as far as possible and appends the remainder without existence checks; symlink loops follow the same strict/non-strict error policy in 3.13.

Rank 2 contains Path.resolve and the complete current strict/non-strict behavior for a nonexistent path or symlink loop in the 3.13 snapshot; rank 3 adds the historical version-change note. Rank 1 is the neighboring os.path API, so provenance must distinguish them. The answer is supported without requiring a multi-chunk union.

Rank 1: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [13799, 14755); chunk `0e041a13a302c39d0382da320f043159486f8bcf10dd538d810d285418f2cacf`.

~~~text
Some errors that are handled this way include “access denied”, “not a
directory”, or “bad argument to internal function”. Thus, the
resulting path may be missing or inaccessible, may still contain
links or loops, and may traverse non-directories.

This behavior can be modified by keyword arguments:

If strict is True , the first error encountered when evaluating the path is
re-raised.
In particular, FileNotFoundError is raised if path does not exist,
or another OSError if it is otherwise inaccessible.

If strict is os.path.ALLOW_MISSING , errors other than FileNotFoundError are re-raised (as with strict=True ).
Thus, the returned path will not contain any symbolic links, but the named
file and some of its parent directories may be missing.

Note

This function emulates the operating system’s procedure for making a path
canonical, which differs slightly between Windows and UNIX with respect
to how links and subsequent path components interact.
~~~

Rank 2: [pathlib](https://docs.python.org/3.13/library/pathlib.html), category `File and Directory Access`, span [24388, 25191); chunk `f1a000af0f0a4984d277d60a4e41b80dae00561c2641faa1a3cd13287971529a`.

~~~text
>>> p = Path ( 'tests' ) >>> p PosixPath('tests') >>> p . absolute () PosixPath('/home/antoine/pathlib/tests')

Path. resolve ( strict = False )

Make the path absolute, resolving any symlinks. A new path object is
returned:

>>> p = Path () >>> p PosixPath('.') >>> p . resolve () PosixPath('/home/antoine/pathlib')

“ .. ” components are also eliminated (this is the only method to do so):

>>> p = Path ( 'docs/../setup.py' ) >>> p . resolve () PosixPath('/home/antoine/pathlib/setup.py')

If a path doesn’t exist or a symlink loop is encountered, and strict is True , OSError is raised. If strict is False , the path is
resolved as far as possible and any remainder is appended without checking
whether it exists.

Changed in version 3.6: The strict parameter was added (pre-3.6 behavior is strict).
~~~

Rank 3: [pathlib](https://docs.python.org/3.13/library/pathlib.html), category `File and Directory Access`, span [25193, 25793); chunk `ad41fdf4ee7ceec118c653e5c61344720b3aa68790dc242368ce0a800dab7b30`.

~~~text
Changed in version 3.13: Symlink loops are treated like other errors: OSError is raised in
strict mode, and no exception is raised in non-strict mode. In previous
versions, RuntimeError is raised no matter the value of strict .

Path. readlink ( )

Return the path to which the symbolic link points (as returned by os.readlink() ):

>>> p = Path ( 'mylink' ) >>> p . symlink_to ( 'setup.py' ) >>> p . readlink () PosixPath('setup.py')

Added in version 3.9.

Changed in version 3.13: Raises UnsupportedOperation if os.readlink() is not
available. In previous versions, NotImplementedError was raised.
~~~

### B · q17 · 2/2

Why can commonprefix return an invalid filesystem path, and which function should be used to find a common path prefix?

Đáp án cần hỗ trợ: It works character by character and can return invalid paths; use commonpath for a common path prefix.

Rank 1 chứa cảnh báo trả path không hợp lệ do xét từng ký tự và khuyên dùng commonpath; rank 2 minh họa /usr/l và /usr. Đủ trả lời độc lập với chunk thứ ba không liên quan trực tiếp.

Rank 1: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [2747, 3608); chunk `5b704f9ea7c8f832a3ea1b4c8b4c40ada4020e00db020e4f8aa18c25cb75a044`.

~~~text
Return the longest common sub-path of each pathname in the iterable paths . Raise ValueError if paths contain both absolute
and relative pathnames, if paths are on different drives, or
if paths is empty. Unlike commonprefix() , this returns a
valid path.

Added in version 3.5.

Changed in version 3.6: Accepts a sequence of path-like objects .

Changed in version 3.13: Any iterable can now be passed, rather than just sequences.

os.path. commonprefix ( list , / )

Return the longest string prefix (taken character-by-character) that is a
prefix of all strings in list . If list is empty, return the empty string
( '' ).

Warning

This function may return invalid paths because it works a
character at a time.
If you need a common path prefix , then the algorithm
implemented in this function is not secure. Use commonpath() for finding a common path prefix.
~~~

Rank 2: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [3610, 4531); chunk `0e5c164249e0f4e4a91cb3f8f098f4e928bad37ef3e71ddb654b98dcd6bd6859`.

~~~text
>>> os . path . commonprefix ([ '/usr/lib' , '/usr/local/lib' ]) '/usr/l' >>> os . path . commonpath ([ '/usr/lib' , '/usr/local/lib' ]) '/usr'

Changed in version 3.6: Accepts a path-like object .

os.path. dirname ( path , / )

Return the directory name of pathname path . This is the first element of
the pair returned by passing path to the function split() .

Changed in version 3.6: Accepts a path-like object .

os.path. exists ( path )

Return True if path refers to an existing path or an open
file descriptor. Returns False for broken symbolic links. On
some platforms, this function may return False if permission is
not granted to execute os.stat() on the requested file, even
if the path physically exists.

Changed in version 3.3: path can now be an integer: True is returned if it is an
open file descriptor, False otherwise.

Changed in version 3.6: Accepts a path-like object .

os.path. lexists ( path )
~~~

Rank 3: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [13799, 14755); chunk `0e041a13a302c39d0382da320f043159486f8bcf10dd538d810d285418f2cacf`.

~~~text
Some errors that are handled this way include “access denied”, “not a
directory”, or “bad argument to internal function”. Thus, the
resulting path may be missing or inaccessible, may still contain
links or loops, and may traverse non-directories.

This behavior can be modified by keyword arguments:

If strict is True , the first error encountered when evaluating the path is
re-raised.
In particular, FileNotFoundError is raised if path does not exist,
or another OSError if it is otherwise inaccessible.

If strict is os.path.ALLOW_MISSING , errors other than FileNotFoundError are re-raised (as with strict=True ).
Thus, the returned path will not contain any symbolic links, but the named
file and some of its parent directories may be missing.

Note

This function emulates the operating system’s procedure for making a path
canonical, which differs slightly between Windows and UNIX with respect
to how links and subsequent path components interact.
~~~

### B · q18 · 2/2

On Windows, when reopening a NamedTemporaryFile with delete=True and delete_on_close=False through builtin open, what must happen before context-manager exit?

Đáp án cần hỗ trợ: Additional opens that do not share delete access must be closed before exiting; otherwise os.unlink on exit raises PermissionError.

Rank 1 giữ trọn ngữ cảnh Windows, ba lựa chọn và điều kiện đóng additional opens trước exit; rank 2 làm rõ delete/delete_on_close. Đủ ngoại lệ PermissionError và truy nguồn tempfile.

Rank 1: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [4746, 5738); chunk `df8accac72f4ad7758f170bd6ea91acb6061d8c4c964f77b9178ed86835bf3dc`.

~~~text
On Windows, make sure that at least one of the following conditions are
fulfilled:

delete is false

additional open shares delete access (e.g. by calling os.open() with the flag O_TEMPORARY )

delete is true but delete_on_close is false. Note, that in this
case the additional opens that do not share delete access (e.g.
created via builtin open() ) must be closed before exiting the
context manager, else the os.unlink() call on context manager
exit will fail with a PermissionError .

On Windows, if delete_on_close is false, and the file is created in a
directory for which the user lacks delete access, then the os.unlink() call on exit of the context manager will fail with a PermissionError .
This cannot happen when delete_on_close is true because delete access is
requested by the open, which fails immediately if the requested access is not
granted.

On POSIX (only), a process that is terminated abruptly with SIGKILL
cannot automatically delete any NamedTemporaryFiles it created.
~~~

Rank 2: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [3788, 4744); chunk `63ecef0f78f670ff3831ebd35813615e511d9679f71b7d55f92573a47199b1fb`.

~~~text
If delete is true (the default) and delete_on_close is true (the
default), the file is deleted as soon as it is closed. If delete is true
and delete_on_close is false, the file is deleted on context manager exit
only, or else when the file-like object is finalized. Deletion is not
always guaranteed in this case (see object.__del__() ). If delete is
false, the value of delete_on_close is ignored.

Therefore to use the name of the temporary file to reopen the file after
closing it, either make sure not to delete the file upon closure (set the delete parameter to be false) or, in case the temporary file is created in
a with statement, set the delete_on_close parameter to be false.
The latter approach is recommended as it provides assistance in automatic
cleaning of the temporary file upon the context manager exit.

Opening the temporary file again by its name while it is still open works as
follows:

On POSIX the file can always be opened again.
~~~

Rank 3: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [7862, 8840); chunk `21b96f020ce37f164ec48f0b25a3c3e71b3bb3de07b02a98329142c08eabdb90`.

~~~text
The directory can be explicitly cleaned up by calling the cleanup() method. If ignore_cleanup_errors is true, any unhandled
exceptions during explicit or implicit cleanup (such as a PermissionError removing open files on Windows) will be ignored,
and the remaining removable items deleted on a “best-effort” basis.
Otherwise, errors will be raised in whatever context cleanup occurs
(the cleanup() call, exiting the context manager, when the object
is garbage-collected or during interpreter shutdown).

The delete parameter can be used to disable cleanup of the directory tree
upon exiting the context. While it may seem unusual for a context manager
to disable the action taken when exiting the context, it can be useful during
debugging or when you need your cleanup behavior to be conditional based on
other logic.

Warning

Cleanup is not robust against the tree being modified while it is removed.
Files outside of the tree may have their permissions and file flags reset.
~~~

### B · q19 · 2/2

User context: restrict retrieval to the official chapter 'File Formats'. Why should CSV files be opened with newline='' when fields can contain newlines or a platform writes CRLF?

Đáp án cần hỗ trợ: Without it, embedded newlines in quoted fields are not interpreted correctly and CRLF platforms may add an extra carriage return on write; csv handles newline translation itself.

Rank 1 là toàn bộ footnote nêu cả quoted embedded newline, extra carriage return trên CRLF và csv tự xử lý newline; các rank còn lại cung cấp cách mở writer/reader. Đủ hai vế câu hỏi.

Rank 1: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [21215, 21515); chunk `f4ce2c234b6ef871430fd8335055b214db80527cda8c0b364399ef30a4bd8679`.

~~~text
If newline='' is not specified, newlines embedded inside quoted fields
will not be interpreted correctly, and on platforms that use \r\n line endings
on write an extra \r will be added. It should always be safe to specify newline='' , since the csv module does its own
( universal ) newline handling.
~~~

Rank 2: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [20362, 21213); chunk `4c066dfce8fe43600df6a5b40be12e83dc8e32e68762b819f2a3fdc825cf2b70`.

~~~text
The same applies to writing in something other than the system default
encoding: specify the encoding argument when opening the output file.

Registering a new dialect:

import csv csv . register_dialect ( 'unixpwd' , delimiter = ':' , quoting = csv . QUOTE_NONE ) with open ( 'passwd' , newline = '' ) as f : reader = csv . reader ( f , 'unixpwd' )

A slightly more advanced use of the reader — catching and reporting errors:

import csv , sys filename = 'some.csv' with open ( filename , newline = '' ) as f : reader = csv . reader ( f ) try : for row in reader : print ( row ) except csv . Error as e : sys . exit ( f 'file { filename } , line { reader . line_num } : { e } ' )

And while the module doesn’t directly support parsing strings, it can easily be
done:

import csv for row in csv . reader ([ 'one,two,three' ]): print ( row )

Footnotes
~~~

Rank 3: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [3092, 4089); chunk `815793762db16c0aa8694c52a59ce0d779610375cc953f6f03da5d59f9844a3b`.

~~~text
Return a writer object responsible for converting the user’s data into delimited
strings on the given file-like object. csvfile can be any object with a write() method. If csvfile is a file object, it should be opened with newline='' [ 1 ] . An optional dialect parameter can be given which is used to define a set of parameters specific to a
particular CSV dialect. It may be an instance of a subclass of the Dialect class or one of the strings returned by the list_dialects() function. The other optional fmtparams keyword arguments
can be given to override individual formatting parameters in the current
dialect. For full details about dialects and formatting parameters, see
the Dialects and Formatting Parameters section. To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string. While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data
~~~

### B · q20 · 2/2

How should Python values be bound into sqlite3 SQL statements to avoid SQL injection?

Đáp án cần hỗ trợ: Use placeholders, such as ?, to bind values instead of string formatting.

Rank 1 giữ warning SQL injection và hướng dẫn DB-API parameter substitution bằng placeholder + tuple truyền vào execute; rank 2 có VALUES(?). Bằng chứng tương đương hợp lệ trên trang sqlite3 dù không đúng literal gold quote khai báo.

Rank 1: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [53718, 54562); chunk `fa13dc466ec9d42974f36ac63b33557ac7a9718661bcfbb5756e5cd7d4711980`.

~~~text
### How to use placeholders to bind values in SQL queries

SQL operations usually need to use values from Python variables. However,
beware of using Python’s string operations to assemble queries, as they
are vulnerable to SQL injection attacks . For example, an attacker can simply
close the single quote and inject OR TRUE to select all rows:

>>> # Never do this -- insecure! >>> symbol = input () ' OR TRUE; -- >>> sql = "SELECT * FROM stocks WHERE symbol = ' %s '" % symbol >>> print ( sql ) SELECT * FROM stocks WHERE symbol = '' OR TRUE; --' >>> cur . execute ( sql )

Instead, use the DB-API’s parameter substitution. To insert a variable into a
query string, use a placeholder in the string, and substitute the actual values
into the query by providing them as a tuple of values to the second
argument of the cursor’s execute() method.
~~~

Rank 2: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [63235, 63933); chunk `354bd0aa36a7e7bbdddb612b9462f8f568860e15ef740d870ec9269a7336c1d6`.

~~~text
con = sqlite3 . connect ( ":memory:" ) con . execute ( "CREATE TABLE lang(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE)" ) # Successful, con.commit() is called automatically afterwards with con : con . execute ( "INSERT INTO lang(name) VALUES(?)" , ( "Python" ,)) # con.rollback() is called after the with block finishes with an exception, # the exception is still raised and must be caught try : with con : con . execute ( "INSERT INTO lang(name) VALUES(?)" , ( "Python" ,)) except sqlite3 . IntegrityError : print ( "couldn't add Python twice" ) # Connection object used as context manager only commits or rollbacks transactions, # so the connection object should be closed manually con . close ()
~~~

Rank 3: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [41127, 42070); chunk `96404e351b5edf0fc013fa8da10999b5c8318b860ca9839bd69d65c3fb47dcfa`.

~~~text
Raises :

ProgrammingError – If sql contains more than one SQL statement,
or is not a DML statement.

Example:

rows = [ ( "row1" ,), ( "row2" ,), ] # cur is an sqlite3.Cursor object cur . executemany ( "INSERT INTO data VALUES(?)" , rows )

Note

Any resulting rows are discarded,
including DML statements with RETURNING clauses .

Deprecated since version 3.12, will be removed in version 3.14: DeprecationWarning is emitted if named placeholders are used
and the items in parameters are sequences
instead of dict s.
Starting with Python 3.14, ProgrammingError will
be raised instead.

executescript ( sql_script , / )

Execute the SQL statements in sql_script .
If the autocommit is LEGACY_TRANSACTION_CONTROL and there is a pending transaction,
an implicit COMMIT statement is executed first.
No other implicit transaction control is performed;
any transaction control must be added to sql_script .

sql_script must be a string .

Example:
~~~

### C · q16 · 2/2

User context: restrict retrieval to the official chapter 'File and Directory Access'. In Python 3.13, how does Path.resolve handle a nonexistent path or symlink loop with strict=True versus strict=False?

Đáp án cần hỗ trợ: Strict mode raises OSError. Non-strict mode resolves as far as possible and appends the remainder without existence checks; symlink loops follow the same strict/non-strict error policy in 3.13.

Rank 2 contains Path.resolve and the complete current strict/non-strict behavior for a nonexistent path or symlink loop in the 3.13 snapshot; rank 3 adds the historical version-change note. Rank 1 is the neighboring os.path API, so provenance must distinguish them. The answer is supported without requiring a multi-chunk union.

Rank 1: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [13799, 14755); chunk `0e041a13a302c39d0382da320f043159486f8bcf10dd538d810d285418f2cacf`.

~~~text
Some errors that are handled this way include “access denied”, “not a
directory”, or “bad argument to internal function”. Thus, the
resulting path may be missing or inaccessible, may still contain
links or loops, and may traverse non-directories.

This behavior can be modified by keyword arguments:

If strict is True , the first error encountered when evaluating the path is
re-raised.
In particular, FileNotFoundError is raised if path does not exist,
or another OSError if it is otherwise inaccessible.

If strict is os.path.ALLOW_MISSING , errors other than FileNotFoundError are re-raised (as with strict=True ).
Thus, the returned path will not contain any symbolic links, but the named
file and some of its parent directories may be missing.

Note

This function emulates the operating system’s procedure for making a path
canonical, which differs slightly between Windows and UNIX with respect
to how links and subsequent path components interact.
~~~

Rank 2: [pathlib](https://docs.python.org/3.13/library/pathlib.html), category `File and Directory Access`, span [24388, 25191); chunk `f1a000af0f0a4984d277d60a4e41b80dae00561c2641faa1a3cd13287971529a`.

~~~text
>>> p = Path ( 'tests' ) >>> p PosixPath('tests') >>> p . absolute () PosixPath('/home/antoine/pathlib/tests')

Path. resolve ( strict = False )

Make the path absolute, resolving any symlinks. A new path object is
returned:

>>> p = Path () >>> p PosixPath('.') >>> p . resolve () PosixPath('/home/antoine/pathlib')

“ .. ” components are also eliminated (this is the only method to do so):

>>> p = Path ( 'docs/../setup.py' ) >>> p . resolve () PosixPath('/home/antoine/pathlib/setup.py')

If a path doesn’t exist or a symlink loop is encountered, and strict is True , OSError is raised. If strict is False , the path is
resolved as far as possible and any remainder is appended without checking
whether it exists.

Changed in version 3.6: The strict parameter was added (pre-3.6 behavior is strict).
~~~

Rank 3: [pathlib](https://docs.python.org/3.13/library/pathlib.html), category `File and Directory Access`, span [25193, 25793); chunk `ad41fdf4ee7ceec118c653e5c61344720b3aa68790dc242368ce0a800dab7b30`.

~~~text
Changed in version 3.13: Symlink loops are treated like other errors: OSError is raised in
strict mode, and no exception is raised in non-strict mode. In previous
versions, RuntimeError is raised no matter the value of strict .

Path. readlink ( )

Return the path to which the symbolic link points (as returned by os.readlink() ):

>>> p = Path ( 'mylink' ) >>> p . symlink_to ( 'setup.py' ) >>> p . readlink () PosixPath('setup.py')

Added in version 3.9.

Changed in version 3.13: Raises UnsupportedOperation if os.readlink() is not
available. In previous versions, NotImplementedError was raised.
~~~

### C · q17 · 2/2

Why can commonprefix return an invalid filesystem path, and which function should be used to find a common path prefix?

Đáp án cần hỗ trợ: It works character by character and can return invalid paths; use commonpath for a common path prefix.

Rank 1 chứa cảnh báo trả path không hợp lệ do xét từng ký tự và khuyên dùng commonpath; rank 2 minh họa /usr/l và /usr. Đủ trả lời độc lập với chunk thứ ba không liên quan trực tiếp.

Rank 1: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [2747, 3608); chunk `5b704f9ea7c8f832a3ea1b4c8b4c40ada4020e00db020e4f8aa18c25cb75a044`.

~~~text
Return the longest common sub-path of each pathname in the iterable paths . Raise ValueError if paths contain both absolute
and relative pathnames, if paths are on different drives, or
if paths is empty. Unlike commonprefix() , this returns a
valid path.

Added in version 3.5.

Changed in version 3.6: Accepts a sequence of path-like objects .

Changed in version 3.13: Any iterable can now be passed, rather than just sequences.

os.path. commonprefix ( list , / )

Return the longest string prefix (taken character-by-character) that is a
prefix of all strings in list . If list is empty, return the empty string
( '' ).

Warning

This function may return invalid paths because it works a
character at a time.
If you need a common path prefix , then the algorithm
implemented in this function is not secure. Use commonpath() for finding a common path prefix.
~~~

Rank 2: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [3610, 4531); chunk `0e5c164249e0f4e4a91cb3f8f098f4e928bad37ef3e71ddb654b98dcd6bd6859`.

~~~text
>>> os . path . commonprefix ([ '/usr/lib' , '/usr/local/lib' ]) '/usr/l' >>> os . path . commonpath ([ '/usr/lib' , '/usr/local/lib' ]) '/usr'

Changed in version 3.6: Accepts a path-like object .

os.path. dirname ( path , / )

Return the directory name of pathname path . This is the first element of
the pair returned by passing path to the function split() .

Changed in version 3.6: Accepts a path-like object .

os.path. exists ( path )

Return True if path refers to an existing path or an open
file descriptor. Returns False for broken symbolic links. On
some platforms, this function may return False if permission is
not granted to execute os.stat() on the requested file, even
if the path physically exists.

Changed in version 3.3: path can now be an integer: True is returned if it is an
open file descriptor, False otherwise.

Changed in version 3.6: Accepts a path-like object .

os.path. lexists ( path )
~~~

Rank 3: [os.path](https://docs.python.org/3.13/library/os.path.html), category `File and Directory Access`, span [13799, 14755); chunk `0e041a13a302c39d0382da320f043159486f8bcf10dd538d810d285418f2cacf`.

~~~text
Some errors that are handled this way include “access denied”, “not a
directory”, or “bad argument to internal function”. Thus, the
resulting path may be missing or inaccessible, may still contain
links or loops, and may traverse non-directories.

This behavior can be modified by keyword arguments:

If strict is True , the first error encountered when evaluating the path is
re-raised.
In particular, FileNotFoundError is raised if path does not exist,
or another OSError if it is otherwise inaccessible.

If strict is os.path.ALLOW_MISSING , errors other than FileNotFoundError are re-raised (as with strict=True ).
Thus, the returned path will not contain any symbolic links, but the named
file and some of its parent directories may be missing.

Note

This function emulates the operating system’s procedure for making a path
canonical, which differs slightly between Windows and UNIX with respect
to how links and subsequent path components interact.
~~~

### C · q18 · 2/2

On Windows, when reopening a NamedTemporaryFile with delete=True and delete_on_close=False through builtin open, what must happen before context-manager exit?

Đáp án cần hỗ trợ: Additional opens that do not share delete access must be closed before exiting; otherwise os.unlink on exit raises PermissionError.

Rank 1 giữ trọn ngữ cảnh Windows, ba lựa chọn và điều kiện đóng additional opens trước exit; rank 2 làm rõ delete/delete_on_close. Đủ ngoại lệ PermissionError và truy nguồn tempfile.

Rank 1: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [4746, 5738); chunk `df8accac72f4ad7758f170bd6ea91acb6061d8c4c964f77b9178ed86835bf3dc`.

~~~text
On Windows, make sure that at least one of the following conditions are
fulfilled:

delete is false

additional open shares delete access (e.g. by calling os.open() with the flag O_TEMPORARY )

delete is true but delete_on_close is false. Note, that in this
case the additional opens that do not share delete access (e.g.
created via builtin open() ) must be closed before exiting the
context manager, else the os.unlink() call on context manager
exit will fail with a PermissionError .

On Windows, if delete_on_close is false, and the file is created in a
directory for which the user lacks delete access, then the os.unlink() call on exit of the context manager will fail with a PermissionError .
This cannot happen when delete_on_close is true because delete access is
requested by the open, which fails immediately if the requested access is not
granted.

On POSIX (only), a process that is terminated abruptly with SIGKILL
cannot automatically delete any NamedTemporaryFiles it created.
~~~

Rank 2: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [3788, 4744); chunk `63ecef0f78f670ff3831ebd35813615e511d9679f71b7d55f92573a47199b1fb`.

~~~text
If delete is true (the default) and delete_on_close is true (the
default), the file is deleted as soon as it is closed. If delete is true
and delete_on_close is false, the file is deleted on context manager exit
only, or else when the file-like object is finalized. Deletion is not
always guaranteed in this case (see object.__del__() ). If delete is
false, the value of delete_on_close is ignored.

Therefore to use the name of the temporary file to reopen the file after
closing it, either make sure not to delete the file upon closure (set the delete parameter to be false) or, in case the temporary file is created in
a with statement, set the delete_on_close parameter to be false.
The latter approach is recommended as it provides assistance in automatic
cleaning of the temporary file upon the context manager exit.

Opening the temporary file again by its name while it is still open works as
follows:

On POSIX the file can always be opened again.
~~~

Rank 3: [tempfile](https://docs.python.org/3.13/library/tempfile.html), category `File and Directory Access`, span [7862, 8840); chunk `21b96f020ce37f164ec48f0b25a3c3e71b3bb3de07b02a98329142c08eabdb90`.

~~~text
The directory can be explicitly cleaned up by calling the cleanup() method. If ignore_cleanup_errors is true, any unhandled
exceptions during explicit or implicit cleanup (such as a PermissionError removing open files on Windows) will be ignored,
and the remaining removable items deleted on a “best-effort” basis.
Otherwise, errors will be raised in whatever context cleanup occurs
(the cleanup() call, exiting the context manager, when the object
is garbage-collected or during interpreter shutdown).

The delete parameter can be used to disable cleanup of the directory tree
upon exiting the context. While it may seem unusual for a context manager
to disable the action taken when exiting the context, it can be useful during
debugging or when you need your cleanup behavior to be conditional based on
other logic.

Warning

Cleanup is not robust against the tree being modified while it is removed.
Files outside of the tree may have their permissions and file flags reset.
~~~

### C · q19 · 2/2

User context: restrict retrieval to the official chapter 'File Formats'. Why should CSV files be opened with newline='' when fields can contain newlines or a platform writes CRLF?

Đáp án cần hỗ trợ: Without it, embedded newlines in quoted fields are not interpreted correctly and CRLF platforms may add an extra carriage return on write; csv handles newline translation itself.

Rank 1 là toàn bộ footnote nêu cả quoted embedded newline, extra carriage return trên CRLF và csv tự xử lý newline; các rank còn lại cung cấp cách mở writer/reader. Đủ hai vế câu hỏi.

Rank 1: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [21215, 21515); chunk `f4ce2c234b6ef871430fd8335055b214db80527cda8c0b364399ef30a4bd8679`.

~~~text
If newline='' is not specified, newlines embedded inside quoted fields
will not be interpreted correctly, and on platforms that use \r\n line endings
on write an extra \r will be added. It should always be safe to specify newline='' , since the csv module does its own
( universal ) newline handling.
~~~

Rank 2: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [20362, 21213); chunk `4c066dfce8fe43600df6a5b40be12e83dc8e32e68762b819f2a3fdc825cf2b70`.

~~~text
The same applies to writing in something other than the system default
encoding: specify the encoding argument when opening the output file.

Registering a new dialect:

import csv csv . register_dialect ( 'unixpwd' , delimiter = ':' , quoting = csv . QUOTE_NONE ) with open ( 'passwd' , newline = '' ) as f : reader = csv . reader ( f , 'unixpwd' )

A slightly more advanced use of the reader — catching and reporting errors:

import csv , sys filename = 'some.csv' with open ( filename , newline = '' ) as f : reader = csv . reader ( f ) try : for row in reader : print ( row ) except csv . Error as e : sys . exit ( f 'file { filename } , line { reader . line_num } : { e } ' )

And while the module doesn’t directly support parsing strings, it can easily be
done:

import csv for row in csv . reader ([ 'one,two,three' ]): print ( row )

Footnotes
~~~

Rank 3: [csv](https://docs.python.org/3.13/library/csv.html), category `File Formats`, span [3092, 4089); chunk `815793762db16c0aa8694c52a59ce0d779610375cc953f6f03da5d59f9844a3b`.

~~~text
Return a writer object responsible for converting the user’s data into delimited
strings on the given file-like object. csvfile can be any object with a write() method. If csvfile is a file object, it should be opened with newline='' [ 1 ] . An optional dialect parameter can be given which is used to define a set of parameters specific to a
particular CSV dialect. It may be an instance of a subclass of the Dialect class or one of the strings returned by the list_dialects() function. The other optional fmtparams keyword arguments
can be given to override individual formatting parameters in the current
dialect. For full details about dialects and formatting parameters, see
the Dialects and Formatting Parameters section. To make it
as easy as possible to interface with modules which implement the DB API, the
value None is written as the empty string. While this isn’t a
reversible transformation, it makes it easier to dump SQL NULL data values to
CSV files without preprocessing the data
~~~

### C · q20 · 2/2

How should Python values be bound into sqlite3 SQL statements to avoid SQL injection?

Đáp án cần hỗ trợ: Use placeholders, such as ?, to bind values instead of string formatting.

Rank 1 giữ warning SQL injection và hướng dẫn DB-API parameter substitution bằng placeholder + tuple truyền vào execute; rank 2 có VALUES(?). Bằng chứng tương đương hợp lệ trên trang sqlite3 dù không đúng literal gold quote khai báo.

Rank 1: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [53718, 54562); chunk `fa13dc466ec9d42974f36ac63b33557ac7a9718661bcfbb5756e5cd7d4711980`.

~~~text
### How to use placeholders to bind values in SQL queries

SQL operations usually need to use values from Python variables. However,
beware of using Python’s string operations to assemble queries, as they
are vulnerable to SQL injection attacks . For example, an attacker can simply
close the single quote and inject OR TRUE to select all rows:

>>> # Never do this -- insecure! >>> symbol = input () ' OR TRUE; -- >>> sql = "SELECT * FROM stocks WHERE symbol = ' %s '" % symbol >>> print ( sql ) SELECT * FROM stocks WHERE symbol = '' OR TRUE; --' >>> cur . execute ( sql )

Instead, use the DB-API’s parameter substitution. To insert a variable into a
query string, use a placeholder in the string, and substitute the actual values
into the query by providing them as a tuple of values to the second
argument of the cursor’s execute() method.
~~~

Rank 2: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [63235, 63933); chunk `354bd0aa36a7e7bbdddb612b9462f8f568860e15ef740d870ec9269a7336c1d6`.

~~~text
con = sqlite3 . connect ( ":memory:" ) con . execute ( "CREATE TABLE lang(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE)" ) # Successful, con.commit() is called automatically afterwards with con : con . execute ( "INSERT INTO lang(name) VALUES(?)" , ( "Python" ,)) # con.rollback() is called after the with block finishes with an exception, # the exception is still raised and must be caught try : with con : con . execute ( "INSERT INTO lang(name) VALUES(?)" , ( "Python" ,)) except sqlite3 . IntegrityError : print ( "couldn't add Python twice" ) # Connection object used as context manager only commits or rollbacks transactions, # so the connection object should be closed manually con . close ()
~~~

Rank 3: [sqlite3](https://docs.python.org/3.13/library/sqlite3.html), category `Data Persistence`, span [41127, 42070); chunk `96404e351b5edf0fc013fa8da10999b5c8318b860ca9839bd69d65c3fb47dcfa`.

~~~text
Raises :

ProgrammingError – If sql contains more than one SQL statement,
or is not a DML statement.

Example:

rows = [ ( "row1" ,), ( "row2" ,), ] # cur is an sqlite3.Cursor object cur . executemany ( "INSERT INTO data VALUES(?)" , rows )

Note

Any resulting rows are discarded,
including DML statements with RETURNING clauses .

Deprecated since version 3.12, will be removed in version 3.14: DeprecationWarning is emitted if named placeholders are used
and the items in parameters are sequences
instead of dict s.
Starting with Python 3.14, ProgrammingError will
be raised instead.

executescript ( sql_script , / )

Execute the SQL statements in sql_script .
If the autocommit is LEGACY_TRANSACTION_CONTROL and there is a pending transaction,
an implicit COMMIT statement is executed first.
No other implicit transaction control is performed;
any transaction control must be added to sql_script .

sql_script must be a string .

Example:
~~~

## Metadata — toàn bộ 45 records

Metadata đúng nguồn khác với tuân thủ filter; A/q19/rank3 có metadata đúng nhưng ngoài phạm vi câu hỏi.

| Strategy | Question | Rank | Page | Category | Đủ/đúng | Filter |
|---|---|---:|---|---|---|---|
| A | q16 | 1 | pathlib | File and Directory Access | Có | True |
| A | q16 | 2 | os.path | File and Directory Access | Có | True |
| A | q16 | 3 | pathlib | File and Directory Access | Có | True |
| A | q17 | 1 | os.path | File and Directory Access | Có | N/A |
| A | q17 | 2 | os.path | File and Directory Access | Có | N/A |
| A | q17 | 3 | os.path | File and Directory Access | Có | N/A |
| A | q18 | 1 | tempfile | File and Directory Access | Có | N/A |
| A | q18 | 2 | tempfile | File and Directory Access | Có | N/A |
| A | q18 | 3 | tempfile | File and Directory Access | Có | N/A |
| A | q19 | 1 | csv | File Formats | Có | True |
| A | q19 | 2 | csv | File Formats | Có | True |
| A | q19 | 3 | difflib | Text Processing Services | Có | False |
| A | q20 | 1 | sqlite3 | Data Persistence | Có | N/A |
| A | q20 | 2 | sqlite3 | Data Persistence | Có | N/A |
| A | q20 | 3 | sqlite3 | Data Persistence | Có | N/A |
| B | q16 | 1 | os.path | File and Directory Access | Có | True |
| B | q16 | 2 | pathlib | File and Directory Access | Có | True |
| B | q16 | 3 | pathlib | File and Directory Access | Có | True |
| B | q17 | 1 | os.path | File and Directory Access | Có | N/A |
| B | q17 | 2 | os.path | File and Directory Access | Có | N/A |
| B | q17 | 3 | os.path | File and Directory Access | Có | N/A |
| B | q18 | 1 | tempfile | File and Directory Access | Có | N/A |
| B | q18 | 2 | tempfile | File and Directory Access | Có | N/A |
| B | q18 | 3 | tempfile | File and Directory Access | Có | N/A |
| B | q19 | 1 | csv | File Formats | Có | True |
| B | q19 | 2 | csv | File Formats | Có | True |
| B | q19 | 3 | csv | File Formats | Có | True |
| B | q20 | 1 | sqlite3 | Data Persistence | Có | N/A |
| B | q20 | 2 | sqlite3 | Data Persistence | Có | N/A |
| B | q20 | 3 | sqlite3 | Data Persistence | Có | N/A |
| C | q16 | 1 | os.path | File and Directory Access | Có | True |
| C | q16 | 2 | pathlib | File and Directory Access | Có | True |
| C | q16 | 3 | pathlib | File and Directory Access | Có | True |
| C | q17 | 1 | os.path | File and Directory Access | Có | N/A |
| C | q17 | 2 | os.path | File and Directory Access | Có | N/A |
| C | q17 | 3 | os.path | File and Directory Access | Có | N/A |
| C | q18 | 1 | tempfile | File and Directory Access | Có | N/A |
| C | q18 | 2 | tempfile | File and Directory Access | Có | N/A |
| C | q18 | 3 | tempfile | File and Directory Access | Có | N/A |
| C | q19 | 1 | csv | File Formats | Có | True |
| C | q19 | 2 | csv | File Formats | Có | True |
| C | q19 | 3 | csv | File Formats | Có | True |
| C | q20 | 1 | sqlite3 | Data Persistence | Có | N/A |
| C | q20 | 2 | sqlite3 | Data Persistence | Có | N/A |
| C | q20 | 3 | sqlite3 | Data Persistence | Có | N/A |
