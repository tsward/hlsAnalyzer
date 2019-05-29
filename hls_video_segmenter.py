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


def run_ffmpeg(video_file_loc, input_streams, extra_params=''):
    """"""
    n_streams = len(input_streams)
    # TODO: consider this when it's running
    if n_streams >= 10:
        print("COMPICATED BONERS ([vout00X] below...)")
        exit()
    streams = []
    if input_streams is not None:
        for stream in input_streams:
            video_data = get_video_stream(video_file_loc)
            if len(stream.split()) == 1:
                bit_rate = stream[:-1]
                height = video_data.height
                width = video_data.width
            else:
                height, width, bit_rate = get_stream_param_metada(stream.split())
            fps = video_data.fps    
            streams.append(Stream(height, width, bit_rate, fps))
    extra_param_str = ''
    for token in extra_params:
        extra_param_str += token 
    video_file = video_file_loc.split('/')[len(video_file_loc.split('/'))-1]
    cur_dir_root = video_file_loc.split('/')[0]
    if cur_dir_root == 'hlsPlayer':
        seg_loc = 'hlsPlayer/segmented_videos/'
    else:
        seg_loc = 'segmented_videos/'       
    cmd = 'ffmpeg -i hlsPlayer/videos/' + video_file_loc + ' '
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
    #resolution_index = 0
    stream_index = 0        
    for stream in streams:
        tmp_line = '-map '
        if n_streams == 1:
            tmp_line += 'v:'
        else: 
            tmp_line += '[vout00' + str(stream_index + 1) + ']'
        #tmp_line += str(resolution_index)
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
    tmp_line += 'hlsPlayer/' + seg_loc + video_file.split('.')[0] + '/stream_%v.m3u8'
    cmd += tmp_line
    print("~~~COMMANDING BONERS~~~")
    print("\"" + cmd + "\"")
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    exit()
    os.system(cmd)


#----https://gist.github.com/oldo/dc7ee7f28851922cca09------------------
# function to find the resolution of the input video file
def get_video_stream(video_file):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append('hlsPlayer/videos/' + video_file)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    height = ffprobeOutput['streams'][0]['height']
    width = ffprobeOutput['streams'][0]['width']
    bit_rate = str(int(int(ffprobeOutput['streams'][0]['bit_rate']) / 1000))
    fps = ffprobeOutput['streams'][0]['r_frame_rate'].split('/')[0]
    return Stream(height, width, bit_rate, fps)


def get_stream_param_metada(stream):
    ''' '''
    h = stream[0].split('x')[0]
    w = stream[0].split('x')[1]
    br = stream[1][:-1] 
    return h, w, br


def display_video_specs(video_file):
    """ """
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append('hlsPlayer/videos/' + video_file)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ffprobeOutput)


def invalid_streams(streams):
    """ """
    # TODO: finish this before Wed!
    return 0
    print("FRUMP SIZE", len(streams))
    for stream in streams:
        stream = stream.split()
        print("BIG FRUMP SIZE", len(stream))
        print("SCREAMING boners: \"" + str(stream) + "\"")
        if len(stream) != 2:
            print("invalid stream input parameter: \"" + str(stream) + "\"")
            return True
        resolution = stream[0]
        height = resolution.split('x')[0]
        print("WIPING BONERS", resolution, height)
        width = resolution.split('x')[1]
        #print("RESOLVING BONERS", 
        bit_rate = stream[1]
    print('shbyes')
    #exit()
    return False


def invalid_input_file_params(input_file_loc, streams, extra_params):
    """ """
    print("INPUTTING BONERS", input_file_loc, os.getcwd())
    if not os.path.isfile(input_file_loc):
        print("INVALIDATIONINGS WHATEVER")
        return 1
    if len(streams) > 0:
        print("INVALIDATIONINGS TRESsed")
        return 1
    elif len(extra_params) > 0:
        print("INVALIDATIONINGS CINKO")
        return 1
    return 0

def invalid_input_file_content(input_file_loc):
    """ """
    # TODO: finish this
    with open(input_file_loc, 'r') as fp:
        line = fp.readline()
        while line:
            if line.strip() == '' or line.strip()[0] == '#':
                line = fp.readline()
                continue
            tokens = line.split()
            #print("BLINDING BONERS: \"" + str(tokens) + "\"")
            #if tokens
            line = fp.readline()
    return False
    
    
