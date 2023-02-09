import os
import sys
import json
import argparse

import pycocotools.mask
import matplotlib.pyplot as plt

env_path = os.path.join(os.path.dirname(__file__), '..')
if env_path not in sys.path:
    sys.path.append(env_path)

from pytracking.evaluation import Tracker


def main():
    parser = argparse.ArgumentParser(description='Run the tracker on your webcam.')
    parser.add_argument('--dataset', type=str, default=os.path.expanduser("~/dataset/CoRL_real/"))
    parser.add_argument('-v', '--video', type=str, default='0002')
    parser.add_argument('--tracker_name', type=str, default="rts", help='Name of tracking method.')
    parser.add_argument('--tracker_param', type=str, default="rts50", help='Name of parameter file.')
    parser.add_argument('--optional_box', type=float, default=None, nargs="+", help='optional_box with format x y w h.')
    parser.add_argument('--debug', type=int, default=0, help='Debug level.')
    parser.add_argument('-s', '--save_results', default=False, action='store_true', help='Save bounding boxes')
    args = parser.parse_args()

    video_path = os.path.join(args.dataset, args.video)
    color_im_files = sorted(os.listdir(os.path.join(video_path, 'color')))
    print(f"{len(color_im_files) = }")
    color_im_paths = [os.path.join(video_path, 'color', im_file) for im_file in color_im_files]
    output_folder = os.path.join(video_path, 'pytracker')

    optional_mask = None
    # with open(os.path.join(output_folder, '0001-color.json'), 'r') as fp:
    #     data = json.load(fp)
    # optional_mask = pycocotools.mask.decode(data['mask_rle'])
    # plt.imshow(optional_mask)
    # plt.show()

    tracker = Tracker(args.tracker_name, args.tracker_param)
    tracker.run_frames(frame_paths=color_im_paths, optional_mask=optional_mask, optional_box=args.optional_box,
                       debug=args.debug, save_results=args.save_results, output_folder=output_folder)


if __name__ == '__main__':
    main()
