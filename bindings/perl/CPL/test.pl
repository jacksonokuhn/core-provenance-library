#
# test.pl
# Core Provenance Library
#
# Copyright 2011
#      The President and Fellows of Harvard College.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE UNIVERSITY OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# Contributor(s): Peter Macko
#

use warnings;
use strict;

use CPL;
use Error qw(:try);
use File::Temp  qw/ tempfile /;

my $ORIGINATOR = "edu.harvard.pass.cpl.perl.test";


#
# Function: Print contents of a hash
#
sub print_hash_ref {
    my ($hash, $prefix) = @_;
	if (!$prefix) { $prefix = "    " }
    
    while (my ($k, $v) = each %$hash) {
		if (ref($v) eq "HASH") {
			print "$prefix$k =>\n";
			print_hash_ref($v, $prefix . "    ");
		}
		else {
			print "$prefix$k => $v\n";
		}
    }
}


#
# Function: Stringify the contents of a hash
#
sub str_hash_ref {
    my ($hash) = @_;
    
    my $str = "";
    while (my ($k, $v) = each %$hash) {
        if ($str ne "") { $str .= ", " }
        $str .= "$k => $v";
    }

    return $str;
}


#
# Function: Print contents of an array
#
sub print_array_ref {
    my ($a, $prefix) = @_;
	if (!$prefix) { $prefix = "    " }
    
    foreach my $v (@$a) {
		if (ref($v) eq "HASH") {
			print "$prefix\{\n";
			print_hash_ref($v, $prefix . "    ");
            print "$prefix\}\n";
		}
		else {
			print "$prefix$v\n";
		}
    }
}


#
# Check whether the array contains the given ID
#
sub array_ref_contains_id {
    my ($a, $find_id) = @_;
    
    foreach my $v (@$a) {
		my $id = $v->{id};
		if (%$id eq %$find_id) {
			return 1;
		}
    }

	return undef;
}


#
# Finds the associated array entry with the given id
#
sub array_ref_find_id {
    my ($a, $find_id) = @_;
    
    foreach my $v (@$a) {
		my $id = $v->{id};
		if (%$id eq %$find_id) {
			return $v;
		}
    }

	return undef;
}



#
# Initialize
#

print "CPL ver. $CPL::VERSION\n";
print "\n";


#
# Open an ODBC connection
#

my $backend_type = "ODBC";

if ($backend_type eq "ODBC") {
	my $connection_string = "DSN=CPL;";
	print "CPL::attach_odbc(\"$connection_string\")";
	CPL::attach_odbc($connection_string);
	print "\n";
}
elsif ($backend_type eq "RDF") {
	my $url_query = "http://localhost:8080/sparql/";
	my $url_update = "http://localhost:8080/update/";
	print "CPL::attach_rdf(\"$url_query\", \"$url_update\")";
	CPL::attach_rdf($url_query, $url_update);
	print "\n";
}
else {
	die "Unsupported backend type: $backend_type";
}

print "CPL::get_current_session()";
my $session = CPL::get_current_session();
print ": " . str_hash_ref($session) . "\n";

print "\n";


#
# Create objects
#

print "CPL::create_object(\"Process A\", \"Proc\")";
my $obj1 = CPL::create_object($ORIGINATOR, "Process A", "Proc");
print ": " . str_hash_ref($obj1) . "\n";

print "CPL::create_object(\"Object A\", \"File\", obj1)";
my $obj2 = CPL::create_object($ORIGINATOR, "Object A", "File", $obj1);
print ": " . str_hash_ref($obj2) . "\n";

print "CPL::create_object(\"Process B\", \"Proc\", obj1)";
my $obj3 = CPL::create_object($ORIGINATOR, "Process B", "Proc", $obj1);
print ": " . str_hash_ref($obj3) . "\n";

print "CPL::create_object(\"Object B\", \"File\", CPL::NONE)";
my $obj4 = CPL::create_object($ORIGINATOR, "Object B", "File", $CPL::NONE);
print ": " . str_hash_ref($obj4) . "\n";

print "CPL::lookup_or_create_object(\"Object B\", \"File\", CPL::NONE)";
my $obj4t = CPL::lookup_or_create_object($ORIGINATOR, "Object B", "File", $CPL::NONE);
print ": " . str_hash_ref($obj4t) . "\n";
if (!CPL::id_eq($obj4, $obj4t)) {die "Object lookup returned the wrong object";}

print "CPL::lookup_or_create_object(\"Object C\", \"File\",  obj1)";
my $obj5 = CPL::lookup_or_create_object($ORIGINATOR, "Object C", "File", $obj1);
print ": " . str_hash_ref($obj5) . "\n";

