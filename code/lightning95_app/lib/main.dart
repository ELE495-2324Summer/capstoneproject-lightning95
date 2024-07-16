import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(options: firebaseOptions);
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lightning95',
      theme: ThemeData(
        primaryColor: Colors.black,
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final DatabaseReference root = FirebaseDatabase.instance.ref('platform');
  final TextEditingController _textController = TextEditingController();
  String crossedRedLine = '';
  String parkingState = '';
  int plate = 0;
  bool systemInProgress = false;
  String systemState = '';

  @override
  void initState() {
    super.initState();
    getData();
  }

  void getData() {
    root.child('crossed-red-line').onValue.listen((event) {
      setState(() {
        dynamic _crossedRedLine = event.snapshot.value;

        crossedRedLine = _crossedRedLine.toString();
      });
    });

    root.child('parking-state').onValue.listen((event) {
      setState(() {
        dynamic _parkingState = event.snapshot.value;

        if(_parkingState == 'EN_PARKING_NOT_COMPLETED') {
          parkingState = 'Park Bitmedi';
        }

        if(_parkingState == 'EN_PARKING_COMPLETED') {
          parkingState = 'Park Bitti';
        }

        if(_parkingState == 'EN_PARKING_PLATE_NOT_FOUND') {
          parkingState = 'Plaka Yok';
        }
      });
    });

    root.child('plate').onValue.listen((event) {
      setState(() {
        dynamic _plate = event.snapshot.value;

        plate = _plate;
      });
    });

    root.child('system-in-progress').onValue.listen((event) {
      setState(() {
        dynamic _systemInProgress = event.snapshot.value;

        if(_systemInProgress == 'EN_SYSTEM_NOT_IN_PROGRESS') {
          systemInProgress = false;
        }

        else {
          systemInProgress = true;
        }
      });
    });

    root.child('system-state').onValue.listen((event) {
      setState(() {
        dynamic _systemState = event.snapshot.value;

        if(_systemState == 'EN_SYSTEM_SEARCHING') {
          systemState = 'Çizgi Arıyor';
        }

        if(_systemState == 'EN_SYSTEM_LINE_FOLLOWING') {
          systemState = 'Çizgi İzleniyor';
        }

        if(_systemState == 'EN_SYSTEM_TEMP_STATE') {
          systemState = 'Dönüyor';
        }

        if(_systemState == 'EN_SYSTEM_BACKWARD_TURN') {
          systemState = 'Dönüyor';
        }

        if(_systemState == 'EN_SYSTEM_NUMBER_DETECTED') {
          systemState = 'Sayı Okunuyor';
        }

        if(_systemState == 'EN_SYSTEM_RED_LINE') {
          systemState = 'Park Yapılıyor';
        }

        if(_systemState == 'EN_SYSTEM_COMPLETED') {
          systemState = 'Tamamlandı';
        }

        if(_systemState == 'EN_SYSTEM_RESET') {
          systemState = 'Reset';
        }
      });
    });
  }

  void _startStop() {
    setState(() {
      systemInProgress = !systemInProgress;
    });

    root.update({'system-in-progress': systemInProgress ? 'EN_SYSTEM_IN_PROGRESS' : 'EN_SYSTEM_NOT_IN_PROGRESS'});
  }

  void _reset() {
    setState(() {
      root.update({'crossed-red-line': 0});
      root.update({'parking-state': 'EN_PARKING_NOT_COMPLETED'});
      root.update({'plate': 0});
      root.update({'system-in-progress': 'EN_SYSTEM_NOT_IN_PROGRESS'});
      root.update({'system-state': 'EN_SYSTEM_RESET'});
    });
  }
  
  void _plateUpdate() {
    setState(() {
      root.update({'plate': int.tryParse(_textController.text)});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage('assets/background.jpg'),
            fit: BoxFit.cover,
          ),
        ),
        child: Padding(
          padding: const EdgeInsets.all(25),
          child:
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Center(
                child: Image.asset('assets/logo.png'),
              ),
              _inputCard(),
              const SizedBox(height: 1),
              _valueCard('Kırmızı Çizgi İhlali:', crossedRedLine == '0' ? crossedRedLine : '-$crossedRedLine'),
              const SizedBox(width: 10),
              const SizedBox(height: 1),
              _valueCard('Park Durumu:', parkingState),
              const SizedBox(height: 1),
              _valueCard('Plaka:', plate == 0 || plate > 10 ? 'Geçersiz' : plate.toString()),
              const SizedBox(height: 1),
              _valueCard('Çalışma Durumu:', systemInProgress ? 'Çalışıyor' : 'Çalışmıyor'),
              const SizedBox(height: 1),
              _valueCard('Sistem Durumu:', systemState),
              const SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  _startStopButton(),
                  const SizedBox(width: 10),
                  _resetButton(),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _startStopButton() {
    return ElevatedButton(
      onPressed: _startStop,
      style: ElevatedButton.styleFrom(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        backgroundColor: systemInProgress ? Colors.red : Colors.green,
        padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
      ),
      child: Text(
        systemInProgress ? 'Durdur' : 'Başlat',
        style: const TextStyle(fontSize: 20, color: Colors.white, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _resetButton() {
    return ElevatedButton(
      onPressed: _reset,
      style: ElevatedButton.styleFrom(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
        ),
        backgroundColor: Colors.red,
        padding: const EdgeInsets.symmetric(horizontal: 50, vertical: 15),
      ),
      child: const Text(
        'Reset',
        style: TextStyle(fontSize: 20, color: Colors.white, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _valueCard(String title, String value) {
    return Card(
      elevation: 5,
      color: const Color(0x96C78959),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: const TextStyle(fontSize: 18, color: Colors.black, fontWeight: FontWeight.bold),
            ),
            Text(
              value,
              style: const TextStyle(fontSize: 18, color: Colors.white, fontWeight: FontWeight.bold),
            ),
          ],
        ),
      ),
    );
  }

  Widget _inputCard() {
    return Card(
      elevation: 5,
      color: const Color(0x96C78959),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Expanded(
              child: TextField(
              controller: _textController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(
                filled: true,
                fillColor: Colors.white24,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10.0),
                  borderSide: BorderSide.none,
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12.0),
                  borderSide: const BorderSide(
                    color: Colors.white10,
                    width: 2.0,
                  ),
                ),
                labelText: 'Plaka giriniz',
                labelStyle: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              ),
            ),
            const SizedBox(width: 10),
            ElevatedButton(
              onPressed: _plateUpdate,
              style: ElevatedButton.styleFrom(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                backgroundColor: Colors.green,
                padding: const EdgeInsets.symmetric(horizontal: 15, vertical: 15),
              ),
              child: const Text(
                'Güncelle',
                style: TextStyle(fontSize: 20, color: Colors.white, fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
      ),
    );
  }
}