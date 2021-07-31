from mongo_connect import DB
from mongo_utils import MongoUtils
from music21 import *


def get_mongo_utils():
    return MongoUtils(DB)


def get_database():
    return DB


def from_json_to_score(user_data):
    stream_parts = user_data.get('streamParts')
    key_1 = user_data.get('keySignature', 'C')
    time_signature = user_data.get('timeSignature', '4/4')
    part_1 = from_json_to_stream_part(stream_parts[0], key_1, time_signature)
    part_2 = from_json_to_stream_part(stream_parts[1], key_1, time_signature)

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
        offset = notes.get('offset')
        if 'timeSignature' in notes:
            element = meter.TimeSignature(notes.get('timeSignature'))
            if offset is None:
                m01.append(element)
            else:
                m01.insert(offset, element)
        if 'keySignature' in notes:
            element = key.Key(notes.get('keySignature'))
            if offset is None:
                m01.append(element)
            else:
                m01.insert(offset, element)
        if 'chord' in notes:
            chord_notes = [from_json_to_note(chord_note) for chord_note in notes.get('chord')]
            element = chord.Chord(chord_notes, quarterLength=duration)

        elif 'note' in notes:
            element = note.Note(notes.get('note').replace('/', ''), quarterLength=duration)
        else:
            element = note.Rest(quarterLength=duration)
        if offset is None:
            m01.append(element)
        else:
            m01.insert(offset, element)
        counter -= duration
        if counter == 0:
            if offset is not None:
                m01.offset = offset + duration
            part_1.append(m01)
            m01 = stream.Measure()
            counter = time_sign.numerator
    if counter != 0 and counter != time_sign.numerator:
        rest = note.Rest(quarterLength=counter)
        m01.append(rest)
        part_1.append(m01)

    p0.append(part_1)
    return p0


def from_json_to_note(json_note, dur=None):
    if dur is None:
        converted_note = note.Note(json_note.get('note', 'D').replace('/', ''))
    else:
        converted_note = note.Note(json_note.get('note', 'D').replace('/', ''), quarterLength=dur)

    if json_note.get('tie') is not None:
        converted_note.tie = tie.Tie(json_note.get('tie'))

    return converted_note


def from_score_to_json(score: stream.Score, current_data):
    current_time = current_data.get('timeSignature')
    current_key = current_data.get('keySignature')
    data = [from_stream_part_to_json(score.parts[0].chordify(), current_time, current_key),
            from_stream_part_to_json(score.parts[1].chordify(), current_time, current_key)]
    result = {
        'streamParts': data,
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
        json_element = {
            'dur': element.duration.quarterLength*8
#            'offset': element.offset
        }
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
            data.append(json_element)
            continue
        if isinstance(element, note.Note):
            data.append(from_note_to_json(element, json_element))
            continue
        if isinstance(element, chord.Chord):
            json_element['chord'] = [from_note_to_json(chord_note) for chord_note in element.notes]
            data.append(json_element)
            continue

    return data


def from_note_to_json(note_element, json_element=None):
    sub_element = {} if json_element is None else json_element
    sub_element['note'] = refactor_note_output(str(note_element.pitch))
    if note_element.tie is not None:
        sub_element['tie'] = note_element.tie.type
    return sub_element


def refactor_note_output(string_note):
    if not string_note[-1].isnumeric():
        return string_note + '/' + '4'
    return string_note[:-1] + '/' + string_note[-1]