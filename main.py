import time
import os
import telebot

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from keep_alive import keep_alive

# Set webdriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# Initiate webdriver
driver = webdriver.Chrome(options=chrome_options)
url = "https://covid19.saglik.gov.tr/"



# Get the API key from environment variable
API_KEY = os.environ['API_KEY']
# Initiate bot
bot = telebot.TeleBot(API_KEY)
turkiye_nufus = 83614362

# Wrapper functions for commands
@bot.message_handler(commands=['hello'])
def hello(message):
	time.sleep(0.5)
	try:
		bot.send_message(message.chat.id, "Hello!")
	except Exception as e:
		print("message not sent. exception: {}".format(e))

# WIP
@bot.message_handler(commands=['gunluk'])
def gunluk_rapor(message):
	pass


@bot.message_handler(commands=['asi'])
def vacc_check(message):
	time.sleep(0.5)
	# Make sure page is loaded
	if driver.current_url == url:
		driver.refresh()
	else:
		try:
			driver.get(url)
		except Exception as e:
			print(e)
			bot.send_message(message.chat.id, f"bir hata oluştu... hata: {e}")
	time.sleep(1)
	success = False
	while not success:
		time.sleep(0.5)
		# Parse necessary information from the page
		try:
			turkiye_ort_doz_1 = driver.find_element_by_class_name("dozturkiyeortalamasi").text
			turkiye_ort_doz_2 = driver.find_element_by_class_name("doz2turkiyeortalamasi").text

			butun_dozlar_toplam = driver.find_element_by_class_name("toplamasidozusayisi").text
			birinci_doz = driver.find_element_by_class_name("doz1asisayisi").text
			ikinci_doz = driver.find_element_by_class_name("doz2asisayisi").text
			ucuncu_doz = driver.find_element_by_class_name("doz3asisayisi").text

			son_guncelleme_yeni = driver.find_element_by_class_name("asidozuguncellemesaati").text
			birinci_doz_oran = int(birinci_doz.replace('.', '')) * 100 / turkiye_nufus
			ikinci_doz_oran = int(ikinci_doz.replace('.', '')) * 100 / turkiye_nufus
			ucuncu_doz_oran = int(ucuncu_doz.replace('.', '')) * 100 / turkiye_nufus

			# Set the formatted message to be sent
			asi_message = (
				f"1. DOZ TÜRKİYE ORTALAMASI : {turkiye_ort_doz_1}\n"
				f"2. DOZ TÜRKİYE ORTALAMASI : {turkiye_ort_doz_2}\n"
				f"TOPLAM YAPILAN AŞI DOZU SAYISI : {butun_dozlar_toplam}\n"
				f"TÜRKİYE NÜFUSU : 83.614.362\n"
				f"1. DOZ : {birinci_doz} (ORAN : % {birinci_doz_oran:.2f})\n"
				f"2. DOZ : {ikinci_doz} (ORAN : % {ikinci_doz_oran:.2f})\n"
				f"3. DOZ : {ucuncu_doz} (ORAN : % {ucuncu_doz_oran:.2f})\n"
				f"SON GÜNCELLEME : {son_guncelleme_yeni}\n"
				"https://covid19.saglik.gov.tr/"
			)


			# WIP
			"""
			if son_guncelleme != son_guncelleme_yeni:
				bugunku_toplam_int = int(butun_dozlar_toplam.replace('.', ''))
				gunluk_yapilan_asi = bugunku_toplam_int - dunku_toplam
				dunku_toplam = bugunku_toplam_int
				son_guncelleme = son_guncelleme_yeni
				asi_message += f"\nSON GÜNCELLEMEDEN BU YANA YAPILAN AŞI SAYISI : {gunluk_yapilan_asi}"
			"""
			# Send the message
			bot.send_message(
				message.chat.id,
				asi_message
				)
			success = True
		except Exception as e:
			print("message not sent. exception: {}".format(e))
			success = False
			driver.refresh()
"""	try:
		driver.close()
	except Exception as e:
		print(e.message)"""


# Keep the bot alive
if __name__ == "__main__":
	keep_alive()

bot.polling()

