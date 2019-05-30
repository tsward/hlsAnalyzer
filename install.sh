



echo "---Installing HLS Stream Segment Analyzer---"

# TODO: invalid arg check


if [[ "$OSTYPE" == "linux-gnu" ]]; then
        echo "++version 1.1 linux-gnu++"
elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "++version 1.1 OS X++"
else
    echo "Windows not supported."
    exit 1
fi

clean=0

if [ "$1" == "-clean" ]; then
    echo "=performing clean installation="
    clean=1
fi

if [ -d "videos" ]; then 
    if [ "$clean" == 0 ]; then
        echo "videos directory exists, error installing. aborting"
        exit 1
    fi
    rm -rf segmented_videos
fi

if [ -d "segmented_videos" ]; then 
    if [ "$clean" == 0 ]; then
        echo "segmented_videos directory exists, error installing. aborting"
        exit 1
    fi
    rm -rf segmented_videos
fi

if [ -d "log_files" ]; then
    if [ "$clean" == 0 ]; then
        echo "log_files directory exists, error installing. aborting"
        exit 1
    fi
    rm -rf log_files
fi

if [ -d "graphs" ]; then 
    if [ "$clean" == 0 ]; then
        echo "graphs directory exists, error installing. aborting"
        exit 1
    fi
    rm -rf graphs
fi


mkdir videos
mkdir segmented_videos
mkdir log_files
mkdir graphs

echo "---Installation complete!---"