print "\n";


#
# Lookup objects
#

print "CPL::lookup_object(\"Process A\", \"Proc\")";
my $obj1x = CPL::lookup_object($ORIGINATOR, "Process A", "Proc");
print ": " . str_hash_ref($obj1x) . "\n";
if (%$obj1 ne %$obj1x) { die "Object lookup returned the wrong object"; }

print "CPL::lookup_object(\"Object A\", \"File\")";
my $obj2x = CPL::lookup_object($ORIGINATOR, "Object A", "File");
print ": " . str_hash_ref($obj2x) . "\n";
if (%$obj2 ne %$obj2x) { die "Object lookup returned the wrong object"; }

print "CPL::try_lookup_object(\"Process B\", \"Proc\")";
my $obj3x = CPL::try_lookup_object($ORIGINATOR, "Process B", "Proc");
print ": " . str_hash_ref($obj3x) . "\n";
if (%$obj3 ne %$obj3x) { die "Object lookup returned the wrong object"; }

print "CPL::try_lookup_object(\"Object B\", \"File\")";
my $obj4x = CPL::try_lookup_object($ORIGINATOR, "Object B", "File");
print ": " . str_hash_ref($obj4x) . "\n";
if (!CPL::id_eq($obj4, $obj4x)) {die "Object lookup returned the wrong object";}

print "CPL::try_lookup_object(\"Object C\", \"File\")";
my $obj5x = CPL::lookup_or_create_object($ORIGINATOR, "Object C", "File");
print ": " . str_hash_ref($obj5x) . "\n";
if (!CPL::id_eq($obj5, $obj5x)) {die "Object lookup returned the wrong object";}

print "CPL::try_lookup_object(...should fail...)";
my $objfx = CPL::try_lookup_object($ORIGINATOR, "%%%%%%", "****");
if (!defined($objfx)) { print ": OK\n"; }
if (defined($objfx)) { die "Object lookup did not fail as expected"; }

