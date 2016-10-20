#!/usr/bin/env perl
use strict;
use warnings;
use Data::Dumper;
use DBI;

my $id = 9;
my $name = 'chip';
my $age = 70;
my $birthday = '1946/10/25';

my $dbh = DBI->connect("dbi:SQLite:dbname=friends.db");
#テーブル情報
#$dbh->do("create table friends(id integer primary key autoincrement, name text, age text, birthday text);");
#登録情報
#$dbh->do("insert into friends (name, age, birthday) values ('yamada', '25', '1990/12/12');");
#$dbh->do("insert into friends (name, age, birthday) values ('yamaguchi', '45', '1980/06/10');");
#$dbh->do("insert into friends (name, age, birthday) values ('satou', '30', '1985/08/01');");
#$dbh->do("insert into friends (name, age, birthday) values ('ikeda', '26', '1989/10/22');");
#$dbh->do("insert into friends (name, age, birthday) values ('kobayashi', '25', '1991/02/22');");

edit_friend_data($dbh, $id, $name, $age, $birthday);
my $friends = select_all_friends($dbh);
print Dumper $friends;




$dbh->disconnect;

print "OK\n";

sub edit_friend_data {
  my ($dbh, $id, $name, $age, $birthday) = @_;
  my $sql  = 'update friends ';
     $sql .= 'set name = ?,age = ?,birthday = ? ';
     $sql .= 'where id = ?';

  my $sth = $dbh->prepare($sql);
  $sth->execute($name, $age, $birthday, $id);
}

sub select_all_friends {
    my $dbh = shift;

    my $sql = 'select * from friends';

    my $sth = $dbh->prepare($sql);
    $sth->execute;

    my @friends;
    while(my @row = $sth->fetchrow_array) {
        my ($id, $name, $age, $birthday) = @row;
        push @friends, [$id, $name, $age, $birthday];
    }

    return \@friends;

}
