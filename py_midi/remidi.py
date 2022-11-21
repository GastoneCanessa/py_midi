# import argparse
import midi
from midi import *
import os
from random import randint
import json
import sys
import fire



def get_pair(text):

    number = int(''.join(filter(str.isdigit, text)))
    l = len(str(number))

    return (number, text[l:])



def c_params(t, params):

    if t.find('t') >= 0 and len(t) > 0:
        ttext = t[:t.find('t')]
        if len(ttext) > 0:
            params['tick'] = get_pair(ttext)[0]
            t = t[t.find('t'):]

    if t.find('c') >= 0 and len(t) > 0:
        ctext = t[:t.find('c')]
        if len(ctext) > 0:
            params['channel'] = get_pair(ctext)[0]
            t = t[t.find('c'):]

    if t.find('d') >= 0 and len(t) > 0:
        params['data'] = []
        ds = t.split('d')
        for dd in ds:
            if len(dd) > 0:
                params['data'].append(get_pair(dd)[0])

    return params



def create_tracks(si, td, eh):
    tracks = {}

    for index in range(si, len(td)):

        t = td[index]
        result = t
        params = {}
        tick = None
        channel = None
        data = []
        i = t.find('event') + 5
        etext = t[:i]
        ev_num, ev = get_pair(etext)
        print(ev)
        c = getattr(midi, eh[ev])
        t = t[i:]
        params["track"] = ev_num
        params["event"] = ev
        params["class"] = c
        params = c_params(t, params)
        # print(params)
        if ev_num not in tracks:
            tracks[ev_num] = [ params ]
        else:
            tracks[ev_num].append(params)

    return tracks



def c_pattern(keys, tracks, pattern):
    for k in keys:
        trk = midi.Track()
        tname_param = None
        for pm in tracks[k]:
            if pm['class'].__name__ == 'TrackNameEvent':
                klass = pm['class']
                trk.append(TrackNameEvent(tick=pm["tick"], text='TRACK ' + str(k), data=pm["data"]))

        for pm in tracks[k]:
            if pm['class'].__name__ != 'TrackNameEvent' and pm['class'].__name__ != 'CopyrightMetaEvent':
                klass = pm['class']
                trk.append(klass(**pm))
        pattern.append(trk)

        return pattern



def remidi(data_file, out_file, resolution=96):
    events_list = [i for i in dir(midi.events) if i.find('Event') >= 0]
    events_hash = {}
    for evt in events_list:
        events_hash[evt.lower()] = evt

    with open(data_file, 'r') as f:
        textdata = f.read().split(" ")

    pattern = midi.Pattern()
    start_index = 0

    try:
        pattern.resolution = int(textdata[0])
        start_index = 1
    except:
        pattern.resolution = resolution

    tracks = create_tracks(start_index, textdata, events_hash)
    keys = sorted(tracks.keys())
    pattern = c_pattern(keys, tracks, pattern)
    print(pattern)
    midi.write_midifile(out_file, pattern)



def main(data_file, out_file, resolution=96):

    remidi(data_file, out_file, resolution)


if __name__ == "__main__":

    fire.Fire(main)
