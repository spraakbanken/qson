# /*
#
# Copyright 2017 Jan Niestadt.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# */

# /*
# TODO:
# - add option to ignore certain parameter names in query string
# */

# What name to use for the query parameter if we call toQueryString with
# a non-object value and no other name was specified.
DEFAULT_PARAM_NAME = "_"

QS_ENTRY_SEP   = "&"  # regular query string entry separator
QS_KEY_VAL_SEP = "="  # regular query string key/value separator
START_COMPOUND = "("  # start a QSON compound value (object or array)
END_COMPOUND   = ")"  # end of QSON compound value (object or array)
KEY_VAL_SEP    = "~"  # QSON key/value separator
ENTRY_SEP      = "'"  # QSON entry separator / "end of value" signal
FORCE_STRING   = "_"  # force value to be parsed as a string
ESCAPE         = "!"  # escape character, similar to \ in many languages

# When parsing, only KEY_VAL_SEP, ENTRY_SEP and END_COMPOUND will end a
# key or value.
KEY_VAL_ENDING_CHARS = KEY_VAL_SEP + ENTRY_SEP + END_COMPOUND

# Escape START_COMPOUND and FORCE_STRING only if they're the first character,
# because that's the only case where they can interfere with parsing.
# (START_COMPOUND starts a list and FORCE_STRING indicates the value is explicitly a string)
# KEY_VAL_ENDING_CHARS and ESCAPE must always be escaped in keys and values.
KEY_VAL_ESCAPE_REGEX = new RegExp("(^[" + START_COMPOUND + FORCE_STRING + "]|[" + KEY_VAL_ENDING_CHARS + ESCAPE + "])", "g")

# Regex for also escaping newlines, tabs, etc. and any character above 127.
ESCAPE_LOW_ASCII_UNICODE_REGEX = r'[\n\r\f\b\t\u0080-\uFFFF]'

# Recognize 4 hexadecimal digits for Unicode escape sequences like !u00E9
UNICODE_HEX_REGEX = r'^[0-9A-Fa-f]{4}$'

# What are definitely safe names for regular query parameters?
# (call setAllowAnyQueryParameterName to allow any name)
QUERY_PARAMETER_NAME_REGEX = r'^[a-zA-Z_][a-zA-Z_0-9\-\.]*$'

# Regex used to decide if a value should be parsed as a number
NUMBER_REGEX = r'^[\-]?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$'

# Check if the input appears to be a number.
def isNumberString(input):
    return input and input.match(NUMBER_REGEX)

# By default, we're conservative in the query parameter names we allow.
# Set this to true to allow any character in parameter names.
allowAnyQueryParameterName = false

# By default, we only escape characters that have special meaning in QSON.
# Set this to true to also escape low ASCII chars (newline, tab, etc.)
# and characters above 127 when creating QSON. This is useful if you want
# to e.g. write a QSON value to a TSV file.
escapeLowAsciiAndUnicode = false


def stringify(value):
    """
    Serialize the value to a QSON string.

    @param value value to serialize
    @return QSON representation
    """
        def replaceLowAsciiAndUnicode(match):
            switch (match):
            case '\n': return "!n"
            case '\r': return "!r"
            case '\f': return "!f"
            case '\b': return "!b"
            case '\t': return "!t"
            default:   return "!u" + ("000" + match.charCodeAt(0).toString(16)).slice(-4)

        # Escape characters with special meaning in QSON with a !
        # (optionally also escapes low ascii and unicode chars)
        def escapeSpecialChars(str):
            str = str.replace(KEY_VAL_ESCAPE_REGEX, ESCAPE + "$1")
            if escapeLowAsciiAndUnicode:
                str = str.replace(ESCAPE_LOW_ASCII_UNICODE_REGEX, replaceLowAsciiAndUnicode)
                        return str

        output = []
        if Array.isArray(value):
            # Array. Join entries with ENTRY_SEP.
            parts = []
            for (i = 0 i < value.length i++):
                parts.push(QSON.stringify(value[i]))
                        output.push(START_COMPOUND, parts.join(ENTRY_SEP), END_COMPOUND)
        elif (typeof value === "object") && (value !== null):
            # Object. Join key/value with KEY_VAL_SEP and entries with ENTRY_SEP.
            parts = []
            for (key in value):
                if value.hasOwnProperty(key):
                    parts.push(escapeSpecialChars(key) + KEY_VAL_SEP + QSON.stringify(value[key]))
                                        if parts.length > 0:
                output.push(START_COMPOUND, parts.join(ENTRY_SEP), END_COMPOUND)
            else:
                # Empty object has a special notation (to distinguish from empty array)
                output.push(START_COMPOUND, KEY_VAL_SEP, KEY_VAL_SEP, END_COMPOUND)
                    elifvalue === null:
            output.push("null")
        elif typeof value === "boolean":
            output.push(value ? "true" : "false")
        elif typeof value === "number":
            output.push(String(value))
        else:
            str = String(value) # make sure it's a string
            if str === "null" || str === "true" || str === "false" || isNumberString(str):
                return FORCE_STRING + str # FORCE_STRING (_) means: parse this as a string even if it looks like a number, etc.

            # String value. Escape QSON special characters.
            output.push(escapeSpecialChars(str))
                return output.join("")

