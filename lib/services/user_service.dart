import 'package:isar/isar.dart';
import '../models/user.dart';

class UserService {
  final Isar isar;
  UserService(this.isar);

  Future<void> addUser(User user) async {
    await isar.writeTxn(() async {
      await isar.users.put(user);
    });
  }

  Future<List<User>> getAllUsers() async {
    return await isar.users.where().findAll();
  }

  Future<User?> getUserById(Id id) async {
    return await isar.users.get(id);
  }

  Future<void> deleteUser(Id id) async {
    await isar.writeTxn(() async {
      await isar.users.delete(id);
    });
  }
}
