from pystyle import System
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from time import sleep



# إعدادات النظام
System.Clear()
console = Console()

# قواميس الترجمة لدعم لغات متعددة
translations = {
    "ar": {
        "tool_title": "\u0623\u062f\u0627\u0629 \u0627\u0644\u062a\u062d\u0642\u0642 \u0645\u0646 \u062d\u0633\u0627\u0628\u0627\u062a \u0641\u064a\u0633\u0628\u0648\u0643",
        "developer_credit": "\u062d\u0642\u0648\u0642 \u0627\u0644\u0623\u062f\u0627\u0629: \u0645\u062d\u0645\u062f \u0639\u0644\u0627\u0621 \u0645\u062d\u0645\u062f",
        "choose_language": "\u0627\u062e\u062a\u0631 \u0627\u0644\u0644\u063a\u0629",
        "invalid_choice": "\u0627\u062e\u062a\u064a\u0627\u0631 \u063a\u064a\u0631 \u0635\u0627\u0644\u062d.",
        "enter_url": "\u0623\u062f\u062e\u0644 \u0631\u0627\u0628\u0637 \u0627\u0644\u062d\u0633\u0627\u0628:",
        "checking": "\u062c\u0627\u0631\u064a \u0627\u0644\u062a\u062d\u0642\u0642...",
        "account_disabled": "\u0627\u0644\u062d\u0633\u0627\u0628 \u0645\u062d\u0638\u0648\u0631 \u0645\u0646 \u0642\u0628\u0644 \u0641\u064a\u0633\u0628\u0648\u0643.",
        "account_deleted": "\u0627\u0644\u062d\u0633\u0627\u0628 \u063a\u064a\u0631 \u0645\u0648\u062c\u0648\u062f \u0623\u0648 \u0645\u062d\u0630\u0648\u0641.",
        "account_active": "\u0627\u0644\u062d\u0633\u0627\u0628 \u064a\u0639\u0645\u0644 \u0628\u0634\u0643\u0644 \u0637\u0628\u064a\u0639\u064a.",
        "browser_error": "\u062d\u062f\u062b \u062e\u0637\u0623 \u0623\u062b\u0646\u0627\u0621 \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0645\u062a\u0635\u0641\u062d:",
        "result": "\u0627\u0644\u0646\u062a\u064a\u062c\u0629",
        "retry": "\u0647\u0644 \u062a\u0631\u063a\u0628 \u0641\u064a \u0627\u0644\u0645\u062d\u0627\u0648\u0644\u0629 \u0645\u0631\u0629 \u0623\u062e\u0631\u0649؟ \u0623\u062f\u062e\u0644 (y/n): "
    },
    "en": {
        "tool_title": "Facebook Account Checker Tool",
        "developer_credit": "Developed by: Mohamed Alaa Mohamed",
        "choose_language": "Choose Language",
        "invalid_choice": "Invalid choice.",
        "enter_url": "Enter The Account URL :",
        "checking": "Checking...",
        "account_disabled": "The account is disabled by Facebook.",
        "account_deleted": "The account does not exist or has been deleted.",
        "account_active": "The account is working normally.",
        "browser_error": "An error occurred while launching the browser:",
        "result": "Result",
        "retry": "Would You Like to Try Again? Enter (y/n): "
    }
}

def display_banner(language):
    """عرض شعار الأداة مع حقوق المطور."""
    console.print(Panel(f"[bold cyan]{translations[language]['tool_title']}[/bold cyan]\n[bold green]{translations[language]['developer_credit']}[/bold green]", title="🌐 🌐 🌐"))

def select_language():
    """اختيار اللغة."""
    console.print(Panel(f"[bold yellow]{translations['ar']['choose_language']} | {translations['en']['choose_language']}[/bold yellow]\n1. [bold cyan]العربية [Ar][/bold cyan]\n2. [bold cyan]English [En][/bold cyan]", title="🌍 🌍 🌍"))
    choice = input("\n[-] Set Your Language (1/2): ")
    if choice == "1":
        System.Clear()
        return "ar"
    elif choice == "2":
        System.Clear()
        return "en"
    else:
        console.print("[bold red]Invalid choice. Exiting...[/bold red]")
        quit()

def check_facebook_account(account_url, language):
    """التحقق من حالة حساب فيسبوك باستخدام Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    try:
        console.print(f"[cyan]{translations[language]['checking']}[/]")
        with Progress() as progress:
            task = progress.add_task("[bold yellow]Loading...", total=100)

            # يستخدم WebDriverManager للحصول على ChromeDriver المناسب
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            for _ in range(4):
                progress.update(task, advance=43)
                sleep(1)
                

            driver.get(account_url)

            if "This account is disabled" in driver.page_source:
                return translations[language]['account_disabled']
            elif "Sorry, this content isn't available right now" in driver.page_source:
                return translations[language]['account_deleted']
            else:
                return translations[language]['account_active']
    except Exception as e:
        return f"{translations[language]['browser_error']} {e}"
    finally:
        if 'driver' in locals() and driver:
            driver.quit()

def main():
    language = select_language()
    display_banner(language)

    while True:
        account_url = input(f"\n [-] {translations[language]['enter_url']} ")
        System.Clear()
        result = check_facebook_account(account_url, language)
        console.print(Panel(f"[bold green]{translations[language]['result']} :  {result}[/bold green]" , title="✅ ✅ ✅"))
        System.Clear()
        retry = input(f"\n\33[34;1m[+] {translations[language]['retry']} \33[39;0m")
        if retry.lower() != 'y':
            break

if __name__ == "__main__":
    main()
