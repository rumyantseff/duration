import os
import enum
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import wave
import contextlib
from tkinter import *


root = Tk()
root.title('Audio files information')
# x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
# y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
# root.wm_geometry("+%d+%d" % (x, y))
root.geometry('700x700')


# track_listbox.place(x=10, y=25, height=700, width=700, bordermode=OUTSIDE)


class FileExtensions(enum.Enum):
    EXT_MP3 = 'mp3'
    EXT_MP4 = 'mp4'
    EXT_WAV = 'wav'


def whole_duration(start_path='./audio_files_folder'):
    content = os.listdir(start_path)
    duration = 0
    total_tracks_size = 0
    message = ''
    for item in content:
        item_path = os.path.join(start_path, item)
        file_extension = item.split('.')
        if os.path.isfile(item_path):
            if file_extension[1].lower() == FileExtensions.EXT_MP3.value:
                audio_file = MP3(item_path)
                file_duration = audio_file.info.length
                file_hours, file_remainder = divmod(file_duration, 3600)
                file_minutes, file_seconds = divmod(file_remainder, 60)

            elif file_extension[1].lower() == FileExtensions.EXT_MP4.value:
                audio_file = MP4(item_path)
                file_duration = audio_file.info.length
                file_hours, file_remainder = divmod(file_duration, 3600)
                file_minutes, file_seconds = divmod(file_remainder, 60)

            elif file_extension[1].lower() == FileExtensions.EXT_WAV.value:
                with contextlib.closing(wave.open(item_path, 'r')) as f:
                    frames = f.getnframes()
                    rate = f.getframerate()
                    file_duration = frames/float(rate)
                    file_hours, file_remainder = divmod(file_duration, 3600)
                    file_minutes, file_seconds = divmod(file_remainder, 60)

            file_size = os.path.getsize(item_path)
            total_tracks_size += os.path.getsize(item_path)

            file_hours_str = str(int(file_hours))
            file_minutes_str = str(int(file_minutes))
            file_seconds_str = str(int(file_seconds))
            file_size_MB_str = str(round((file_size/(1000*1000)), 1))
            file_files_B_size = str(file_size)

            message = item_path + \
                '   ' + file_hours_str + \
                ':' + file_minutes_str + \
                ':' + file_seconds_str + \
                '   ' + file_size_MB_str + \
                ' MB (' + file_files_B_size + ' Bytes)'
            print(message)
            duration += file_duration
            # total_tracks_size += os.path.getsize(item_path)
            track_listbox.insert(0, message)
    return duration


def get_tracks_size(start_path='./audio_files_folder'):
    content = os.listdir(start_path)
    total_tracks_size = 0
    for item in content:
        item_path = os.path.join(start_path, item)
        total_tracks_size += os.path.getsize(item_path)
    return total_tracks_size


def delete_item(start_path='./audio_files_folder'):
    content = os.listdir(start_path)
    # selection = track_listbox.curselection()
    # track_listbox.delete(selection[0])
    for selection in content:
        selection = track_listbox.curselection()
        track_listbox.delete(selection[0])
        selection.delete(selection[0])


track_listbox = Listbox(root)
track_listbox.pack(padx=10, pady=10, fill=BOTH, expand=True)

delete_button = Button(text='Delete', width=10, command=delete_item)
delete_button.pack()

if __name__ == "__main__":
    duration = whole_duration()
    total_tracks_size = get_tracks_size()
    print('-------------------------------------------------------------------')
    hours, remainder = divmod(duration, 3600)
    mins, secs = divmod(remainder, 60)
    print(f'Total tracks duration:  {int(hours)}:{int(mins)}:{int(secs)}')
    print(
        f'Total tracks size: {str(round(total_tracks_size/(1000*1000), 1))} MB \
({str(total_tracks_size)} Bytes)'
    )
    root.mainloop()
