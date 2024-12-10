import cv2
import os
def get_video_details(video_path):
   """ Get the total duration of the video in seconds and its frame rate. """
   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
       raise FileNotFoundError(f"Could not open video: {video_path}")
   frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
   total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Total frames
   duration = total_frames / frame_rate  # Duration in seconds
   cap.release()
   return {
       "duration_seconds": duration,
       "frame_rate": frame_rate,
       "total_frames": total_frames,
   }


def extract_frames(video_path, output_dir):
   """Extract one frame per minute from the video."""
   video_details = get_video_details(video_path)
   duration_seconds = video_details['duration_seconds']
   minutes = int(duration_seconds // 60)
   cap = cv2.VideoCapture(video_path)
   os.makedirs(output_dir, exist_ok=True)
   frame_paths = []
   for minute in range(minutes + 1):
       timestamp = minute * 60 * 1000  # Convert minutes to milliseconds
       cap.set(cv2.CAP_PROP_POS_MSEC, timestamp)
       success, frame = cap.read()
       if success:
           frame_filename = f"frame_{minute}.jpg"
           frame_path = os.path.join(output_dir, frame_filename)
           cv2.imwrite(frame_path, frame)
           frame_paths.append(frame_path)
   cap.release()
   return frame_paths