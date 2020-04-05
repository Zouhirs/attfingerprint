<?php
$servername = "127.0.0.1";
$username = "root";
$password = "";
$dbname = "attendance_ensaf";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error . "\n");
echo "Connected successfully.<br><br>";

$sql = "SELECT `id`, `first_week`, `last_week` FROM subjects";

$result = $conn->query($sql);

while($row = $result->fetch_assoc()) {
    $sql = "CREATE TABLE IF NOT EXISTS ".$row['id']."(id TINYINT(2) NOT NULL,
                                                    first_name VARCHAR(20),
                                                    last_name VARCHAR(40),
                                                    PRIMARY KEY (id),
                                                    FOREIGN KEY (id) REFERENCES students(id),
                                                    FOREIGN KEY (first_name) REFERENCES students(first_name),
                                                    FOREIGN KEY (last_name) REFERENCES students(last_name))";

    $conn->query($sql);

    for ($i=$row['first_week']; $i <= $row['last_week']; $i++) {
      $sql = "ALTER TABLE ".$row['id']."
              ADD S".$i." VARCHAR(2) DEFAULT 'A' ";
      $conn->query($sql);
    }

    $sql = "INSERT IGNORE INTO ".$row['id']." (id, first_name, last_name)
            SELECT id, first_name, last_name FROM students;";

    $conn->query($sql);
}

$conn->close();
?>
