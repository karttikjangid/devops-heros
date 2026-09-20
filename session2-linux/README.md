# linux tasks

## Task 1: Soft Link & Hard Link

A hard link is another name for the same file, both point to the same data. delete one name and the file is still there.

A soft link (symlink) is a shortcut, it just points to the path of the real file. delete the real file and the soft link breaks.

make a hard link: `ln target.txt link.txt`
Make a soft link: `ln -s target.txt link.txt`
delete a link: `rm link.txt`

check the inode with `ls -li`, same inode number = same file.

Interview answer: hard link shares the inode with the original so it survives even if the original gets deleted, soft link is a separate file storing a path so it breaks if the target is gone (dangling link). hard links only work within one filesystem and cant point to directories, soft links can do both.

## task 2: adduser vs useradd

useradd is the basic command, no prompts, no home folder unless you pass a flag for it.

adduser is the friendlier one, it asks questions (like a password) and makes the home folder for you. on Ubuntu its a script that calls useradd underneath.

Ubuntu recommends adduser since its harder to mess up.

command to make a test user: `sudo adduser testuser`

## Task 3 - journalctl

journalctl reads logs collected by systemd-journald, boot logs kernel logs and service logs all in one place.

see all logs: `journalctl`
Watch logs live: `journalctl -f`
logs for one service: `journalctl -u nginx`
journalctl -b shows logs from just the current boot

## Task 4: Linux command cheat sheet

commands i practiced:

- ls, cd, pwd = moving around folders
- cp, mv, rm = copy, move, delete files
- chmod, chown -> permissions and owner
- grep, find = search text and files
- ps, top = running processes
- df and du = disk space
- tar = archives
- ssh, scp, curl, wget = network stuff
