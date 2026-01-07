import 'package:isar/isar.dart';
part 'commentaire.g.dart';

@Collection()
class Commentaire {
  Id id = Isar.autoIncrement;

  late int userId;
  late int monumentId;
  late String text;
  late DateTime date;

  Commentaire();
}
