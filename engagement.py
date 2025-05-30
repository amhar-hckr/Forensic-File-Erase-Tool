import random
import time
import os
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.progress import track

console = Console()

# ASCII Art title
TITLE = """
[bold cyan]
███████╗███╗   ██╗ ██████╗  █████╗  ██████╗ ███████╗██████╗ 
██╔════╝████╗  ██║██╔════╝ ██╔══██╗██╔════╝ ██╔════╝██╔══██╗
█████╗  ██╔██╗ ██║██║  ███╗███████║██║  ███╗█████╗  ██║  ██║
██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██║   ██║██╔══╝  ██║  ██║
███████╗██║ ╚████║╚██████╔╝██║  ██║╚██████╔╝███████╗██████╔╝
╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═════╝ 
[/bold cyan]"""


def loading_animation(message="Loading"):
    """Show a loading animation"""
    with console.status(f"[bold blue]{message}...[/bold blue]", spinner="dots"):
        time.sleep(random.uniform(0.5, 1.5))

def clear():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
def press_enter():
    """Wait for user to press Enter"""
    console.input("\n[bold cyan]Press Enter to continue...[/bold cyan]")

def guess_the_number():
    clear()
    console.print(Panel.fit("[bold magenta]🎯 Guess the Number (1-100)[/bold magenta]", border_style="magenta"))
    number = random.randint(1, 100)
    attempts = 0
    
    while True:
        try:
            guess = int(console.input("[cyan]Enter your guess: [/cyan]"))
            attempts += 1
            
            if guess < number:
                console.print("[yellow]Too low! ⬆️[/yellow]")
            elif guess > number:
                console.print("[yellow]Too high! ⬇️[/yellow]")
            else:
                console.print(f"[bold green]🎉 Correct! You guessed it in {attempts} tries![/bold green]\n")
                break
        except ValueError:
            console.print("[red]Please enter a valid number![/red]")
    
    press_enter()

def rock_paper_scissors():
    clear()
    console.print(Panel.fit("[bold blue]✊ Rock 🧻 Paper ✂️ Scissors[/bold blue]", border_style="blue"))
    choices = ['rock', 'paper', 'scissors']
    emojis = {'rock': '✊', 'paper': '🧻', 'scissors': '✂️'}
    
    player = console.input("[cyan]Choose rock, paper, or scissors: [/cyan]").lower()
    if player not in choices:
        console.print("[red]Invalid choice![/red]")
        press_enter()
        return
        
    computer = random.choice(choices)
    loading_animation("Computer choosing")
    
    console.print(f"\n[yellow]You chose: {emojis[player]}[/yellow]")
    console.print(f"[yellow]Computer chose: {emojis[computer]}[/yellow]")
    
    if player == computer:
        console.print("[blue]It's a tie! 🤝[/blue]")
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'paper' and computer == 'rock') or \
         (player == 'scissors' and computer == 'paper'):
        console.print("[green]You win! 🏆[/green]")
    else:
        console.print("[red]You lose! 😢[/red]")
    
    press_enter()

def math_quiz():
    clear()
    console.print(Panel.fit("[bold yellow]🧮 Math Quiz Challenge[/bold yellow]", border_style="yellow"))
    score = 0
    
    for i in track(range(5), description="[cyan]Solving problems...[/cyan]"):
        a, b = random.randint(1, 20), random.randint(1, 20)
        op = random.choice(['+', '-', '*'])
        answer = eval(f"{a}{op}{b}")
        
        try:
            console.print(f"\n[bold cyan]Question {i+1}:[/bold cyan]")
            user_ans = int(console.input(f"[yellow]{a} {op} {b} = [/yellow]"))
            if user_ans == answer:
                console.print("[green]✓ Correct![/green]")
                score += 1
            else:
                console.print(f"[red]✗ Wrong! Answer was {answer}[/red]")
        except ValueError:
            console.print("[red]Invalid input![/red]")
    
    console.print(f"\n[bold]Final Score: {score}/5[/bold]")
    press_enter()

def quick_riddle():
    clear()
    console.print(Panel.fit("[bold magenta]🧠 Riddle Challenge[/bold magenta]", border_style="magenta"))
    
    riddles = [
        ("What has to be broken before you can use it?", "egg", "🥚"),
        ("I'm tall when I'm young, and short when I'm old. What am I?", "candle", "🕯️"),
        ("What month of the year has 28 days?", "all", "📅"),
        ("What has keys, but no locks; space, but no room; and you can enter, but not go in?", "keyboard", "⌨️"),
        ("What gets wetter and wetter the more it dries?", "towel", "🧺")
    ]
    
    q, a, emoji = random.choice(riddles)
    console.print(f"\n[cyan]Riddle: {q}[/cyan] {emoji}")
    
    user = console.input("[yellow]Your answer: [/yellow]").strip().lower()
    if a in user:
        console.print("[green]🎉 Correct! You're a riddle master![/green]")
    else:
        console.print(f"[red]❌ Not quite! The answer was: {a}[/red]")
    
    press_enter()

def story_generator():
    clear()
    console.print(Panel.fit("[bold green]📖 Story Generator[/bold green]", border_style="green"))
    
    loading_animation("Generating your story")
    
    subjects = ["A mysterious cat 🐱", "A brave astronaut 👨‍🚀", "A friendly robot 🤖", "A powerful wizard 🧙‍♂️"]
    actions = ["discovered a magical portal", "invented a time machine", "befriended a dragon", "solved an ancient puzzle"]
    places = ["in a haunted castle", "on a distant planet", "under a rainbow", "inside a giant book"]
    
    story = f"{random.choice(subjects)} {random.choice(actions)} {random.choice(places)}..."
    console.print(Panel(f"[bold cyan]{story}[/bold cyan]", border_style="green"))
    
    press_enter()

def ascii_art():
    clear()
    arts = [
        r""" 
        /\_/\
       ( o.o )
        > ^ < 
        """,
        r""" 
        ,--.
       ( oo|   
       _\=/_  
      /     \  
     |     |   
     ||---||   
    """
    ]
    print("🎨 ASCII Art Viewer\n")
    print(random.choice(arts))

def show_menu():
    """Display the main menu"""
    console.print(TITLE)
    console.print(Panel.fit(
        "[bold green]🎮 Mini-Games Menu[/bold green]\n\n"
        "1. 🎯 Guess the Number\n"
        "2. ✊ Rock Paper Scissors\n"
        "3. 🧮 Math Quiz\n"
        "4. 🧠 Riddle Challenge\n"
        "5. 📖 Story Generator\n"
        "6. 🎨 ASCII Art Gallery\n"
        "7. ❌ Exit\n",
        border_style="cyan",
        box=box.DOUBLE
    ))
    
    return console.input("[bold yellow]Select a game (1-7): [/bold yellow]")

def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            guess_the_number()
        elif choice == '2':
            rock_paper_scissors()
        elif choice == '3':
            math_quiz()
        elif choice == '4':
            quick_riddle()
        elif choice == '5':
            story_generator()
        elif choice == '6':
            ascii_art()
        elif choice == '7':
            console.print("[bold yellow]Thanks for playing! Goodbye! 👋[/bold yellow]")
            break
        else:
            console.print("[red]Invalid choice! Please try again.[/red]")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Game interrupted. Goodbye! 👋[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")
