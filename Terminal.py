import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box

from news_scraper import fetch_news
from ai_models import classify_news, get_relevant_articles

console = Console()

# Function to display results in a rich table
def display_relevant_articles(articles_with_reasons):
    table = Table(title="Relevant Articles for Your Goal", show_lines=True, box=box. ASCII)
    table.add_column("Headline", justify="left", style="yellow", width=25)
    table.add_column("Reason", justify="left")

    for _, article in articles_with_reasons.iterrows():
        table.add_row(article["Headline"], article["Reason"])

    console.print(table)


def display_articles(news_df):
    table = Table(title="News Classification Results", show_lines=True, box=box. ASCII)
    table.add_column("Headline", justify="left", overflow="fold")
    table.add_column("Published", justify="center", style="green")
    table.add_column("Source", justify="center", style="yellow", width=10)
    table.add_column("URL", justify="left", style="magenta", overflow="fold", width=16)

    for _, row in news_df.iterrows():
        table.add_row(
            row["Headline"],
            row["Published"],
            row["Source"] or "N/A",
            row["URL"],
        )

    console.print(table)

def main():
    console.print("\n[bold blue]Welcome to the News Classification Demo![/bold blue]\n")
    search_terms = console.input("[bold yellow]Enter search terms, separated by commas: [/bold yellow]").split(",")
    search_terms = [term.strip() for term in search_terms if term.strip()]
    if not search_terms:
        console.print("[bold red]No search terms provided. Exiting.[/bold red]")
        return

    max_articles = 20
    console.print("\n[bold green]Fetching news articles...[/bold green]")
    news_df = fetch_news(search_terms, max_articles)

    if news_df.empty:
        console.print("[bold red]No articles found! Try different search terms.[/bold red]")
        return

    # Ask the user if they have a goal or not
    user_goal = console.input("\n[bold yellow]Do you have a specific goal in mind? (yes/no): [/bold yellow]").strip().lower()

    if user_goal == "yes":
        # Ask for the user's goal
        user_goal = console.input("\n[bold yellow]Please describe your goal or what you are looking for: [/bold yellow]").strip()

        # Get relevant articles from the LLM
        console.print("\n[bold green]Fetching relevant articles based on your goal...[/bold green]")
        relevant_articles = get_relevant_articles(user_goal, news_df)

        # Display the relevant articles in a table format
        console.print("\n[bold green]Here are two articles that might help with your goal:[/bold green]")
        display_relevant_articles(relevant_articles)
    
    else:
        # No goal, just display the top articles
        console.print("\n[bold green]Classifying headlines using LLM...[/bold green]")
        news_df = classify_news(news_df)

        while True:
            # Prompt user to choose sort option using numbers (1, 2, 3)
            console.print("\n[bold yellow]Sort by (choose one):")
            console.print("[bold]1.[/bold] Collaboration/Partnership")
            console.print("[bold]2.[/bold] Industry Growth/Trends")
            console.print("[bold]3.[/bold] Leadership Change")
            console.print("[bold]4.[/bold] Exit")

            # Get user input for sorting choice
            user_choice = input("\nEnter the number corresponding to your choice: ").strip()

            if user_choice == "4":
                console.print("\n[bold blue]Exiting News Classification Demo.[/bold blue]")
                break
            
            # Map user input to the correct column name
            sort_mapping = {
                "1": "Collaboration/Partnership",
                "2": "Industry Growth/Trends",
                "3": "Leadership Change"
            }

            # Validate and sort the DataFrame based on user input
            if user_choice in sort_mapping:
                sort_column = sort_mapping[user_choice]
                news_df = news_df.sort_values(by=sort_column, ascending=False)  # Sort in descending order
            else:
                console.print("\n[bold red]Invalid input. Sorting by default (Collaboration/Partnership).[/bold red]")
                news_df = news_df.sort_values(by='Collaboration/Partnership', ascending=False)

            # Display the results after sorting
            console.print("\n[bold blue]Classification Complete. Here are the results:[/bold blue]")
            display_articles(news_df.head(5))





        '''
    console.print("[bold blue]Welcome to the News Classification Demo![/bold blue]")
    search_terms = console.input("Enter search terms, separated by commas: ").split(",")
    search_terms = [term.strip() for term in search_terms if term.strip()]
    if not search_terms:
        console.print("[bold red]No search terms provided. Exiting.[/bold red]")
        return

    max_articles = int(console.input("Enter the maximum number of articles to fetch: "))
    console.print("\n[bold green]Fetching news articles...[/bold green]")
    news_df = fetch_news(search_terms, max_articles)

    if news_df.empty:
        console.print("[bold red]No articles found! Try different search terms.[/bold red]")
        return

    # Ask the user for their goal
    user_goal = input("\n[bold yellow]Please describe your goal or what you are looking for: [/bold yellow]").strip()

    # Get relevant articles from the LLM
    console.print("\n[bold blue]Fetching relevant articles...[/bold blue]")

    relevant_articles = get_relevant_articles(user_goal, news_df)

    # Display the relevant articles in a table format
    console.print("\n[bold blue]Here are two articles that might help with your goal:[/bold blue]")
    display_relevant_articles(relevant_articles)

    '''
        '''
    console.print("\n[bold green]Classifying headlines using LLM...[/bold green]")
    news_df = classify_and_compute_scores(news_df)

    while True:
        # Prompt user to choose sort option using numbers (1, 2, 3)
        console.print("\n[bold yellow]Sort by (choose one):")
        console.print("[bold]1.[/bold] Collaboration/Partnership")
        console.print("[bold]2.[/bold] Industry Growth/Trends")
        console.print("[bold]3.[/bold] Leadership Change")
        console.print("[bold]4.[/bold] Exit")

        # Get user input for sorting choice
        user_choice = input("\nEnter the number corresponding to your choice: ").strip()

        if user_choice == "4":
            console.print("\n[bold blue]Exiting the sorting loop.[/bold blue]")
            break
        
        # Map user input to the correct column name
        sort_mapping = {
            "1": "Collaboration/Partnership",
            "2": "Industry Growth/Trends",
            "3": "Leadership Change"
        }

        # Validate and sort the DataFrame based on user input
        if user_choice in sort_mapping:
            sort_column = sort_mapping[user_choice]
            news_df = news_df.sort_values(by=sort_column, ascending=False)  # Sort in descending order
        else:
            console.print("\n[bold red]Invalid input. Sorting by default (Collaboration/Partnership).[/bold red]")
            news_df = news_df.sort_values(by='Collaboration/Partnership', ascending=False)

        # Display the results after sorting
        console.print("\n[bold blue]Classification Complete. Here are the results:[/bold blue]")
        display_articles(news_df)
        '''

    
    
if __name__ == "__main__":
    main()
