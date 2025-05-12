#!/usr/bin/perl -w
### This perl script will search the specified directory for .csv files and convert them to T-HIS .cur files
### (Single curves are expected)
### First argument should be the directory to search
### If no arguments are supplied then the current working directory will be searched
use Cwd;
my $cwd = cwd();

# Check for supplied command-line argument
# If none supplied, then use the current directory
my $path_exists=0;
if (scalar @ARGV >0) {
    $arg=$ARGV[0];
    print "The first supplied command-line argument is: $arg\n";
    if (-d $arg) {
        print "$arg appears to be a directory\n";
        $path_exists=1;
        $path=$arg;
        if ($path !~ /^\//) {$fullpath=$cwd.$path} else {$fullpath=$path}
    }
} else {
    print "No arguments are supplied, using current directory $cwd\n";
    $path_exists=1;
    $path=$cwd;
    $fullpath=$path;
}
##
## Searches directory for .csv files
##
$dir = $fullpath;
chomp $dir;  # remove newline character from $dir
print "directory $dir\n";
$filesfound=0;
opendir (DIR, $dir) or die "Could not open $dir\n"; # open directory
# searches directory for .csv file
while ($line = readdir(DIR)) {
 if ($line =~ /\.csv$/) {
  $filesfound++;
  $nfile[$filesfound] = $line;
  print "Found $line\n";
 }
}
die "No .csv files found\n" if $filesfound==0;
print "$filesfound .csv files found\n" if $filesfound>1;
closedir DIR; # close directory

##
## Reads each .csv file and outputs .cur files
##
$i=1;
while ($line = $nfile[$i]) {
  $header=0;
  $file = "$dir/$line"; # determine input file, including path
  print "$file\n";
  open(FILE, $file) or die "Could not open $file\n"; # open file
  $outfile = "$file\.cur"; # determine .cur file, including path
  open(OUT, ">$outfile") or die "Could not open $outfile\n";# open output file
  while ($fileline = <FILE>) {
    chomp $fileline;
    #print "IN: $fileline\n";
    #<STDIN>;
    # deal with header first
    if ($header == 0) {
      ($xlabel, $ylabel) = split (',' , $fileline);
      print {OUT} "\n\n\n"; # print 3 blank lines
      print {OUT} "$ylabel\n"; # print y-axis title as fourth line
      $header = 1
    }
    elsif ($header ==1) {
      ($x, $y) = split (',' , $fileline);
      printf {OUT} ("%20.10f %20.10f\n", $x, $y);
    }
  }
  close OUT;
  $i++
}
