# check115.py
# script used to merge John's UTF8 changes into the 1.15 version

import re

file115_orig = "macbain-1.15-base.txt"	# 1.15 created from 1.14 with some importing from JTM to facilitate comparison
file115_conv = "macbain-1.15-new.txt"	# 1.15 base with auto greek conversion
# the real 1.15 is taken from 1.15-new with a few updated comments

fileJTM_orig = "macbain-1.12b.txt"		# orig version from JTM (not used in this script)
fileJTM_conv = "macbain-1.12b-mod.txt"	# orig file with some importing from 1.14 to facilitate comparison

# lines to skip exact match check
skiplines = (
	52,		# comment about encoding - safe to ignore
	14381,	# greek in comment - safe to ignore
	100000)


# -----
# create the 1.15b version with auto-greek conversion
# -----

def convert_greek():
	rxGreek = re.compile(r"@G\[([^]]+)\]")
	
	f115 = open(file115_orig, "r")
	f115b = open(file115_conv, "w")
	
	for line in f115:
		new = ""
		last_char = 0
		for match in rxGreek.finditer(line):
			#print "match: " + match.group(0) + " core: " + match.group(1)
			new += line[last_char:match.start(0)]
			new += "@G[" + fixup_greek(match.group(1)) + "]"
			last_char = match.end(0)
		new += line[last_char:]
	
		f115b.write(new)
		
	f115.close()
	f115b.close()


def fixup_greek(str):
	# multi-char match (longest match first)
	# 5
	str = re.sub(r"e@'@n", r"ε῏", str)	# e@'@nimi ε῏ιμι
	str = re.sub(r"i@'@n", r"ἶ", str)	# ei@'@nmi εἶμι
	str = re.sub(r"u@`@n", r"ὗ", str)	# ou@`@n-tos οὗ-τος (ὖ?)
	str = re.sub(r"u@'@n", r"ὖ", str)
	str = re.sub(r"w@'@n", r"ὦ", str)
	# 4
	str = re.sub(r"a@'/", r"ἄ", str)
	str = re.sub(r"a@`/", r"ἅ", str)
	str = re.sub(r"a@'\\", r"ἂ", str)
	str = re.sub(r"c@'/", r"ἤ", str)
	str = re.sub(r"e@'/", r"ἒ", str)
	str = re.sub(r"e@`/", r"ἕ", str)
	str = re.sub(r"e@'\\", r"ἔ", str)
	str = re.sub(r"e@`\\", r"ἓ", str)
	str = re.sub(r"i@'/", r"ἲ", str)
	str = re.sub(r"i@`/", r"ἵ", str)
	str = re.sub(r"o@'/", r"ὄ", str)
	str = re.sub(r"o@`/", r"ὅ", str)
	str = re.sub(r"u@'/", r"ὔ", str)
	str = re.sub(r"u@`/", r"ὕ", str)
	str = re.sub(r"w@'/", r"ὤ", str)
	# 3
	str = re.sub(r"a@'", r"ἀ", str)
	str = re.sub(r"a@`", r"ἁ", str)
	str = re.sub(r"a@n", r"ᾶ", str)
	str = re.sub(r"c@'", r"ἠ", str)
	str = re.sub(r"c@`", r"ἡ", str)
	str = re.sub(r"c@n", r"ῆ", str)
	str = re.sub(r"e@'", r"ἐ", str)
	str = re.sub(r"e@`", r"ἑ", str)
	str = re.sub(r"e@n", r"ε῀", str)		# review converted accent
	str = re.sub(r"i@'", r"ἰ", str)
	str = re.sub(r"i@`", r"ἱ", str)		# review accent
	str = re.sub(r"i@n", r"ῖ", str)
	str = re.sub(r"o@'", r"ὀ", str)
	str = re.sub(r"o@`", r"ὁ", str)
	str = re.sub(r"o@n", r"ο῀", str)		# review converted accent
	str = re.sub(r"r@`", r"ῥ", str)
	str = re.sub(r"u@'", r"ὐ", str)
	str = re.sub(r"u@`", r"ὑ", str)
	str = re.sub(r"u@n", r"ῦ", str)
	str = re.sub(r"w@'", r"ὠ", str)
	str = re.sub(r"w@n", r"ῶ", str)
	# 2
	str = re.sub(r"c/", r"ή", str)
	str = re.sub(r"ï/", r"ΐ", str)
	str = re.sub(r"s$", r"ς", str)		# final sigma
	str = re.sub(r"s-", r"σ-", str)		# final sigma?
	str = re.sub(r"s\)", r"ς)", str)	# final sigma
	str = re.sub(r"w/", r"ώ", str)
	
	# single char match
	str = re.sub(r"a", r"α", str)
	str = re.sub(r"á", r"ά", str)
	str = re.sub(r"ā", r"ᾱ", str)	# a@-
	str = re.sub(r"b", r"β", str)
	str = re.sub(r"c", r"η", str)
	str = re.sub(r"d", r"δ", str)
	str = re.sub(r"e", r"ε", str)
	str = re.sub(r"é", r"έ", str)
	str = re.sub(r"f", r"φ", str)
	str = re.sub(r"F", r"ϝ", str)	# digamma
	str = re.sub(r"g", r"γ", str)
	str = re.sub(r"h", r"χ", str)
	str = re.sub(r"i", r"ι", str)
	str = re.sub(r"í", r"í", str)
	str = re.sub(r"î", r"î", str)
	str = re.sub(r"k", r"κ", str)
	str = re.sub(r"l", r"λ", str)
	str = re.sub(r"m", r"μ", str)
	str = re.sub(r"n", r"ν", str)
	str = re.sub(r"o", r"ο", str)
	str = re.sub(r"ó", r"ό", str)
	str = re.sub(r"p", r"π", str)
	str = re.sub(r"q", r"θ", str)
	str = re.sub(r"r", r"ρ", str)
	str = re.sub(r"s", r"σ", str)
	str = re.sub(r"t", r"τ", str)
	str = re.sub(r"u", r"υ", str)
	str = re.sub(r"ú", r"ύ", str)
	str = re.sub(r"ū́", r"ῡ́", str)
	str = re.sub(r"v", r"v", str)
	str = re.sub(r"w", r"ω", str)
	str = re.sub(r"x", r"ξ", str)
	str = re.sub(r"y", r"ψ", str)
	str = re.sub(r"z", r"ζ", str)

	# roman
	str = re.sub(r"%", r"f", str)

	return str


