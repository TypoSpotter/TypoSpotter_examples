#!/usr/bin/perl -w
use Cwd;
my $cwd = cwd();

### This perl script will extract force vectors and coordinates from an optistruct model
###   - First it will scan the optistruct model for any lines beginning with "FORCE"
###      - When it finds FORCEs it will read in and store the node number, and xyz components
###   - It will scan the optistruct model a second time to find all nodes referenced in the first step
###      - Whenever a node is found, the xyz coordinates are stored
###   - Finally a .csv file will be written out containing: xyz coordinates of every node with a FORCE applied, then xyz components of that force
### The values from the .csv file can be pasted into a spreadsheet, which is used to set up multiple LS-Dyna impact models in the Primer model builder
###
### First argument should be the optistruct model file
##
## Sets $file as the input file
## Sets $out as the output file
##
if (scalar @ARGV >0) {
    $arg=$ARGV[0];
    print "The first supplied command-line argument is: $arg\n";
    if (-f $arg) {
        print "$arg appears to be a file, using $cwd/$arg\n";
        $file=$cwd."/".$arg;
    } else {die "$arg is not a file! Exiting\n"}
} else {
    die "Please provide a filename\n";
}
$out = "$file.csv";                               # this is the output file
print "file $file\n";
##
## Scan model for FORCE lines and read in force id, node id, vector xyz
## Normalise vector xyz to unit magnitude
## Store in arrays @force, @node, @x, @y, @z
##
open(FILE, $file) or die "Could not open $file\n"; # open input file
##
##
while ($fileline = <FILE>) {
    if ( $fileline =~ /^FORCE/ ) {
#        $a = substr($fileline,8,8);
        $b = substr($fileline,16,8);
        $c = substr($fileline,40,8); $c =~ s/(\d)-/${1}E-/;
        $d = substr($fileline,48,8); $d =~ s/(\d)-/${1}E-/;
        $e = substr($fileline,56,8); $e =~ s/(\d)-/${1}E-/;
        $mag = sqrt ($c**2+$d**2+$e**2);
        $c = $c/$mag;
        $d = $d/$mag;
        $e = $e/$mag;
#        push (@force, $a);
        push (@node, $b);
        push (@comp_Fx,$c); push (@comp_Fy,$d); push (@comp_Fz,$e);
    }
}

close FILE;                                           # close file
##
## Now scan model for xyz coordinates for each node
##
open(FILE, $file) or die "Could not open $file\n"; # open input file
##
@x = (); @y = (); @z = ();
$#x = $#node; $#y = $#node; $#z = $#node;
while ($fileline = <FILE>) {
    if ( $fileline =~ /^GRID/ ) {
        $a = substr($fileline,8,8);
        $b = substr($fileline,24,8);
        $c = substr($fileline,32,8);
        $d = substr($fileline,40,8);
#        push (@force, $a); push (@node, $b); push (@x,$c); push (@y,$d); push (@z,$e);
        for ($i=0; $i<scalar(@node); $i++) {
            if ($a == $node[$i]) {
                $x[$i]=$b;
                $y[$i]=$c;
                $z[$i]=$d;
            }
        }
    }
}
close FILE;                                           # close file
##
## Writes output file: csv with force vector then location coordinates
##
open(OUT, ">$out") or die "Could not open $out\n"; # open output file
for ($i=0; $i<$#node; $i++) {
    print {OUT} "$comp_Fx[$i],$comp_Fy[$i],$comp_Fz[$i],$x[$i],$y[$i],$z[$i]\n";
}
close OUT;                                            # close file
print "$out written\nPress Return to quit\n";
<STDIN>;
