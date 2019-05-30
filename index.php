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

        <a href="videos/demo.mp4" download>Demo MP4</a>
        <br><br>
        <video controls>
            <source src="segmented_videos/demo/master.m3u8" type="video/mp4">
        </video>
        <br><br>
        <?php
            /* TODO: get this working
            $dir    = 'segmented_videos';
            $video_files = [];
            foreach(glob($dir.'/*') as $file) {
                foreach(glob($file.'/*') as $seg_file) {
                    $file_parts = pathinfo($seg_file);
                    if ($file_parts['extension'] == "m3u8"){
                        #$tmp = substr($file, strpos($file, "/") + 1);    
                        print $seg_file;
                        echo "<br>";
                        #if($file_parts == "master.m3u8") {
                        echo "<video controls>";
                        echo "<source src=". $seg_file ." type='video/mp4'>";
                        echo "</video><br/>";
                        print "<br>";
                    }
                }
            }
            */
        ?>
        <br><br><br><br>
        <br><br><br><br>
        <a href="../" style="font-size: 20px;">Software Development Home</a>
        <br>
        <a href="../../" style="font-size: 20px;">Home</a>
        </div>
    </body>
</html>

