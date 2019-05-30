#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hls_video_segmenter.py
#
#
#
import queue as Q
import os
import glob
import argparse
import subprocess
import shlex
import json
import pprint




class Stream(object):
    def __init__(self, w, h, br, fps):
        self.width = w
        self.height = h
        self.bit_rate = br
        self.fps = fps
    
    def __lt__(self, other):
        return self.bit_rate > other.bit_rate

    
    def __str__(self):
        return ('Resolution: ' + str(self.height) + 'x' + str(self.width) +
                '; bit rate: ' + str(self.bit_rate) + 'k; fps: ' + str(self.fps))


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
        tmp_line += ' ' + str(bit_rate) + 'k' + ' '
        cmd += tmp_line
        stream_index += 1
    tmp_line = ''    
    for stream in streams:
        tmp_line += '-map a:0 '
    seg_dir = 'segmented_videos/' + video_file_loc.split('/')[1].split('.')[0]
    tmp_line += ('-c:a aac -b:a 128k -ac 2 ' +
                 '-f hls -hls_time 4 -hls_playlist_type event ' +
                 '-master_pl_name master.m3u8 ' +
                 # TODO: why doesn't folder structure work?
                 #'-hls_segment_filename ' + seg_dir + '/stream_%v/data%06d.ts ' + 
                 #'-use_localtime_mkdir 1 ' + 
                 '-var_stream_map "')
    stream_index = 0
    for stream in streams:
        tmp_line += 'v:' + str(stream_index) + ',a:' + str(stream_index)
        if stream_index < n_streams - 1:
            tmp_line += ' '
        stream_index += 1
    tmp_line += '" '
    tmp_line += seg_dir + '/stream_%v.m3u8'
    cmd += tmp_line
    print("~~~COMMAND~~~")
    print("\"" + cmd + "\"")
    #exit()
    os.system(cmd)


#----https://gist.github.com/oldo/dc7ee7f28851922cca09------------------
# function to find the resolution of the input video file
def get_video_stream(video_file_loc):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(video_file_loc)
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    width = ffprobeOutput['streams'][0]['width']
    height = ffprobeOutput['streams'][0]['height']
    fps = ffprobeOutput['streams'][0]['r_frame_rate'].split('/')[0]
    return Stream(width, height, -1, fps)



def display_video_specs(video_file):
    """ """
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append('videos/' + video_file)
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(ffprobeOutput)


def get_streams(video_file_loc, streams):
    """ """
    brs = []
    ret = Q.PriorityQueue()
    base_stream = get_video_stream(video_file_loc)
    fps = base_stream.fps
    found_base = False
    for stream in streams:
        stream = stream.split()
        if len(stream) != 2:
            print("Invalid resolution parameters 1 \"" + str(stream) + "\"")
            return None
        res = stream[0]
        if res == 'base':
            if found_base:
                print("duplicate base stream", streams)
                return None
            found_base = True
            w = base_stream.width
            h = base_stream.height
        else:
            res = res.split('x')
            try:
                w = int(res[0])
                h = int(res[1])
            except:
                print("Invalid resolution parameters 2 \"" + str(res) + "\"")
                return None
        try:
            br = stream[1]
        except IndexError:
            print("no bit rate supplied for stream")
            return None
        c = br[len(br)-1]
        if c != 'k':
            print("Invalid bit rate parameter 1 \"" + str(br) + "\"")
            return None
        br = br[:len(br)-1]
        try:
            br = int(br)
        except:
            print("Invalid bit rate parameter 2 \"" + str(br) + "\"")
            return None
        if br in brs:
            print("duplicate bit rate in streams: ", br)
            return None
        brs.append(br)
        ret.put(Stream(w, h, br, fps))
    if not found_base:
        print("no base stream specified")
        return None
    return ret
     
    
def get_args(args):
    """ """
    # TODO: finish this
    parser = argparse.ArgumentParser()
    parser.add_argument('-vf', '--video_file', required=True, type=str)
    parser.add_argument('-ow', '--overwrite', action='store_true')
    parser.add_argument('-vs', '--display_video_specs', action='store_true')
    parser.add_argument('-streams', required=True, nargs='+')
    parser.add_argument('-params', '--extra_params', default=[], nargs='+') 
    args = parser.parse_args()
    video_file = args.video_file
    overwrite = args.overwrite
    extra_params = args.extra_params
    video_file_loc = 'videos/' + video_file
    if not os.path.exists(video_file_loc):
        print("Video \"" + video_file + "\" does not exists in the videos folder")
        return None
    if len(args.streams) == 0:
        args.streams.append(get_video_stream(video_file_loc)) 
    else:
        fps = get_video_stream(video_file_loc).fps
        args.streams = get_streams(video_file_loc, args.streams)
        if args.streams is None:
            print("invalid stream parameters")
            return None
        tmp_streams = args.streams
        args.streams = []
        while not tmp_streams.empty():
            args.streams.append(tmp_streams.get())
    seg_loc = 'segmented_videos/'
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
        print("Error detected: aborting")
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
    
    run_ffmpeg(video_file_loc, args.streams, args.extra_params)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

