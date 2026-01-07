import 'package:isar/isar.dart';
import '../models/favoris.dart';

class FavorisService {
  final Isar isar;

  FavorisService(this.isar);

  /// إضافة favoris جديد
  Future<void> addFavoris(Favoris favoris) async {
    await isar.writeTxn(() async {
      await isar.favoris.put(favoris); // الاسم صحيح هنا
    });
  }

  /// استرجاع جميع favoris ديال user محدد
  Future<List<Favoris>> getFavorisByUser(int userId) async {
    return await isar.favoris
        .filter()
        .userIdEqualTo(userId)
        .findAll();
  }

  /// حذف favoris باستعمال id
  Future<void> removeFavoris(Id id) async {
    await isar.writeTxn(() async {
      await isar.favoris.delete(id);
    });
  }

  /// التحقق واش favoris موجود مسبقاً
  Future<bool> isFavorisExist(int userId, int monumentId) async {
    final count = await isar.favoris
        .filter()
        .userIdEqualTo(userId)
        .and()
        .monumentIdEqualTo(monumentId)
        .count();
    return count > 0;
  }
}
