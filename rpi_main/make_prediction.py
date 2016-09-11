# -*- coding: utf-8 -*-

import argparse
import os
import pickle

from rpi_methods import Reader
from rpi_methods.baby_cry_predictor import BabyCryPredictor
from rpi_methods.feature_engineer import FeatureEngineer
from rpi_methods.majority_voter import MajorityVoter


def main():
    # /!\ ADAPT PATHS /!\

    parser = argparse.ArgumentParser()
    parser.add_argument('--load_path_data',
                        default="~/Documents/baby_cry/Data/Recordings")
    parser.add_argument('--load_path_model',
                        default="~/Documents/baby_cry/Data/Model/")
    parser.add_argument('--save_path',
                        default="~/Documents/baby_cry/Data/Prediction/")

    # Arguments
    args = parser.parse_args()
    load_path_data = args.load_path_data
    load_path_model = args.load_path_model
    save_path = args.save_path

    ####################################################################################################################
    # READ RAW SIGNAL
    ####################################################################################################################

    # Read signal
    file_name = os.listdir(load_path_data)         # [0] /!\ in the real usage there will only be one file in the folder
    file_reader = Reader(os.path.join(load_path_data, file_name))
    play_list = file_reader.read_audio_file()

    ####################################################################################################################
    # iteration
    ####################################################################################################################

    # iterate on play_list for feature engineering and prediction

    ####################################################################################################################
    # FEATURE ENGINEERING
    ####################################################################################################################

    # Feature extraction
    engineer = FeatureEngineer()

    play_list_processed = list()

    for signal in play_list:
        tmp = engineer.feature_engineer(signal)
        play_list_processed.append(tmp)

    ####################################################################################################################
    # MAKE PREDICTION
    ####################################################################################################################

    with open((os.path.join(load_path_model, 'model.pkl')), 'rb') as fp:
        model = pickle.load(fp)

    predictor = BabyCryPredictor(model)

    predictions = list()

    for signal in play_list_processed:
        tmp = predictor.classify(signal)
        predictions.append(tmp)

    ####################################################################################################################
    # MAJORITY VOTE
    ####################################################################################################################

    majority_voter = MajorityVoter(predictions)
    majority_vote = majority_voter.vote()

    ####################################################################################################################
    # SAVE
    ####################################################################################################################

    # Save prediction result
    with open(os.path.join(save_path, 'prediction.txt'), 'wb') as text_file:
        text_file.write("{0}".format(majority_vote))

if __name__ == '__main__':
    main()
