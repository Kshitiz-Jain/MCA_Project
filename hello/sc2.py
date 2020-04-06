import os
import os.path
import cv2
from Katna.video import Video
import multiprocessing


def main():

    # Extract specific number of key frames from video
    # if os.name == 'nt':
    #     multiprocessing.freeze_support()

    vd = Video()

    # folder to save extracted images
    output_folder_video_image = "selectedframes"
    out_dir_path = os.path.join(".", output_folder_video_image)

    if not os.path.isdir(out_dir_path):
        os.mkdir(out_dir_path)

    # number of images to be returned
    no_of_frames_to_returned = 20
    # VIdeo file path
    video_file_path = os.path.join("alligator-chili (1).mp4")
    #print(f"Input video file path = {video_file_path}")

    imgs = vd.extract_frames_as_images(
        no_of_frames=no_of_frames_to_returned, file_path=video_file_path
    )

    # Save it to disk
    for counter, img in enumerate(imgs):
        vd.save_frame_to_disk(
            img,
            file_path=out_dir_path,
            file_name="test_" + str(counter),
            file_ext=".jpeg",
        )
    print(f"Exracted key frames file path = {out_dir_path}")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()
