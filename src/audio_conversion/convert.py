from pydub import AudioSegment
from io import BytesIO


def convert_m4a_to_mp3(m4a_io):
    """
    Convert an M4A audio file to MP3 format.

    Args:
        m4a_io (BytesIO): A BytesIO object containing the M4A audio data.

    Returns:
        BytesIO: A BytesIO object containing the converted MP3 audio data.
    """
    # Load M4A file from BytesIO
    audio = AudioSegment.from_file(m4a_io, format="m4a")

    # Convert to MP3 and store in a BytesIO object
    mp3_io = BytesIO()
    audio.export(mp3_io, format="mp3")
    mp3_io.seek(0)

    return mp3_io
