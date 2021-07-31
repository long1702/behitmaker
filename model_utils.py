from musicautobot.multitask_transformer import *
from musicautobot.music_transformer import *
from musicautobot.config import *
import torch

learn_model = None

def init_model():
    print("========Start=======")
    torch.set_num_threads(4)
    print("========LOAD_DATA=======")
    data = load_data('./data', 'multiitem_data_save.pkl', num_workers=1)
    print("========LOAD_MODEL=======")
    model_path = os.environ.get('MODEL_PATH', 'MultitaskSmallKeyC.pth')
    global learn_model
    if learn_model is None:
        learn_model = multitask_model_learner(data, config=multitask_config(),
                                    pretrained_path='./data/models/'+model_path)
    if torch.cuda.is_available(): learn_model.model.cuda()
    print("========DONE_LOAD_MODEL=======")


def generate(init_stream, n_words=200, temperatures=(1.2, 0.8), top_k=30, top_p=0.8):
    print("========Start_Predict=======")
    global learn_model
    if learn_model is None:
        init_model()
    full = nw_predict_from_midi(learn_model, stream=init_stream, n_words=n_words, seed_len=20, temperatures=temperatures,
                                      top_k=top_k, top_p=top_p)
    stream = separate_melody_chord(full.to_stream())
    combined = s2s_predict_from_midi(learn_model, midi=stream, pred_melody=True)
    result = separate_melody_chord(combined.to_stream())
    print("========End_Predict=======")
    return result
