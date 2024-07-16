from pytube import YouTube
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
import requests
import os

def download_video_as_mp3(youtube_url, output_path):
    try:
        # Descargar el video
        yt = YouTube(youtube_url)
        video = yt.streams.filter(only_audio=True).first()
        output_file = video.download(output_path)

        #Convertir el archivo de audio a MP3
        base, ext = os.path.splitext(output_file)
        new_file = os.path.join(output_path, yt.title + '.mp3')  # Guardar en la carpeta de música con el título del video como nombre
        audio = AudioSegment.from_file(output_file)
        audio.export(new_file, format='mp3')

        # Descargar la carátula
        thumbnail_url = yt.thumbnail_url
        thumbnail_response = requests.get(thumbnail_url)
        thumbnail_file = base + '.jpg'
        with open(thumbnail_file, 'wb') as f:
            f.write(thumbnail_response.content)

        # Añadir metadatos al archivo MP3
        audiofile = MP3(new_file, ID3=ID3)

        # Agregar ID3 tags si no existen
        try:
            audiofile.add_tags()
        except:
            pass

        audiofile.tags.add(TIT2(encoding=3, text=yt.title))
        audiofile.tags.add(TPE1(encoding=3, text=yt.author))
        audiofile.tags.add(TALB(encoding=3, text=yt.title))
        with open(thumbnail_file, 'rb') as albumart:
            audiofile.tags.add(
                APIC(
                    encoding=3, 
                    mime='image/jpeg', 
                    type=3, 
                    desc=u'Cover', 
                    data=albumart.read()
                )
            )

        audiofile.save()

        # Eliminar el archivo de audio original y la carátula temporal
        os.remove(output_file)
        os.remove(thumbnail_file)
        
        print(f"Archivo descargado y convertido: {new_file}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Solicitar la URL del video de YouTube
    youtube_url = input("Por favor, ingresa la URL del video de YouTube: ")

    # Ruta de salida para el archivo MP3 (cambiar según tu carpeta de música)
    output_path = '/home/kogaraashi/Música'

    download_video_as_mp3(youtube_url, output_path)

if __name__ == "__main__":
    main()
