<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
            <title>HLS Streaming</title>
    </head>
    <body background="images/textured_stripes.png">
        <div align="center">
            <h1>HLS Streaming</h1>
            <br><br><br><br>

            <?php

/*
$dir    = './segmented_videos/test';
$video_files = [];

foreach(glob($dir.'/*.*') as $file) {
    $file_parts = pathinfo($file);
    if ($file_parts['extension'] == "m3u8"){
    #print "DUNKING BONERS" ;
    #if($file_parts == "master.m3u8") {
        #print "DUNKING BONERS: ";
        #echo "<video autoplay>";
        #echo "<source src=". $file ." type='video/mp4'>";
        #echo "</video><br/>";
        echo "<a href=\"https://www.w3schools.com/html/\">Visit our HTML tutorial</a>";
        echo "<br>";
    }
}
*/

$dir    = './segmented_videos';
$video_files = [];

echo "<a href=\"segmented_videos/demo/master.m3u8\" style=\"font-size: 25px;\">Demo</a>";



foreach(glob($dir.'/*') as $boner) {
    #print "$boner ";
    #print $boner.$dir # http:// master.m3u8" +  "hey boner";
    #echo "<a href=\"https://" + $dir + "/master.m3u8\">$boner</a>"; #"localhost/masters_project/hlsPlayer/segmented_videos/test\">$boner</a>";
    
    #echo "<a href=\"masters_project/hlsPlayer/segmented_videos/test/master.m3u8\">$boner</a>";
    #echo"<br>";
}

?>
            
            <br><br><br><br>
        <br><br><br><br>
        <a href="../" style="font-size: 20px;">Software Development Home</a>
        <br>
        <!--
        <a href="../.." style="font-size: 20px;">Computer Science Portfolio Home</a>
        <br>
        -->
        <a href="../../" style="font-size: 20px;">Home</a>
        </div>
        </body>
</html>

