import 'package:isar/isar.dart';
part 'favoris.g.dart';

@Collection()
class Favoris {
  Id id = Isar.autoIncrement;

  late int userId;
  late int monumentId;
  late DateTime date;

  Favoris();
}
