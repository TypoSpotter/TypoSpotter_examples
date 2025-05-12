#!/usr/local/bin/perl -w
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
## Searches directory for .cur files
##
$dir = $fullpath;
chomp $dir;  # remove newline character from $dir
print "directory $dir\n";
$filesfound=0;
opendir (DIR, $dir) or die "Could not open $dir\n"; # open directory
# searches directory for .cur file
while ($line = readdir(DIR)) {
 if ($line =~ /\.cur$/) {
  $filesfound++;
  $nfile[$filesfound] = $line;
  print "Found $line\n";
 }
}
die "No .cur files found\n" if $filesfound==0;
print "$filesfound .cur files found\n" if $filesfound>1;
closedir DIR; # close directory

##
## Reads each .cur file and outputs .csv files
##
$header=0;
$i=1;
while ($line = $nfile[$i]) {
  $file = "$dir\\$line"; # determine input file, including path
  print "$file\n";
  open(FILE, $file) or die "Could not open $file\n"; # open file
  $csvfile = "$file\.csv"; # determine .csv file, including path
  open(OUT, ">$csvfile") or die "Could not open $csvfile\n";# open .csv file
  while ($fileline = <FILE>) {
    chomp $fileline;
    if ($fileline !~ /^\$/ && $header == 0) {
      $line1 = $fileline ; chomp $line1;
      $fileline = <FILE>; $line2 = $fileline ; chomp $line2;
      $fileline = <FILE>; $line3 = $fileline ; chomp $line3;
      $fileline = <FILE>; $line4 = $fileline ; chomp $line4;
      $curvetitle = "$line1 : $line4";
      print {OUT} "$line2,$curvetitle\n";
      $header = 1
    }
    if ($fileline =~ /([\d.E+-]+)[\s]+([\d.E+-]+)/ && $header ==1) {
      printf {OUT} ("%.5f %s %.7f\n", $1, ",", $2);
    }
  }
  close OUT;
  $i++
}
