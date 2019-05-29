#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  graph_maker.py
#
#
#

from mpl_toolkits.mplot3d import Axes3D
import os
import re
import matplotlib.pyplot as plt
import time
import argparse
import glob


def get_seg_color(stream):
    """ """
    if stream == 360:
        return 'green'
    elif stream == 1930:
        return 'blue'
    elif stream == 3850:
        return 'black'
    elif stream == 7000:
        return 'purple'
    print("IMPOSSIBLE")
    return None


# 360, 1930, 3850, 7000
def get_stream(stream):
    """ """
    if stream == 0:
        return 360
    elif stream == 1:
        return 1930
    elif stream == 2:
        return 3850
    elif stream == 3:
        return 7000
    print("IMPOSSIBLE")
    return None



def get_elapsed_seg_time(init_time_digits, cur_time_digits):
    init_time = time.mktime(time.strptime("2019" + init_time_digits[0] + init_time_digits[1] + init_time_digits[2], "%Y%H%M%S"))
    cur_time = time.mktime(time.strptime("2019" + cur_time_digits[0] + cur_time_digits[1] + cur_time_digits[2], "%Y%H%M%S"))
    if cur_time - init_time < 0:
        print("UH OHS?")
        #exit()
    return float(cur_time - init_time)


def get_requested_video_files(apache_log_file):
    """ """
    requested_video_files = []
    try:
        open('log_files/' + apache_log_file, 'r')
    except FileNotFoundError:
        print("file '" + apache_log_file, "' not present in current directory")
        return None
    with open('log_files/' + apache_log_file, 'r') as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if line.strip() == "":
                line = fp.readline()
                cnt += 1
                continue
            time_from_line = line.split()[3][1:]
            cur_time = time_from_line[12:]
            if cnt == 1:
                print("Parsing apache log beginning from", time_from_line)
            line_tokens = line.split()
            file_requested = line_tokens[6]
            file_req_tokens = file_requested.split('/')
            try:
                if file_req_tokens[3] == 'segmented_videos':
                    file_requested = file_req_tokens[5] 
                    if file_requested.split('.')[1] == 'm3u8':
                        line = fp.readline()
                        cnt += 1
                        continue
                    requested_video_files.append([file_requested, cur_time])
            except IndexError:
                pass
            line = fp.readline()
            cnt += 1
    return requested_video_files

    
    
def make_apache_log_graph(name, title, files, colors, bit_rates, legend_x, legend_y, legend_names, zoom=-1):
    """ """    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    index = 0
    for dir_name in files:
        requested_video_files = get_requested_video_files(dir_name)
        if not requested_video_files:
            return 1
        x = []
        y = []
        z = []
        init_time_digits = requested_video_files[0][1].split(':')
        #print("number of video segments:", len(requested_video_files))
        for pair in requested_video_files:
            filename = pair[0]
            segment_time = pair[1]
            time_digits = segment_time.split(':')
            elapsed_seg_time = get_elapsed_seg_time(init_time_digits, time_digits)
            if zoom > -1 and elapsed_seg_time >= zoom:
                print("ZOOOOOMING BONERS")
                break
            stream = re.findall(r'\d+', filename)[0]
            which_stream = get_stream(int(stream[0]))
            if elapsed_seg_time is not None:
                x.append(elapsed_seg_time)
                y.append(bit_rates[index])
                z.append(which_stream)
        plt.plot(x, y, z, color=colors[index], zdir='z') 
        #plt.scatter(100.0, 100.0, 100.0, color='magenta')
        last_seg_time = elapsed_seg_time
        index += 1
        
    axes = plt.gca()
    axes.set_ylim([0,10000])
    x = 0
    xs = []
    while x < 660:
        xs.append(x)
        x += 60
    x_labels = range(0, 11) 
    plt.xticks(xs, x_labels)
    i = 0
    for label in ax.xaxis.get_ticklabels(): 
        if i % 2 != 0:
            label.set_visible(False)
        i += 1
    y_labels = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5] #, 11]
    #plt.yticks(plt.yticks()[0], y_labels)
    i = 0
    for label in ax.yaxis.get_ticklabels(): #[2::]:
        if i % 2 != 0:
            #label.set_visible(False)
            pass
        i += 1
    plt.xlabel("Duration (minutes)")
    plt.ylabel("Max Start BW (kbps)", labelpad=10)
    #ax.get_yticklabels()[len(ax.get_yticklabels())-1].set_color("red")
    ax.set_zlabel("Requested Bit Rate (kbps)", labelpad=10) #, ax.get_zticks())
    #ax.set_zticks([1000, 2000, 3000, 4000, 5000]) #, y_labels)
    #ax.zaxis.set_ticklabels([1, 2, 3, 4, 5, 6, 7, 8])
    i = 0
    for label in ax.zaxis.get_ticklabels(): 
        if i % 2 != 0:
            #label.set_visible(False)
            pass
        i += 1
    plt.legend(legend_names, title='Delay', loc='center left',
                    bbox_to_anchor=(legend_x, legend_y)) #, fancybox=True)
    #plt.show()
    #plt.title(title, loc='right')
    plt.savefig("graphs/apache_graphs/" + name + ".png", format='png')
    plt.close()
    #exit()
    
    
