# Bộ câu hỏi và gold evidence

Bản đọc thuận tiện của questions.jsonl đã khóa; không phải thay đổi BENCHMARK.md. Evidence được xác minh trên snapshot trước retrieval.

## q01 · dev · direct

What does Template.is_valid() return when a template contains invalid placeholders?

**Đáp án cần hỗ trợ:** False; those invalid placeholders would make substitute() raise ValueError.

**Nguồn/page:** [py313-string / string](https://docs.python.org/3.13/library/string.html)

**Filter trước truy xuất:** {}

~~~text
is_valid ( )

Returns False if the template has invalid placeholders that will cause substitute() to raise ValueError .
~~~

## q02 · dev · direct

User context: restrict retrieval to the official chapter 'Text Processing Services'. Why is the raw-string spelling r"\n" useful for a regex, and how many characters does that Python string contain?

**Đáp án cần hỗ trợ:** Raw strings do not handle backslashes specially; it contains two characters, a backslash and n, whereas the ordinary literal contains one newline.

**Nguồn/page:** [py313-re / re](https://docs.python.org/3.13/library/re.html)

**Filter trước truy xuất:** {"category": "Text Processing Services"}

~~~text
The solution is to use Python’s raw string notation for regular expression
patterns; backslashes are not handled in any special way in a string literal
prefixed with 'r' . So r"\n" is a two-character string containing '\' and 'n' , while "\n" is a one-character string containing a
newline. Usually patterns will be expressed in Python code using this raw
string notation.
~~~

## q03 · dev · conditional

For SequenceMatcher's default junk heuristic, which sequence is inspected and what length and frequency thresholds apply?

**Đáp án cần hỗ trợ:** Only the second sequence is inspected. If it has at least 200 items, items accounting for more than 1% are treated as junk.

**Nguồn/page:** [py313-difflib / difflib](https://docs.python.org/3.13/library/difflib.html)

**Filter trước truy xuất:** {}

~~~text
The default heuristic is asymmetric : only the second sequence is
inspected when determining what is considered junk, so comparing A to B can
give different results than comparing B to A and reversing the result.

By default, if the second input sequence is at least 200 items long, items
that account for more than 1% it are considered junk .
~~~

## q04 · dev · paraphrase

When dedenting text, do a leading space and a leading tab count as the same common indentation?

**Đáp án cần hỗ trợ:** No. Tabs and spaces are whitespace but not equal, so " hello" and "\thello" have no common leading whitespace.

**Nguồn/page:** [py313-textwrap / textwrap](https://docs.python.org/3.13/library/textwrap.html)

**Filter trước truy xuất:** {}

~~~text
Note that tabs and spaces are both treated as whitespace, but they are not
equal: the lines " hello" and "\thello" are considered to have no
common leading whitespace.
~~~

## q05 · dev · direct

In Unicode normalization, what operations distinguish NFKD from NFKC?

**Đáp án cần hỗ trợ:** NFKD applies compatibility decomposition. NFKC applies compatibility decomposition followed by canonical composition.

**Nguồn/page:** [py313-unicodedata / unicodedata](https://docs.python.org/3.13/library/unicodedata.html)

**Filter trước truy xuất:** {}

~~~text
The normal form KD (NFKD) will apply the compatibility decomposition, that is,
replace all compatibility characters with their equivalents. The normal form KC
(NFKC) first applies the compatibility decomposition, followed by the canonical
composition.
~~~

## q06 · dev · conditional

User context: restrict retrieval to the official chapter 'Binary Data Services'. What mode does struct use if a format string has no prefix, and what happens to alignment padding?

**Đáp án cần hỗ trợ:** Native mode, based on the interpreter's platform/compiler; padding bytes maintain C type alignment in packing and unpacking.

**Nguồn/page:** [py313-struct / struct](https://docs.python.org/3.13/library/struct.html)

**Filter trước truy xuất:** {"category": "Binary Data Services"}

~~~text
When no prefix character is given, native mode is the default. It
packs or unpacks data based on the platform and compiler on which
the Python interpreter was built.
The result of packing a given C struct includes pad bytes which
maintain proper alignment for the C types involved; similarly,
alignment is taken into account when unpacking. In contrast, when
communicating data between external sources, the programmer is
responsible for defining byte ordering and padding between elements.
See Byte Order, Size, and Alignment for details.
~~~

## q07 · dev · conditional

User context: restrict retrieval to the official chapter 'Binary Data Services'. For utf-8-sig, which three bytes are written at the start on encoding and when are they skipped on decoding?

**Đáp án cần hỗ trợ:** 0xef, 0xbb, 0xbf are written first. They are skipped on decoding only if they are the first three bytes; a UTF-8 BOM is generally discouraged.

**Nguồn/page:** [py313-codecs / codecs](https://docs.python.org/3.13/library/codecs.html)

**Filter trước truy xuất:** {"category": "Binary Data Services"}

~~~text
in iso-8859-1), this increases the probability that a utf-8-sig encoding can be
correctly guessed from the byte sequence. So here the BOM is not used to be able
to determine the byte order used for generating the byte sequence, but as a
signature that helps in guessing the encoding. On encoding the utf-8-sig codec
will write 0xef , 0xbb , 0xbf as the first three bytes to the file. On
decoding utf-8-sig will skip those three bytes if they appear as the first
three bytes in the file. In UTF-8, the use of the BOM is discouraged and
should generally be avoided.
~~~

## q08 · dev · paraphrase

Does looking up an absent item in a Counter raise KeyError?

**Đáp án cần hỗ trợ:** No. Counter returns a zero count for a missing item.

**Nguồn/page:** [py313-collections / collections](https://docs.python.org/3.13/library/collections.html)

**Filter trước truy xuất:** {}

~~~text
Counter objects have a dictionary interface except that they return a zero
count for missing items instead of raising a KeyError :
~~~

## q09 · dev · conditional

What happens at the opposite end when new items are appended to an already full bounded deque?

**Đáp án cần hỗ trợ:** A corresponding number of items are discarded from the opposite end; maxlen bounds the deque.

**Nguồn/page:** [py313-collections / collections](https://docs.python.org/3.13/library/collections.html)

**Filter trước truy xuất:** {}

~~~text
If maxlen is not specified or is None , deques may grow to an
arbitrary length. Otherwise, the deque is bounded to the specified maximum
length. Once a bounded length deque is full, when new items are added, a
corresponding number of items are discarded from the opposite end. Bounded
length deques provide functionality similar to the tail filter in
Unix. They are also useful for tracking transactions and other pools of data
where only the most recent activity is of interest.
~~~

## q10 · dev · conditional

Which heap list position gives the smallest item without removing it, and what does heappop do on an empty heap?

**Đáp án cần hỗ trợ:** heap[0] gives the smallest item without popping. heappop raises IndexError if the heap is empty.

**Nguồn/page:** [py313-heapq / heapq](https://docs.python.org/3.13/library/heapq.html)

**Filter trước truy xuất:** {}

~~~text
Pop and return the smallest item from the heap , maintaining the heap
invariant. If the heap is empty, IndexError is raised. To access the
smallest item without popping it, use heap[0] .
~~~

## q11 · dev · conditional

Can several threads safely run bisect or insort_left on the same list while another thread mutates it?

**Đáp án cần hỗ trợ:** No. These functions are not thread-safe; concurrent use or mutation can have undefined behavior, and insort_left may leave the list unsorted.

**Nguồn/page:** [py313-bisect / bisect](https://docs.python.org/3.13/library/bisect.html)

**Filter trước truy xuất:** {}

~~~text
The functions in this module are not thread-safe. If multiple threads
concurrently use bisect functions on the same sequence, this
may result in undefined behaviour. Likewise, if the provided sequence
is mutated by a different thread while a bisect function
is operating on it, the result is undefined. For example, using insort_left() on the same list from multiple threads
may result in the list becoming unsorted.
~~~

## q12 · dev · paraphrase

What bookkeeping mechanism does deepcopy use to avoid repeated copying of objects during the current pass?

**Đáp án cần hỗ trợ:** It keeps a memo dictionary of objects already copied during the current copying pass.

**Nguồn/page:** [py313-copy / copy](https://docs.python.org/3.13/library/copy.html)

**Filter trước truy xuất:** {}

~~~text
The deepcopy() function avoids these problems by:

keeping a memo dictionary of objects already copied during the current
copying pass; and
~~~

## q13 · dev · conditional

What two conditions must hold for a datetime object d to be aware rather than naive?

**Đáp án cần hỗ trợ:** d.tzinfo is not None, and d.tzinfo.utcoffset(d) does not return None. Otherwise d is naive.

**Nguồn/page:** [py313-datetime / datetime](https://docs.python.org/3.13/library/datetime.html)

**Filter trước truy xuất:** {}

~~~text
A datetime object d is aware if both of the following hold:

d.tzinfo is not None

d.tzinfo.utcoffset(d) does not return None

Otherwise, d is naive.
~~~

## q14 · dev · paraphrase

Does constructing Decimal from a float round away the float representation error, or exactly convert the float value?

**Đáp án cần hỗ trợ:** Construction performs an exact conversion of the float's value; using a decimal string avoids importing an existing binary floating-point approximation.

**Nguồn/page:** [py313-decimal / decimal](https://docs.python.org/3.13/library/decimal.html)

**Filter trước truy xuất:** {}

~~~text
Decimal instances can be constructed from integers, strings, floats, or tuples.
Construction from an integer or a float performs an exact conversion of the
value of that integer or float. Decimal numbers include special values such as NaN which stands for “Not a number”, positive and negative Infinity , and -0 :
~~~

## q15 · dev · conditional

Does harmonic_mean validate every subsequent input after it encounters a zero?

**Đáp án cần hỗ trợ:** No. The current algorithm exits early on zero, so later inputs are not tested for validity; this may change in future.

**Nguồn/page:** [py313-statistics / statistics](https://docs.python.org/3.13/library/statistics.html)

**Filter trước truy xuất:** {}

~~~text
The current algorithm has an early-out when it encounters a zero
in the input. This means that the subsequent inputs are not tested
for validity. (This behavior may change in the future.)
~~~

## q16 · test · conditional

User context: restrict retrieval to the official chapter 'File and Directory Access'. In Python 3.13, how does Path.resolve handle a nonexistent path or symlink loop with strict=True versus strict=False?

**Đáp án cần hỗ trợ:** Strict mode raises OSError. Non-strict mode resolves as far as possible and appends the remainder without existence checks; symlink loops follow the same strict/non-strict error policy in 3.13.

**Nguồn/page:** [py313-pathlib / pathlib](https://docs.python.org/3.13/library/pathlib.html)

**Filter trước truy xuất:** {"category": "File and Directory Access"}

~~~text
If a path doesn’t exist or a symlink loop is encountered, and strict is True , OSError is raised. If strict is False , the path is
resolved as far as possible and any remainder is appended without checking
whether it exists.

Changed in version 3.6: The strict parameter was added (pre-3.6 behavior is strict).

Changed in version 3.13: Symlink loops are treated like other errors: OSError is raised in
strict mode, and no exception is raised in non-strict mode. In previous
versions, RuntimeError is raised no matter the value of strict .
~~~

## q17 · test · paraphrase

Why can commonprefix return an invalid filesystem path, and which function should be used to find a common path prefix?

**Đáp án cần hỗ trợ:** It works character by character and can return invalid paths; use commonpath for a common path prefix.

**Nguồn/page:** [py313-os.path / os.path](https://docs.python.org/3.13/library/os.path.html)

**Filter trước truy xuất:** {}

~~~text
This function may return invalid paths because it works a
character at a time.
If you need a common path prefix , then the algorithm
implemented in this function is not secure. Use commonpath() for finding a common path prefix.
~~~

## q18 · test · conditional

On Windows, when reopening a NamedTemporaryFile with delete=True and delete_on_close=False through builtin open, what must happen before context-manager exit?

**Đáp án cần hỗ trợ:** Additional opens that do not share delete access must be closed before exiting; otherwise os.unlink on exit raises PermissionError.

**Nguồn/page:** [py313-tempfile / tempfile](https://docs.python.org/3.13/library/tempfile.html)

**Filter trước truy xuất:** {}

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
~~~

## q19 · test · conditional

User context: restrict retrieval to the official chapter 'File Formats'. Why should CSV files be opened with newline='' when fields can contain newlines or a platform writes CRLF?

**Đáp án cần hỗ trợ:** Without it, embedded newlines in quoted fields are not interpreted correctly and CRLF platforms may add an extra carriage return on write; csv handles newline translation itself.

**Nguồn/page:** [py313-csv / csv](https://docs.python.org/3.13/library/csv.html)

**Filter trước truy xuất:** {"category": "File Formats"}

~~~text
If newline='' is not specified, newlines embedded inside quoted fields
will not be interpreted correctly, and on platforms that use \r\n line endings
on write an extra \r will be added. It should always be safe to specify newline='' , since the csv module does its own
( universal ) newline handling.
~~~

## q20 · test · direct

How should Python values be bound into sqlite3 SQL statements to avoid SQL injection?

**Đáp án cần hỗ trợ:** Use placeholders, such as ?, to bind values instead of string formatting.

**Nguồn/page:** [py313-sqlite3 / sqlite3](https://docs.python.org/3.13/library/sqlite3.html)

**Filter trước truy xuất:** {}

~~~text
Notice that ? placeholders are used to bind data to the query.
Always use placeholders instead of string formatting to bind Python values to SQL statements,
to avoid SQL injection attacks (see How to use placeholders to bind values in SQL queries for more details).
~~~

