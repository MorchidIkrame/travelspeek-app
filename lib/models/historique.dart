import 'package:isar/isar.dart';
part 'historique.g.dart';

@Collection()
class Historique {
  Id id = Isar.autoIncrement;

  late int userId;
  late int monumentId;
  late DateTime date;

  Historique();
}
