<?php
session_start();
require_once '../configure.php';

// Debug: Log all POST data
error_log("POST data received: " . print_r($_POST, true));
error_log("Request method: " . $_SERVER['REQUEST_METHOD']);
error_log("Content type: " . ($_SERVER['CONTENT_TYPE'] ?? 'not set'));

// Check if this is a POST request
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    $_SESSION['donation_request_error'] = "Invalid request method. Please use the form.";
    header("Location: ../index.php");
    exit();
}

// Check if the connection was successful
if (!$conn) {
    $e = oci_error();
    $_SESSION['donation_request_error'] = "Database connection failed: " . $e['message'];
    header("Location: ../index.php");
    exit();
}


if(isset($_POST['requestdonation'])) {
    error_log("Processing donation request...");
    
    // Get all form data
    $name = $_POST['name'] ?? '';
    $phone = $_POST['phone'] ?? '';
    $emgphone = $_POST['emergencynumber'] ?? '';
    $district = $_POST['district'] ?? '';
    $postalcode = $_POST['postalcode'] ?? '';
    $address = $_POST['address'] ?? '';
    $message = $_POST['message'] ?? '';

    error_log("Form data: name=$name, phone=$phone, district=$district, postalcode=$postalcode, address=$address");

    // Validate inputs
    if(empty($name) || empty($phone) || empty($district) || empty($postalcode) || empty($address)) {
        $_SESSION['donation_request_error'] = "All required fields must be filled. Missing: " . 
            (!empty($name) ? '' : 'Name ') . 
            (!empty($phone) ? '' : 'Phone ') . 
            (!empty($district) ? '' : 'District ') . 
            (!empty($postalcode) ? '' : 'Postal Code ') . 
            (!empty($address) ? '' : 'Address');
        header("Location: ../index.php");
        exit();
    }

    // Sanitize inputs
    $name = htmlspecialchars(strip_tags($name));
    $phone = htmlspecialchars(strip_tags($phone));
    $emgphone = htmlspecialchars(strip_tags($emgphone));
    $district = htmlspecialchars(strip_tags($district));
    $postalcode = htmlspecialchars(strip_tags($postalcode));
    $address = htmlspecialchars(strip_tags($address));
    $message = htmlspecialchars(strip_tags($message));
   // Prepare the SQL statement (remove id from INSERT since it's auto-generated)
    $sql = "INSERT INTO donation_requests (name, phone, emergency_phone, district, postal_code, address, message) 
            VALUES (:name, :phone, :emergency_phone, :district, :postal_code, :address, :message)";
    $stmt = oci_parse($conn, $sql);
    
    if (!$stmt) {
        $e = oci_error($conn);
        $_SESSION['donation_request_error'] = "Error preparing statement: " . $e['message'];
        header("Location: ../index.php");
        exit();
    }
    
    // Bind the parameters
    oci_bind_by_name($stmt, ':name', $name);
    oci_bind_by_name($stmt, ':phone', $phone);
    oci_bind_by_name($stmt, ':emergency_phone', $emgphone);
    oci_bind_by_name($stmt, ':district', $district);
    oci_bind_by_name($stmt, ':postal_code', $postalcode);
    oci_bind_by_name($stmt, ':address', $address);
    oci_bind_by_name($stmt, ':message', $message);

    
    // Execute the statement
    if (oci_execute($stmt)) {
        $_SESSION['donation_request_success'] = "Donation request submitted successfully!";
        header("Location: ../index.php");
    } else {
        $e = oci_error($stmt);
        $_SESSION['donation_request_error'] = "Error submitting donation request: " . $e['message'];
        header("Location: ../index.php");
    }

    // Free the statement and close the connection
    oci_free_statement($stmt);
    oci_close($conn);


}

// If no valid POST request, show debugging info
error_log("No requestdonation parameter found. Available POST keys: " . implode(', ', array_keys($_POST)));
error_log("POST data dump: " . var_export($_POST, true));

$_SESSION['donation_request_error'] = "Invalid request. Please try again. Debug: " . 
    (empty($_POST) ? "No POST data received" : "POST data received but missing 'requestdonation' parameter");
header("Location: ../index.php");
exit();

?>

