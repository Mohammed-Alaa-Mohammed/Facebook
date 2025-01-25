from pystyle import System
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from time import sleep


System.Clear()

console = Console()

def display_banner(language):
    """عرض شعار الأداة مع حقوق المطور."""
    if language == "ar":
        console.print(Panel("[bold cyan]أداة التحقق من حسابات فيسبوك[/bold cyan]\n[bold green]حقوق الأداة: محمد علاء محمد[/bold green]", title="🌐 [bold magenta]التحقق[/bold magenta] 🌐"))
    else:
        console.print(Panel("[bold cyan]Facebook Account Checker Tool[/bold cyan]\n[bold green]Developed by: Mohamed Alaa Mohamed[/bold green]", title="🌐 [bold magenta]Checker[/bold magenta] 🌐"))

def select_language():
    """اختيار اللغة."""
    console.print(Panel("[bold yellow]اختر اللغة | Choose Language[/bold yellow]\n1. [bold cyan]العربية [Ar][/bold cyan]\n2. [bold cyan]English [En] [/bold cyan]", title="🌍 [bold green]Language[/bold green] 🌍  </>  [bold red]By Mohammed Alaa Mohammed[/bold red] </> "))
    print ("\33[33;2m┌────────────────────────────────┐\33[39;0m")
    choice = input("\33[92;1m ╰┈┈┈┈ Set Your Language \33[39;0m┈┈┈➤  ")
    print("\33[33;2m└────────────────────────────────┘\33[39;0m")
    if choice == "1" or choice.lower() == 'ar':
        System.Clear()
        return "ar"
    elif choice == "2" or choice.lower() == 'en':
        System.Clear()
        return "en"
    
    else:
        
        System.Clear()
        console.print("[bold red]اختيار غير صالح.[/bold red]")
        quit()

def check_facebook_account(account_url, language):
    """التحقق من حالة حساب فيسبوك باستخدام Selenium."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # تشغيل المتصفح في الوضع المخفي
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    try:
        console.print("[bold cyan]جاري فتح المتصفح...[/]" if language == "ar" else "[bold cyan]Launching browser...[/]")
        # يستخدم WebDriverManager للحصول على ChromeDriver المناسب
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(account_url)
        sleep(3)  # الانتظار لتحميل الصفحة

        if "This account is disabled" in driver.page_source:
            return "الحساب محظور من قبل فيسبوك." if language == "ar" else "The account is disabled by Facebook."
        elif "Sorry, this content isn't available right now" in driver.page_source:
            return "الحساب غير موجود أو محذوف." if language == "ar" else "The account does not exist or has been deleted."
        else:
            return "الحساب يعمل بشكل طبيعي." if language == "ar" else "The account is working normally."
    except Exception as e:
        return f"حدث خطأ أثناء تشغيل المتصفح: {e}" if language == "ar" else f"An error occurred while launching the browser: {e}"
    finally:
        if 'driver' in locals() and driver:
            driver.quit()

# تشغيل الأداة
language = select_language()
display_banner(language)

if language == "ar":
    account_url = input("أدخل رابط الحساب: ")
    console.print("[bold yellow]جاري التحقق...[/bold yellow]")
else:
    account_url = input("\n\33[96;1m[\33[91;1m ╰┈➤  \33[96;1m]\33[91;1m\33[94;1m Enter The Account URL : \33[39;0m").capitalize()
    console.print("[bold yellow]Checking...[/bold yellow]")

result = check_facebook_account(account_url, language)

# عرض النتيجة
if language == "ar":
    console.print(Panel(f"[bold green]النتيجة: {result}[/bold green]", title="✅ [bold cyan]نتيجة[/bold cyan] ✅"))
else:
    console.print(Panel(f"[bold green]Result: {result}[/bold green]", title="✅ [bold cyan]Result[/bold cyan] ✅"))

