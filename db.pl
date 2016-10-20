#!/usr/bin/env perl

use strict;
use warnings;
use DBI;
use Data::Dumper;

my $where_column = 'name';
my $search_word  = 'a';

my $dbh = DBI->connect("dbi:SQLite:dbname=friends.db");
# search_friend_data($dbh, $where_column->('name'), $search_word->('da'));

my $search_friends = search_friend_data($dbh, $where_column, $search_word);

print Dumper $search_friends;
 #$dbh->do("create table friends(id integer primary key autoincrement, name text, age text, birthday text);");
# $dbh->do("insert into friends (name, age, birthday) values ('kamae', '27', '1989/06/03');");
 # $dbh->do("delete from friends where id=34;");
#
# my $sql = 'select * from friends where name like "%d%"';
# # my $sql = 'select * from friends ';
# my $sth = $dbh->prepare($sql);
# $sth->execute;
# #
# while(my @row = $sth->fetchrow_array) {
#     print @row,"\n";
# }
$dbh->disconnect;
print "OK\n";

sub search_friend_data {
   my ($dbh, $where_column, $search_word) = @_;
   $search_word = '%'. $search_word. '%';

   my $sql = "select * from friends where $where_column like '$search_word'";
   my $sth = $dbh->prepare($sql);
   $sth->execute();
#    while(my @row = $sth->fetchrow_array) {
#        print @row,"\n";
#    }
# }
my @search_friends;
   while(my @row = $sth->fetchrow_array) {
       my ($id, $name, $age, $birthday) = @row;
       push @search_friends, [$id, $name, $age, $birthday];
   }
   return \@search_friends;
}
