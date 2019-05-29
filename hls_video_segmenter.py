#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hls_video_segmenter.py
#
#
#

import os
import glob
import argparse
import subprocess
import shlex
import json
import pprint



class Stream:
    def __init__(self, h, w, br, fps):
        self.height = h
        self.width = w
        self.bit_rate = br
        self.fps = fps
    
    def __str__(self):
        return ('Resolution: ' + str(self.height) + 'x' + str(self.width) +
                '; bit rate: ' + str(self.bit_rate) + '; fps: ' + str(self.fps))


def run_ffmpeg(video_file_loc, streams, extra_params=''):
    """"""
    n_streams = len(streams)
    # TODO: case where >= 10 streams
    video_data = get_video_stream(video_file_loc)
    fps = video_data.fps 
    extra_param_str = ''
    for token in extra_params:
        extra_param_str += token 
    video_file = video_file_loc.split('/')[len(video_file_loc.split('/'))-1]
    cur_dir_root = video_file_loc.split('/')[0]
    seg_loc = 'segmented_videos/'       
    cmd = 'ffmpeg -i ' + video_file_loc + ' '
    if n_streams > 1:
        tmp_line = '-filter_complex "[v:0]split=' + str(n_streams)
        for i in range(0, n_streams):
            if i < n_streams - 1:
                tmp_line += '[vtemp00' + str(i+1) + ']'
            else:
                tmp_line += '[vout00' + str(i+1) + ']'
        tmp_line += ';'
        for i in range(1, n_streams):
            stream = streams[i]
            tmp = ('[vtemp00' + str(i) + ']scale=w=' + str(stream.height) + 
                                                   ':h=' + str(stream.width) +
                     '[vout00' + str(i) + ']')
            if i < n_streams - 1:
                tmp += ';'
            tmp_line += tmp
        tmp_line += '" '
        cmd += tmp_line  
    cmd += ('-g ' + str(fps) + ' -sc_threshold 0 ' + extra_param_str + ' ')
    stream_index = 0        
    for stream in streams:
        tmp_line = '-map '
        if n_streams == 1:
            tmp_line += 'v:0'
        else: 
            tmp_line += '[vout00' + str(stream_index + 1) + ']'
        tmp_line += ' -c:v:' + str(stream_index) + ' libx264'
        tmp_line += ' -b:v:' + str(stream_index)
        bit_rate = stream.bit_rate
        tmp_line += ' ' + bit_rate + 'k' + ' '
        cmd += tmp_line
        stream_index += 1
    tmp_line = ''    
    for stream in streams:
        tmp_line += '-map a:0 '
    tmp_line += ('-c:a aac -b:a 128k -ac 2 ' +
                 '-f hls -hls_time 4 -hls_playlist_type event ' +
                 '-master_pl_name master.m3u8 ' +
                 '-var_stream_map "')
    stream_index = 0
    for stream in streams:
        tmp_line += 'v:' + str(stream_index) + ',a:' + str(stream_index)
        if stream_index < n_streams - 1:
            tmp_line += ' '
        stream_index += 1
    tmp_line += '" '
    tmp_line += seg_loc + video_file.split('.')[0] + '/stream_%v.m3u8'
    cmd += tmp_line
    os.system(cmd)


#----https://gist.github.com/oldo/dc7ee7f28851922cca09------------------
# function to find the resolution of the input video file
def get_video_stream(video_file_loc):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(video_file_loc)
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    height = ffprobeOutput['streams'][0]['height']
    width = ffprobeOutput['streams'][0]['width']
    bit_rate = str(int(int(ffprobeOutput['streams'][0]['bit_rate']) / 1000))
    fps = ffprobeOutput['streams'][0]['r_frame_rate'].split('/')[0]
    return Stream(height, width, bit_rate, fps)



def display_video_specs(video_file):
    """ """
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append('videos/' + video_file)
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ffprobeOutput)


def invalid_streams(streams):
    """ """
    # TODO: finish this
    return 0

    
def get_args(args):
    """ """
    # TODO: finish this
    parser = argparse.ArgumentParser()
    parser.add_argument('-vf', '--video_file', default='', type=str)
    parser.add_argument('-ow', '--overwrite', action='store_true')
    parser.add_argument('-vs', '--display_video_specs', action='store_true')
    parser.add_argument('-streams', default=[], nargs='+') #, type=[])
    parser.add_argument('-params', '--extra_params', default=[], nargs='+') 
    args = parser.parse_args()
    video_file = args.video_file
    overwrite = args.overwrite
    # TODO: add functionality to order streams if not in ascending br order
    # for command line args and input file option
    streams = args.streams
    extra_params = args.extra_params
    if video_file == '':
        print("INVALID 1")
        return None
    vid_loc = 'videos/' + video_file
    if not os.path.exists(vid_loc):
        print("Video \"" + video_file + "\" does not exists in the videos folder. aborting")
        return None
    if streams is not None:
        if invalid_streams(streams):
            print("INVALID 2")
            return None
    seg_loc = 'hlsPlayer/segmented_videos/'
    segmented_video_file_dir = seg_loc + video_file.split('.')[0]
    if overwrite:
        if not os.path.isdir(segmented_video_file_dir):
            print("Directory \"" + segmented_video_file_dir + "\" does not exist to overwite. aborting")
            return None
    elif os.path.isdir(segmented_video_file_dir):
        print("Directory \"" +  segmented_video_file_dir + "\" already exists. aborting")
        return None
    return args


def main(args):
    args = get_args(args)
    if args is None:
        return 1
    elif args.display_video_specs:
        display_video_specs(args.video_file)
        return 0
    video_file_loc = 'videos/' + args.video_file 
    if not os.path.isdir('segmented_videos'):
        os.system('mkdir segmented_videos')
    seg_loc = 'segmented_videos/'
    segmented_video_file_dir = seg_loc + args.video_file.split('.')[0] 
    overwrite = args.overwrite
    if overwrite:
        files = glob.glob(segmented_video_file_dir + '/*')
        for f in files:
            os.remove(f)
    else:
        os.system('mkdir ' + segmented_video_file_dir)
    if len(args.streams) == 0:
        args.streams.append(get_video_stream(video_file_loc))
    run_ffmpeg(video_file_loc, args.streams, args.extra_params)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