print "CPL::lookup_all_objects(\"Object A\", \"File\")";
my @obj2all = CPL::lookup_all_objects($ORIGINATOR, "Object A", "File");
my $obj2allok = array_ref_contains_id(\@obj2all, $obj2);
if ($obj2allok) {
	print ": " . ($#obj2all+1) . " elements, OK\n";
}
else {
	print ": " . ($#obj2all+1) . " elements, Fail\n";
	die "Object lookup did not find the requested object";
}

print "CPL::get_all_objects():\n";
my @objall = CPL::get_all_objects();
print "  object 0:\n";
print_hash_ref($objall[0]);
print "  object 1:\n";
print_hash_ref($objall[1]);
print "  object 2:\n";
print_hash_ref($objall[2]);
print "  ... (" . ($#objall+1) . " elements)\n";

print "CPL::get_all_objects_fast():\n";
my @objall_fast = CPL::get_all_objects_fast();
print "  object 0:\n";
print_hash_ref($objall_fast[0]);
print "  object 1:\n";
print_hash_ref($objall_fast[1]);
print "  object 2:\n";
print_hash_ref($objall_fast[2]);
print "  ... (" . ($#objall_fast+1) . " elements)\n";

print "\n";


#
# Data and control flow / dependencies
#

print "CPL::data_flow(obj2, obj1)";
my $r1 = CPL::data_flow($obj2, $obj1);
if (!$r1) { print " [duplicate ignored]" }
print "\n";

print "CPL::data_flow(obj2, obj1, CPL::DATA_INPUT)";
my $r2 = CPL::data_flow($obj2, $obj1, $CPL::DATA_INPUT);
if (!$r2) { print " [duplicate ignored]" }
print "\n";

print "CPL::data_flow(obj3, obj2, CPL::DATA_INPUT)";
my $r3 = CPL::data_flow($obj3, $obj2, $CPL::DATA_INPUT);
if (!$r3) { print " [duplicate ignored]" }
print "\n";

print "CPL::control_flow(obj3, obj1, CPL::CONTROL_START)";
my $r4 = CPL::control_flow($obj3, $obj1, $CPL::CONTROL_START);
if (!$r4) { print " [duplicate ignored]" }
print "\n";

print "CPL::data_flow_ext(obj1, obj3, 0, CPL::DATA_TRANSLATION)";
my $r5 = CPL::data_flow_ext($obj1, $obj3, 0, $CPL::DATA_TRANSLATION);
if (!$r5) { print " [duplicate ignored]" }
print "\n";

print "\n";


#
# Get version
#

print "CPL::get_version(obj1)";
my $ver1 = CPL::get_version($obj1);
printf ": %d\n", $ver1;

print "CPL::get_version(obj2)";
my $ver2 = CPL::get_version($obj2);
printf ": %d\n", $ver2;

print "CPL::get_version(obj3)";
my $ver3 = CPL::get_version($obj3);
printf ": %d\n", $ver3;

print "CPL::get_version(obj4)";
my $ver4 = CPL::get_version($obj4);
printf ": %d\n", $ver4;

print "\n";


#
# Get session info
#

print "CPL::get_session_info(session)";
my %session_info = CPL::get_session_info($session);
print ":\n";
print_hash_ref(\%session_info);
print "\n";


#
# Get object info
#

print "CPL::get_object_info(obj1)";
my %info1 = CPL::get_object_info($obj1);
print ":\n";
print_hash_ref(\%info1);
print "\n";

print "CPL::get_object_info(obj2)";
my %info2 = CPL::get_object_info($obj2);
print ":\n";
print_hash_ref(\%info2);
print "\n";


#
# Get version info
#

print "CPL::get_version_info(obj1, $ver1)";
my %version_info1 = CPL::get_version_info($obj1, $ver1);
print ":\n";
print_hash_ref(\%version_info1);
print "\n";

print "CPL::get_version_info(obj2, $ver2)";
my %version_info2 = CPL::get_version_info($obj2, $ver2);
print ":\n";
print_hash_ref(\%version_info2);
print "\n";


#
# Ancestry
#

print "CPL::get_object_ancestry(obj1, undef, CPL::D_ANCESTORS, 0)";
my @anc1a = CPL::get_object_ancestry($obj1, undef, $CPL::D_ANCESTORS, 0);
print ":\n";
print_array_ref(\@anc1a);
print "\n";

print "CPL::get_object_ancestry(obj1, undef, CPL::D_DESCENDANTS, 0)";
my @anc1d = CPL::get_object_ancestry($obj1, undef, $CPL::D_DESCENDANTS, 0);
print ":\n";
print_array_ref(\@anc1d);
print "\n";

print "CPL::get_object_ancestry(obj1, 0, CPL::D_ANCESTORS)";
my @anc1v0a = CPL::get_object_ancestry($obj1, 0, $CPL::D_ANCESTORS);
print ":\n";
print_array_ref(\@anc1v0a);
print "\n";

print "CPL::get_object_ancestry(obj1, 0, CPL::D_DESCENDANTS, 0)";
my @anc1v0d = CPL::get_object_ancestry($obj1, 0, $CPL::D_DESCENDANTS, 0);
print ":\n";
print_array_ref(\@anc1v0d);
print "\n";

print "CPL::get_object_ancestry(obj1, 0, CPL::D_DESCENDANTS,\n";
print "                         CPL::A_NO_DATA_DEPENDENCIES)";
my @anc1v0d_1 = CPL::get_object_ancestry($obj1, 0, $CPL::D_DESCENDANTS,
        $CPL::A_NO_DATA_DEPENDENCIES);
print ":\n";
print_array_ref(\@anc1v0d_1);
print "\n";

print "CPL::get_object_ancestry(obj1, 0, CPL::D_DESCENDANTS,\n";
print "                         CPL::A_NO_CONTROL_DEPENDENCIES)";
my @anc1v0d_2 = CPL::get_object_ancestry($obj1, 0, $CPL::D_DESCENDANTS,
        $CPL::A_NO_CONTROL_DEPENDENCIES);
print ":\n";
print_array_ref(\@anc1v0d_2);
print "\n";

print "CPL::get_object_ancestry(obj1, 0, CPL::D_DESCENDANTS,\n";
print "        CPL::A_NO_DATA_DEPENDENCIES | CPL::A_NO_CONTROL_DEPENDENCIES)";
my @anc1v0d_3 = CPL::get_object_ancestry($obj1, 0, $CPL::D_DESCENDANTS,
        $CPL::A_NO_DATA_DEPENDENCIES | $CPL::A_NO_CONTROL_DEPENDENCIES);
print ":\n";
print_array_ref(\@anc1v0d_3);
print "\n";


#
# Properties
#

print "CPL::add_property(obj1, \"dog\", \"fido\")";
CPL::add_property($obj1, "dog", "fido");
print ": OK\n";

print "CPL::add_property(obj1, \"dog\", \"bowser\")";
CPL::add_property($obj1, "dog", "bowser");
print ": OK\n";

print "CPL::add_property(obj1, \"cat\", \"kimi\")";
CPL::add_property($obj1, "cat", "kimi");
print ": OK\n";

print "CPL::new_version(obj1)";
my $obj1v_prop = CPL::new_version($obj1);

print "CPL::add_property(obj1, \"dog\", \"gazda\")";
CPL::add_property($obj1, "dog", "gazda");
print ": OK\n";

print "CPL::get_properties(obj1)";
my @prop1 = CPL::get_properties($obj1);
print ":\n";
print_array_ref(\@prop1);
print "\n";

print "CPL::get_properties(obj1, \"dog\")";
my @prop1a = CPL::get_properties($obj1, "dog");
print ":\n";
print_array_ref(\@prop1a);
print "\n";

print "CPL::get_properties(obj1, \"dog\", $obj1v_prop)";
my @prop1b = CPL::get_properties($obj1, "dog", $obj1v_prop);
print ":\n";
print_array_ref(\@prop1b);
print "\n";

my $obj1v_prop_b = $obj1v_prop-1;
print "CPL::get_properties(obj1, undef, $obj1v_prop_b)";
my @prop1c = CPL::get_properties($obj1, undef, $obj1v_prop_b);
print ":\n";
print_array_ref(\@prop1c);
print "\n";

print "CPL::lookup_by_property(\"dog\", \"gazda\")";
my @prop1check = CPL::lookup_by_property("dog", "gazda");
my $prop1check_ok = array_ref_contains_id(\@prop1check, $obj1);
if ($prop1check_ok) {
    my $v = array_ref_find_id(\@prop1check, $obj1);
	print ": " . ($#prop1check+1) . " elements, OK, version = $v->{version}\n";
}
else {
	print ": " . ($#prop1check+1) . " elements, Fail\n";
	die "The object lookup did not find the requested object";
}

print "CPL::try_lookup_by_property(\"cat\", \"kimi\")";
my @prop1check_a = CPL::try_lookup_by_property("cat", "kimi");
my $prop1check_a_ok = array_ref_contains_id(\@prop1check_a, $obj1);
if ($prop1check_a_ok) {
    my $v = array_ref_find_id(\@prop1check_a, $obj1);
	print ": " . ($#prop1check_a+1)." elements, OK, version = $v->{version}\n";
}
else {
	print ": " . ($#prop1check_a+1)." elements, Fail\n";
	die "The object lookup did not find the requested object";
}

print "CPL::try_lookup_by_property(\"dog\", \"---> cat <---\")";
my @prop1check_b = CPL::try_lookup_by_property("dog", "---> cat <---");
if ($#prop1check_b == -1) {
	print ": OK\n";
}
else {
	print ": " . ($#prop1check_b+1)." elements, Fail\n";
	die "The object lookup was not supposed to find any mathing objects";
}

print "\n";


#
# Create a new version
#

printf "CPL::get_version(obj1): %d\n", CPL::get_version($obj1);
printf "CPL::new_version(obj1): %d\n", CPL::new_version($obj1);
printf "CPL::new_version(obj1): %d\n", CPL::new_version($obj1);
printf "CPL::new_version(obj1): %d\n", CPL::new_version($obj1);

print "\n";


#
# File API
#

my ($fh1, $filename1) = tempfile();
print $fh1 "Hello1\n";

my ($fh2, $filename2) = tempfile();
print $fh2 "Hello2\n";

print "CPL::create_object_for_file($filename1)";
my $f1 = CPL::create_object_for_file($filename1);
print ": " . str_hash_ref($f1) . "\n";

print "CPL::get_object_for_file($filename2)";
my $f2 = CPL::get_object_for_file($filename2);
print ": " . str_hash_ref($f2) . "\n";

print "CPL::get_object_for_file($filename1, F_LOOKUP_ONLY)";
my $f1x = CPL::get_object_for_file($filename1, $CPL::F_LOOKUP_ONLY);
print ": " . str_hash_ref($f1x) . "\n";
if (%$f1 ne %$f1x) { die "Object lookup returned the wrong object"; }

close($fh1);
close($fh2);
unlink($filename1);
unlink($filename2);

print "\n";



#
# Error handling
#

my $obj4e;

eval {

    # Should succeed
    $obj4e = CPL::lookup_object($ORIGINATOR, "Object B", "File");

    # Should fail
    my $_v = CPL::get_version($CPL::NONE);

};
if ($@) {
    print "Error handling test - eval: OK\n";
    #print "Error message: $@\n";
}

if (%$obj4e ne %$obj4) {
    die "The object lookup returned a wrong object ID";
}

try {
    
    # Should fail
    my $_v = CPL::get_version($CPL::NONE);
}
catch Error with {
    my $ex = shift;
    print "Error handling test - try/catch: OK\n";
    #print "Error: $ex\n";
};

print "\n";


#
# Close the connection
#

print "CPL::detach()";
CPL::detach();
print "\n";

