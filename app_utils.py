from mongo_connect import DB
from mongo_utils import MongoUtils
from music21 import *


def get_mongo_utils():
    return MongoUtils(DB)


def get_database():
    return DB

def from_json_to_score(user_data):
    stream_parts = user_data.get('streamParts')
    key = user_data.get('keySignature', 'C')
    time_signature = user_data.get('timeSignature', '4/4')
    part_1 = from_json_to_stream_part(stream_parts[0], key, time_signature)
    part_2 = from_json_to_stream_part(stream_parts[1], key, time_signature)

    if len(part_1) != len(part_2):
        for _ in range(abs(len(part_2) - len(part_1))):
            m_temp = stream.Measure()
            rest = note.Rest(quarterLength=float(time_signature.split('/')[0]))
            m_temp.append(rest)
            part_1.append(m_temp) if len(part_1) < len(part_2) else part_2.append(m_temp)

    result = stream.Score()
    result.insert(0, part_1)
    result.insert(0, part_2)
    return result


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
        if 'timeSignature' in notes:
            m01.append(meter.TimeSignature(notes.get('timeSignature')))
        if 'keySignature' in notes:
            m01.append(key.Key(notes.get('keySignature')))
        if 'chord' in notes:
            m01.append(chord.Chord([x.replace('/', '') for x in notes.get('chord')], quarterLength=duration))
        else:
            m01.append(note.Note(notes.get('note').replace('/', ''), quarterLength=duration))
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


def from_score_to_json(score: stream.Score, current_data):
    current_time = current_data.get('timeSignature')
    current_key = current_data.get('keySignature')
    data = [from_stream_part_to_json(score.parts[0], current_time, current_key),
            from_stream_part_to_json(score.parts[1], current_time, current_key)]
    result = {
        'data': data,
        'timeSignature': current_time,
        'keySignature': current_key
    }
    return result


def from_stream_part_to_json(stream_part: stream.Part, time, key_sign):
    notes_to_parse = stream_part.recurse()
    data = []
    current_time, time_signature = time, time
    current_key, key_signature = key_sign, key_sign
    for element in notes_to_parse:
        json_element = {'dur': element.duration.quarterLength*8}
        if isinstance(element, meter.TimeSignature):
            time_signature = str(element.numerator) + '/' + str(element.denominator)
            continue
        if isinstance(element, key.KeySignature):
            key_signature = str(element.asKey()).split()[0]
            continue
        if current_time != time_signature:
            json_element['timeSignature'] = time_signature
            current_time = time_signature
        if current_key != key_signature:
            json_element['keySignature'] = key_signature
            current_key = key_signature
        if isinstance(element, note.Rest):
            json_element['isRest'] = True
            data.append(json_element)
            continue
        if isinstance(element, note.Note):
            json_element['note'] = str(element.pitch)
            data.append(json_element)
            continue
        if isinstance(element, chord.Chord):
            json_element['chord'] = [str(chord_note.pitch) for chord_note in element.notes]
            data.append(json_element)
            continue

    return data
