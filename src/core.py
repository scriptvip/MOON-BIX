from src.__init__ import *
from src.moonbix import MoonBix
def menu():
    print(f"         {Colors.MAGENTA}=> Main Menu\n")
    menu_item(1, "Start Script")
    menu_item(2, 'Edit Config')
    menu_item(3, 'About Devoloper')
    menu_item(99, 'Exit')
    options = {
        '1': start_script,
        '2': edit_config,
        '3': about_devoloper,
        '99': exit_code
    }
    print()
    while True:
        choice = input(f'{Colors.CYAN} Choice : ')
        if choice not in options:
            print(f'{Colors.YELLOW} Choose Valid Option')
            continue
        break

    options[choice]()
        
def start_script():
    while True:
        awak()
        tokens = load_tokens()
        log(Colors.CYAN + f' Number of Accounts {Colors.GREEN}{len(tokens)}')
        
        for index, token in enumerate(tokens):
            try:
                log_line()
                countdown_timer(config('TIME_BETWEEN_ACCOUNTS', 10))
                account = MoonBix(token, random_proxy(), config('TIMEOUT', 6))
                log(f'{Colors.BLUE} Account Number : {Colors.GREEN}{index+1}')
                log(f'{Colors.BLUE} Account Username : {Colors.GREEN}{get_username(token)}')
                log(f'{Colors.YELLOW} Trying To Login ...')
                res = account.login()

                if res == 'success': log(f'{Colors.GREEN} Done Login Success !')
                else:
                    if res == 'fail':
                        log(f'{Colors.RED} Faild To Login Please Check Account Token !')
                    else:
                        log(f'{Colors.BLACK} {res}')
                        log(f'{Colors.RED} UnExpected Erro Please Contact With Devoloper To Fix !')
                    continue
                
                while True:
                    res = account.user_info()
                    if not res['success']:
                        log(f'{Colors.RED} Faild To Retrive Account info !')
                        break
                    total_attempts = res['data']['metaInfo']['totalAttempts']
                    avilble_attempts = total_attempts - res['data']['metaInfo']['consumedAttempts']
                    log(f'{Colors.BLACK} ---------------------------------')
                    log(f"{Colors.BLUE} Account Balance : {Colors.GREEN}{res['data']['metaInfo']['totalGrade']}")
                    log(f'{Colors.BLUE} Total Tickets : {Colors.GREEN}{total_attempts}')
                    log(f'{Colors.BLUE} Avilble Tickets : {Colors.GREEN}{avilble_attempts}')
                    

                    if avilble_attempts < 1:
                        log(f'{Colors.YELLOW} No Tickets Avilable !')
                        break

                    countdown_timer(config('SMALL_DELAY', 3))

                    log(f' {Colors.BLUE}Starting game !')
                    res = account.start_game()
                    
                    if res == 'success': log(f' {Colors.GREEN}Done Game Has Started !')
                    else:
                        if res == 'attempts not enough':
                            log(f' {Colors.BLUE}Attempts not enough !')
                        else :
                            log(f' {Colors.BLACK} {res}')
                            log(f' {Colors.RED} UnExpected Erro Please Contact With Devoloper To Fix !')
                        continue
                    
                    countdown_timer(config('GAME_TIME', 42))

                    log(f' {Colors.BLUE}Getting game data ... ')
                    
                    retry = config('MAX_RETRY', 3)
                    for __ in range(retry):
                        res = account.game_data()
                        if res == 'success':
                            log(f' {Colors.GREEN}Done Game Data Dumped !')
                            retry = 0
                            break
                    
                    if retry:
                        log(f' {Colors.RED}Faild To Dump Game Data !')
                        log(f' {Colors.RED}If This message appear more than onece Please Tell The Devoloer [WARRING] !')
                        log(f' {Colors.RED}{res}')
                        continue

                    countdown_timer(config('SMALL_DELAY', 3))
                    
                    res = account.complete_game()
                    
                    log(f' {Colors.BLUE}Completing The Game ...')

                    if res == 'success':
                        log(f' {Colors.GREEN}Success + {account.game["log"]} (^__*)')
                    else:
                        log(f' {Colors.RED}Faild To Dump Game Data !')
                        log(f' {Colors.RED}If This message appear more than onece Please Tell The Devoloer [WARRING] !')
                        continue
                    
                    countdown_timer(config('DELAY_AFTER_GAME', 5))

                countdown_timer(config('SMALL_DELAY', 3))
            except KeyboardInterrupt:
                exit_code()
            except Exception as E:
                log(f'{Colors.RED} {E}')
        countdown_timer(config('DELAY_BEFORE_RESTART', 70))
            

def edit_config():
    awak()
    config_values = read_config()
    i=1
    print(f"         {Colors.MAGENTA}=> Edit Config\n")
    conf = []
    for key, val in config_values.items():
        menu_item(i, key+Colors.YELLOW+' : '+Colors.GREEN+str(val))
        conf.append([key, val])
        i += 1
    menu_item(99, f'{Colors.YELLOW}Back\n')

    while True:
        choice = input(f'{Colors.CYAN} Choice : ')
        if choice == '99':
            awak()
            menu()
            return
        try:int(choice)
        except:
            print(f'{Colors.YELLOW} Choose Valid Intger')
            continue

        if int(choice)<1 or int(choice)>len(conf):
            print(f'{Colors.YELLOW} Choose Valid Option')
            continue
        break

    choice = int(choice)-1
    while True:
        value = input(f'{Colors.GREEN} {conf[choice][0]} = ')
        
        try:int(value)
        except:
            print(f'{Colors.YELLOW} Enter Vaild Number !')
            continue

        break
    
    edit_config_value(conf[choice][0], eval(value))

    awak()
    menu()

    
def about_devoloper():
    awak()
    print(f"{Colors.BLUE} Devoloper : {Colors.GREEN}Abdo Sleem")
    print(f"{Colors.BLUE} Github : {Colors.GREEN}https://github.com/scriptvip")
    print(f"{Colors.BLUE} Telegram : {Colors.GREEN}https://t.me/glitch_no")
    log_line()
    input(f"\n   {Colors.YELLOW} Press Enter To Back !")
    awak()
    menu()

def exit_code():
    log_line()
    log(f'{Colors.RED} Exiting ...')
    exit()