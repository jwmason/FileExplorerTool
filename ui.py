# Mason Wong
# masonjw1@uci.edu
# 48567424

from pathlib import Path
import os
from Profile import Profile, Post
import ds_client
import ipaddress


def recursive_print(path, print_dir=True, _name=None, _ext=None):
    '''Recursively prints all items in path.'''
    contents = list(path.iterdir())
    for thing in contents:
        if thing.is_dir():
            contents.append(thing)
            contents.remove(thing)

    for child in contents:
        if child.is_dir():
            if print_dir:
                print(child)
            recursive_print(child, print_dir, _name, _ext)
        else:
            if _name:
                if child.name == _name:
                    print(child)
            elif _ext:
                if _ext == child.suffix[1:]:
                    print(child)
            else:
                print(child)


def simple_print(path, _name=None, _ext=None):
    '''Prints all folders but not subfolders in path.'''
    for child in path.iterdir():
        if _name:
            if child.name == _name:
                print(child)
        elif _ext:
            if child.suffix[1:] == _ext:
                print(child)
        else:
            if child.is_file():
                print(child)


def print_everything(path):
    '''Prints everything in the path, files first and directories last.'''
    myList = []
    for child in path.iterdir():
        if os.path.isfile(child):
            print(child)
        else:
            myList.append(child)
    for i in myList:
        print(i)


def e_p_commands2(path, user_input):
    '''User interface that handles editing and printing inside DSU file.'''
    if user_input != 'Q':
        profile = Profile()
        profile.load_profile(f'{path}')
        if user_input == '1':
            print("\n1. Edit username")
            print("2. Edit password")
            print("3. Edit bio")
            print("4. Add post")
            print("5. Delete post")
            print("Q. Quit\n")
            user_input = str(input('Enter your choice: '))
            if user_input == '1':
                username = str(input('Enter new username: '))
                profile.username = username
                print("Username updated.\n")
            elif user_input == '2':
                password = str(input('Enter new username: '))
                profile.password = password
                print("Password updated.\n")
            elif user_input == '3':
                bio = str(input('Enter new bio: '))
                if bio == '' or bio == ' ':
                    print('Bio cannot be empty or whitespace.')
                else:
                    profile.bio = bio
                    print('\nBio updated.\n')
                    user_input = input('Would you like to publish this bio? (y/n): ')
                    if user_input == 'y':
                        ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, profile._posts, profile.bio)
                        print("\nBio published.\n")
                    elif user_input == 'n':
                        pass
                    else:
                        error()
            elif user_input == '4':
                post = str(input('Enter post: '))
                if post == '' or post == ' ':
                    print('Post cannot be empty or whitespace.')
                else:
                    post = Post(post)
                    profile.add_post(post)
                    user_input = input('Would you like to publish this post online? (y/n): ')
                    if user_input == 'y':
                        user_input = input('Would you like to publish a bio with this post? (y/n): ')
                        if user_input == 'y':
                            bio_choice = int(input('Would you like to use\n1. Current Bio\n2. New Bio\nEnter your choice: '))
                            if bio_choice == 1:
                                ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, Post.get_entry(post), profile.bio)
                                print("\nBio published.\n")
                            elif bio_choice == 2:
                                bio = str(input('Enter your new bio: '))
                                profile.bio = bio
                                ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, Post.get_entry(post), profile.bio)
                                print("\nBio published.\n")
                            else:
                                error()
                        elif user_input == 'n':
                            pass
                        else:
                            error()
                        ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, Post.get_entry(post))
                        print('\nPost published.\n')
                    elif user_input == 'n':
                        pass
                    else:
                        error()
            elif user_input == '5':
                try:
                    index = int(input('Enter index of post you want to delete (0 is the first index): '))
                    print('Post Deleted:', profile.del_post(index), "\n")
                except IndexError:
                    print('Post index does not exist.\n')
            elif user_input == 'Q':
                pass
            else:
                error()
            profile.save_profile(f'{path}')
        elif user_input == '2':
            print("\n1. Print username")
            print("2. Print password")
            print("3. Print bio")
            print("4. Print posts")
            print("5. Print post")
            print("6. Print all")
            print("Q. Quit\n")
            user_input = str(input('Enter your choice: '))
            if user_input == '1':
                print('Username: ' + profile.username, '\n')
            elif user_input == '2':
                print('Password: ' + profile.password, '\n')
            elif user_input == '3':
                print('Bio: ' + profile.bio, '\n')
            elif user_input == '4':
                posts = profile.get_posts()
                print('Posts: ', posts, '\n')
            elif user_input == '5':
                try:
                    index = int(user_input.index('-post')) + 1
                    index = int(user_input[index])
                    print('Post:', profile._posts[index], '\n')
                except IndexError:
                    print('Post index does not exist.\n')
            elif user_input == '6':
                print('DSU Server: ' + profile.dsuserver)
                print('Username: ' + profile.username)
                print('Password: ' + profile.password)
                print('Bio: ' + profile.bio)
                posts = profile.get_posts()
                print('All Posts:', posts, '\n')
            elif user_input == 'Q':
                pass
            else:
                error()
        else:
            error()
    else:
        pass


def e_p_commands(path):
    '''Handles the main menu of the Edit and Print Commands that is accessed after the initial
    commands C or O.'''
    print("1. Edit profile information")
    print("2. Print profile information")
    print("Q. Quit\n")
    user_input = input('Enter your choice: ')
    while user_input != 'Q':
        e_p_commands2(path, user_input)
        print("1. Edit profile information")
        print("2. Print profile information")
        print("Q. Quit\n")
        user_input = input('Enter your choice: ')
    print('\nLeft the DSU File. Back in main menu.\nPress Q again to quit program.')


