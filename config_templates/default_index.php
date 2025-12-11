<?php
/**
 * Default index file for EzyPanel
 * This file will be copied to new domains when they are created
 */
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to <?php echo htmlspecialchars("$hostname"); ?></title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }
        .container {
            background: #f9f9f9;
            border-radius: 8px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .logo {
            max-width: 150px;
            margin-bottom: 1.5rem;
        }
        .php-info {
            margin-top: 2rem;
            text-align: left;
            background: white;
            padding: 1rem;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9rem;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to <?php echo htmlspecialchars("$hostname"); ?></h1>
        <p>Your website is up and running on EzyPanel!</p>
        
        <div class="php-info">
            <h3>Server Information:</h3>
            <p><strong>PHP Version:</strong> <?php echo phpversion(); ?></p>
            <p><strong>Server Software:</strong> <?php echo $_SERVER['SERVER_SOFTWARE'] ?? 'N/A'; ?></p>    
        </div>
        
        <p style="margin-top: 2rem; color: #666; font-size: 0.9rem;">
            This is a default page. Replace this file with your own content.
        </p>
        <p align="center">
            Hosted with <a href="https://github.com/AhmadShamli/EzyPanel" target="_blank">EzyPanel</a>
        </p>
    </div>
</body>
</html>
