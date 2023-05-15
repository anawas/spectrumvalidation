"""
This search can take a long time, depending on the connection and the number of 
files in a folder.
"""
import os
import datetime as dt
import webdav.WebdavConnector as wdav
import tempfile
from validation import snr
from radiospectra.sources import CallistoSpectrogram
import math

def get_tempfile_name():
    tmpfile = tempfile.NamedTemporaryFile(mode="w")
    tmpfile.close()
    return os.path.join(tmpdir, tmpfile.name)

def get_snr_for_spectrogram(spec):
    sig_to_noise = snr.calculate_snr(spec.data)
    if math.isnan(sig_to_noise):
        sig_to_noise = -1.
    return sig_to_noise


# BASE_DIR = "/eCallisto/bursts"
BASE_DIR = "/temp"
client = wdav.WebdavConnector()
subfolders = client.list_dir(BASE_DIR)

for i in range(1,len(subfolders)):
    folder = os.path.join(BASE_DIR, subfolders[i])
    print(f"Scanning folder {folder}")
    files = client.list_dir(folder)
    if len(files) == 0:
        continue
    for i in range(1, len(files)):
        if files[i] is None:
            continue
        remote_file_path = os.path.join(folder, files[i])
        # exclude jpg files
        if remote_file_path.endswith("jpg"):
            continue
        print(f"Reading file {remote_file_path}")
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_filename = get_tempfile_name()
            client.get_file(remote_file_path, tmp_filename)
            spec = CallistoSpectrogram.read(tmp_filename)
            sig_to_noise = get_snr_for_spectrogram(spec)
            # Don't overwrite existing data
            if 'snr' not in spec.header:
                # spec.header.append(('snr', sig_to_noise, 'signal-to-noise ratio (-1.0 if nan)'))
                client.put_file(remote_file_path, tmp_filename, overwrite=True)
            os.remove(os.path.join("temp", tmp_filename))

