import pytest

from qson.qson import stringify


def _test_stringify(v, e):
    r = stringify(v)
    assert v == e


def _test_encode(v, e_s, e_qs):
    s = stringify(v)
    assert s == e_s
    assert parse(s) == v


@pytest.mark.parametrize('value,expected',[
    ('', ''),
])
def test_stringify(value, expected):
    _test_stringify(value, expected)

#
#
# def init():
#
#
#
# 	document.getElementById("decoded").value = ''
#
# 	unitTests()
#
#
#
# 	# If we have a query string, try to decode it as an QSON query string and put the JSON in the input box.
#
# 	var search = location.search
#
# 	var usingGitHubPreview = search.substr(0, 19) === "?https:#github.com"
#
# 	if search and search.length > 1 and !usingGitHubPreview:
#
# 		search = search.substr(1)
#
# 		var result = undefined
#
# 		try:
#
# 			result = QSON.fromQueryString(search)
#
# 		except Exception as e:
#
# 			alert("Couldn't parse: " + search)
#
# 			raise e
#
# 		if result:
#
# 			document.getElementById("input").value = JSON.stringify(result, null, 2)
#
#
#
# 		test(true)
#
#
#
# def test(appendToDecoded):
#
#
#
# 	# See if we can parse the JSON
#
# 	var inputEl = document.getElementById("input")
#
# 	try:
#
# 		var inputJson = inputEl.value
#
# 		var input = JSON.parse(inputJson)
#
# 		var compactedLength = JSON.stringify(input).length
#
# 		var optComp = compactedLength != inputJson.length ? " (" + compactedLength + " without whitespace)" : ""
#
# 		document.getElementById("inputMsg").innerHTML = inputJson.length + " chars" + optComp
#
# 		inputEl.style.backgroundColor = "#fff"
#
# 	except Exception as e:
#
# 		inputEl.style.backgroundColor = "#fdd"
#
# 		return
#
#
#
# 	# Encode to QSON
#
# 	var encoded = QSON.stringify(input)
#
# 	var altEncoded = QSON.toQueryString(input)
#
# 	document.getElementById("encoded").value = "stringify():\n" + encoded + "\n\ntoQueryString():\n" + altEncoded
#
# 	var orig = inputJson.length
#
# 	def calcSavings(orig, newVal): var v = Math.round(100 * (newVal - orig) / orig) if v > 0) return "+" + v else return "" + v 	var savings = [ calcSavings(compactedLength, encoded.length), calcSavings(compactedLength, altEncoded.length ]
#
# 	document.getElementById("encodedMsg").innerHTML = encoded.length + " / " + altEncoded.length + " chars (" + savings[0] + " / " + savings[1] + "%)"
#
#
#
# 	# Decode and encode to JSON again, and compare with the original input.
#
#
#
# 	var decoded = QSON.parse(encoded)
#
# 	var decodedJson = JSON.stringify(decoded)
#
# 	var output = "parse():\n" + decodedJson + "\n"
#
# 	var error = false
#
# 	if decodedJson !== JSON.stringify(input):
#
# 		output += "(ERROR)"
#
# 		error = true
#
# 	else:
#
# 		output += "(OK)"
#
#
#
# 	var altDecoded = QSON.fromQueryString(altEncoded)
#
# 	var altDecodedJson = JSON.stringify(altDecoded)
#
# 	output += "\n\nfromQueryString():\n" + altDecodedJson + "\n"
#
# 	if altDecodedJson !== JSON.stringify(input):
#
# 		output += "(ERROR)"
#
# 		error = true
#
# 	else:
#
# 		output += "(OK)"
#
#
#
# 	document.getElementById("decodedMsg").innerHTML = decodedJson.length + " chars"
#
#
#
# 	var decodedEl = document.getElementById("decoded")
#
# 	if !appendToDecoded
#
# 		decodedEl.value = ''
#
# 	decodedEl.value += output
#
# 	decodedEl.style.backgroundColor = error ? "#fdd" : "#fff"
#
#
#
# def unitTests():
#
#
#
# 	var anyFailed = false
#
#
#
# 	var decodedEl = document.getElementById("decoded")
#
#
#
# 	def output(msg):
#
# 		decodedEl.value += msg + "\n"
#
#
#
# 	def test(name, value, expected, expectError):
#
# 		var v = JSON.stringify(value)
#
# 		var e = JSON.stringify(expected)
#
# 		if v !== e:
#
# 			output("FAIL " + name + ": Expected " + (expectError ? "exception" : e) + ", got " + v)
#
# 			anyFailed = true
#
# 		else:
#
# 			output("SUCCESS " + name + ": " + v)
#
#
#
# 	def onError(name, expected, expectError, e):
#
# 		if expectError:
#
# 			output("SUCCESS " + name + ": errored as expected")
#
# 		else:
#
# 			output("FAIL " + name + ": Expected " + expected + ", got exception")
#
# 			anyFailed = true
#
# 			console.log("Exception for test '" + name + "':")
#
# 			console.log(e)
#
#
#
# 	def map():
#
# 		var result =:
#
# 		for (var i = 0 i < arguments.length i += 2):
#
# 			result[arguments[i]] = arguments[i + 1]
#
# 				return result
#
#
#
# 	def list():
#
# 		var result = []
#
# 		for (var i = 0 i < arguments.length i++):
#
# 			result.push(arguments[i])
#
# 				return result
#
#
#
# def testEncode(name, value, expStringified, expQueryString):
#
#   try:
#
# 	var a = QSON.stringify(value)
#
# 	test(name + " stringify", a, expStringified)
#
#   except Exception as e:
#
# 	output("FAIL " + name + " stringify " + JSON.stringify(value) + ": Expected " + JSON.stringify(expStringified) + ", threw an exception")
#
# 			raise e
#
#
#
# 		try:
#
# 			var b = QSON.parse(a)
#
# 			test(name + " parse", b, value)
#
# 		except Exception as e:
#
# 			output("FAIL " + name + " parse " + a + ": Expected " + JSON.stringify(value) + ", threw an exception")
#
# 			raise e
#
#
#
# 		try:
#
# 			var c = QSON.toQueryString(value)
#
# 			test(name + " toQueryString", c, expQueryString)
#
# 		except Exception as e:
#
# 			output("FAIL " + name + " toQueryString " + JSON.stringify(value) + ": Expected " + JSON.stringify(expQueryString) + ", threw an exception")
#
# 			raise e
#
#
#
# 		try:
#
# 			var d = QSON.fromQueryString(c)
#
# 			test(name + " fromQueryString", d, value)
#
# 		except Exception as e:
#
# 			output("FAIL " + name + " fromQueryString " + c + ": Expected " + JSON.stringify(value) + ", threw an exception")
#
# 			raise e
#
#
#
# 	def testDecodeQueryString(name, queryString, expected, expectError):
#
# 		try:
#
# 			test(name, QSON.fromQueryString(queryString, null, ["ignoreThis"]), expected, expectError)
#
# 		except Exception as e:
#
# 			onError(name, expected, expectError, e)
#
#
#
# 	def testDecodeQsonValue(name, qsonValue, expected, expectError):
#
# 		try:
#
# 			test(name, QSON.parse(qsonValue), expected, expectError)
#
# 		except Exception as e:
#
# 			onError(name, expected, expectError, e)
#
#
#
# 	def allowAnyName(b):
#
# 		QSON.setAllowAnyQueryParameterName(b)
#
#
#
# 	def introduceEscapes(b):
#
# 		QSON.setEscapeLowAsciiAndUnicode(b)
#
#
#
# def test_perform_tests():
#
# 	# NOTE: this test code is directly portable between Java and JavaScript!
#
#
#
# 	# Special values
#
@pytest.mark.parametrize('name,value,ex_stringify,ex_query_string', [
    ("empty string", "", "", "_="),

    ("string", "a", "a", "_=a"),

    ("None", None, "null", "_=null"),

    ("True", True, "true", "_=true"),

    ("False", False, "false", "_=false"),

    ("1", 1, "1", "_=1"),
    ("1", 1.0, "1.0", "_=1.0"),

    ("1.2", 1.2, "1.2", "_=1.2"),

    ("1e3", 1e3, "1000.0", "_=1000.0"),

    ("1e-20", 1e-20, "1e-20", "_=1e-20"),

    ("null string", "null", "_null", "_=_null"),
    ("none string", "none", "_null", "_=_null"),
    ("None string", "None", "_null", "_=_null"),

    ("1 string", "1", "_1", "_=_1"),

    ("1.0 string", "1", "_1", "_=_1"),



# 	 URL encoding

    ("URL-encoding 1", "a\nb", "a\nb", "_=a%0Ab"),

    ("URL-encoding 2", "a & b", "a & b", "_=a%20%26%20b"),

    ("URL-encoding 3", {"a&b": 3}, "(a&b~3)", "_=(a%26b~3)"),

    ("URL-encoding 4", "a + b", "a + b", "_=a%20%2B%20b"),



# 	 Arrays

    ("simple array 1", [1.0], "(1.0)", "_=(1.0)"),

    ("simple array 2", [1, 2, 3], "(1'2'3)", "_=(1'2'3)"),

    ("empty array", [], "()", "_=()"),



# 	 Objects
     ("simple object 1", {"a": 3}, "(a~3)", "a=3"),

("simple object 2", {"a": 3, "b": "c"}, "(a~3'b~c)", "a=3&b=c"),

    ("empty key", {"": 3}, "(~3)", "_=(~3)"),

    ("empty key and value", {"": ""}, "(~)", "_=(~)"),

    ("empty object", {}, "(~~)", ""),

    ("whitespace 1", {" a ": " b "}, "( a ~ b )", "_=(%20a%20~%20b%20)"),

    ("whitespace 2", {"a": " b "}, "(a~ b )", "a=%20b%20"),

    ("special char keys", {"(": 1, "!": 2, "_": 3}, "(!(~1'!!~2'!_~3)", "_=(!(~1'!!~2'!_~3)"),

    ("key starts with _", {"_a": "b"}, "(!_a~b)", "_a=b"),

    ("key contains _", {"a_b": "c"}, "(a_b~c)", "a_b=c"),

    ("key containing number", {"a1": "b"}, "(a1~b)", "a1=b"),

    ("key starts with number", {"1a": "b"}, "(1a~b)", "_=(1a~b)"),

    ("key containing dash and dot", {"a.b": "c", "a-b": "d"}, "(a.b~c'a-b~d)", "a.b=c&a-b=d"),

    ("key starting with dot", {".a": "b"}, "(.a~b)", "_=(.a~b)"),

    ("keys that look like values 1", {"null": 3}, "(null~3)", "null=3"),
    ("keys that look like values 2", {"null": 3.0}, "(null~3.0)", "null=3.0"),

    ("keys that look like values 3", {"1.2": 3.4}, "(1.2~3.4)", "_=(1.2~3.4)"),

    ("nested structures in object (int)",
        {
            "a": [1, 2],
            "b": {
                "c": {
                    "d": "e"
                },
            },
            "f": [[[3]]]
        },
        "(a~(1'2)'b~(c~(d~e))'f~(((3))))",
        "a=(1'2)&b=(c~(d~e))&f=(((3)))"
    ),
    ("nested structures in object (float)",
        {
            "a": [1.0, 2.0],
            "b": {
                "c": {
                    "d": "e"
                },
            },
            "f": [[[3.0]]]
        },
        "(a~(1.0'2.0)'b~(c~(d~e))'f~(((3.0))))",
        "a=(1.0'2.0)&b=(c~(d~e))&f=(((3.0)))"
    ),
])
def test_encode(name, value, ex_stringify, ex_query_string):
    _test_encode(value, ex_stringify, ex_query_string)