def get_args(args):
    """ """
    # TODO: finish this
    parser = argparse.ArgumentParser()
    parser.add_argument('-if', '--input_file', default='', type=str)
    parser.add_argument('-ow', '--overwrite', action='store_true')
    parser.add_argument('-vs', '--display_video_specs', action='store_true')
    # if 'if' parameter is not '' than none of the following params matter
    parser.add_argument('-vf', '--video_file', default='', type=str)
    parser.add_argument('-streams', default=[], nargs='+') #, type=[])
    parser.add_argument('-params', '--extra_params', default=[], nargs='+') 
    args = parser.parse_args()
    input_file = args.input_file
    video_file = args.video_file
    overwrite = args.overwrite
    # TODO: add functionality to order streams if not in ascending br order
    # for command line args and input file option
    streams = args.streams
    extra_params = args.extra_params
    #--input file option--------------------------------------------------
    if input_file != '':
        input_file_loc = 'hlsPlayer/ffmpeg_input_files/' + input_file
        if invalid_input_file_params(input_file_loc, streams, extra_params):
            return None
        print("INPUTTING BONERS", input_file)
        #exit() 
        # TODO: test valid input file (contents not loc)
        if invalid_input_file_content(input_file_loc):
            return None
        with open(input_file_loc, 'r') as fp:
            line = fp.readline()
            while line:
                if line.strip() == '' or line.strip()[0] == '#':
                    line = fp.readline()
                    continue
                tokens = line.split()
                if tokens[0][:5] == 'video':
                    if len(tokens) == 1:
                        args.video_file = tokens[0].split('=')[1] 
                    elif len(tokens) == 2:
                        if tokens[1][0] == '=':
                            args.video_file = tokens[1][1:]
                        else:
                            args.video_file = tokens[1]
                    elif len(tokens) == 3:
                        args.video_file = tokens[2]
                    else:
                        print("IMPOSSIBLE")
                        exit()
                elif tokens[0][:6] == 'stream' or tokens[0][:11] == 'base_stream': # stream(x)
                    if len(tokens) == 1:
                        args.streams.append(tokens[0].split('=')[1])
                    elif len(tokens) == 2:
                        print('2')
                        if len(tokens[0].split('=')) == 1:
                            args.streams.append(tokens[1].split('=')[1])
                        else:
                            args.streams.append(tokens[0].split('=')[1] + ' ' + tokens[1])
                    elif len(tokens) == 3:
                        if tokens[1][0] == '=':
                            args.streams.append(tokens[1][1:] + ' ' + tokens[2])
                        else:
                            args.streams.append(tokens[1] + ' ' + tokens[2])
                    elif len(tokens) == 4:
                        args.streams.append(tokens[2] + ' ' + tokens[3])
                    else:
                        print("IMPOSSIBLE")
                        exit()
                elif tokens[0][:6] == 'params': # stream(x)
                    print("WHAMMING BONERS")
                    exit()
                else:
                    print("IMPOSSIBLE") 
                    exit()
                line = fp.readline()
        print("SHYBED", args.video_file, args.streams)
        #exit()
        return args
    #---------------------------------------------------------------------
    if video_file == '':
        print("INVALIDATIONINGS TRESing")
        return None
    vid_loc = 'hlsPlayer/videos/' + video_file
    if not os.path.exists(vid_loc):
        print("Video \"" + video_file + "\" does not exists in the videos folder. aborting")
        return None
    if streams is not None:
        if invalid_streams(streams):
            print("INVALIDATIONINGS CUATRO")
            #exit()
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
        print("~~~ERROR BYE~~~")
        return 1
    elif args.display_video_specs:
        display_video_specs(args.video_file)
        return 0
    video_file = args.video_file
    seg_loc = 'hlsPlayer/segmented_videos/'
    segmented_video_file_dir = seg_loc + video_file.split('.')[0]
    overwrite = args.overwrite
    if overwrite:
        files = glob.glob(segmented_video_file_dir + '/*')
        for f in files:
            os.remove(f)
    else:
        os.system('mkdir ' + segmented_video_file_dir)
    run_ffmpeg(video_file, args.streams, args.extra_params)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


#==Graveyard==============

'''    
    extra_param_str = ''
    for token in extra_params:
        extra_param_str += token 
    video_file = video_file_loc.split('/')[len(video_file_loc.split('/'))-1]
    cur_dir_root = video_file_loc.split('/')[0]
    if cur_dir_root == 'hlsPlayer':
        seg_loc = 'hlsPlayer/segmented_videos/'
    else:
        seg_loc = 'segmented_videos/'
    cmd = ('ffmpeg -i ' + video_file_loc + ' \
    	-filter_complex "[v:0]split=4[vtemp001][vtemp002][vtemp003][vout004];' +
         '[vtemp001]scale=w=768:h=432[vout001];' +
         '[vtemp002]scale=w=960:h=540[vout002];' +
         '[vtemp003]scale=w=1280:h=720[vout003]" \
    	  -g ' + str(frames_per_second) + ' -sc_threshold 0 \
    		' + extra_param_str + ' \
            -map [vout001] -c:v:0 libx264 -b:v:0 360k \
    		-map [vout002] -c:v:1 libx264 -b:v:1 1930k \
            -map [vout003] -c:v:2 libx264 -b:v:2 3850k \
            -map [vout004] -c:v:3 libx264 -b:v:3 7000k \
    		-map a:0 -map a:0 -map a:0 -map a:0 -c:a aac -b:a 128k -ac 2 \
    		-f hls -hls_time 4 -hls_playlist_type event \
    		-master_pl_name master.m3u8 \
    		-var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3" ' + seg_loc +
            video_file.split('.')[0] + '/stream_%v.m3u8')
    os.system(cmd)
'''



