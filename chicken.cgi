#!/usr/bin/env perl

use strict;
use warnings;
use Encode;
use utf8;
use CGI;
use DBI;
use Template;
use FindBin;
use File::Basename;
use Data::Dumper;

my $TEMPLATE_DIR    = '/var/www/html/friend/';
my $TEMPLATE_FILE   = 'search.html';
my $SCRIPT  = basename($0);
my $TITLE   = 'Friends_List';
my $VER ='1.0';
my $sucess = undef;

my %ERROR_MESSAGE = (
    nodata => 'データが見つかりません',
    except => '例外が発生しました'
);
#テストのためHTMLヘッダーを一番最初にセット
#※※これで気になる変数をHTMLに表示することができます。※※
print "Content-type: text/html; charset=utf-8\n\n";#cgiを動作させるもの
main();
exit;

sub main {

#テンプレート変数
my $tmpl_var = {
   script => $SCRIPT,
   title  => $TITLE,
   ver    => $VER
};

my $form = post_param();#postされた値をset

$tmpl_var->{form} = $form;

#DB接続
my $dbh = db_connect();
#初期表示の処理
$form->{action} = 'init' unless $form->{action};

$tmpl_var->{search_friends} = search_friend_data($dbh, $form->{where_column}, $form->{search_word}) if $form->{action} eq 'search';
edit_friend_data($dbh, $form->{id}, $form->{name}, $form->{age}, $form->{birthday}) if $form->{action} eq 'edit';
delete_friend_data($dbh, $form->{id}) if $form->{action} eq 'delete';
insert_friend_data($dbh, $form->{name}, $form->{age}, $form->{birthday}) if $form->{action} eq 'insert';



#すべてのデータを取得
$tmpl_var->{friends} = select_all_friends($dbh);

#DB切断
db_disconnect($dbh);

#HTML出力処理
show($tmpl_var);
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
print $output;
}

sub post_param {
  my %form;
  my $obj = new CGI;
  my @names = $obj->param;
  for my $name (@names){
    $form{$name} = $obj->param($name);
  }
  return \%form;
}

sub search_friend_data {
    my ($dbh, $where_column, $search_word) = @_;
    $search_word = '%'. $search_word. '%';

    my $sql = "select * from friends where $where_column like '$search_word'";
    my $sth = $dbh->prepare($sql);
    $sth->execute();

    my @search_friends;
    while(my @row = $sth->fetchrow_array) {
        my ($id, $name, $age, $birthday) = @row;
        push @search_friends, [$id, $name, $age, $birthday];
    }
    return \@search_friends;
}

sub edit_friend_data {
  my ($dbh, $id, $name, $age, $birthday) = @_;
  my $sql  = 'update friends ';
     $sql .= 'set name = ?,age = ?,birthday = ? ';
     $sql .= 'where id = ?';

  my $sth = $dbh->prepare($sql);
  $sth->execute($name, $age, $birthday, $id);
  return $sucess;
}

sub delete_friend_data {
  my ($dbh, $id) = @_;
  my $sql  = 'delete from friends ';
     $sql .= 'where id = ?';

  my $sth = $dbh->prepare($sql);
  $sth->execute($id);
  return $sucess;
}

sub insert_friend_data {
  my ($dbh, $name, $age, $birthday) = @_;
  my $sql  = 'insert into ';
     $sql .= 'friends (name, age, birthday) ';
     $sql .= 'values (?, ?, ?)';
  my $sth = $dbh->prepare($sql);
  $sth->execute($name, $age, $birthday);
}

sub select_all_friends {
   my $dbh = shift;

   my $sql = 'select * from friends';
   my $sth = $dbh->prepare($sql);
   $sth->execute;

   my @friends;
   while(my @row = $sth->fetchrow_array) {
      my ($id, $name, $age, $birthday) = @row;
      #  my $ = @row; #ここに @friendsにSELECT結果を追加する
       push @friends, [$id, $name, $age, $birthday];
  }

  return \@friends;
}

sub db_connect {
   my $dbh = DBI->connect("dbi:SQLite:dbname=friends.db");
   return $dbh;
}

sub db_disconnect {
   my $dbh = shift;
   $dbh->disconnect;
}
