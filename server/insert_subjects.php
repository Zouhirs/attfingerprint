<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$value = $_GET['real'];
if($value==0){
  $start_times = ["00", "12", "36", "48"];
  $end_times = ["11", "23", "47", "59"];
}elseif($value==1){
  $start_times = ["08:30", "10:30", "14:30", "16:30"];
  $end_times = ["10:30", "12:30", "16:30", "18:30"];
}
$conn->query("DROP TABLE `subjects`");
$sql = "CREATE TABLE IF NOT EXISTS subjects(id VARCHAR(4) NOT NULL PRIMARY KEY,
                                            name VARCHAR(50) NOT NULL,
                                            teacher VARCHAR(20) NOT NULL,
                                            first_week INT(2) NOT NULL,
                                            last_week INT(2) NOT NULL,
                                            day VARCHAR(3) NOT NULL,
                                            start_time VARCHAR(5) NOT NULL,
                                            end_time VARCHAR(5) NOT NULL)";

$conn->query($sql);

$stmnt = $conn->prepare("INSERT INTO subjects(id, name, teacher, first_week, last_week, day, start_time, end_time) VALUES (?,?,?,?,?,?,?,?)");
$stmnt->bind_param("sssiisss", $id, $name, $teacher, $first_week, $last_week, $day, $start_time, $end_time);

$id = "M251";
$name = "Intelligence Artificielle";
$teacher = "H. CHOUGRAD";
$first_week = 1;
$last_week = 8;
$day = "THU";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M252";
$name = "Réseaux De neurones";
$teacher = "M. MELLOULI";
$first_week = 6;
$last_week = 9;
$day = "THU";
$start_time = $start_times[2];
$end_time = $end_times[3];
$stmnt->execute();

$id = "M261";
$name = "Soft Embarqué";
$teacher = "A. MANSOURI";
$first_week = 1;
$last_week = 11;
$day = "WED";
$start_time = $start_times[2];
$end_time = $end_times[3];
$stmnt->execute();

$id = "M262";
$name = "Programmation temps réel";
$teacher = "S. MOTAHHIR";
$first_week = 5;
$last_week = 11;
$day = "SAT";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M271";
$name = "Codage Source et Canal";
$teacher = "M. ALAMI";
$first_week = 1;
$last_week = 10;
$day = "WED";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M272";
$name = "Modulation Analogique et numérique";
$teacher = "H. BELKBIR";
$first_week = 1;
$last_week = 11;
$day = "FRI";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M281";
$name = "Technologie Aéronautique";
$teacher = "M. MELLOULI";
$first_week = 1;
$last_week = 10;
$day = "MON";
$start_time = $start_times[2];
$end_time = $end_times[3];
$stmnt->execute();

$id = "M282";
$name = "Régulation des systèmes avancée";
$teacher = "H. HIHI";
$first_week = 3;
$last_week = 12;
$day = "MON";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M291";
$name = "Electronique RF, HF";
$teacher = "I. EZZAZI";
$first_week = 7;
$last_week = 13;
$day = "TUE";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M292";
$name = "Réseaux Mobiles";
$teacher = "I. EZZAZI";
$first_week = 1;
$last_week = 6;
$day = "TUE";
$start_time = $start_times[0];
$end_time = $end_times[1];
$stmnt->execute();

$id = "M301";
$name = "PFA";
$teacher = "-";
$first_week = 1;
$last_week = 13;
$day = "SAT";
$start_time = $start_times[2];
$end_time = $end_times[3];
$stmnt->execute();

$id = "M311";
$name = "Droit social";
$teacher = "L. ALLA";
$first_week = 1;
$last_week = 12;
$day = "FRI";
$start_time = $start_times[2];
$end_time = $end_times[2];
$stmnt->execute();

$id = "M312";
$name = "Gestion des ressources humaines";
$teacher = "A. SBAI";
$first_week = 8;
$last_week = 13;
$day = "FRI";
$start_time = $start_times[3];
$end_time = $end_times[3];
$stmnt->execute();

$id = "M313";
$name = "Responsabilité sociale de l’entreprise";
$teacher = "A. SBAI";
$first_week = 2;
$last_week = 7;
$day = "FRI";
$start_time = $start_times[3];
$end_time = $end_times[3];
$stmnt->execute();

$id = "M321";
$name = "TEC 4";
$teacher = "K. MADANI";
$first_week = 1;
$last_week = 13;
$day = "TUE";
$start_time = $start_times[2];
$end_time = $end_times[2];
$stmnt->execute();

$id = "M322";
$name = "Anglais 4";
$teacher = "M. DAHBI";
$first_week = 1;
$last_week = 13;
$day = "TUE";
$start_time = $start_times[3];
$end_time = $end_times[3];
$stmnt->execute();

$stmnt->close();
$conn->close();
?>