def handle_input(user_input):
    '''Handles the input of the User and his/her initial commands.'''
    if user_input == 'L':
        _path = Path(input('\nEnter the path you would like to use: '))
        if not os.path.exists(_path):
            print('Error. Path does not exist.')
            handle_input(user_input)
        print('\n1. List contents of source directory')
        print('2. List files in specificed directory')
        print('3. Display all file paths with file name in it')
        print('4. Display all files with certain suffix')
        print('5. List contents of source directory and subdirectories (includes recursive options for #2, #3, #4)')
        print('Q. Quit\n')
        user_input = str(input('Enter your choice: '))

        if user_input == '1':
            try:
                print_everything(_path)
            except FileNotFoundError:
                error()
        elif user_input == '2':
            simple_print(_path)
        elif user_input == '5':
            print('\n1. Recursively display all file paths with file name in it')
            print('2. Recursively display all files with certain suffix')
            print('3. Recursively list files in specificed directory')
            print('4. Recursively list contents of source directory')
            print('Q. Quit\n')
            user_input = str(input('Enter your choice: '))

            if user_input == '1':
                user_input = str(input('Enter file (including suffix): '))
                _name = str(user_input)
                recursive_print(_path, False, str(_name))
            elif user_input == '2':
                user_input = str(input('Enter suffix (three characters): '))
                _ext = str(user_input)
                recursive_print(_path, False, None, str(_ext))
            elif user_input == '3':
                recursive_print(_path, False)
            elif user_input == '4':
                recursive_print(_path)
            elif user_input == 'Q':
                pass
            else:
                error()
        elif user_input == '3':
            _name = str(' '.join(list(user_input)[4:]))
            simple_print(_path, _name)
        elif user_input == '4':
            _ext = str(' '.join(list(user_input)[4:]))
            simple_print(_path, None, _ext)
        elif user_input == 'Q':
            pass
        else:
            error()

    elif user_input == 'C':
        _path = Path(input('\nEnter the path you would like to create a DSU file in: '))
        if os.path.exists(_path):
            pass
        else:
            print('Error. Path does not exist.')
            handle_input(user_input)
        user_input = str(input('Enter the name of the DSU file you would like to create: '))
        new_file = f'\{user_input}.dsu'
        C_path = str(_path) + new_file
        if os.path.exists(Path(C_path)):
            if os.path.getsize(C_path) != 0:
                with open(f'{C_path}', 'r') as myFile:
                    print('DSU FILE ' + C_path.split('\\')[-1] + ' LOADED\n')
            else:
                print('DSU FILE ' + C_path.split('\\')[-1] + ' LOADED')
                print('EMPTY\n')
            e_p_commands(C_path)
        else:
            try:
                user_name_input = str(input('Username: '))
                password_input = str(input('Password: '))
                dsuserver = str(input('DSU Server: '))
                cond = True
                try:
                    ip = ipaddress.ip_address(dsuserver)
                except ValueError:
                    cond = False
                    print('This DSU Server is not open. Please enter another.')
                if cond is True:
                    with open(f'{user_input}.dsu', 'x') as f:
                        profile = Profile(dsuserver, user_name_input, password_input)
                        profile.save_profile(f'{C_path}')
                        print('You have created the DSU File: ' + C_path.split('\\')[-1] + '\n')
                        e_p_commands(C_path)
            except FileExistsError:
                error()

    elif user_input == 'O':
        _path = Path(input('\nEnter the path to the DSU file you would like to open (including the file): '))
        if os.path.exists(_path):
            pass
        else:
            print('Error. Path does not exist.')
            handle_input(user_input)
        try:
            O_path = str(_path).split("\\")
            file = O_path[-1]
            if file[-3:] == 'dsu':
                if os.path.getsize(_path) != 0:
                    with open(f'{_path}', 'r') as myFile:
                        print('DSU FILE LOADED\n')
                else:
                    print('DSU FILE LOADED')
                    print('EMPTY\n')
                e_p_commands(_path)
            else:
                error()
        except FileNotFoundError:
            error()
    elif user_input == 'D':
        _path = Path(input('\nEnter the path of the file you would like to delete (including the file): '))
        if os.path.exists(_path):
            pass
        else:
            print('Error. Path does not exist.')
            handle_input(user_input)
        D_path = _path
        try:
            D_path.unlink()
            print(f'{D_path} DELETED')
        except FileNotFoundError:
            error()
    elif user_input == 'R':
        _path = Path(input('\nEnter the path of the DSU you would like to read (inlcuding the file): '))
        if os.path.exists(_path):
            pass
        else:
            print('Error. Path does not exist.')
        handle_input(user_input)
        R_path = str(_path).split("\\")
        file = R_path[-1]
        try:
            if file[-3:] == 'dsu':
                if os.path.getsize(_path) != 0:
                    with open(f'{_path}', 'r') as myFile:
                        line = myFile.read()
                        line = line.rstrip('\n')
                        print(line)
                else:
                    print('DSU File EMPTY')
            else:
                error()
        except FileNotFoundError:
            error()
    else:
        error()


def error():
    '''Function that prints ERROR when is it encountered.'''
    print('ERROR')


def run():
    '''Runs the user interface.'''
    print('Hello User! Welcome to my program!')
    while (cmd := input('\nPress L to list files and directories (L), create a file (C), open a file (O), or delete a file (D).\nPress Q to quit the program.\nEnter your choice: ')) != 'Q':
        handle_input(cmd)
    print('\nProgram exited. Have a nice day!')
