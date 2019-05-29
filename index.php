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




    $dir = "segmented_videos/";
    $videoW = 320;
    $videoH = 240;

    if (is_dir($dir))
    {

        if ($dh = opendir($dir)){
            while (($file = readdir($dh)) !== false){

                if($file != '.' && $file != '..'){
                    echo 
                    "
                        <div style='display: block'>
                            <video width=\"$videoW\" height=\"$videoH\" controls>
                              <source src=\"". $dir . $file ."\" type=\"application/x-mpegURL\">
                            </video>
                        </div>
                    ";

                }

            }

            closedir($dh);

          }
          
    }
    


/*
$dir    = './segmented_videos/demo';
$video_files = [];


$videos = array();
$video_ext = array('m3u8');
#foreach ($video_array as $path) {
    foreach(glob($dir.'/*.*') as $path) {
  if (in_array(pathinfo($path,  PATHINFO_EXTENSION), $video_ext)) {
  //less general, but will work if you know videos always end in mp4
  //if (pathinfo($path, PATHINFO_EXTENSION) == "mp4") {
    $videos[] = $path;
    print $path;
  }
}
*/

/*
foreach(glob($dir.'/*.*') as $file) {
    
    $file_parts = pathinfo($file);
    if ($file_parts['extension'] == "m3u8"){
        $tmp = substr($file, strpos($file, "/") + 1);    
        #print $tmp;
    #if($file_parts == "master.m3u8") {
        echo "<video autoplay>";
        echo "<source src=". $file ." type='video/mp4'>";
        echo "</video><br/>";
        #echo "<a href=\"https://www.w3schools.com/html/\">Visit our HTML tutorial</a>";
        #echo "<br>";
    }
}
*/


/*
$dir    = 'segmented_videos';
$video_files = [];

#echo "<a href=\"segmented_videos/demo/master.m3u8\" style=\"font-size: 25px;\">Demo</a>";


foreach(glob($dir.'/*') as $seg_file) {
    
    $tmp = substr($seg_file, strpos($seg_file, "/") + 1);    
    echo $tmp;
    $eric = "\<a href=segmented_videos"; #demo/master.m3u8\" style=\"font-size: 25px;\">Demo</a>";
    #$eric += "hi";
    echo $eric;
    #list($second) = explode("/", $seg_file);
    # $seg_file = current(explode("/", $seg_file, 1));

    #$tmp = strtok($seg_file, '/');
    #print "$seg_file ";
    #print $hi.$dir # http:// master.m3u8" +  "hey hi";
    #echo "<a href=\"https://" + $dir + "/master.m3u8\">$hi</a>"; #"localhost/masters_project/hlsPlayer/segmented_videos/test\">$boner</a>";
    
    #echo "<a href=\"masters_project/hlsPlayer/segmented_videos/test/master.m3u8\">$hi</a>";
    #echo"<br>";
}
*/
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

