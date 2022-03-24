import picamera

def main():
    print(f'Instantiating PiCamera object')
    with picamera.PiCamera() as camera:
        print(f'Camera EXIF Data: {camera.exif_tags}')

if __name__ == '__main__':
    main()
