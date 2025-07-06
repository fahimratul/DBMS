<?php
session_start();

// Log all received data for debugging
error_log("=== DONATION REQUEST DEBUG ===");
error_log("Request method: " . $_SERVER['REQUEST_METHOD']);
error_log("POST data: " . print_r($_POST, true));
error_log("Raw input: " . file_get_contents('php://input'));

// Check if this is a POST request
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    $_SESSION['donation_request_error'] = "Invalid request method: " . $_SERVER['REQUEST_METHOD'];
    header("Location: ../index.php");
    exit();
}

// Check if POST data exists
if (empty($_POST)) {
    $_SESSION['donation_request_error'] = "No POST data received. Raw input: " . substr(file_get_contents('php://input'), 0, 100);
    header("Location: ../index.php");
    exit();
}

// Check for the requestdonation parameter
if (!isset($_POST['requestdonation'])) {
    $_SESSION['donation_request_error'] = "Missing requestdonation parameter. Available keys: " . implode(', ', array_keys($_POST));
    header("Location: ../index.php");
    exit();
}

// Get form data
$name = $_POST['name'] ?? '';
$phone = $_POST['phone'] ?? '';
$emergency = $_POST['emergencynumber'] ?? '';
$district = $_POST['district'] ?? '';
$postal = $_POST['postalcode'] ?? '';
$address = $_POST['address'] ?? '';
$message = $_POST['message'] ?? '';

// Basic validation
$missing = [];
if (empty($name)) $missing[] = 'Name';
if (empty($phone)) $missing[] = 'Phone';
if (empty($district)) $missing[] = 'District';
if (empty($postal)) $missing[] = 'Postal Code';
if (empty($address)) $missing[] = 'Address';

if (!empty($missing)) {
    $_SESSION['donation_request_error'] = "Missing required fields: " . implode(', ', $missing);
    header("Location: ../index.php");
    exit();
}

// Success - simulate database save
$_SESSION['donation_request_success'] = "Donation request received successfully! Name: $name, District: $district";
header("Location: ../index.php");
exit();
?>