def make_apache_graphs():
    """ """
    
    files = (
        'IOS_OSX_BW1000kb.txt',
        'IOS_OSX_BW2000kb.txt',
        'IOS_OSX_BW3000kb.txt',
        'IOS_OSX_BW4000kb.txt',
        'IOS_OSX_BW5000kb.txt',
        'IOS_OSX_BW6000kb.txt',
        'IOS_OSX_BASE.txt', 
    )
    colors = ['black', 'brown', 'green', 'grey', 'blue', 'teal', 'red']
    bit_rates = [1000, 2000, 3000, 4000, 5000, 6000, 10000] 
    legend_x = -0.17
    legend_y = 0.85
    legend_names = [ '1000', '2000', '3000', '4000', '5000', '6000', 'None']    
    make_apache_log_graph('g1_IOS', 'iOS', files, colors, bit_rates, legend_x, legend_y, legend_names)

    files = (
        'OSX_LINUX_BW2000kb.txt',
        'OSX_LINUX_BW4000kb.txt',
        'OSX_LINUX_BW5000kb.txt',
        'OSX_LINUX_BW6000kb.txt',
        'OSX_LINUX_BW9000kb.txt',
        'OSX_LINUX_BW10000kb.txt',
        'OSX_LINUX_BASE.txt', 
    )
    colors = ['blue', 'green', 'black', 'purple', 'black', 'maroon', 'red']
    bit_rates = [2000, 4000, 5000, 6000, 9000, 10000, 11000]
    legend_names = [ 'BWL 2000', 'BWL 4000', 'BWL 5000', 'BWL 6000', 'BWL 9000', 'BWL 10000', 'BWL:None']
    make_apache_log_graph('g2_OSX', 'OS X', files, colors, bit_rates, legend_x, legend_y, legend_names)
    
    files = (
        'IOS_OSX_BW2000_4000kb.txt',
        'IOS_OSX_BW4000_8000kb.txt',
        'IOS_OSX_BW5000_10000kb.txt',
        'IOS_OSX_BASE.txt', 
    )
    colors = ['green', 'black', 'blue', 'red']
    bit_rates = [2000, 4000, 5000, 10000] 
    legend_names = [ '2000 to 4000', '4000 to 8000', '5000 to 10000', "BWL None"]
    make_apache_log_graph('g3_ios_osx_bwtimes2', 'iOS', files, colors, bit_rates, legend_x, legend_y, legend_names)
    
    files = (
        'OSX_LINUX_BW2000_4000kb.txt',
        'OSX_LINUX_BW4000_8000kb.txt',
        'OSX_LINUX_BW5000_10000kb.txt',
        'OSX_LINUX_BASE.txt', 
    )
    colors = ['green', 'black', 'blue', 'red']
    bit_rates = [2000, 4000, 5000, 10000] 
    make_apache_log_graph('g4_osx_linux_bwtimes2', 'OS X', files, colors, bit_rates, legend_x, legend_y, legend_names)
    
    files = (
        'IOS_OSX_BASE.txt', 
        'IOS_OSX_BW12000_6000kb.txt',
        'IOS_OSX_BW10000_5000kb.txt',
        'IOS_OSX_BW8000_4000kb.txt',
        'IOS_OSX_BW4000_2000kb.txt',
    )
    legend_names = [ '12000 to 6000', '10000 to 5000', '8000 to 4000', '4000 to 2000', "BWL None"]
    colors = ['red', 'black', 'blue', 'brown', 'green']
    bit_rates = [13000, 12000, 10000, 8000, 4000]   
    make_apache_log_graph('g5_ios_osx_bwdiv2', 'iOS', files, colors, bit_rates, legend_x, legend_y, legend_names)
    
    files = (
        'OSX_LINUX_BASE.txt', 
        'OSX_LINUX_BW12000_6000kb.txt',
        'OSX_LINUX_BW10000_5000kb.txt',
        'OSX_LINUX_BW8000_4000kb.txt',
        'OSX_LINUX_BW4000_2000kb.txt',
        
    )
    colors = ['red', 'black', 'blue', 'brown', 'green']
    bit_rates = [13000, 12000, 10000, 8000, 4000]  
    make_apache_log_graph('g6_osx_linux_bwdiv2', 'OS X', files, colors, bit_rates, legend_x, legend_y, legend_names)


