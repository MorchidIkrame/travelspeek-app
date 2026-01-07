import 'package:isar/isar.dart';

part 'monument.g.dart';

@Collection()
class Monument {
  Id id = Isar.autoIncrement;

  late String nom;
  late String ville;
  late String description;
  late String localisation;
  late List<String> images;

  Monument();

  factory Monument.fromJson(Map<String, dynamic> json) {
    return Monument()
      ..nom = json['nom'] ?? ''
      ..ville = json['ville'] ?? ''
      ..description = json['description'] ?? ''
      ..localisation = json['localisation'] ?? ''
      ..images = List<String>.from(json['images'] ?? []);
  }
}
