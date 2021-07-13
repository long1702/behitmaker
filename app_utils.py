from mongo_connect import DB
from mongo_utils import MongoUtils
from music21 import *


def get_mongo_utils():
    return MongoUtils(DB)


def get_database():
    return DB


def from_json_to_stream_part(stream_part, key_signature, time_signature):
    p0 = stream.Part()
    time_sign = meter.TimeSignature(time_signature)
    p0.append(time_sign)
    p0.append(key.Key(key_signature))

    part_1 = []
    counter = time_sign.numerator
    m01 = stream.Measure()
    for notes in stream_part:
        duration = float(notes.get('dur', '32')) / 8 if counter - float(notes.get('dur', '32')) / 8 > 0 else counter
        m01.append(note.Note(notes.get('note'), quarterLength=duration))
        counter -= duration
        if counter == 0:
            part_1.append(m01)
            m01 = stream.Measure()
            counter = time_sign.numerator
    if counter != 0 and counter != time_sign.numerator:
        rest = note.Rest(quarterLength=counter)
        m01.append(rest)
        part_1.append(m01)

    p0.append(part_1)
    return p0
