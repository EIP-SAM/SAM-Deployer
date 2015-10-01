<?php

////////////////////////
// CONSTANTS
///////////////////////
define("TEST_DIR_NAME", "Tests");
define("PRO_FILE_NAME", "Tests.pro");
define("BIN_TEST_NAME", "Tests");

////////////////////////
//Options management
///////////////////////
$options = getopt("d:h", array(
    "clean-start",
    "cs",
    "clean-end",
    "ce",
    "help",
));

if (isset($options['h']) || isset($options['help'])) {
    displayHelp();
    exit;
}

if (empty($options['d'])) {
    echo "Missing target directory ! (option -d)" . PHP_EOL . PHP_EOL;
    exit;
}

$makeCommand = "make";
if (isset($options['cs']) || isset($options['clean-start'])) {
    $makeCommand = "make clean && make";
}

$cleanAfterTest = false;
if (isset($options['ce']) || isset($options['clean-end'])) {
    $cleanAfterTest = true;
}

////////////////////////
//List all Tests content
///////////////////////
$root = $options['d'];
$startPath = getcwd();

$iter = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($root, RecursiveDirectoryIterator::SKIP_DOTS),
        RecursiveIteratorIterator::SELF_FIRST,
	    RecursiveIteratorIterator::CATCH_GET_CHILD // Ignore "Permission denied"
	    );

$paths = array();
foreach ($iter as $path => $dir) {
    if ($dir->isDir() && $dir->getFileName() == TEST_DIR_NAME) {
        $paths[realpath($dir->getPathName())] = getDirContents($path);
    }
}

////////////////////////
//Compile and execute all tests
///////////////////////
foreach ($paths as $path => $content) {
    $retval = -1;
    if (!in_array(PRO_FILE_NAME, $content)){
        echo getColoredString("No " . PRO_FILE_NAME . " found in folder " . $path . PHP_EOL, 'yellow');
        continue;
    }
    chdir($path);
    system('qmake ' . PRO_FILE_NAME, $retval);
    if ($retval == 0) {
        ob_start();
        $lastLine = system($makeCommand, $retval);
        ob_end_clean();
        if ($retval == 0) {
            system('./' . BIN_TEST_NAME, $retval);
            if ($retval == 0) {
                echo getColoredString("Tests OK", 'green') . PHP_EOL;
            } else {
                echo getColoredString("Tests error in" . $path, 'red') . PHP_EOL;
            }
            if ($cleanAfterTest == true) {
                system('make clean', $retval);
                system('rm '. BIN_TEST_NAME, $retval);
                system('rm Makefile', $retval);
            }
        } else {
            echo getColoredString("Error when compiling with Makefile in folder " . $path . PHP_EOL, 'yellow');
        }
    } else {
        echo getColoredString("Error when compiling " . PRO_FILE_NAME . " in folder " . $path . PHP_EOL, 'yellow');
    }
    chdir($startPath);
}

////////////////////////
//Display Help
///////////////////////
function displayHelp() {
    echo "-d 'start_test_dir'\t\t\t : Base dir to found and exec Tests. (Mandatory)" . PHP_EOL;
    echo "--cs / --clean-start\t\t\t : Perform a 'make clean' before compiling Tests" . PHP_EOL;
    echo "--ce / --clean-end\t\t\t : Rm all temp files after running Tests" . PHP_EOL;
    echo "-h / --help \t\t\t\t : Display this help" . PHP_EOL;
}

////////////////////////
//Return given string colored
///////////////////////
function getColoredString($string, $color) {
    $colors = array(
        'red' => '41',
        'green' => '42',
        'cyan' => '46',
        'yellow' => '43',
    );

    $colored_string = "\033[" . $colors[$color] . "m";

    $colored_string .=  $string . "\033[0m";

    return $colored_string;
}

////////////////////////
//Return directory content recurcively
///////////////////////
function getDirContents($dir, &$results = array()){
    $files = scandir($dir);

    foreach($files as $key => $value){
        $path = realpath($dir.DIRECTORY_SEPARATOR.$value);
        if(!is_dir($path)) {
            $results[] = $value;
        } else if(is_dir($path) && $value != "." && $value != "..") {
            getDirContents($path, $results);
            $results[] = $value;
        }
    }

    return $results;
}

?>