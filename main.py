import typer
from rich import box, console
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.text import Text
from github_client import GithubClient

app=typer.Typer(name="Git Forge",help="This Typer-CLI App shows personal Github streaks and stats.",add_completion = False)

#Fetches all the GitHub account's data and displays it in Tabular form with Rich.
@app.command()
def me():
    gh_client=GithubClient()
    user_info=gh_client.get_user()
    console=Console()

    tb=Table(title=f"[bold white]Github Profile: {user_info['login']}[/]",box=box.ROUNDED)
    tb.add_column("Keys",style="bold White")
    tb.add_column("Value",style="bold green")
    tb.add_row("Name",user_info.get("name") or "Unknown")
    tb.add_row("Bio",user_info.get("bio") or "Unknown")
    tb.add_row("Location",user_info.get("location") or "Unknown")
    tb.add_row("Public Repos",str(user_info["public_repos"]))
    tb.add_row("Followers",str(user_info["followers"]))
    tb.add_row("Following",str(user_info["following"]))
    tb.add_row("Created",user_info["created_at"][:10])
    console.print(tb)

@app.command()
def gh_streak():
    gh_client=GithubClient()
    calender=gh_client.contribution_streak()
    console=Console()
    weeks=calender["weeks"]
    contribution_days=[]

    #This will add number of contributions of a certain day on a date it was contributed, as key-value pair inside a python list.
    for week in weeks:
        for day in week['contributionDays']:
            contribution_days.append((day['date'],day['contributionCount']))

    current_streak=0
    for date,count in contribution_days[::-1]:
        if count>0:
            current_streak+=1
        elif count==0:
            if date!=contribution_days[-1]: #This condition checks if the date is today, then it dosen't reset the streak.
                current_streak=0
        else:
            if date!=contribution_days[-1]:
                break

    #Checking streaks for last 2 months(60 Days):
    recent_months = [day[1] for day in contribution_days[-60:]]
    rm = "".join("█" if contribution > 0 else "░" for contribution in recent_months)

    #Displaying all using Panel from Rich:
    console.print(Panel(
        f"[bold red] Current Contribution Streak: {current_streak} days[/]\n\n"
        f"[bold blue]Last 2 Months:[/] {rm}",
        title="Contribution Streak",
        border_style="white"
    ))

if __name__ == "__main__":
    app()