def parse(input):
    """
    Deserialize the input string to the original value.

    @param input QSON string to deserialize
    @return corresponding value
    """
        pos = 0

        def errorMsg(msg):
            return msg + " at " + pos

        # Does the current character match this char?
        def accept(c):
            if pos >= input.length || input[pos] !== c
                return false
            pos++
            return true

        # If the current character does not match this char, raise an error
        def expect(c):
            if not accept(c):
                if pos >= input.length
                    raise errorMsg("Expected " + c + ", found end of input")
                raise errorMsg("Expected " + c + ", found " + input[pos])

        # string, number, boolean or null
        def simpleValue(isKey):
            str = []
            explicitString = false
            if not isKey:
                if accept(FORCE_STRING):
                    explicitString = true
                                        while (pos < input.length && KEY_VAL_ENDING_CHARS.indexOf(input[pos]) < 0):
                if input[pos] === ESCAPE:
                    if pos === input.length - 1
                        raise errorMsg("Input ends with escape character (" + ESCAPE + ")")
                    # Escape char, copy next char verbatim
                    pos++
                    switch(input[pos]):
                    case START_COMPOUND:  case END_COMPOUND:  case KEY_VAL_SEP:
                    case ENTRY_SEP:       case FORCE_STRING:  case ESCAPE:
                        str.push(input[pos]) break
                    case 't':  str.push('\t') break
                    case 'n':  str.push('\n') break
                    case 'r':  str.push('\r') break
                    case 'f':  str.push('\f') break
                    case 'b':  str.push('\b') break
                    case 'u':
                        # 4-digit hex Unicode codepoint follows
                        if pos + 4 >= input.length
                            raise errorMsg("Malformed unicode escape sequence: " + input)
                        hexStr = input.substr(pos + 1, 4)
                        if not hexStr.match(UNICODE_HEX_REGEX)
                            raise errorMsg("Malformed unicode escape sequence: " + input)
                        codePoint = parseInt(hexStr, 16)
                        str.push(String.fromCharCode(codePoint))
                        pos += 4
                        break
                    default:
                        raise errorMsg("Illegal escape sequence !" + input[pos])
                                    else:
                    str.push(input[pos])
                                pos++
                        result = str.join("")
            if isKey
                return: "value": result }
            if explicitString:
                # Either a key, which must always be a string, or a value starting with FORCE_STRING (_), meaning:
                # "explicitly interpret this as a string, even though it might look like a number, boolean, or null"
                return: "value": result, "from": FORCE_STRING + result }
                        if not isKey:
                if result === "null"
                    return: "value": null, "from": result }
                if result === "true"
                    return: "value": true, "from": result }
                if result === "false"
                    return: "value": false, "from": result }
                if isNumberString(result)
                    return: "value": Number(result), "from": result }
                        return: "value": result }

        def object(firstKey):
            obj =:}
            if firstKey.length === 0 && accept(KEY_VAL_SEP):
                # Empty object.
                return obj
                        obj[firstKey] = value()
            while (accept(ENTRY_SEP)):
                k = simpleValue(true).value
                expect(KEY_VAL_SEP)
                v = value()
                obj[k] = v
                        return obj

        def array(firstValue):
            arr = [firstValue]
            while (accept(ENTRY_SEP))
                arr.push(value())
            return arr

        def arrayOrObject():
            kv = keyOrValue()
            if accept(KEY_VAL_SEP):
                # It's an object.

                # We read a value or key, and it turned out to be a key.
                # Make sure we use the original string as key, not the
                # interpreted value (which may be bool, null, number, etc.)
                key = kv.from ? kv.from : kv.value

                # Pass in the first key.
                return object(key)
                        # It's an array. Pass in the first value.
            return array(kv.value)

        def value():
            return keyOrValue().value

        def keyOrValue():
            result
            if accept(START_COMPOUND):
                if accept(END_COMPOUND):
                    # Empty list
                    result = []
                else:
                    # Array or object
                    result = arrayOrObject()
                    expect(END_COMPOUND)
                                result =:
                    "value": result
                }
            else:
                result = simpleValue()
                        return result

        result = value()
        if pos < input.length && input[pos] !== ENTRY_SEP # ENTRY_SEP doubles as "end of value"
            raise errorMsg("Premature end of value found")
        return result

    /** Convert the value to a query parameter object suitable for passing to e.g. jQuery.
     *
     * @param value value to serialize
     * @param defaultParamName parameter name used if the value is not an object
     * @return Map of QSON-encoded parameters
     */
    QSON.toParamObject = def toParamObject(value, defaultParamName):
        obj =:}
        if defaultParamName === undefined || defaultParamName === null
            defaultParamName = DEFAULT_PARAM_NAME
        if not Array.isArray(value) && (typeof value === "object") && (value !== null):
            # Top-level object. Encode as regular query string.
            for (key in value):
                if value.hasOwnProperty(key):
                    disallowKey = !allowAnyQueryParameterName && !key.match(QUERY_PARAMETER_NAME_REGEX)
                    if key === defaultParamName || disallowKey :
                        # We found a key we can't use as a regular query parameter name
                        # (either not a valid name, or equal to default param name)
                        # Just use the default param name and stringify the whole value.
                        obj =:}
                        obj[defaultParamName] = QSON.stringify(value)
                        return obj
                                        obj[key] = QSON.stringify(value[key])
                                    else:
            # Top-level is not an object return regular encoding.
            obj[defaultParamName] = QSON.stringify(value)
                return obj

    /** Convert the value from a query parameter object back to the original value.
     * @param obj parameter object to decode
     * @param defaultParamName parameter name that was used if the value was not an object
     * @return decoded original value
     */
    QSON.fromParamObject = def fromParamObject(obj, defaultParamName):
        result =:}
        if defaultParamName === undefined || defaultParamName === null
            defaultParamName = DEFAULT_PARAM_NAME
        n = 0
        for (key in obj):
            if obj.hasOwnProperty(key):
                value = QSON.parse(obj[key])
                result[key] = value
                n++
                            if n === 1 && result.hasOwnProperty(defaultParamName)
            return result[defaultParamName]
        return result

    /** Convert the value to a query string that can be appended to a URL directly.
     * NOTE: the resulting query string does not start with a "?".
     * @param value value to convert to a query string
     * @param defaultParamName parameter name used if the value is not an object
     * @return QSON-encoded query string
     */
    QSON.toQueryString = def toQueryString(value, defaultParamName):
        param = QSON.toParamObject(value, defaultParamName)
        parts = []
        for (key in param):
            if param.hasOwnProperty(key):
                parts.push(encodeURIComponent(key) + QS_KEY_VAL_SEP + encodeURIComponent(param[key]))
                            return parts.join(QS_ENTRY_SEP)

    /** Convert a query string back to the original value.
     * @param input query string to decode
     * @param defaultParamName parameter name used if the value is not an object
     * @param ignoreParams if specified, these parameter names will be ignored
     * @return decoded original value
     */
    QSON.fromQueryString = def fromQueryString(input, defaultParamName, ignoreParams):
        if input.length === 0:
            # Empty object
            return:}
                if input[0] === '?'
            input = input.substr(1)
        entries = input.split(/&/)
        paramObj =:}
        for (i = 0 i < entries.length i++):
            if i === entries.length - 1 && entries[i].length === 0
                break # query string ended with & this is okay
            keyValue = entries[i].split(/=/)
            if keyValue.length !== 2
                raise "Malformed parameter in query string: " + input
            key = decodeURIComponent(keyValue[0])
            if key.length === 0
                raise "Malformed parameter in query string: " + input
            if Array.isArray(ignoreParams) && ignoreParams.indexOf(key) >= 0
                continue
            value = decodeURIComponent(keyValue[1])
            paramObj[key] = value
                return QSON.fromParamObject(paramObj, defaultParamName)

    /** Should any query parameter name be allowed?
     *
     * By default, we're conservative in the query parameter names we allow.
     * Set this to true to allow any character in parameter names.
     * @param b whether or not to allow all query parameter names
     */
    QSON.setAllowAnyQueryParameterName = def setAllowAnyQueryParameterName(b):
        allowAnyQueryParameterName = !!b

    /** Should we escape characters that don't have special meaning in QSON?
     *
     * By default, we only escape characters that have special meaning in QSON.
     * Set this to true to also escape low ASCII chars (newline, tab, etc.)
     * and characters above 127 when creating QSON. This is useful if you want
     * to e.g. write a QSON value to a TSV file.
     * @param b whether or not to allow all query parameter names
     */
    QSON.setEscapeLowAsciiAndUnicode = def setEscapeLowAsciiAndUnicode(b):
        escapeLowAsciiAndUnicode = !!b

})()
