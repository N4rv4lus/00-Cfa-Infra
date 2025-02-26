Hello people, here you will find some command lines to learn & use shell and linux distributions (this is not exhaustive and if you have an issue or want to understand how works some specifics commands, use the "command" + "-help" in your command line)

## Base commands :

Print current directory in shell, the actual path where you are
```shell
pwd
```

Change Directory - CD :
```shell
cd 
```

"cd + ." will "go to your current directory
```shell
cd .
```

"cd + .." will "go to the parent directory, ".." open the directory above the current one
```shell
cd ..
```

"cd + ~" will open the home directory, "~" = open home directory ex : "/home/user" (depends of your user)
```shell
cd ~
```

"cd + -" will open the parent directory and print where you are, "-"  permit cd to go to the parent directory and print the current directory you are after executing the cli "/home/admin"
```shell
cd -
```

"cd + path" will permit you to go to a specific directory, here is an exemple with the path "/home/user/test"
```shell
cd /home/user/test
```

## List Directory - "ls"

"ls" will list the current directory contents (files and folders)
```shell
ls
```

"ls + /directory1/directory2" (list the directory asked)
```shell
ls /etc
```

"ls + -a"                     (list every files even the hidden ones)
```shell
ls -a
```

"ls + -l" list the directory and gives informations about the files like rights and owners
```shell
ls -l
```

"ls + -la" will list the directory with flags/arguments/options to combine commands, here l + a will give informations of all files even hidden ones with the rights according to
```shell
ls -la
```

"ls + -R" (list all of the directories inside the directory you are and they will print the files stored inside those directories)
```shell
ls -R
```

"ls + -r" list all directories but reversed
```shell
ls -r
```

"ls + -t" list all directories by modification time newest first
```shell
ls -t
```

## File permission(s)
    
drwxr-xr-x        7                  pete          team1       4096           Nov 20 16:37    Desktop
file permission nombre de lien name_owner name_group size_in_bytes timestamp file/directory name
d: "d"=directory / "-" = file / "l" = link file /
rwx: "rwx" read write execute for the owner
rwx: read write excute for the group
rwx: for everyone else
if a character is replace by "-" means that he doens't have the permission
    
touch = create some simple file
```shell
touch new_file         # (create a file and choose the name)
```

```shell
touch existing_file    # (change the timestamp of a file)
```

file (show the description of the file content)
```shell  
file name_of_file      # (show description of the file's or folder content)
```

cat (concatenate file and show the output)
```shell
cat name_file 	#  (will show output of file or/and directories)
```

less (display text page by page)
    
```shell
less + /diretory1/diretory2/diretory3/file_name #(will open the file page by page)
```
to navigate in the less use : "q" to quit / move in the page with the arrow keys / "g" to move to the beginning of the file
"G" to move to the end of the file / "/name_of_the_words_you_searching" to search a specific word
"h" for help
    
## research command
    
arrow key top (run the last command)
!! (run the last command without typing it)
```shell
!!
```

! + the command number, will run the last command
```shell
!42
```

df (analyse disque)
df + -h (analyse disk + -h metrics)
```shell
df -h
```

history (list all the commands you have passed)

Tree cli will permit you to check the directories & files stored in a specific directory, and will order them following this order Parent-folder > Child-folder > files
```shell
tree /directory_to_check
```

## ADVANCE
stdin 0 / stdout  1  / stderr 2
< >     (stdin standard in redirection)
            
cat + < + file_you_want_to_redirect + > + file_receiver (will output file_you_want_to_redirect in file receiver)
```shell
cat < file_you_want_to_redirect > file_receiver
```

"> | >>" (stdout standard Out display something on a file)
echo + "phrase" + > + filename (will display phrase in your file)

```shell
echo "phrase" > filename
```

echo + "phrase" + >> + filename (will display your phrase and will not overwrite your file)
```shell
echo "phrase" >> filename
```

stderr (Standard Error)
            
