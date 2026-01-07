import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:isar/isar.dart';
import '../models/monument.dart';

class MonumentService {
  final Isar isar;
  MonumentService(this.isar);

  Future<void> insertMonuments() async {
    final count = await isar.monuments.count();
    if (count > 0) return;

    final jsonString = await rootBundle.loadString('assets/data.json');
    final List list = json.decode(jsonString);

    final monuments = list
        .map((e) => Monument.fromJson(Map<String, dynamic>.from(e)))
        .toList();

    await isar.writeTxn(() async {
      await isar.monuments.putAll(monuments);
    });
  }

  Future<List<Monument>> getAllMonuments() async {
    return await isar.monuments.where().findAll();
  }
}
