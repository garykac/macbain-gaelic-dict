# fixup-1.14.pl
# this script removed the cross references from 1.14 and creates 1.14b so that the resulting can be more
# easily compared with macbain-1.13.txt

$szLexName = "macbain-1.14.txt";
$szLexName2 = "mb1.14b.txt";

%Entry = ();
%MultiEntry = ();

init_sortmaps();

# PASS 1 - extract headwords
$fStart = 0;
$nErrors = 0;
$szLastEntry = "";
$szEntry = "";
open(IN, $szLexName);
while(<IN>)
{
	chomp;
	if (m/--page 1/)
		{$fStart = 1;}
	if (!$fStart)
		{next;}
	if (m/^--/)
		{next;}
	if (m/^(†)?<([^>]+)>/)
	{
		$szEntry = $2;
		if (defined($Entry{$szEntry}))
		{
			print "duplicate entry: $szEntry\n";
			$nErrors++;
		}
		$Entry{$szEntry} = 1;
		
		# check sort order
		#if (sortkey($szLastEntry) gt sortkey($szEntry))
		#{
		#	print "incorrect sort order: $szLastEntry (" . sortkey($szLastEntry) . ") > $szEntry (" . sortkey($szEntry) . ")\n";
		#	$nErrors++;
		#}
		$szLastEntry = $szEntry;

		if ($szEntry =~ m/^(.+)\.([0-9])$/)
		{
			if (!defined($MultiEntry{$1}))
			{
				$MultiEntry{$1} = 1;
			}
			if (!defined($Entry{"$1.1"}))
			{
				print "couldn't find $1.1\n";
				$nErrors++;
			}
		}
	}
	elsif (m/^  /)
	{
	}
	else
	{
		die "unrecognized line: $_\n";
	}
}
close(IN);

@Keys = keys(%Entry);
print "$#Keys entries\n";

if ($nErrors != 0)
{
	print "$nErrors errors\n";
	print "Errors found - Terminating\n";
	die;
}

# PASS 2
$fStart = 0;
$nErrors = 0;
$szEntry = "";
open(IN, $szLexName);
open(OUT, ">$szLexName2");
while(<IN>)
{
	chomp;
	if (m/^--/)
	{
		print OUT "$_\n";
		next;
	}
	
	$szLine = $_;
	while ($szLine =~ m/^(.*)\@Ref(.*)$/)
		{$szLine = "$1$2";}
	while ($szLine =~ m/^(.*)([[<])([^]>]+)\.[0-9]([]>])(.*)$/)
		{$szLine = "$1$2$3$4$5";}
	print OUT "$szLine\n";
}
close(OUT);
close(IN);

sub contains
{
	my($szChars, $szStr) = @_;
	
	foreach my $ch (split("",$szChars))
	{
		if (index($szStr, $ch) != -1)
			{return 1;}
	}
	return 0;
}

sub init_sortmaps
{
	%SortMap = ();
	foreach my $k (split(//, "abcdefghijklmnopqrstuvwxyz"))
	{
		$SortMap{$k} = $k;
	}
	foreach my $k (split(//, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
	{
		$SortMap{$k} = lc($k);
	}
	foreach my $k (split(//, ".-' !0123456789"))
	{
		$SortMap{$k} = "";
	}
	foreach my $k (split(/,/, "à=a,è=e,é=e,ì=i,ò=o,ó=o,ù=u"))
	{
		($s1,$s2) = split(/=/,$k);
		$SortMap{$s1} = $s2;
	}
	
}

sub sortkey
{
	my($szStr) = @_;
	
	my $szSort = "";
	foreach my $ch (utf8_split($szStr))
	{
		if (!defined($SortMap{$ch}))
		{
			print "ERROR - unmapped char: '$ch' in $szStr\n";
			die;
		}
		$szSort .= $SortMap{$ch};
	}
	
	#$szSort . ":" . $szStr;
	$szSort;
}

# split a string into an array of utf8 characters
sub utf8_split()
{
	my ($str) = @_;
	my @STR = ();
	
	while ($str ne "")
	{
		my $ch1 = unpack("C",$str);
		if ($ch1 <= 0x7f)
		{
			push(@STR, substr($str,0,1));
			$str = substr($str,1);
		}
		elsif ($ch1 <= 0xdf)
		{
			push(@STR, substr($str,0,2));
			$str = substr($str,2);
		}
		elsif ($ch1 <= 0xef)
		{
			push(@STR, substr($str,0,3));
			$str = substr($str,3);
		}
		else
		{
			push(@STR, substr($str,0,4));
			$str = substr($str,4);
		}
	}
	@STR;
}