def make_segment_graph(dir_name, zoom): 
    """ """ 
    print("SCRAMBLING BONERS", dir_name, zoom)
    requested_video_files = get_requested_video_files(dir_name)
    if not requested_video_files:
        return 1
    segment_num = 0
    x = []
    y = []
    #prev_color = None
    #cunt = 0
    colors = []
    init_time_digits = requested_video_files[0][1].split(':')
    for req_vid_file in requested_video_files:
        filename = req_vid_file[0]
        segment_time = req_vid_file[1]
        time_digits = segment_time.split(':')
        elapsed_seg_time = get_elapsed_seg_time(init_time_digits, time_digits)
        if zoom > 1 and elapsed_seg_time >= zoom:
            print("ZOOMING BONERS", zoom, elapsed_seg_time)
            break
        stream = re.findall(r'\d+', filename)[0]
        which_stream = get_stream(int(stream[0]))
        if elapsed_seg_time is not None:
            color = get_seg_color(which_stream)
            #print("COLORING FRUMPS", color, which_stream)
            x.append(elapsed_seg_time)
            y.append(segment_num)
            
            if [color, which_stream] not in colors:
                print("SNUGGLING BONERS", color, which_stream)
                #exit()
                #if not prev_color or prev_color != color:
                #prev_color = color
                plt.scatter(elapsed_seg_time, segment_num, color=color, marker='x') 
                #cunt +=1 
                colors.append([color, which_stream])
            else:
                plt.scatter(elapsed_seg_time, segment_num, color=color, marker='x', label='_nolegend_')
                
            segment_num += 1
    plt.xlabel("Duration (seconds)")
    plt.ylabel("Segment Number")
    legend_x = 0#-0.175
    legend_y = 0.85
    #legend_names = ['360', '1930', '3850', '7000']
    
    print("SETTING BONERS", colors)
    #exit()
    
    i = 0
    legend_names = []
    frumps = []
    for x in colors:
        frumps.append(x[1])
    for color in set(frumps):
        print('POOPY FRUMPS', color)
        legend_names.append(str(color) + ' kb/s')
        i += 1
    
    print("LEGENDARY BONERS", legend_names)
    #exit()
    if zoom > -1:
        plt.xlim(-25, zoom)
    else:
        plt.xlim(-25, 600)
        
    plt.legend(legend_names, loc='center left',
                    bbox_to_anchor=(legend_x, legend_y))
    
    if zoom > 1:
        plt.savefig("graphs/segment_graphs/ZOOM_SEG_" + dir_name.split('.')[0] + ".png", format='png')
    else:
        plt.savefig("graphs/segment_graphs/SEG_" + dir_name.split('.')[0] + ".png", format='png')
    plt.close()