#
#
#
# 	allowAnyName(true)
#
# 	testEncode("allow any query parameter name", map(" ", 1.0, "|", 2.0, "\u00e9", 3.0), "( ~1'|~2'\u00e9~3)", "%20=1&%7C=2&%C3%A9=3")
#
# 	allowAnyName(false)
#
#
#
# 	introduceEscapes(true)
#
# 	testEncode("introduce escapes low ascii", "\n\r\f\b\t", "!n!r!f!b!t", "_=!n!r!f!b!t")
#
# 	testEncode("introduce escapes unicode", "\u00e9", "!u00e9", "_=!u00e9")
#
# 	introduceEscapes(false)
#
#
#
# 	# Below tests values that are never returned from stringify() or toQueryString()
#
# 	# some are valid, some invalid Qson values.
#
#
#
# 	testDecodeQueryString("special parameter name", "a=b&_=c", map("a", "b", "_", "c"), false)
#
# 	testDecodeQueryString("query string ending in &", "a=b&", map("a", "b"), false)
#
# 	testDecodeQueryString("query string starting with ?", "?a=b", map("a", "b"), false)
#
# 	testDecodeQueryString("invalid query string starting with &", "&a=b", null, true)
#
# 	testDecodeQueryString("invalid query string &&", "a=b&&c=d", null, true)
#
# 	testDecodeQueryString("invalid query string no =", "a", null, true)
#
# 	testDecodeQueryString("invalid query string empty key", "=1", null, true)
#
# 	testDecodeQueryString("ignore parameter", "a=b&ignoreThis=2", map("a", "b"), false)
#
#
#
# 	testDecodeQsonValue("key starting with underscore 1", "(_1~3)", map("_1", 3.0), false)
#
# 	testDecodeQsonValue("key starting with underscore 2", "(a~b'_1~3)", map("a", "b", "_1", 3.0), false)
#
# 	testDecodeQsonValue("end of value character", "1'2", 1.0, false)
#
# 	testDecodeQsonValue("illegal string 2", "1~2", null, true)
#
# 	testDecodeQsonValue("illegal string 3", "1)2", null, true)
#
# 	testDecodeQsonValue("illegal string 4", "(1", null, true)
#
# 	testDecodeQsonValue("forced empty string", "_", "", false)
#
# 	testDecodeQsonValue("malformed object 1", "(a~b')", null, true)
#
# 	testDecodeQsonValue("malformed object 2", "('a~b)", null, true)
#
# 	testDecodeQsonValue("malformed object 3", "(a~b'c)", null, true)
#
#
#
# 	# Escapes
#
# 	testDecodeQsonValue("character escapes", "!n!r!f!b", "\n\r\f\b", false)
#
# 	testDecodeQsonValue("unicode escapes", "!u0041!u00e9!u03A3!u306C", "\u0041\u00e9\u03A3\u306C", false)
#
# 	testDecodeQsonValue("illegal escape 1", "Test!", null, true)
#
# 	testDecodeQsonValue("illegal escape 2", "!q", null, true)
#
# 	testDecodeQsonValue("illegal unicode escape 1", "!u007", null, true)
#
# 	testDecodeQsonValue("illegal unicode escape 2", "!uBABY", null, true)
#
#
#
