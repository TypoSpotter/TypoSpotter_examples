#!/usr/bin/perl -w
use Cwd;use File::Copy;use File::Remove 'remove';
my $dir = cwd();

### You would use this script to run femzip_dyna (by SIDACT) to compress LS-Dyna plot files (.ptf)
### The manual process (that users were following before this script was written) is:
###    - Log in to the Linux server and cd to the directory containing the Dyna results
###    - Enter the following command to create a parameter file: femzip_dyna -I model.ptf -P param.txt
###    - Modify the parameter file param.txt
###      - Set appropriate values for required data by changing the number: usually coordinates and effective plastic strain
###    - Enter the following command to create the compressed results file: femzip_dyna -I model.ptf -C param.txt -L 3 -O model_12345.d3plot
### To use this script the user can either:
###    - cd to the directory and invoke the script with no arguments OR
###    - invoke the script with the path to the directory as the first argument
### The script will create the parameter file, modify the parameter file (coordinates and effective plastic strain), and compress the results

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
    }
} else {
    print "No arguments are supplied, using current directory $dir\n";
    $path_exists=1;
    $path=$dir;
}
# Check that we have a valid directory
if ($path_exists==1) {
    #print "\$path is defined as: $path\n";
    #$path =~ s"/$""; print "Removing trailing slash, \$path = $path\n";
    $path = $path."/" if ($path !~ /\/$/); #print "Adding trailing slash where doesn't exist, \$path = $path\n";
    if (-d $path) {print "$path is a valid directory\n"} else {print "$path is not a valid directory\n"}
} else {
    die "No valid directory defined\n"
}

# Search the directory for .ptf files. Stop if no .ptf files found
$filesfound=0;
opendir (DIR, $path) or die "Could not open $path\n"; # open directory
# searches directory for .ptf file
while ($line = readdir(DIR)) {
 if ($line =~ /\.ptf$/) {
  $filesfound++;
  $ptf = $line;
  print "Found $ptf\n";
 }
}
closedir DIR; # close directory
if ($filesfound == 0) {die "No .ptf files found\n"}
##
## Perform file operations
##
# extract directory name from $path if it contains more than one slash
if ($path =~ /(.+)\/([^\/]+)\/$/) {print "more than one slash in path!\n"; $run=$2} else {($run=$path)=~s"/""}
$param = "param.txt";
$d3plot = $run.".d3plot"; #print "\$d3plot = $d3plot\n";
($key = $ptf) =~ s/.ptf$/.key/; #print "\$key = $key\n";
(my $thf = $key) =~ s/.key$/.thf/; #print "\$thf = $thf\n";
my $binout = "binout\*"; my $glstat = "glstat"; 
# Create femzip parameter file
$cmd="femzip_dyna -I $path$ptf -P $path$param";
print "$cmd\n"; system($cmd);
# Confirm that parameter file, then modify lines of parameter file
if (-e "$path$param") {print "Parameter file exists\n";
# First write new parameters to a temporary file
    open(PARAM, "$path$param") or die "Could not open $path$param\n"; # open param file
    open(PARAM2, ">$path$param.temp") or die "Could not open $path$param.temp\n";# open new param file
    while ($fileline = <PARAM>) {
        if ($fileline =~ /coordinates/i) {
            $fileline =~ s/:.+$/:       0.001     /
        } elsif ($fileline =~ /plastic_strain/i) {
            $fileline =~ s/:.+$/:        0.001     /
        }
        print {PARAM2} $fileline
    }
    close PARAM; close PARAM2;
# Then overwrite original parameter file with temp file, then delete temp file
    if (-e "$path$param" && -e "$path$param.temp") {
        copy("$path$param.temp","$path$param") or die "Failed to copy $path$param.temp to $path$param\n";
        remove("$path$param.temp") or die "Failed to remove $path$param.temp\n";
        print "Parameter file successfully modified\n"
    } 
}
# Create femzip compressed file, using parameter file
$cmd="femzip_dyna -L 3 -I $path$ptf -C $path$param -O $path$d3plot";
print "$cmd\n"; system($cmd);
if (-e "$path$d3plot") {print "Femzip file exists\n"}
# Delete useless adptmp, scr00* and d3full* files
$cmd="cd $path; rm -f adptmp\* scr00\* d3full\*";
print "$cmd\n"; system($cmd);

print "$d3plot written\nExiting\n";
