


my $dbh = db_connect();

edit_friend_data($dbh, $form->{id}, $form->{name}, $form->{age}, $form->{birthday}) if $form->{action} eq 'edit';
delete_friend_data($dbh, $form->{id}) if $form->{action} eq 'delete';
insert_friend_data($dbh, $form->{name}, $form->{age}, $form->{birthday}) if $form->{action} eq 'insert';
# #すべてのデータを取得
# $tmpl_var->{friends} = select_all_friends($dbh);

#DB切断
db_disconnect($dbh);

sub insert_friend_data {
  my ($dbh, $name, $age, $birthday) = @_;
  my $sql  = 'insert into ';
     $sql .= 'friends (name, age, birthday) ';
     $sql .= 'values (?, ?, ?)';
  my $sth = $dbh->prepare($sql);
  $sth->execute($name, $age, $birthday);
}

sub edit_friend_data {
  my ($dbh, $id, $name, $age, $birthday) = @_;
  my $sql  = 'update friends ';
     $sql .= 'set name = ?,age = ?,birthday = ? ';
     $sql .= 'where id = ?';

  my $sth = $dbh->prepare($sql);
  $sth->execute($name, $age, $birthday, $id);
}

sub delete_friend_data {
  my ($dbh, $id) = @_;
  my $sql  = 'delete from friends ';
     $sql .= 'where id = ?';

  my $sth = $dbh->prepare($sql);
  $sth->execute($id);