#def make_segment_graph(filename, zoom=-1):
#    """ """
#    make_segment_graph(filename, zoom)


def make_segment_graphs(zoom=-1):
    """ """ 
    print("MAKING BONERS")
    #if filename == 'make_all':
    for filename in glob.iglob('log_files/*.txt'):
        print(filename)
        make_segment_graph(filename.split('/')[1], zoom) 
    #else:
    #filename = 'OSX_LINUX_BW5000_10000kb.txt'
    #    make_segment_graph(filename, zoom)
    
 
def main(args):
    platform = sys.platform
    if platform == "linux" or platform == "linux2":
        apache_log_dir = '/var/log/apache2/access.log'
    elif platform == "darwin":
        apache_log_dir = '/private/var/log/apache2/access_log'
    else:
        print("This program is not designed to run with Windows!")
        return 1
    
    if not os.path.isdir('graphs/apache_graphs'):
        os.mkdir('graphs/apache_graphs')   
        
    if not os.path.isdir('graphs/segment_graphs'):
        os.mkdir('graphs/segment_graphs')
        
    #make_apache_graphs()
    
    #make_segment_graphs()
    #make_segment_graphs(100)
    
    #make_segment_graph('OSX_LINUX_BW10000_5000kb.txt', -1)
    
    files = (
        #'IOS_OSX_BW1000kb.txt',
        #'IOS_OSX_BW2000kb.txt',
        #'IOS_OSX_BW3000kb.txt',
        #'IOS_OSX_BW4000kb.txt',
        #'IOS_OSX_BW5000kb.txt',
        #'IOS_OSX_BW6000kb.txt',
        #'IOS_OSX_BASE.txt',
        'OSX_LINUX_BASE.txt', 
        'OSX_delay5ms.txt',
        'OSX_delay10ms.txt',
        'OSX_delay25ms.txt',
        
    )
    colors = ['red', 'brown', 'green', 'purple'] #, 'blue', 'teal', 'red']
    bit_rates = [10000, 7500, 5000, 2500] #, 5000, 6000, 10000] 
    legend_x = -0.17
    legend_y = 0.85
    legend_names = [ 'NONE', '5', '10', '25'] #, '4000', '5000', '6000', 'None']    
    make_apache_log_graph('whatnot', 'iOS', files, colors, bit_rates, legend_x, legend_y, legend_names)

    files = (
        #'IOS_OSX_BW1000kb.txt',
        #'IOS_OSX_BW2000kb.txt',
        #'IOS_OSX_BW3000kb.txt',
        #'IOS_OSX_BW4000kb.txt',
        #'IOS_OSX_BW5000kb.txt',
        #'IOS_OSX_BW6000kb.txt',
        #'IOS_OSX_BASE.txt',
        'IOS_OSX_BASE.txt', 
        'IOS_delay5.txt',
        'IOS_delay10.txt',
        'IOS_delay25.txt',
        
    )
    colors = ['red', 'brown', 'green', 'purple'] #, 'blue', 'teal', 'red']
    bit_rates = [10000, 7500, 5000, 2500] #, 5000, 6000, 10000] 
    legend_x = -0.17
    legend_y = 0.85
    legend_names = [ 'NONE', '5', '10', '25'] #, '4000', '5000', '6000', 'None']    
    make_apache_log_graph('buttnot', 'iOS', files, colors, bit_rates, legend_x, legend_y, legend_names)

    
    
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
