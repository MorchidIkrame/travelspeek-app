import 'package:flutter/material.dart';
import 'package:isar/isar.dart';
import 'package:path_provider/path_provider.dart';

import 'models/monument.dart';
import 'models/user.dart';
import 'models/favoris.dart';
import 'models/historique.dart';
import 'models/commentaire.dart';

import 'services/monument_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // فتح قاعدة البيانات مع جميع الـ schemas
  final dir = await getApplicationDocumentsDirectory();
  final isar = await Isar.open(
    [
      MonumentSchema,
      UserSchema,
      FavorisSchema,
      HistoriqueSchema,
      CommentaireSchema,
    ],
    directory: dir.path,
  );

  // إدخال بيانات JSON ديال monuments مرة وحدة
  final monumentService = MonumentService(isar);
  await monumentService.insertMonuments();

  // Debug : عرض عدد monuments فالكونسول
  final monuments = await isar.monuments.where().findAll();
  print('Nombre de monuments : ${monuments.length}');

  runApp(MyApp(isar: isar));
}

class MyApp extends StatelessWidget {
  final Isar isar;
  const MyApp({super.key, required this.isar});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Monuments App',
      home: HomePage(isar: isar),
    );
  }
}

class HomePage extends StatelessWidget {
  final Isar isar;
  const HomePage({super.key, required this.isar});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Liste des Monuments')),
      body: FutureBuilder<List<Monument>>(
        future: isar.monuments.where().findAll(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('Aucun monument trouvé.'));
          }

          final monuments = snapshot.data!;
          return ListView.builder(
            itemCount: monuments.length,
            itemBuilder: (_, index) {
              final monument = monuments[index];
              return ListTile(
                title: Text(monument.nom),
                subtitle: Text(monument.ville),
                // لو بغيت تعرض الصور:
                // leading: monument.images.isNotEmpty
                //     ? Image.asset(monument.images.first, width: 50, height: 50)
                //     : null,
              );
            },
          );
        },
      ),
    );
  }
}
