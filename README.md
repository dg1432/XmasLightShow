# Christmas Light Show
This project is based on [this Instructable](http://www.instructables.com/id/Raspberry-Pi-Christmas-Tree-Light-Show/) with an added Flask web interface, sequence creator, and some extra sequence files.

## Setup
TODO

## Web Interface
TODO

## Sequence Creator
With the Sequence Creator, production time can be greatly reduced when creating new sequence files as the user can "play along" as the song is playing. The keyboard input captured while the song is playing is translated to lines in the corresponding sequence file.

To run the Sequence Creator, run `sudo python /path/to/sequence_creator.py mp3_filename` in the terminal, without the .mp3 file extension. The program will open a small window and play the specified song. As the song is playing, the program will accept user input from the keyboard to write lines to the song’s sequence file. Once the song is finished playing, the user input captured during the duration of the song will be merged with existing lines in the sequence file. The following keys map to the following channels:
- ; -> 1 (top of the tree)
- L -> 2
- K -> 3
- J -> 4
- Spacebar -> 5 (bottom of the tree)
- A -> 6 (blue)
- S -> 7 (green)
- D -> 8 (red)

## Songs
The following is a list of songs that have been sequenced. Some of the sequence files come straight from the Instructable that I based this project on and from some of the comments.
- Carol of the Bells
- Let It Go
- A Mad Russian’s Christmas
- God Rest Ye Merry Gentlemen
- Linus and Lucy
- Silent Night
- Wizards in Winter
- Twelve Days of Christmas

## Contributions
Code and sequence file contributions to this project are welcome, or feel free to fork the project. Please make a pull request and wait for approval before merging. If you are adding sequence files, you may also want to add a comment to the original Instructable so others can see your songs more easily. :)
