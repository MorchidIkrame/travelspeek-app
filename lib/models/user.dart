import 'package:isar/isar.dart';
part 'user.g.dart';

@Collection()
class User {
  Id id = Isar.autoIncrement;

  late String username;
  late String email;
  late String password;

  User();
}
