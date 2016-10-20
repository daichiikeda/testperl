#!/usr/bin/env perl

use strict;
use warnings;
use Encode;
use utf8;
use CGI;
use Template;
use FindBin;
use File::Basename;
use Data::Dumper;



my $SJIS = Encode::find_encoding('sjis');
my $UTF8 = Encode::find_encoding('utf8');
my $TEMPLATE_DIR    = '/var/www/html/friend/';
my $TEMPLATE_FILE   = 'search.html';
my $SCRIPT  = basename($0);
my $TITLE   = '友達表';
my $VER ='1.0';

main();
exit;

sub main {

   my $tmpl_var = {
       script => $SCRIPT,
       title  => $TITLE,
       ver    => $VER
   };
   $tmpl_var->{name} = 'sample_name';
   show($tmpl_var)
}

sub show {
   my $tmpl = shift;

   my $tt = Template->new({
       ABSOLUTE     => 1,
       INCLUDE_PATH => $TEMPLATE_DIR,
       ENCODING     => 'utf8'
   });

   my $output;
   $tt->process($TEMPLATE_FILE,$tmpl,\$output) or die $tt->error;
   print "Content-type: text/html; charset=utf-8\n\n";
   print $UTF8->encode($output);
}
