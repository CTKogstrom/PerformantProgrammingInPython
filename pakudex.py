from pakuri import Pakuri

def print_menu():
    print("\nPakudex Main Menu")
    print("-----------------")
    print('1. List Pakuri')
    print('2. Show Pakuri')
    print('3. Add Pakuri')
    print('4. Remove Pakuri')
    print('5. Change Pakuri Level')
    print('6. Exit \n')

def handle_list_pakuri(pakudex):
    if len(pakudex.keys()) == 0:
        print('\nNo Pakuri in Pakudex yet!')
        return
    print('\nPakuri in Pakudex:')
    i = 1
    paku_names = sorted(pakudex.keys())

    for pakuri in paku_names:
        print(f'{i}. {pakuri} ({pakudex[pakuri].species}, level {pakudex[pakuri].level})')
        i += 1


def handle_show_pakuri(pakudex):
    paku_name = input('\nEnter the name of the Pakuri to display: ')
    if paku_name in pakudex.keys():
        print(f'\nName: {paku_name}')
        print(f'Species: {pakudex[paku_name].species}')
        print(f'Level: {pakudex[paku_name].level}')
        print(f'CP: {pakudex[paku_name].cp}')
        print(f'HP: {pakudex[paku_name].hp}')
    else:
        print('Error: No such Pakuri!')


def handle_add_pakuri(pakudex):
    print('\nPakuri Information')
    print('------------------')
    new_name = input('Name: ')
    if new_name in pakudex.keys():
        print('Error: Pakudex already contains this Pakuri!')
        return pakudex
    new_species = input('Species: ')

    while True:
        try:
            new_level = int(input('Level: '))
        except:
            print('Invalid level!')
            continue
        if new_level in range(0,51):
            break
        elif new_level < 0:
            print('Level cannot be negative.')
        elif new_level > 50:
            print('Maximum level for Pakuri is 50.')
    new_paku = Pakuri(new_name, new_species, new_level)
    print(f'\nPakuri {new_paku.name} ({new_paku.species}, level {new_paku.level}) added!')

    pakudex.update({new_name:new_paku})

    return pakudex



def handle_remove_pakuri(pakudex):
    remove_name = input('\nEnter the name of the Pakuri to remove: ')
    if remove_name in pakudex.keys():
        pakudex.pop(remove_name)
        print(f'Pakuri {remove_name} removed.')
    else:
        print('Error: No such Pakuri!')
    return pakudex


def handle_change_pakuri_level(pakudex):
    paku_change = input('\nEnter the name of the Pakuri to change: ')

    if not(paku_change in pakudex.keys()):
        print('Error: No such Pakuri!')
        return pakudex

    while True:
        try:
            new_level = int(input('Enter the new level for the Pakuri: '))
        except:
            print('Invalid level!')
            continue
        if new_level in range(0, 51):
            pakudex[paku_change].level = new_level
            return pakudex
        elif new_level < 0:
            print('Level cannot be negative.')
        elif new_level > 50:
            print('Maximum level for Pakuri is 50.')


def main():
    print("Welcome to Pakudex: Let's Go!")
    pakudex = {}
    choices = {1: handle_list_pakuri, 2: handle_show_pakuri, 3: handle_add_pakuri, 4: handle_remove_pakuri, 5: handle_change_pakuri_level}

    running = 1

    while running:

        print_menu()
        try:
            choice = int(input('What would you like to do? '))
        except:
            print('\nUnrecognized menu selection!')
            continue

        if choice in range(3,6):
            pakudex = choices[choice](pakudex)
        elif choice in range(1,3):
            choices[choice](pakudex)
        elif choice == 6:
            del pakudex
            print("\nThanks for using Pakudex: Let's Go! Bye!")
            break
        else:
            print('\nUnrecognized menu selection!')
            continue


if __name__ == '__main__':
    main()