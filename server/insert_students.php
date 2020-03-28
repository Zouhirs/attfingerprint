<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$conn->query("DROP TABLE `students`");
$sql = 'CREATE TABLE IF NOT EXISTS `students`(`id` TINYINT(2) NOT NULL,
                                              `first_name` VARCHAR(20) NOT NULL,
                                              `last_name` VARCHAR(40) NOT NULL,
                                              `cin` VARCHAR(8) NOT NULL,
                                              `cne` VARCHAR(10) NOT NULL,
                                              PRIMARY KEY(id),
                                              INDEX(first_name),
                                              INDEX(last_name))';
$conn->query($sql);

$content = file_get_contents("/opt/lampp/htdocs/attendance_ensaf/Students_Lists/GSEII2.json");
$data = json_decode($content, true);

$stmnt = $conn->prepare("INSERT IGNORE INTO students(id, first_name, last_name, cin, cne) VALUES (?,?,?,?,?)");
$stmnt->bind_param("issss", $id, $first_name, $last_name, $cin, $cne);

for ($i=0; $i < count($data['students']); $i++) {
  $id = $i;
  $first_name = $data['students'][$i]['first_name'];
  $last_name = $data['students'][$i]['last_name'];
  $cin = $data['students'][$i]['cin'];
  $cne = $data['students'][$i]['cne'];
  $stmnt->execute();
  echo "$first_name $last_name inserted successfully.<br>";
}

$stmnt->close();
$conn->close();
?>