# -----
# match 1.15 against JTM's latest version
# -----

def compare():	
	# match entries with sense ids: <a.1> @Ref<as>, @Ref<a.1> [a] [a.1] @Ref[a.1]
	rxSenseIDs = re.compile(r"(@Ref|@G)?([<\[])([^\]\@>\.\d]+)(\.\d+)?([>\]])")
	
	fJTM = open(fileJTM_conv, "r")
	f115 = open(file115_conv, "r")
	
	done = False
	num_diff = 0
	max_diffs = 5
	line_num = 0
	
	skipline_index = 0
	next_skip_line = skiplines[skipline_index]
	
	while done == False:
		line_num += 1
		
		lineJTM = fJTM.readline()
		if lineJTM == "":
			done = True
			break
			
		lineJTM = lineJTM.rstrip("\r\n")
		line115 = f115.readline().rstrip("\r\n")
	
		# check if we should skip this line check
		if line_num == next_skip_line:
			print "skipping ",
			print line_num
			skipline_index += 1
			next_skip_line = skiplines[skipline_index]
			continue
			
		# remove new markup before checking for a match
		new = ""
		last_char = 0
		for match in rxSenseIDs.finditer(line115):
			#if line_num == 11531:
			#	print "match: " + match.group(0) + " core: " + match.group(3)
			new += line115[last_char:match.start(0)]
			new += match.group(2) + match.group(3) + match.group(5)
			last_char = match.end(0)
		new += line115[last_char:]
	
		if lineJTM != new:
			print "*** line : ",
			print line_num
			print "jtm: " + lineJTM
			print "115: " + line115	
			print "new: " + new	

			# note that if new is shorter than lineJTM, this will cause an 'index out of range' error			
			# oh, well.
			for i in range(len(lineJTM)):
				if lineJTM[i] != new[i]:
					startindex = 0
					if i > 10:
						startindex = i-10
					print "index " + `i` + " differs: '" + lineJTM[startindex:i+1] + "' - '" + new[startindex:i+1] + "'"
					break;
					
			num_diff += 1
			if num_diff > max_diffs:
				done = True
	
	fJTM.close()
	f115.close()


# -----
# main
# -----

convert_greek()
compare()

