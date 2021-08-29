from __future__ import division

from pydub.audio_segment import AudioSegment, AUDIO_FILE_EXT_ALIASES, fix_wav_headers
import os
import subprocess
from tempfile import NamedTemporaryFile
import sys
from pydub.logging_utils import log_conversion, log_subprocess_output
from pydub.utils import mediainfo_json, fsdecode, _fd_or_path_or_tempfile

from io import BytesIO

try:
    from itertools import izip
except:
    izip = zip

from pydub.exceptions import CouldntDecodeError

if sys.version_info >= (3, 0):
    basestring = str
    xrange = range
    StringIO = BytesIO


class FixedAudioSegment(AudioSegment):
    @classmethod
    def from_file(cls, file, format=None, codec=None, parameters=None, start_second=None, duration=None, **kwargs):
        orig_file = file
        try:
            filename = fsdecode(file)
        except TypeError:
            filename = None
        file, close_file = _fd_or_path_or_tempfile(file, 'rb', tempfile=False)

        if format:
            format = format.lower()
            format = AUDIO_FILE_EXT_ALIASES.get(format, format)

        def is_format(f):
            f = f.lower()
            if format == f:
                return True

            if filename:
                return filename.lower().endswith(".{0}".format(f))

            return False

        if is_format("wav"):
            try:
                if start_second is None and duration is None:
                    return cls._from_safe_wav(file)
                elif start_second is not None and duration is None:
                    return cls._from_safe_wav(file)[start_second*1000:]
                elif start_second is None and duration is not None:
                    return cls._from_safe_wav(file)[:duration*1000]
                else:
                    return cls._from_safe_wav(file)[start_second*1000:(start_second+duration)*1000]
            except:
                file.seek(0)
        elif is_format("raw") or is_format("pcm"):
            sample_width = kwargs['sample_width']
            frame_rate = kwargs['frame_rate']
            channels = kwargs['channels']
            metadata = {
                'sample_width': sample_width,
                'frame_rate': frame_rate,
                'channels': channels,
                'frame_width': channels * sample_width
            }
            if start_second is None and duration is None:
                return cls(data=file.read(), metadata=metadata)
            elif start_second is not None and duration is None:
                return cls(data=file.read(), metadata=metadata)[start_second*1000:]
            elif start_second is None and duration is not None:
                return cls(data=file.read(), metadata=metadata)[:duration*1000]
            else:
                return cls(data=file.read(), metadata=metadata)[start_second*1000:(start_second+duration)*1000]

        conversion_command = [cls.converter,
                              '-y',  # always overwrite existing files
                              ]

        # If format is not defined
        # ffmpeg/avconv will detect it automatically
        if format:
            conversion_command += ["-f", format]

        if codec:
            # force audio decoder
            conversion_command += ["-acodec", codec]

        read_ahead_limit = kwargs.get('read_ahead_limit', -1)
        if filename:
            conversion_command += ["-i", filename]
            stdin_parameter = None
            stdin_data = None
        else:
            if cls.converter == 'ffmpeg':
                conversion_command += ["-read_ahead_limit", str(read_ahead_limit),
                                       "-i", "cache:pipe:0"]
            else:
                conversion_command += ["-i", "-"]
            stdin_parameter = subprocess.PIPE
            stdin_data = file.read()

        if codec:
            info = None
        else:
            info = mediainfo_json(orig_file, read_ahead_limit=read_ahead_limit)
        if info:
            audio_streams = [x for x in info['streams']
                             if x['codec_type'] == 'audio']
            # This is a workaround for some ffprobe versions that always say
            # that mp3/mp4/aac/webm/ogg files contain fltp samples
            audio_codec = audio_streams[0].get('codec_name')
            if (audio_streams[0].get('sample_fmt') == 'fltp' and
                    audio_codec in ['mp3', 'mp4', 'aac', 'webm', 'ogg']):
                bits_per_sample = 16
            else:
                bits_per_sample = audio_streams[0]['bits_per_sample']
            if bits_per_sample == 8:
                acodec = 'pcm_u8'
            else:
                acodec = 'pcm_s%dle' % bits_per_sample

            conversion_command += ["-acodec", acodec]

        conversion_command += [
            "-vn",  # Drop any video streams if there are any
            "-f", "wav"  # output options (filename last)
        ]

        if start_second is not None:
            conversion_command += ["-ss", str(start_second)]

        if duration is not None:
            conversion_command += ["-t", str(duration)]

        conversion_command += ["-"]

        if parameters is not None:
            # extend arguments with arbitrary set
            conversion_command.extend(parameters)

        log_conversion(conversion_command)

        with open(os.devnull, 'rb') as devnull:
            p = subprocess.Popen(conversion_command, stdin=devnull,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_out, p_err = p.communicate(input=stdin_data)

        if p.returncode != 0 or len(p_out) == 0:
            if close_file:
                file.close()
            raise CouldntDecodeError(
                "Decoding failed. ffmpeg returned error code: {0}\n\nOutput from ffmpeg/avlib:\n\n{1}".format(
                    p.returncode, p_err.decode(errors='ignore') ))

        p_out = bytearray(p_out)
        fix_wav_headers(p_out)
        p_out = bytes(p_out)
        obj = cls(p_out)

        if close_file:
            file.close()

        if start_second is None and duration is None:
            return obj
        elif start_second is not None and duration is None:
            return obj[0:]
        elif start_second is None and duration is not None:
            return obj[:duration * 1000]
        else:
            return obj[0:duration * 1000]

    @classmethod
    def from_file_using_temporary_files(cls, file, format=None, codec=None, parameters=None, start_second=None, duration=None, **kwargs):
        orig_file = file
        file, close_file = _fd_or_path_or_tempfile(file, 'rb', tempfile=False)

        if format:
            format = format.lower()
            format = AUDIO_FILE_EXT_ALIASES.get(format, format)

        def is_format(f):
            f = f.lower()
            if format == f:
                return True
            if isinstance(orig_file, basestring):
                return orig_file.lower().endswith(".{0}".format(f))
            if isinstance(orig_file, bytes):
                return orig_file.lower().endswith((".{0}".format(f)).encode('utf8'))
            return False

        if is_format("wav"):
            try:
                obj = cls._from_safe_wav(file)
                if close_file:
                    file.close()
                if start_second is None and duration is None:
                    return obj
                elif start_second is not None and duration is None:
                    return obj[start_second*1000:]
                elif start_second is None and duration is not None:
                    return obj[:duration*1000]
                else:
                    return obj[start_second*1000:(start_second+duration)*1000]
            except:
                file.seek(0)
        elif is_format("raw") or is_format("pcm"):
            sample_width = kwargs['sample_width']
            frame_rate = kwargs['frame_rate']
            channels = kwargs['channels']
            metadata = {
                'sample_width': sample_width,
                'frame_rate': frame_rate,
                'channels': channels,
                'frame_width': channels * sample_width
            }
            obj = cls(data=file.read(), metadata=metadata)
            if close_file:
                file.close()
            if start_second is None and duration is None:
                return obj
            elif start_second is not None and duration is None:
                return obj[start_second * 1000:]
            elif start_second is None and duration is not None:
                return obj[:duration * 1000]
            else:
                return obj[start_second * 1000:(start_second + duration) * 1000]

        input_file = NamedTemporaryFile(mode='wb', delete=False)
        try:
            input_file.write(file.read())
        except(OSError):
            input_file.flush()
            input_file.close()
            input_file = NamedTemporaryFile(mode='wb', delete=False, buffering=2 ** 31 - 1)
            if close_file:
                file.close()
            close_file = True
            file = open(orig_file, buffering=2 ** 13 - 1, mode='rb')
            reader = file.read(2 ** 31 - 1)
            while reader:
                input_file.write(reader)
                reader = file.read(2 ** 31 - 1)
        input_file.flush()
        if close_file:
            file.close()

        output = NamedTemporaryFile(mode="rb", delete=False)

        conversion_command = [cls.converter,
                              '-y',  # always overwrite existing files
                              ]

        # If format is not defined
        # ffmpeg/avconv will detect it automatically
        if format:
            conversion_command += ["-f", format]

        if codec:
            # force audio decoder
            conversion_command += ["-acodec", codec]

        conversion_command += [
            "-i", input_file.name,  # input_file options (filename last)
            "-vn",  # Drop any video streams if there are any
            "-f", "wav"  # output options (filename last)
        ]

        if start_second is not None:
            conversion_command += ["-ss", str(start_second)]

        if duration is not None:
            conversion_command += ["-t", str(duration)]

        conversion_command += [output.name]

        if parameters is not None:
            # extend arguments with arbitrary set
            conversion_command.extend(parameters)

        log_conversion(conversion_command)

        if sys.platform == 'win32':
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0
        with open(os.devnull, 'rb') as devnull:
            p = subprocess.Popen(conversion_command, stdin=devnull, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=creationflags)
        p_out, p_err = p.communicate()

        log_subprocess_output(p_out)
        log_subprocess_output(p_err)

        try:
            if p.returncode != 0:
                raise CouldntDecodeError(
                    "Decoding failed. ffmpeg returned error code: {0}\n\nOutput from ffmpeg/avlib:\n\n{1}".format(
                        p.returncode, p_err.decode(errors='ignore') ))
            obj = cls._from_safe_wav(output)
        finally:
            input_file.close()
            output.close()
            os.unlink(input_file.name)
            os.unlink(output.name)

        if start_second is None and duration is None:
            return obj
        elif start_second is not None and duration is None:
            return obj[0:]
        elif start_second is None and duration is not None:
            return obj[:duration * 1000]
        else:
            return obj[0:duration * 1000]