ls + error_you_want_display + 2 + > + file_displayer (will display and redirect you error to the file you're pointing at)
```shell
ls error_you_want_display 2 > file_displayer
```

ls + error_you_want_display + & + > + file_displayer (will redirect stdout and stderr to the file you're pointing at with ">")
```shell
ls error_you_want_display & > file_displayer
```

ls + error_you_want_display + 2 + > + /dev/null (will send your error message to a discard folder, a black hole)
```shell
ls error_you_want_display 2 > /dev/null 
```

pipe and tee (display files in "less page")
ls + -la + directory_name_or_file + | + less(will display the file or path to less page ⇒  ctrl + z  to end the page)
```shell
ls -la directory_name_or_file | less
```

ls + | + tee + file_to_display (will display on the screen + in the file) 
```shell
ls | tee file_to_display
```

## env (Environment)

echo $HOME (display path)
```shell
echo $HOME
```

echo $USER   (display username)
```shell
echo $USER
```

env (display environment variable which have been set)
```shell
env
```

echo $PATH (return list of paths used by the system to runs commands)
```shell
echo $PATH
```

## paste (like cat command)
        
paste + -s + filename (will display filename on one line with tabs between words)
```shell
paste -s filename 
```

paste + -d + ' ' + -s + filename (will display filename on one line with space instead of tabs)
```shell
paste -d ' ' -s filename
```

## head (return the first lines of a file)
        
head + /directory1/directory2/filename  (return first 10 lines)
```shell
head /directory1/directory2/filename
```

head + -n + 15 + /directory1/directory2  (-n stands for number of lines)
```shell
head -n 15 /directory1/directory2
```

tail (return the last lines of a file)
        
tail + /directory1/directory2/filename (return the last 10 lines)
```shell
tail /directory1/directory2/filename
```

tail + -n + 15 + /directory1/directory2/filename (-n stands for number of lines)
```shell
tail -n 15 /directory1/directory2/filename
```
tail + -f + /directory1/directory2/filename (return last 10 lines even if the file is "growing")
```shell
tail -f /directory1/directory2/filename
```

## expand and unexpand (change tabs to space in a file)
     
expand + -a + file_name
```shell
expand -a file_name
```

## join and split
        
```
file1.txt
John 1
Jane 2
Mary 3
        
file2.txt
1 Doe
2 Doe
3 Sue
```
        
join + file1.txt + file2.txt (willl join both file by the id (1=1 / 2=2 / 3=3)
```shell
join file1.txt file2.txt 
```

join + -1 2 + -2 1 + file1.txt + file2.txt (join files -1=file1.txt / -2=file2.txt)
```shell
join -1 2 -2 1 file1.txt file2.txt
```

split + file_to_split (will separate files, up to 1000 lines, after files named x** by default)
```shell
split file_to_split
```

## sort
        
sort + file_name (will sort the line by the alphabet)
```shell
sort file_name
```
sort + -r + file_name (will reverse sort by begining by Z as the first letter)
```shell
sort -r file_name
```
sort + -n + file_name (will sort via numerical value)
```shell
sort -n file_name
```
tr (translate)

tr + a-z + A-Z (will convert your text in capital letter)
```shell
tr a-z A-Z
```
## uniq (unique)
        
uniq + file_name (remove duplicates who are adjacent)
```shell
uniq file_name
``` 
uniq + -c + file_name (remove duplicates and will count occurrences) 
```shell
uniq -c file_name
```
uniq + -u + file_name (return only unique values)
```shell
uniq -u file_name
```
uniq + -d + file_name (return only duplicates values)
```shell
uniq -d file_name
```
sort + file_name + | + uniq (remove duplicates even if they are not adjacent)
```shell
sort file_name | uniq 
```
wc and nl (word count + nl number lines)

wc + file_name (number lines + number words + nb bytes + path/name file)
```shell
wc file_name
```    

wc + -l + path/file_name (count only lines)
```shell
wc -l path/file_name
```
wc + -w + path/file_name (count only words)
```shell
wc -w path/file_name
```
wc + -v + path/file_name (count only bytes)
```shell
wc -v path/file_name
```
## grep (search words in file)

grep + wordk_searched + file_name (will show the word you're looking for in the terminal)
```shell
grep wordk_searched file_name
```

grep + -i + pattern + file_name (show word not case sensitively)
```shell
grep -i pattern file_name
```
ls + /somedir + | + grep + '.txt$' (will show all .txt in "/somedir) 
```shell
ls /somedir | grep '.txt$'
```
## TOP
        
        Let's go over what this output means, you don't have to memorize this, but come back to this when you need a reference.
        
        **1st line: This is the same information you would see if you ran the uptime command (more to come)**
        
        The fields are from left to right:
        
        1. Current time
        2. How long the system has been running
        3. How many users are currently logged on
        4. System load average (more to come)
        
        **2nd line: Tasks that are running, sleeping, stopped and zombied**
        
        **3rd line: Cpu information**
        
        1. us: user CPU time - Percentage of CPU time spent running users’ processes that aren’t niced.
        2. sy: system CPU time - Percentage of CPU time spent running the kernel and kernel processes
        3. ni: nice CPU time - Percentage of CPU time spent running niced processes
        4. id: CPU idle time - Percentage of CPU time that is spent idle
        5. wa: I/O wait - Percentage of CPU time that is spent waiting for I/O. If this value is low, the problem probably isn’t disk or network I/O
        6. hi: hardware interrupts - Percentage of CPU time spent serving hardware interrupts
        7. si: software interrupts - Percentage of CPU time spent serving software interrupts
        8. st: steal time - If you are running virtual machines, this is the percentage of CPU time that was stolen from you for other tasks
        
        **4th and 5th line: Memory Usage and Swap Usage**
        
        **Processes List that are Currently in Use**
        
        1. PID: Id of the process
        2. USER: user that is the owner of the process
        3. PR: Priority of process
        4. NI: The nice value
        5. VIRT: Virtual memory used by the process
        6. RES: Physical memory used from the process
        7. SHR: Shared memory of the process
        8. S: Indicates the status of the process: S=sleep, R=running, Z=zombie,D=uninterruptible,T=stopped
        9. %CPU - this is the percent of CPU used by this process
        10. %MEM - percentage of RAM used by this process
        11. TIME+ - total time of activity of this process
        12. COMMAND - name of the process
        
        You can also specify a process ID if you just want to track certain processes:
        
```shell
$ top -p 1
```
        
## USER and GROUPS      
sudo + command_line (will elevate you as the root if you have the password)
```shell
sudo #add any command
```

su (change youre session with the superuser (root) or you can edit the file with visudo /etc/sudoers to make user has the same rights as root without substitute the user)
```shell
su #(substitute user)
```

## /etc/passwd
   
cat /etc/passwd (return list of users)
1username / 2Userpassword(/etc/shadow) / 3 UserID / 4groupID / 5 GECOS field (comments about user) / 6 User's home directory / 7 User's shell) 
```shell
cat /etc/passwd
```
edit /etc/passwd with "vipw" or nano /etc/passwd
```shell
vipw
```
```shell
nano /etc/passwd
```

## /etc/shadow (where are stored the encrypted passwd)
        
sudo cat /etc/shadow
1Usernam / 2encrypted password / 3 date of last password as nb days if 1970 / 4Mininmum password age to change their password again / 5password maximum age / 6password warning period / 7password inactivity nb days/ 8account expiration date / 9Reserved field for future use
```
root:MyEPTEa$6Nonsense:15000:0:99999:7:::
```

/etc/group (show different group of a user)
```shell
cat /etc/group 
```
1groupName / 2groupPassword / 3GroupID / 4List of Users
```shell
root:*:0:pete
```

groups (show your group name)
```shell
groups
```
        
## User Management Tools
useradd (add an user)
sudo + useradd + name_user (will add bob as a USER it can be customisable)
```shell
sudo useradd name_user
```
userdel (delete an user)
sudo + userdel + bob (will delete bob, but you should watch if all the files were deleted) 
```shell
sudo userdel bob
```

passwd (change password)
passwd + username (will allow user to change his password, if you are root you can change it for another user) 
```shell
passwd username
```
            
File Permission
ls + -l directory/tobe/scanned
```shell
ls -l some/directory
```
        
```shell
#output
drwxr - xr - x 2 pete penguins 4096 Dec 1 11:45 .       
```
1 file type "d" / 2 user rwx / 3 group r-x / 4 other r-x
character permission r= read w = write x = execute / 4 name user "pete" / 5 name group "penguins" / 6 other user (empty) / 7 nb bits / 8 date   
        
Modifying Permissions
chmod + 755 (will grand all permissions to a file r / w / x)
4 = read / 2 write / 1 = execute
7 = 4 + 2 + 1, so 7 is the user permissions and it has read, write and execute permissions            
5 = 4 + 1, the group has read and execute permissions            
5 = 4 + 1, and all other users have read and execute permissions
```shell
chmod 755 file
```
Umask (default file permission of a newfile)         
umask + 021 (will change preset file permission by removing permission)
4 = read / 2 write / 1 = execute / 0 = no rights
7 - 0 = user have 4 read 2 write and 1 execute
7 - 2 = group have 4 read and 1 execute (-2 = no write)
7 - 1 = other have read and write (-1 = no execute)
```shell
umask
```    
Ownership Permissions
chown (change file owner of a file)         
sudo + chown + username + myfile (change user owner by "username")
```shell
sudo chown username specific_file
```
sudo + chown + username + : + groupname + myfile (change user + group owner at the same time with ":")
```shell
sudo chown username : groupname : specificfile
```
chgrp (change group owner of file)            
sudo + chgrp + groupname + myfile (change group owner "groupname")
```shell
sudo chgrp groupname myfile
```

## Setuid
```shell
ls -l /usr/bin/passwd
```
output : rwsr-xr-x 1 root root 47032 Dec 1 11:45 /usr/bin/passwd
s = that you change your UID, and it's SUID (superuserid) wich allows you to change your password (it's like if you were using sudo) 
```shell
sudo chmod 4755 myfile
```
4 = as the super user id (SUID) and the other bits are for rwx
        
Setgid
```shell
ls -l /usr/bin/wall
```     
output : rwxr-sr-x 1 root tty 19024 Dec 14 11:45 /usr/bin/wall
```shell
sudo chmod 2555 myfile 
```
2 = will change the group id and permit to use the file as if you were in the group
        
## PROCESS Permissions
        
Effective user ID = the user who is connected and launched the process, decides what access to grant        
When you launch a process, it runs with the same permissions as the user or group that ran it. This UID is used to grant access rights to a process.
Real user ID = this is the ID of the user that launched the process. These are used to track down who the user who launched the process is.
Saved user ID (UID) = allows a process to switch between the effective UID and real UID, vice versa.

Stickybit (only user or root can modify or delete a file)
example : drwxrwxrwxt 6 root root 4096 Dec 15 11:45 /tmp
t = special permission bit, only the root and user (but user is root) can delete the file
sticky bit = 1 
sudo + chmod + 1755 + myfile_or_dir (will set only the user or root can delete the directory or file)
```shell
sudo chmod 1755 myfile_or_dir
```
        
## Processes
ps + aux + | + grep + cat (show processes of other window) 
```shell
ps aux | grep cat
```
Kernel in charge of processes and run a prog that processes get the right amount of ressources
    
PID (Process ID) each process have an ID 
    
ps (processes), will show you the running process
```shell
ps
```
output : 
PID        TTY     STAT   TIME          CMD
41230    pts/4    Ss        00:00:00     bash
51224    pts/4    R+        00:00:00     ps

- PID: Process ID
- TTY: Controlling terminal associated with the process (we'll go in detail about this later)
- STAT: Process status code
- TIME: Total CPU usage time
- CMD: Name of executable/command
        
ps + aux (displays all processes running even by other users + processes details + list all processes without TTY)
```shell
ps aux
```  
ps + a (displays all processes running, including the ones being ran by other users)
```shell
ps a
```  
ps + u (shows more details about the processes.)
```shell
ps u
```     
ps + x (lists all processes that don't have a TTY)
```shell
ps x
```     
- USER: The effective user (the one whose access we are using)
- PID: Process ID
- %CPU: CPU time used divided by the time the process has been running
- %MEM: Ratio of the process's resident set size to the physical memory on the machine
- VSZ: Virtual memory usage of the entire process
- RSS: Resident set size, the non-swapped physical memory that a task has used
- TTY: Controlling terminal associated with the process
- STAT: Process status code
- START: Start time of the process
- TIME: Total CPU usage time
- COMMAND: Name of executable/command
        
## top (displays real time information running processes + refreshment every 10s)
- Controlling Terminal
two types of terminal : 
- TTY1 (first virtual console no graphics + for the OS and Hardware, daemon processes that are running for the system)
- TTY2 (pseudoterminal devices for user known as PTS)
    
Process Creation : 
processes that runs are children (PID) and they have parents (PPID). 
It's the fork system =  destroys the memory management that the kernel put into place for that process and sets up new ones for the new program.
init = process that runs all processes, runs with root privileges 
ps + l (show long format detailed view of running processes) 
```shell
ps l
```
    
## Signals
Ctrl-C or Ctrl-Z (will kill, interrupt or suspend processes) 
- SIGHUP or HUP or 1: Hangup
- SIGINT or INT or 2: Interrupt
- SIGKILL or KILL or 9: Kill (unblockable)
- SIGSEGV or SEGV or 11: Segmentation fault
- SIGTERM or TERM or 15: Software termination
- SIGSTOP or STOP: Stop
- kill (terminate signal processes)
kill + 12540 (kill the process with the PID of 12540, and does cleanup)
kill + -9  + 12445 (kill process 12540 and doesn't do anything else)

/*           
## Niceness (CPU time)
nice (print the niceness, order of process CPU Time required, -20 is most favorable / 19 lest favorable) 
nice + -n + 5 + apt + upgrade
