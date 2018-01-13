import pygame
import time
import sys

def main():
    sequence_data = []
    new_sequence_data = []
    song_file = 'static/music/' + sys.argv[1] + '.mp3'
    sequence_file = 'static/sequences/' + sys.argv[1] + '.txt'

    # Load the song
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)

    # Load the sequence file
    with open(sequence_file, 'r') as f:
        sequence_data = f.readlines()

    # Create a window
    background_colour = (255,255,255)
    (width, height) = (1, 1)
 
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Sequencer Creator')
    screen.fill(background_colour)
    pygame.display.flip()

    print 'Starting!'

    # Start the music and listen for keytaps
    pygame.mixer.music.play()
    start_time = int(round(time.time() * 1000))
    while pygame.mixer.music.get_busy():
        events = pygame.event.get()
        for event in events:
            command = ''
            if event.type == pygame.KEYDOWN:
                curr_time = str(int(round(time.time() * 1000)) - start_time)
                if event.key == pygame.K_SEMICOLON:
                    command = curr_time.zfill(6) + ',1,1\n'
                if event.key == pygame.K_l:
                    command = curr_time.zfill(6) + ',2,1\n'
                if event.key == pygame.K_k:
                    command = curr_time.zfill(6) + ',3,1\n'
                if event.key == pygame.K_j:
                    command = curr_time.zfill(6) + ',4,1\n'
                if event.key == pygame.K_SPACE:
                    command = curr_time.zfill(6) + ',5,1\n'
                if event.key == pygame.K_a:
                    command = curr_time.zfill(6) + ',6,1\n'
                if event.key == pygame.K_s:
                    command = curr_time.zfill(6) + ',7,1\n'
                if event.key == pygame.K_d:
                    command = curr_time.zfill(6) + ',8,1\n'
            elif event.type == pygame.KEYUP:
                curr_time = str(int(round(time.time() * 1000)) - start_time)
                if event.key == pygame.K_SEMICOLON:
                    command = curr_time.zfill(6) + ',1,0\n'
                if event.key == pygame.K_l:
                    command = curr_time.zfill(6) + ',2,0\n'
                if event.key == pygame.K_k:
                    command = curr_time.zfill(6) + ',3,0\n'
                if event.key == pygame.K_j:
                    command = curr_time.zfill(6) + ',4,0\n'
                if event.key == pygame.K_SPACE:
                    command = curr_time.zfill(6) + ',5,0\n'
                if event.key == pygame.K_a:
                    command = curr_time.zfill(6) + ',6,0\n'
                if event.key == pygame.K_s:
                    command = curr_time.zfill(6) + ',7,0\n'
                if event.key == pygame.K_d:
                    command = curr_time.zfill(6) + ',8,0\n'
            if command != '':
                new_sequence_data.append(command)

    # Merge the new commands into the old ones and write to the file
    data_to_write = sequence_data + new_sequence_data
    data_to_write.sort()
    with open(sequence_file, 'w') as f:
        for line in data_to_write:
            f.write(line)

if __name__ == '__main__':
    main()
